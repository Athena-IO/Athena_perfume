<template>
  <UCard class="sticky top-10">
    <template #header>
      <div class="flex items-center justify-between">
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-filter" class="size-5 text-primary" />
          <h2 class="font-bold text-lg">فیلتر محصولات</h2>
        </div>
        <UButton
          v-if="hasActiveFilters"
          size="xs"
          color="neutral"
          variant="ghost"
          @click="resetFilters"
        >
          پاک کردن
        </UButton>
      </div>
    </template>

    <!-- دسته بندی با کارت‌ها -->
    <div class="space-y-3">
      <label
        class="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-2"
      >
        <UIcon name="i-lucide-layers" class="size-4" />
        دسته‌بندی
      </label>
      <URadioGroup
        v-model="localCategory"
        :items="categoryItems"
        color="primary"
        variant="card"
        @update:model-value="handleCategoryChange"
      />
    </div>

    <USeparator class="my-6" label="و" />

    <!-- فیلتر برند -->
    <div class="space-y-3">
      <label
        class="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-2"
      >
        <UIcon name="i-lucide-tag" class="size-4" />
        برند
      </label>
      <div class="space-y-2">
        <UCheckbox
          v-for="brand in brandItems"
          :key="brand.value"
          :model-value="selectedBrandValues[brand.value]"
          :label="brand.label"
          :description="brand.description"
          color="primary"
          size="md"
          @update:model-value="handleBrandChange(brand.value, $event)"
        />
      </div>
    </div>

    <USeparator class="my-6" label="یا" />

    <!-- مرتب سازی -->
    <div class="space-y-3">
      <label
        class="text-sm font-semibold text-gray-900 dark:text-white flex items-center gap-2"
      >
        <UIcon name="i-lucide-arrow-up-down" class="size-4" />
        مرتب‌سازی
      </label>
      <USelect
        v-model="localSort"
        :items="sortItems"
        icon="i-lucide-list-ordered"
        size="md"
        color="primary"
        @update:model-value="handleSortChange"
      />
    </div>

    <template #footer>
      <div
        class="flex items-center gap-2 text-xs text-gray-500 dark:text-gray-400"
      >
        <UIcon name="i-lucide-info" class="size-4" />
        <span>{{ filteredCount }} محصول یافت شد</span>
      </div>
    </template>
  </UCard>
</template>

<script setup>
import { ref, watch, computed, reactive } from "vue";

const props = defineProps({
  selectedCategory: String,
  selectedBrands: {
    type: Array,
    default: () => []
  },
  selectedSort: String,
  filteredCount: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(["update:category", "update:brands", "update:sort"]);

const localCategory = ref(props.selectedCategory);
const localSort = ref(props.selectedSort);

// Create a reactive object to track each brand's checked state
const selectedBrandValues = reactive({
  dior: false,
  chanel: false,
  lancome: false,
  versace: false,
  ysl: false,
  creed: false,
  burberry: false,
  tomford: false,
});

// Initialize selected brands from props
const initializeBrands = () => {
  // Reset all to false first
  Object.keys(selectedBrandValues).forEach(key => {
    selectedBrandValues[key] = false;
  });
  // Set selected ones to true
  props.selectedBrands.forEach(brand => {
    if (selectedBrandValues.hasOwnProperty(brand)) {
      selectedBrandValues[brand] = true;
    }
  });
};

// Initialize on mount
initializeBrands();

// آیتم‌های دسته‌بندی با آیکون
const categoryItems = [
  {
    label: "همه محصولات",
    value: "all",
    description: "نمایش تمام عطرها",
  },
  {
    label: "مردانه",
    value: "male",
    description: "عطرهای مخصوص آقایان",
  },
  {
    label: "زنانه",
    value: "female",
    description: "عطرهای مخصوص بانوان",
  },
  {
    label: "یونیسکس",
    value: "unisex",
    description: "مناسب برای همه",
  },
];

// آیتم‌های برند
const brandItems = [
  {
    label: "دیور",
    value: "dior",
    description: "Dior",
  },
  {
    label: "شنل",
    value: "chanel",
    description: "Chanel",
  },
  {
    label: "لانکوم",
    value: "lancome",
    description: "Lancôme",
  },
  {
    label: "ورساچه",
    value: "versace",
    description: "Versace",
  },
  {
    label: "ایو سن لورن",
    value: "ysl",
    description: "YSL",
  },
  {
    label: "کرید",
    value: "creed",
    description: "Creed",
  },
  {
    label: "بربری",
    value: "burberry",
    description: "Burberry",
  },
  {
    label: "تام فورد",
    value: "tomford",
    description: "Tom Ford",
  },
];

// آیتم‌های مرتب‌سازی
const sortItems = [
  {
    label: "بدون مرتب‌سازی",
    value: "none",
    icon: "i-lucide-minus",
  },
  {
    label: "ارزان‌ترین",
    value: "price_low_high",
    icon: "i-lucide-trending-down",
  },
  {
    label: "گران‌ترین",
    value: "price_high_low",
    icon: "i-lucide-trending-up",
  },
];

// Get currently selected brands as array
const getSelectedBrands = () => {
  return Object.keys(selectedBrandValues).filter(
    key => selectedBrandValues[key] === true
  );
};

// بررسی فیلترهای فعال
const hasActiveFilters = computed(() => {
  const selectedBrands = getSelectedBrands();
  return (
    localCategory.value !== "all" ||
    selectedBrands.length > 0 ||
    localSort.value !== "none"
  );
});

// Handle brand checkbox change
const handleBrandChange = (brandValue, isChecked) => {
  selectedBrandValues[brandValue] = isChecked;
  const selectedBrands = getSelectedBrands();
  emit("update:brands", selectedBrands);
};

// Handle category change
const handleCategoryChange = () => {
  emit("update:category", localCategory.value);
};

// Handle sort change
const handleSortChange = () => {
  emit("update:sort", localSort.value);
};

// ریست کردن فیلترها
const resetFilters = () => {
  localCategory.value = "all";
  localSort.value = "none";
  
  // Reset all brand checkboxes
  Object.keys(selectedBrandValues).forEach(key => {
    selectedBrandValues[key] = false;
  });
  
  emit("update:category", "all");
  emit("update:brands", []);
  emit("update:sort", "none");
};

// همگام‌سازی props → local
watch(
  () => props.selectedCategory,
  (val) => {
    localCategory.value = val;
  }
);

watch(
  () => props.selectedBrands,
  (newBrands) => {
    initializeBrands();
  },
  { deep: true }
);

watch(
  () => props.selectedSort,
  (val) => {
    localSort.value = val;
  }
);
</script>
