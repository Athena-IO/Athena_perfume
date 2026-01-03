<script setup>
import { reactive, ref, watch, computed, onMounted } from "vue";

const MAX_FILE_SIZE = 5 * 1024 * 1024; // 5MB
const ACCEPTED_IMAGE_TYPES = [
  "image/jpeg",
  "image/jpg",
  "image/png",
  "image/webp",
];

const props = defineProps({
  perfume: {
    type: Object,
    default: null,
  },
  mode: {
    type: String,
    default: "add",
    validator: (value) => ["add", "edit"].includes(value),
  },
});

const emit = defineEmits(["success", "cancel"]);

const toast = useToast();
const router = useRouter();

// Form state
const state = reactive({
  name: "",
  slug: "",
  originalPrice: null,
  discountPercent: 0,
  category: "",
  image: null,
  badgeText: "",
  badgeColor: "primary",
  gender: "",
  brands: [],
  similar: "",
  type: "",
  seasons: [],
  volume: "",
  capacity: 0,
  sold: 0,
  description: "", // Rich text HTML content
});

const showBrandModal = ref(false);
const existingImageUrl = ref(null);
const isSubmitting = ref(false);

const stockStatus = computed(() => {
  if (state.capacity === 0) {
    return { available: false, text: "ناموجود", color: "error" };
  } else if (state.capacity <= 5) {
    return {
      available: true,
      text: "تنها چند عدد باقی مانده",
      color: "warning",
    };
  } else {
    return { available: true, text: "موجود", color: "success" };
  }
});

import { useCategoriesStore } from '~/stores/categories.js';
const categoriesStore = useCategoriesStore();

onMounted(() => {
  categoriesStore.fetchCategories();
});

const categoryOptions = computed(() =>
  categoriesStore.categories.map(c => ({
    label: c.label || c.name,
    value: c.value || c.slug,
    slug: c.slug || c.value // for potential link use
  }))
);

const badgeColorOptions = [
  { label: "اصلی", value: "primary" },
  { label: "موفقیت", value: "success" },
  { label: "اطلاعات", value: "info" },
  { label: "هشدار", value: "warning" },
  { label: "خطر", value: "error" },
];

const typeOptions = [
  { label: "Eau de Parfum", value: "Eau de Parfum" },
  { label: "Eau de Toilette", value: "Eau de Toilette" },
  { label: "Eau de Cologne", value: "Eau de Cologne" },
  { label: "Parfum", value: "Parfum" },
];

const seasonOptions = [
  { label: "بهار", value: "spring" },
  { label: "تابستان", value: "summer" },
  { label: "پاییز", value: "autumn" },
  { label: "زمستان", value: "winter" },
  { label: "چهار فصل", value: "all-season" },
];

// Accordion items
const accordionItems = computed(() => [
  {
    label: "اطلاعات اصلی",
    icon: "i-lucide-package",
    slot: "basic",
    defaultOpen: true,
  },
  {
    label: "مشخصات محصول",
    icon: "i-lucide-info",
    slot: "details",
  },
  {
    label: "توضیحات کامل",
    icon: "i-lucide-file-text",
    slot: "description",
  },
  {
    label: "برچسب و تخفیف",
    icon: "i-lucide-tag",
    slot: "badge",
  },
]);

const pageTitle = computed(() => {
  return props.mode === "edit" ? "ویرایش عطر" : "افزودن عطر جدید";
});

const submitButtonText = computed(() => {
  return props.mode === "edit" ? "ذخیره تغییرات" : "افزودن عطر";
});

