<script setup>
import { reactive, watch, computed } from 'vue'

const MAX_FILE_SIZE = 5 * 1024 * 1024 // 5MB
const ACCEPTED_IMAGE_TYPES = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']

// Form state
const state = reactive({
  name: '',
  slug: '',
  originalPrice: null,
  discountPercent: 0,
  category: '',
  image: null,          // single File
  badgeText: '',
  badgeColor: 'primary',
  gender: '',
  brand: '',
  similar: '',
  type: '',
  seasons: [],
  volume: '',
  capacity: 0,
  sold: 0
})

const stockStatus = computed(() => {
  if (state.capacity === 0) {
    return { available: false, text: 'ناموجود', color: 'error' }
  } else if (state.capacity <= 5) {
    return { available: true, text: 'تنها چند عدد باقی مانده', color: 'warning' }
  } else {
    return { available: true, text: 'موجود', color: 'success' }
  }
})

const categoryOptions = [
  { label: 'مردانه', value: 'male' },
  { label: 'زنانه', value: 'female' },
  { label: 'یونیسکس', value: 'unisex' }
]

const badgeColorOptions = [
  { label: 'اصلی', value: 'primary' },
  { label: 'موفقیت', value: 'success' },
  { label: 'اطلاعات', value: 'info' },
  { label: 'هشدار', value: 'warning' },
  { label: 'خطر', value: 'error' }
]

const typeOptions = [
  { label: 'Eau de Parfum', value: 'Eau de Parfum' },
  { label: 'Eau de Toilette', value: 'Eau de Toilette' },
  { label: 'Eau de Cologne', value: 'Eau de Cologne' },
  { label: 'Parfum', value: 'Parfum' }
]

const seasonOptions = [
  { label: 'بهار', value: 'spring' },
  { label: 'تابستان', value: 'summer' },
  { label: 'پاییز', value: 'autumn' },
  { label: 'زمستان', value: 'winter' },
  { label: 'چهار فصل', value: 'all-season' }
]

const toast = useToast()

function validate(formState) {
  const errors = []

  if (!formState.name || formState.name.length < 2) {
    errors.push({ name: 'name', message: 'نام باید حداقل 2 کاراکتر باشد' })
  }

  if (!formState.slug || formState.slug.length < 3) {
    errors.push({ name: 'slug', message: 'اسلاگ باید حداقل 3 کاراکتر باشد' })
  }

  if (!formState.originalPrice || formState.originalPrice <= 0) {
    errors.push({ name: 'originalPrice', message: 'قیمت باید بیشتر از 0 باشد' })
  }

  if (formState.discountPercent < 0 || formState.discountPercent > 100) {
    errors.push({ name: 'discountPercent', message: 'تخفیف باید بین 0 تا 100 باشد' })
  }

  if (!formState.category) {
    errors.push({ name: 'category', message: 'دسته‌بندی الزامی است' })
  }

  if (!formState.image) {
    errors.push({ name: 'image', message: 'لطفا یک تصویر انتخاب کنید' })
  } else {
    if (formState.image.size > MAX_FILE_SIZE) {
      errors.push({ name: 'image', message: 'حجم تصویر باید کمتر از 5MB باشد' })
    }
    if (!ACCEPTED_IMAGE_TYPES.includes(formState.image.type)) {
      errors.push({ name: 'image', message: 'فرمت تصویر باید JPG، PNG یا WebP باشد' })
    }
  }

  if (!formState.gender) {
    errors.push({ name: 'gender', message: 'جنسیت الزامی است' })
  }

  if (!formState.brand) {
    errors.push({ name: 'brand', message: 'برند الزامی است' })
  }

  if (!formState.type) {
    errors.push({ name: 'type', message: 'نوع عطر الزامی است' })
  }

  if (!formState.seasons || formState.seasons.length === 0) {
    errors.push({ name: 'seasons', message: 'حداقل یک فصل انتخاب کنید' })
  }

  if (!formState.volume) {
    errors.push({ name: 'volume', message: 'حجم الزامی است' })
  }

  if (formState.capacity === null || formState.capacity < 0) {
    errors.push({ name: 'capacity', message: 'موجودی باید 0 یا بیشتر باشد' })
  }

  return errors
}

