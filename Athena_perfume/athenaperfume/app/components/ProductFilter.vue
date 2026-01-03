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
      <USelect
        v-model="localCategory"
        :items="categoryDropdownItems"
        color="primary"
        option-variant="card"
        size="md"
        @update:model-value="emit('update:category', localCategory)"
        :loading="categoriesStore.loading"
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
          :loading="brandsStore.loading"
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
        <span>{{ productsStore.filteredProducts.length }} محصول یافت شد</span>
      </div>
    </template>
  </UCard>
</template>

<script setup>
import { useCategoriesStore } from '~/stores/categories.js';
import { useBrandsStore } from '~/stores/brands.js';
import { useProductsStore } from '~/stores/products.js';
import { computed, onMounted } from 'vue';

const productsStore = useProductsStore();
const categoriesStore = useCategoriesStore();
const brandsStore = useBrandsStore();

onMounted(() => {
  categoriesStore.fetchCategories();
  brandsStore.fetchBrands();
});

const categoryDropdownItems = computed(() =>
  categoriesStore.categories.map(c => ({
    label: c.label || c.name,
    value: c.value || c.slug,
    description: c.description
  }))
);

const brandItems = computed(() =>
  brandsStore.brands.map(b => ({ label: b.name, value: b.slug, description: b.name }))
);

const localCategory = computed({
  get: () => productsStore.selectedCategory,
  set: (value) => productsStore.setSelectedCategory(value)
});

const localBrands = computed({
  get: () => productsStore.selectedBrands,
  set: (value) => productsStore.setSelectedBrands(value)
});

const localSort = computed({
  get: () => productsStore.selectedSort,
  set: (value) => productsStore.setSelectedSort(value)
});

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
    productsStore.selectedCategory !== "all" ||
    productsStore.selectedBrands.length > 0 ||
    productsStore.selectedSort !== "none"
);

function handleBrandToggle(brandValue, isChecked) {
  let updatedBrands = [...productsStore.selectedBrands];
  if (isChecked) {
    updatedBrands.push(brandValue);
  } else {
    updatedBrands = updatedBrands.filter((b) => b !== brandValue);
  }
  productsStore.setSelectedBrands(updatedBrands);
}

function resetFilters() {
  productsStore.setSelectedCategory("all");
  productsStore.setSelectedBrands([]);
  productsStore.setSelectedSort("none");
}
</script>