// Validation
function validate(formState) {
  const errors = [];
  if (!formState.name || formState.name.length < 2) {
    errors.push({ name: "name", message: "نام باید حداقل 2 کاراکتر باشد" });
  }
  if (!formState.slug || formState.slug.length < 3) {
    errors.push({ name: "slug", message: "اسلاگ باید حداقل 3 کاراکتر باشد" });
  }
  if (!formState.originalPrice || formState.originalPrice <= 0) {
    errors.push({
      name: "originalPrice",
      message: "قیمت باید بیشتر از 0 باشد",
    });
  }
  if (formState.discountPercent < 0 || formState.discountPercent > 100) {
    errors.push({
      name: "discountPercent",
      message: "تخفیف باید بین 0 تا 100 باشد",
    });
  }
  if (!formState.category) {
    errors.push({ name: "category", message: "دسته‌بندی الزامی است" });
  }
  if (props.mode === "add" && !formState.image) {
    errors.push({ name: "image", message: "لطفا یک تصویر انتخاب کنید" });
  }
  if (formState.image) {
    if (formState.image.size > MAX_FILE_SIZE) {
      errors.push({
        name: "image",
        message: "حجم تصویر باید کمتر از 5MB باشد",
      });
    }
    if (!ACCEPTED_IMAGE_TYPES.includes(formState.image.type)) {
      errors.push({
        name: "image",
        message: "فرمت تصویر باید JPG، PNG یا WebP باشد",
      });
    }
  }
  if (!formState.gender) {
    errors.push({ name: "gender", message: "جنسیت الزامی است" });
  }
  if (!formState.brands || formState.brands.length === 0) {
    errors.push({ name: "brands", message: "حداقل یک برند انتخاب کنید" });
  }
  if (!formState.type) {
    errors.push({ name: "type", message: "نوع عطر الزامی است" });
  }
  if (!formState.seasons || formState.seasons.length === 0) {
    errors.push({ name: "seasons", message: "حداقل یک فصل انتخاب کنید" });
  }
  if (!formState.volume) {
    errors.push({ name: "volume", message: "حجم الزامی است" });
  }
  if (formState.capacity === null || formState.capacity < 0) {
    errors.push({ name: "capacity", message: "موجودی باید 0 یا بیشتر باشد" });
  }
  return errors;
}

// Auto-generate slug
watch(
  () => state.name,
  (newName) => {
    if (props.mode === "add" && !state.slug && newName) {
      state.slug = newName
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^\w\-آ-ی]+/g, "");
    }
  }
);

// Handle brand selection
function onBrandSelect(brand) {
  const exists = state.brands.find((b) => b.id === brand.id);
  if (!exists) {
    state.brands.push({
      id: brand.id,
      name: brand.name,
      slug: brand.slug,
      image: brand.image,
    });
  }
}

// Remove brand
function removeBrand(brandId) {
  state.brands = state.brands.filter((b) => b.id !== brandId);
}

// Load existing perfume data
onMounted(() => {
  if (props.mode === "edit" && props.perfume) {
    Object.assign(state, {
      name: props.perfume.name || "",
      slug: props.perfume.slug || "",
      originalPrice: props.perfume.originalPrice || null,
      discountPercent: props.perfume.discountPercent || 0,
      category: props.perfume.category || "",
      badgeText: props.perfume.badgeText || "",
      badgeColor: props.perfume.badgeColor || "primary",
      gender: props.perfume.gender || "",
      brands: props.perfume.brands || [],
      similar: props.perfume.similar || "",
      type: props.perfume.type || "",
      seasons: props.perfume.seasons || [],
      volume: props.perfume.volume || "",
      capacity: props.perfume.capacity || 0,
      sold: props.perfume.sold || 0,
      description: props.perfume.description || "",
    });

    if (props.perfume.image) {
      existingImageUrl.value = props.perfume.image;
    }
  }
});

async function onSubmit(event) {
  if (isSubmitting.value) return;

  isSubmitting.value = true;

  try {
    const seasonsText = event.data.seasons
      .map((season) => {
        const option = seasonOptions.find((s) => s.value === season);
        return option ? option.label : season;
      })
      .join("، ");

    const formData = new FormData();

    // Add all fields
    formData.append("name", event.data.name);
    formData.append("slug", event.data.slug);
    formData.append("originalPrice", event.data.originalPrice);
    formData.append("discountPercent", event.data.discountPercent || 0);
    formData.append("category", event.data.category);
    formData.append("badgeText", event.data.badgeText || "");
    formData.append("badgeColor", event.data.badgeColor || "primary");
    formData.append("gender", event.data.gender);
    formData.append("brands", JSON.stringify(event.data.brands));
    formData.append("similar", event.data.similar || "");
    formData.append("type", event.data.type);
    formData.append("seasons", JSON.stringify(event.data.seasons));
    formData.append("seasonsText", seasonsText);
    formData.append("volume", event.data.volume);
    formData.append("capacity", event.data.capacity);
    formData.append("sold", event.data.sold || 0);
    formData.append("description", event.data.description || "");

    // Add image if present
    if (event.data.image) {
      formData.append("image", event.data.image);
    }

    let response;
    const apiBaseUrl = "http://127.0.0.1:8000/api/products";

    if (props.mode === "edit") {
      // Update existing perfume
      response = await $fetch(`${apiBaseUrl}/admin/${props.perfume.id}`, {
        method: "PUT",
        body: formData,
      });

      toast.add({
        title: "موفقیت",
        description: "عطر با موفقیت ویرایش شد",
        color: "success",
        icon: "i-lucide-check",
      });
    } else {
      // Create new perfume
      response = await $fetch(`${apiBaseUrl}/admin/create`, {
        method: "POST",
        body: formData,
      });

      toast.add({
        title: "موفقیت",
        description: "عطر با موفقیت اضافه شد",
        color: "success",
        icon: "i-lucide-check",
      });
    }

    console.log("Saved to DB:", response);

    emit("success", response);
    router.push("/admin/perfumes");
  } catch (error) {
    console.error("Error saving perfume:", error);

    // Show detailed error message
    const errorMessage =
      error?.data?.message || error?.message || "خطا در ارتباط با سرور";

    toast.add({
      title: "خطا",
      description: errorMessage,
      color: "error",
      icon: "i-lucide-x",
      timeout: 5000,
    });
  } finally {
    isSubmitting.value = false;
  }
}