// Auto-generate slug (only if slug is empty, so user can override)
watch(
  () => state.name,
  (newName) => {
    if (!state.slug && newName) {
      state.slug = newName
        .toLowerCase()
        .replace(/\s+/g, '-')
        .replace(/[^\w\-آ-ی]+/g, '')
    }
  }
)

async function onSubmit (event) {
  // Convert seasons to readable text (for showing later, optional for DB)
  const seasonsText = event.data.seasons
    .map(season => {
      const option = seasonOptions.find(s => s.value === season)
      return option ? option.label : season
    })
    .join('، ')

  // Prepare the payload you want to store in DB (pure JSON, no blob URLs)
  const payload = {
    slug: event.data.slug,
    name: event.data.name,
    originalPrice: event.data.originalPrice,
    discountPercent: event.data.discountPercent,
    category: event.data.category,
    badgeText: event.data.badgeText || '',
    badgeColor: event.data.badgeColor || 'primary',
    gender: event.data.gender,
    brand: event.data.brand,
    similar: event.data.similar || '',
    type: event.data.type,
    seasons: event.data.seasons,
    seasonsText,
    volume: event.data.volume,
    capacity: event.data.capacity,
    sold: event.data.sold || 0
    // NOTE: image is handled separately below
  }

  // If you want to send the file to backend, use FormData instead of JSON:
  const formData = new FormData()
  Object.entries(payload).forEach(([key, value]) => {
    // stringify arrays/objects
    if (Array.isArray(value) || typeof value === 'object') {
      formData.append(key, JSON.stringify(value))
    } else {
      formData.append(key, String(value))
    }
  })

  if (event.data.image) {
    formData.append('image', event.data.image)
  }

  try {
    // Recommended in Nuxt 3 for POST from components: $fetch[[Which to use](https://stackoverflow.com/questions/76839341)]
    const response = await $fetch('/api/perfumes', {
      method: 'POST',
      body: formData
    })

    console.log('Saved to DB:', response)

    toast.add({
      title: 'موفقیت',
      description: 'عطر با موفقیت اضافه شد',
      color: 'success'
    })
  } catch (error) {
    console.error('Error saving perfume:', error)
    toast.add({
      title: 'خطا',
      description: 'خطا در ذخیره‌سازی عطر در پایگاه داده',
      color: 'error'
    })
  }
}
</script>

