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
    default: "add", // 'add' or 'edit'
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
});

const showBrandModal = ref(false);
const existingImageUrl = ref(null);

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

const categoryOptions = [
  { label: "مردانه", value: "male" },
  { label: "زنانه", value: "female" },
  { label: "یونیسکس", value: "unisex" },
];

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

// Accordion items for better organization
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
  // Only require image for new perfumes
  if (props.mode === "add" && !formState.image) {
    errors.push({ name: "image", message: "لطفا یک تصویر انتخاب کنید" });
  }
  // Validate image if provided
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
    // Only auto-generate slug when adding new perfume and slug is empty
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
    });
  }
}

// Load existing perfume data when in edit mode
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
    });

    // Store existing image URL
    if (props.perfume.image) {
      existingImageUrl.value = props.perfume.image;
    }
  }
});

async function onSubmit(event) {
  const seasonsText = event.data.seasons
    .map((season) => {
      const option = seasonOptions.find((s) => s.value === season);
      return option ? option.label : season;
    })
    .join("، ");

  const payload = {
    slug: event.data.slug,
    name: event.data.name,
    originalPrice: event.data.originalPrice,
    discountPercent: event.data.discountPercent,
    category: event.data.category,
    badgeText: event.data.badgeText || "",
    badgeColor: event.data.badgeColor || "primary",
    gender: event.data.gender,
    brands: event.data.brands,
    similar: event.data.similar || "",
    type: event.data.type,
    seasons: event.data.seasons,
    seasonsText,
    volume: event.data.volume,
    capacity: event.data.capacity,
    sold: event.data.sold || 0,
  };

  const formData = new FormData();
  Object.entries(payload).forEach(([key, value]) => {
    if (Array.isArray(value) || typeof value === "object") {
      formData.append(key, JSON.stringify(value));
    } else {
      formData.append(key, String(value));
    }
  });

  if (event.data.image) {
    formData.append("image", event.data.image);
  }

  try {
    let response;

    if (props.mode === "edit") {
      // Update existing perfume
      response = await $fetch(`/api/perfumes/${props.perfume.id}`, {
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
      response = await $fetch("/api/perfumes", {
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

    // Emit success event and navigate
    emit("success", response);
    router.push("/admin/perfumes");
  } catch (error) {
    console.error("Error saving perfume:", error);
    toast.add({
      title: "خطا",
      description:
        props.mode === "edit"
          ? "خطا در ویرایش عطر در پایگاه داده"
          : "خطا در ذخیره‌سازی عطر در پایگاه داده",
      color: "error",
      icon: "i-lucide-x",
    });
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
        <!-- Main Content - Left Side -->
        <div class="lg:col-span-2 space-y-4">
          <!-- Image Upload Card - Mobile First -->
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

                <!-- Stock Status Indicator -->
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

                <UFormField
                  label="برندها"
                  name="brands"
                  required
                  class="sm:col-span-2"
                >
                  <div class="space-y-2">
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

                    <div
                      v-if="state.brands.length"
                      class="flex flex-wrap gap-2"
                    >
                      <NuxtLink
                        v-for="brand in state.brands"
                        :key="brand.id"
                        :to="`/product_brand/${brand.slug}`"
                        class="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg bg-elevated text-xs font-medium hover:bg-primary/10 hover:text-primary transition-colors ring-1 ring-default"
                      >
                        <span>{{ brand.name }}</span>
                        <button
                          type="button"
                          class="text-muted hover:text-error transition-colors"
                          @click.stop.prevent="
                            state.brands = state.brands.filter(
                              (b) => b.id !== brand.id
                            )
                          "
                        >
                          <UIcon name="i-lucide-x" class="size-3.5" />
                        </button>
                      </NuxtLink>
                    </div>
                    <p v-else class="text-xs text-muted">
                      هنوز برندی انتخاب نشده است.
                    </p>
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

    <!-- Brand picker modal -->
    <BrandSelectModal v-model="showBrandModal" @select="onBrandSelect" />
  </div>
</template>
