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
        @update:model-value="$emit('update:category', localCategory)"
      />
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
        @update:model-value="$emit('update:sort', localSort)"
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
import { ref, watch, computed } from "vue";

const props = defineProps({
  selectedCategory: String,
  selectedSort: String,
  filteredCount: {
    type: Number,
    default: 0,
  },
});

const emit = defineEmits(["update:category", "update:sort"]);

const localCategory = ref(props.selectedCategory);
const localSort = ref(props.selectedSort);

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

// بررسی فیلترهای فعال
const hasActiveFilters = computed(() => {
  return localCategory.value !== "all" || localSort.value !== "none";
});

// ریست کردن فیلترها
const resetFilters = () => {
  localCategory.value = "all";
  localSort.value = "none";
  emit("update:category", "all");
  emit("update:sort", "none");
};

// همگام‌سازی props → local
watch(
  () => props.selectedCategory,
  (val) => (localCategory.value = val)
);
watch(
  () => props.selectedSort,
  (val) => (localSort.value = val)
);
</script>