<template>
  <div class="container mx-auto p-6 max-w-7xl">
    <h1 class="text-3xl font-bold mb-8">افزودن عطر جدید</h1>

    <UForm :validate="validate" :state="state" @submit="onSubmit">
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <!-- Left side -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Basic Information -->
          <div class="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
            <h2 class="text-xl font-semibold mb-4">اطلاعات اصلی</h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <UFormField label="نام عطر" name="name" required>
                <UInput v-model="state.name" placeholder="دیور ساواج" />
              </UFormField>

              <UFormField label="اسلاگ (Slug)" name="slug" required>
                <UInput v-model="state.slug" placeholder="dior-sauvage-4" />
              </UFormField>

              <UFormField label="قیمت اصلی (تومان)" name="originalPrice" required>
                <UInputNumber v-model="state.originalPrice" :min="0" />
              </UFormField>

              <UFormField label="درصد تخفیف" name="discountPercent">
                <UInputNumber v-model="state.discountPercent" :min="0" :max="100" />
              </UFormField>

              <UFormField label="دسته‌بندی" name="category" required>
                <USelect v-model="state.category" :items="categoryOptions" placeholder="انتخاب دسته‌بندی" />
              </UFormField>

              <UFormField label="موجودی انبار" name="capacity" required>
                <UInputNumber v-model="state.capacity" :min="0" placeholder="تعداد موجود در انبار" />
              </UFormField>
            </div>

            <!-- Stock Status -->
            <div
              v-if="state.capacity !== null"
              class="mt-4 p-3 rounded-lg border"
              :class="{
                'bg-red-50 dark:bg-red-900/20 border-red-200 dark:border-red-800': !stockStatus.available,
                'bg-yellow-50 dark:bg-yellow-900/20 border-yellow-200 dark:border-yellow-800': stockStatus.available && state.capacity <= 5,
                'bg-green-50 dark:bg-green-900/20 border-green-200 dark:border-green-800': stockStatus.available && state.capacity > 5
              }"
            >
              <div class="flex items-center gap-2">
                <UIcon
                  :name="stockStatus.available ? 'i-lucide-check-circle' : 'i-lucide-x-circle'"
                  :class="{
                    'text-red-600 dark:text-red-400': !stockStatus.available,
                    'text-yellow-600 dark:text-yellow-400': stockStatus.available && state.capacity <= 5,
                    'text-green-600 dark:text-green-400': stockStatus.available && state.capacity > 5
                  }"
                  class="w-5 h-5"
                />
                <span
                  class="font-medium"
                  :class="{
                    'text-red-700 dark:text-red-300': !stockStatus.available,
                    'text-yellow-700 dark:text-yellow-300': stockStatus.available && state.capacity <= 5,
                    'text-green-700 dark:text-green-300': stockStatus.available && state.capacity > 5
                  }"
                >
                  وضعیت: {{ stockStatus.text }}
                </span>
                <span
                  class="mr-auto text-sm"
                  :class="{
                    'text-red-600 dark:text-red-400': !stockStatus.available,
                    'text-yellow-600 dark:text-yellow-400': stockStatus.available && state.capacity <= 5,
                    'text-green-600 dark:text-green-400': stockStatus.available && state.capacity > 5
                  }"
                >
                  {{ state.capacity }} عدد در انبار
                </span>
              </div>
            </div>
          </div>

          <!-- Badge -->
          <div class="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
            <h2 class="text-xl font-semibold mb-4">برچسب (Badge)</h2>
            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <UFormField label="متن برچسب" name="badgeText">
                <UInput v-model="state.badgeText" placeholder="جدید" />
              </UFormField>

              <UFormField label="رنگ برچسب" name="badgeColor">
                <USelect v-model="state.badgeColor" :items="badgeColorOptions" />
              </UFormField>
            </div>
          </div>

          <!-- Product Info -->
          <div class="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
            <h2 class="text-xl font-semibold mb-4">مشخصات محصول</h2>

            <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
              <UFormField label="جنسیت" name="gender" required>
                <UInput v-model="state.gender" placeholder="مردانه" />
              </UFormField>

              <UFormField label="برند" name="brand" required>
                <UInput v-model="state.brand" placeholder="Dior" />
              </UFormField>

              <UFormField label="عطر مشابه" name="similar">
                <UInput v-model="state.similar" placeholder="Bleu de Chanel" />
              </UFormField>

              <UFormField label="نوع عطر" name="type" required>
                <USelect v-model="state.type" :items="typeOptions" placeholder="انتخاب نوع" />
              </UFormField>

              <UFormField
                label="فصل‌های مناسب"
                name="seasons"
                required
                description="می‌توانید چند فصل انتخاب کنید"
              >
                <USelectMenu
                  v-model="state.seasons"
                  :items="seasonOptions"
                  multiple
                  placeholder="انتخاب فصل‌ها"
                />
              </UFormField>

              <UFormField label="حجم" name="volume" required>
                <UInput v-model="state.volume" placeholder="100ml / 200ml" />
              </UFormField>
            </div>
          </div>

          <!-- Buttons -->
          <div class="flex gap-3">
            <UButton type="submit" size="lg" color="primary">
              افزودن عطر
            </UButton>

            <UButton type="button" size="lg" color="neutral" variant="outline" @click="$router.back()">
              انصراف
            </UButton>
          </div>
        </div>

        <!-- Right side - Image Upload -->
        <div class="lg:col-span-1">
          <div class="sticky top-6">
            <div class="bg-white dark:bg-gray-900 p-6 rounded-lg border border-gray-200 dark:border-gray-800">
              <h2 class="text-xl font-semibold mb-4">تصویر عطر</h2>

              <UFormField name="image" description="JPG, PNG یا WebP (حداکثر 5MB)" required>
                <UFileUpload
                  v-model="state.image"
                  accept="image/*"
                  icon="i-lucide-image"
                  label="تصویر عطر را اینجا رها کنید"
                  description="یا کلیک کنید تا فایل انتخاب کنید"
                  class="min-h-64"
                />
              </UFormField>
            </div>
          </div>
        </div>
      </div>
    </UForm>
  </div>
</template>