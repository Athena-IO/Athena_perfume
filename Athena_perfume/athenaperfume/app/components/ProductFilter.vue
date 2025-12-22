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

    <!-- دسته بندی -->
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
        @update:model-value="emit('update:category', localCategory)"
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
          :model-value="localBrands.includes(brand.value)"
          :label="brand.label"
          :description="brand.description"
          color="primary"
          size="md"
          @update:model-value="handleBrandToggle(brand.value, $event)"
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
        @update:model-value="emit('update:sort', localSort)"
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
const props = defineProps({
  selectedCategory: {
    type: String,
    required: true,
  },
  selectedBrands: {
    type: Array,
    default: () => [],
  },
  selectedSort: {
    type: String,
    required: true,
  },
  filteredCount: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(["update:category", "update:brands", "update:sort"]);

const localCategory = ref(props.selectedCategory);
const localBrands = ref([...props.selectedBrands]);
const localSort = ref(props.selectedSort);

const categoryItems = [
  { label: "همه محصولات", value: "all", description: "نمایش تمام عطرها" },
  { label: "مردانه", value: "male", description: "عطرهای مخصوص آقایان" },
  { label: "زنانه", value: "female", description: "عطرهای مخصوص بانوان" },
  { label: "یونیسکس", value: "unisex", description: "مناسب برای همه" },
];

const brandItems = [
  { label: "دیور", value: "dior", description: "Dior" },
  { label: "شنل", value: "chanel", description: "Chanel" },
  { label: "لانکوم", value: "lancome", description: "Lancôme" },
  { label: "ورساچه", value: "versace", description: "Versace" },
  { label: "ایو سن لورن", value: "ysl", description: "YSL" },
  { label: "کرید", value: "creed", description: "Creed" },
  { label: "بربری", value: "burberry", description: "Burberry" },
  { label: "تام فورد", value: "tomford", description: "Tom Ford" },
];

const sortItems = [
  { label: "بدون مرتب‌سازی", value: "none", icon: "i-lucide-minus" },
  {
    label: "ارزان‌ترین",
    value: "price_low_high",
    icon: "i-lucide-trending-down",
  },
  { label: "گران‌ترین", value: "price_high_low", icon: "i-lucide-trending-up" },
];

const hasActiveFilters = computed(
  () =>
    localCategory.value !== "all" ||
    localBrands.value.length > 0 ||
    localSort.value !== "none"
);

function handleBrandToggle(brandValue, isChecked) {
  if (isChecked) {
    localBrands.value.push(brandValue);
  } else {
    localBrands.value = localBrands.value.filter((b) => b !== brandValue);
  }
  emit("update:brands", localBrands.value);
}

function resetFilters() {
  localCategory.value = "all";
  localBrands.value = [];
  localSort.value = "none";

  emit("update:category", "all");
  emit("update:brands", []);
  emit("update:sort", "none");
}

// Sync props with local state
watch(
  () => props.selectedCategory,
  (val) => {
    localCategory.value = val;
  }
);

watch(
  () => props.selectedBrands,
  (val) => {
    localBrands.value = [...val];
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