function handleCancel() {
  emit("cancel");
  router.push("/admin/perfumes");
}
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 max-w-6xl">
    <!-- Header -->
    <div class="mb-6 sm:mb-8">
      <h1 class="text-2xl sm:text-3xl font-bold text-default">
        {{ pageTitle }}
      </h1>
      <p class="text-sm text-muted mt-1">
        {{
          mode === "edit"
            ? "اطلاعات عطر را ویرایش کنید"
            : "اطلاعات عطر را وارد کنید"
        }}
      </p>
    </div>

    <UForm
      :validate="validate"
      :state="state"
      @submit="onSubmit"
      class="space-y-6"
    >
      <div class="grid grid-cols-1 lg:grid-cols-3 gap-4 lg:gap-6">
        <!-- Main Content -->
        <div class="lg:col-span-2 space-y-4">
          <!-- Mobile Image Upload -->
          <UCard class="lg:hidden">
            <UFormField
              name="image"
              :description="
                mode === 'edit'
                  ? 'اختیاری - برای تغییر تصویر فایل جدید انتخاب کنید'
                  : 'JPG, PNG یا WebP (حداکثر 5MB)'
              "
              :required="mode === 'add'"
            >
              <div
                v-if="mode === 'edit' && existingImageUrl && !state.image"
                class="mb-3"
              >
                <p class="text-sm text-muted mb-2">تصویر فعلی:</p>
                <img
                  :src="existingImageUrl"
                  :alt="state.name"
                  class="w-32 h-32 object-cover rounded-lg"
                />
              </div>
              <UFileUpload
                v-model="state.image"
                accept="image/*"
                icon="i-lucide-image"
                :label="
                  mode === 'edit'
                    ? 'برای تغییر تصویر، فایل جدید را اینجا رها کنید'
                    : 'تصویر عطر را اینجا رها کنید'
                "
                description="یا کلیک کنید تا فایل انتخاب کنید"
                class="min-h-48"
              />
            </UFormField>
          </UCard>

          <!-- Accordion Sections -->
          <UAccordion :items="accordionItems" :default-value="['0']" multiple>
            <!-- Basic Information -->
            <template #basic>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 pb-4">
                <UFormField
                  label="نام عطر"
                  name="name"
                  required
                  class="sm:col-span-2"
                >
                  <UInput
                    v-model="state.name"
                    placeholder="دیور ساواج"
                    size="lg"
                  />
                </UFormField>

                <UFormField
                  label="اسلاگ (Slug)"
                  name="slug"
                  required
                  class="sm:col-span-2"
                >
                  <UInput v-model="state.slug" placeholder="dior-sauvage-4" />
                </UFormField>

                <UFormField
                  label="قیمت اصلی (تومان)"
                  name="originalPrice"
                  required
                >
                  <UInputNumber v-model="state.originalPrice" :min="0" />
                </UFormField>

                <UFormField label="موجودی انبار" name="capacity" required>
                  <UInputNumber
                    v-model="state.capacity"
                    :min="0"
                    placeholder="تعداد"
                  />
                </UFormField>

                <UFormField
                  label="دسته‌بندی"
                  name="category"
                  required
                  class="sm:col-span-2"
                >
                  <USelect
                    v-model="state.category"
                    :items="categoryOptions"
                    placeholder="انتخاب دسته‌بندی"
                  />
                </UFormField>

                <!-- Stock Status -->
                <div
                  v-if="state.capacity !== null"
                  class="sm:col-span-2 p-3 rounded-lg border flex items-center gap-2 text-sm"
                  :class="{
                    'bg-red-50 dark:bg-red-950/50 border-red-200 dark:border-red-800':
                      !stockStatus.available,
                    'bg-yellow-50 dark:bg-yellow-950/50 border-yellow-200 dark:border-yellow-800':
                      stockStatus.available && state.capacity <= 5,
                    'bg-green-50 dark:bg-green-950/50 border-green-200 dark:border-green-800':
                      stockStatus.available && state.capacity > 5,
                  }"
                >
                  <UIcon
                    :name="
                      stockStatus.available
                        ? 'i-lucide-check-circle'
                        : 'i-lucide-x-circle'
                    "
                    :class="{
                      'text-red-600 dark:text-red-400': !stockStatus.available,
                      'text-yellow-600 dark:text-yellow-400':
                        stockStatus.available && state.capacity <= 5,
                      'text-green-600 dark:text-green-400':
                        stockStatus.available && state.capacity > 5,
                    }"
                    class="size-5"
                  />
                  <span class="font-medium">{{ stockStatus.text }}</span>
                  <span class="mr-auto opacity-75"
                    >{{ state.capacity }} عدد</span
                  >
                </div>
              </div>
            </template>

            <!-- Product Details -->
            <template #details>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 pb-4">
                <UFormField label="جنسیت" name="gender" required>
                  <UInput v-model="state.gender" placeholder="مردانه" />
                </UFormField>

                <UFormField label="نوع عطر" name="type" required>
                  <USelect
                    v-model="state.type"
                    :items="typeOptions"
                    placeholder="انتخاب نوع"
                  />
                </UFormField>

                <!-- Brands Section -->
                <UFormField
                  label="برندها"
                  name="brands"
                  required
                  class="sm:col-span-2"
                >
                  <div class="space-y-3">
                    <UButton
                      type="button"
                      color="primary"
                      variant="soft"
                      icon="i-lucide-plus"
                      @click="showBrandModal = true"
                      block
                    >
                      انتخاب برند
                    </UButton>

                    <div v-if="state.brands.length" class="space-y-2">
                      <div class="flex items-center justify-between">
                        <p class="text-xs text-muted">
                          برندهای انتخاب شده: {{ state.brands.length }}
                        </p>
                        <UButton
                          v-if="state.brands.length > 1"
                          type="button"
                          color="error"
                          variant="ghost"
                          size="xs"
                          icon="i-lucide-trash-2"
                          @click="state.brands = []"
                        >
                          حذف همه
                        </UButton>
                      </div>

                      <div class="flex flex-wrap gap-2">
                        <div
                          v-for="brand in state.brands"
                          :key="brand.id"
                          class="group relative inline-flex items-center gap-2 px-3 py-2 rounded-lg bg-elevated hover:bg-primary/5 ring-1 ring-default hover:ring-primary/50 transition-all"
                        >
                          <img
                            v-if="brand.image"
                            :src="brand.image"
                            :alt="brand.name"
                            class="size-6 object-cover rounded ring-1 ring-default"
                          />
                          <div
                            v-else
                            class="size-6 bg-default rounded flex items-center justify-center"
                          >
                            <UIcon
                              name="i-lucide-image"
                              class="size-3 text-muted"
                            />
                          </div>

                          <NuxtLink
                            :to="`/product_brand/${brand.slug}`"
                            target="_blank"
                            class="text-sm font-medium hover:text-primary transition-colors"
                          >
                            {{ brand.name }}
                          </NuxtLink>

                          <button
                            type="button"
                            class="ml-1 p-1 text-muted hover:text-error hover:bg-error/10 rounded transition-all"
                            @click="removeBrand(brand.id)"
                            title="حذف برند"
                          >
                            <UIcon name="i-lucide-x" class="size-3.5" />
                          </button>
                        </div>
                      </div>
                    </div>

                    <div
                      v-else
                      class="text-center py-4 border border-dashed border-default rounded-lg"
                    >
                      <UIcon
                        name="i-lucide-package-search"
                        class="size-8 text-muted mx-auto mb-2"
                      />
                      <p class="text-xs text-muted">
                        هنوز برندی انتخاب نشده است
                      </p>
                    </div>
                  </div>
                </UFormField>

                <UFormField
                  label="عطر مشابه"
                  name="similar"
                  class="sm:col-span-2"
                >
                  <UInput
                    v-model="state.similar"
                    placeholder="Bleu de Chanel"
                  />
                </UFormField>

                <UFormField
                  label="فصل‌های مناسب"
                  name="seasons"
                  required
                  class="sm:col-span-2"
                >
                  <USelectMenu
                    v-model="state.seasons"
                    :items="seasonOptions"
                    multiple
                    placeholder="انتخاب فصل‌ها"
                  />
                </UFormField>

                <UFormField label="حجم" name="volume" required>
                  <UInput v-model="state.volume" placeholder="100ml" />
                </UFormField>
              </div>
            </template>

            <!-- Description Section -->
            <template #description>
              <div class="pb-4">
                <UFormField
                  label="توضیحات کامل محصول"
                  name="description"
                  description="توضیحات کامل محصول را با امکان افزودن متن و تصویر وارد کنید"
                  class="sm:col-span-2"
                >
                  <RichTextEditor
                    v-model="state.description"
                    placeholder="توضیحات محصول، نحوه استفاده، نکات مهم و ..."
                  />
                </UFormField>

                <!-- Preview -->
                <div v-if="state.description" class="mt-4">
                  <p class="text-sm font-medium text-default mb-2">
                    پیش‌نمایش:
                  </p>
                  <div
                    class="prose prose-sm max-w-none p-4 rounded-lg bg-elevated border border-default"
                    v-html="state.description"
                  />
                </div>
              </div>
            </template>

            <!-- Badge Section -->
            <template #badge>
              <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 pb-4">
                <UFormField label="درصد تخفیف" name="discountPercent">
                  <UInputNumber
                    v-model="state.discountPercent"
                    :min="0"
                    :max="100"
                  />
                </UFormField>

                <UFormField label="متن برچسب" name="badgeText">
                  <UInput v-model="state.badgeText" placeholder="جدید" />
                </UFormField>

                <UFormField
                  label="رنگ برچسب"
                  name="badgeColor"
                  class="sm:col-span-2"
                >
                  <USelect
                    v-model="state.badgeColor"
                    :items="badgeColorOptions"
                  />
                </UFormField>
              </div>
            </template>
          </UAccordion>

          <!-- Action Buttons -->
          <UCard>
            <div class="flex flex-col sm:flex-row gap-3">
              <UButton
                type="submit"
                size="lg"
                color="primary"
                icon="i-lucide-save"
                :loading="isSubmitting"
                :disabled="isSubmitting"
                class="flex-1 sm:flex-none"
              >
                {{ submitButtonText }}
              </UButton>

              <UButton
                type="button"
                size="lg"
                color="neutral"
                variant="outline"
                icon="i-lucide-x"
                :disabled="isSubmitting"
                @click="handleCancel"
                class="flex-1 sm:flex-none"
              >
                انصراف
              </UButton>
            </div>
          </UCard>
        </div>

        <!-- Right Sidebar - Image Upload (Desktop) -->
        <div class="hidden lg:block lg:col-span-1">
          <div class="sticky top-6">
            <UCard>
              <template #header>
                <div class="flex items-center gap-2">
                  <UIcon name="i-lucide-image" class="size-5" />
                  <span class="font-semibold">تصویر عطر</span>
                </div>
              </template>

              <UFormField
                name="image"
                :description="
                  mode === 'edit'
                    ? 'اختیاری - برای تغییر تصویر فایل جدید انتخاب کنید'
                    : 'JPG, PNG یا WebP (حداکثر 5MB)'
                "
                :required="mode === 'add'"
              >
                <div
                  v-if="mode === 'edit' && existingImageUrl && !state.image"
                  class="mb-3"
                >
                  <p class="text-sm text-muted mb-2">تصویر فعلی:</p>
                  <img
                    :src="existingImageUrl"
                    :alt="state.name"
                    class="w-full h-48 object-cover rounded-lg"
                  />
                </div>
                <UFileUpload
                  v-model="state.image"
                  accept="image/*"
                  icon="i-lucide-image"
                  :label="
                    mode === 'edit'
                      ? 'برای تغییر تصویر، فایل جدید را اینجا رها کنید'
                      : 'تصویر عطر را اینجا رها کنید'
                  "
                  description="یا کلیک کنید تا فایل انتخاب کنید"
                  class="min-h-64"
                />
              </UFormField>
            </UCard>
          </div>
        </div>
      </div>
    </UForm>

    <!-- Brand Selection Modal -->
    <BrandPicker
      v-model="showBrandModal"
      :selected-brands="state.brands"
      @select="onBrandSelect"
    />
  </div>
</template>
