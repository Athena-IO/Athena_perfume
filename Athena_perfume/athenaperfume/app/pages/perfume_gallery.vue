<script setup>
import { useClipboard } from "@vueuse/core";

const toast = useToast();
const router = useRouter();
const { copy } = useClipboard();

const {
  data: perfumes,
  refresh,
  pending,
} = await useFetch("/api/perfumes", {
  lazy: true,
});

// Filter states
const searchQuery = ref("");
const selectedCategory = ref("all");
const selectedBrands = ref([]);
const selectedSort = ref("none");

// Filter and search logic
const filteredData = computed(() => {
  if (!perfumes.value) return [];

  let filtered = perfumes.value;

  // Category filter
  if (selectedCategory.value !== "all") {
    filtered = filtered.filter((p) => p.category === selectedCategory.value);
  }

  // Brand filter
  if (selectedBrands.value.length > 0) {
    filtered = filtered.filter((p) =>
      p.brands?.some((b) => selectedBrands.value.includes(b.slug))
    );
  }

  // Search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (p) =>
        p.name.toLowerCase().includes(query) ||
        p.slug.toLowerCase().includes(query) ||
        p.brands?.some((b) => b.name.toLowerCase().includes(query))
    );
  }

  // Sorting
  if (selectedSort.value === "price_low_high") {
    filtered = [...filtered].sort((a, b) => a.originalPrice - b.originalPrice);
  } else if (selectedSort.value === "price_high_low") {
    filtered = [...filtered].sort((a, b) => b.originalPrice - a.originalPrice);
  } else if (selectedSort.value === "capacity_low") {
    filtered = [...filtered].sort((a, b) => a.capacity - b.capacity);
  }

  return filtered;
});

// Actions
function editPerfume(perfume) {
  router.push(`/admin/perfumes/edit/${perfume.id}`);
}

async function deletePerfume(perfume) {
  if (!confirm(`آیا مطمئن هستید که می‌خواهید "${perfume.name}" را حذف کنید؟`)) {
    return;
  }

  try {
    await $fetch(`/api/perfumes/${perfume.id}`, {
      method: "DELETE",
    });

    toast.add({
      title: "عطر حذف شد",
      description: `${perfume.name} با موفقیت حذف شد`,
      color: "success",
      icon: "i-lucide-check",
    });

    refresh();
  } catch (error) {
    toast.add({
      title: "خطا در حذف",
      description: "مشکلی در حذف عطر پیش آمد",
      color: "error",
      icon: "i-lucide-x",
    });
  }
}

// Statistics
const stats = computed(() => {
  const data = perfumes.value || [];
  return {
    total: data.length,
    outOfStock: data.filter((p) => p.capacity === 0).length,
    lowStock: data.filter((p) => p.capacity > 0 && p.capacity <= 5).length,
    inStock: data.filter((p) => p.capacity > 5).length,
  };
});

// Helper to get category info
const getCategoryInfo = (category) => {
  const categoryMap = {
    male: { label: "مردانه", color: "info" },
    female: { label: "زنانه", color: "secondary" },
    unisex: { label: "یونیسکس", color: "neutral" },
  };
  return categoryMap[category] || { label: category, color: "neutral" };
};

// Helper to get capacity info
const getCapacityInfo = (capacity) => {
  if (capacity === 0) {
    return { color: "error", label: "ناموجود" };
  } else if (capacity <= 5) {
    return { color: "warning", label: `${capacity} عدد` };
  }
  return { color: "success", label: `${capacity} عدد` };
};

// Calculate final price with discount
const getFinalPrice = (originalPrice, discountPercent = 0) => {
  return originalPrice - (originalPrice * discountPercent) / 100;
};
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 max-w-7xl">
    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-default">
          مدیریت عطرها
        </h1>
        <p class="text-sm text-muted mt-1">لیست و مدیریت عطرهای فروشگاه</p>
      </div>

      <UButton
        to="/admin/perfumes/add"
        color="primary"
        icon="i-lucide-plus"
        size="lg"
      >
        افزودن عطر جدید
      </UButton>
    </div>

    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <UCard>
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-lg bg-primary/10">
            <UIcon name="i-lucide-package" class="size-6 text-primary" />
          </div>
          <div>
            <p class="text-sm text-muted">کل عطرها</p>
            <p class="text-2xl font-bold text-highlighted">{{ stats.total }}</p>
          </div>
        </div>
      </UCard>

      <UCard>
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-lg bg-success/10">
            <UIcon name="i-lucide-check-circle" class="size-6 text-success" />
          </div>
          <div>
            <p class="text-sm text-muted">موجود</p>
            <p class="text-2xl font-bold text-success">{{ stats.inStock }}</p>
          </div>
        </div>
      </UCard>

      <UCard>
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-lg bg-warning/10">
            <UIcon name="i-lucide-alert-triangle" class="size-6 text-warning" />
          </div>
          <div>
            <p class="text-sm text-muted">کمبود موجودی</p>
            <p class="text-2xl font-bold text-warning">{{ stats.lowStock }}</p>
          </div>
        </div>
      </UCard>

      <UCard>
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-lg bg-error/10">
            <UIcon name="i-lucide-x-circle" class="size-6 text-error" />
          </div>
          <div>
            <p class="text-sm text-muted">ناموجود</p>
            <p class="text-2xl font-bold text-error">{{ stats.outOfStock }}</p>
          </div>
        </div>
      </UCard>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Filters -->
      <div class="lg:col-span-1">
        <ProductFilter
          :selected-category="selectedCategory"
          :selected-brands="selectedBrands"
          :selected-sort="selectedSort"
          :filtered-count="filteredData.length"
          @update:category="selectedCategory = $event"
          @update:brands="selectedBrands = $event"
          @update:sort="selectedSort = $event"
        />
      </div>

      <!-- Products Grid -->
      <div class="lg:col-span-3">
        <UCard>
          <template #header>
            <div
              class="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between"
            >
              <!-- Search -->
              <UInput
                v-model="searchQuery"
                placeholder="جستجو بر اساس نام، برند یا اسلاگ..."
                icon="i-lucide-search"
                class="w-full sm:max-w-sm"
                size="md"
              />

              <!-- Refresh Button -->
              <UButton
                color="neutral"
                variant="outline"
                icon="i-lucide-refresh-cw"
                size="sm"
                :loading="pending"
                @click="refresh"
              >
                بروزرسانی
              </UButton>
            </div>
          </template>

          <!-- Loading State -->
          <div
            v-if="pending"
            class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 p-4"
          >
            <div v-for="n in 6" :key="n" class="space-y-3">
              <USkeleton class="h-48 w-full rounded-lg" />
              <USkeleton class="h-4 w-3/4" />
              <USkeleton class="h-4 w-1/2" />
            </div>
          </div>

          <!-- Empty State -->
          <div v-else-if="filteredData.length === 0" class="text-center py-12">
            <UIcon
              name="i-lucide-package-x"
              class="size-16 text-gray-400 mx-auto mb-4"
            />
            <p class="text-gray-600 dark:text-gray-400 text-lg">
              محصولی یافت نشد
            </p>
          </div>

          <!-- Products Cards Grid -->
          <div
            v-else
            class="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-4 p-4"
          >
            <UCard
              v-for="perfume in filteredData"
              :key="perfume.id"
              class="overflow-hidden hover:shadow-lg transition-shadow"
            >
              <!-- Image Section -->
              <div
                class="relative aspect-video overflow-hidden rounded-lg bg-gray-100 dark:bg-gray-800"
              >
                <img
                  :src="perfume.image || '/placeholder.png'"
                  :alt="perfume.name"
                  class="w-full h-full object-cover"
                />

                <!-- Discount Badge -->
                <UBadge
                  v-if="perfume.discountPercent > 0"
                  color="error"
                  class="absolute top-2 right-2"
                >
                  {{ perfume.discountPercent }}% تخفیف
                </UBadge>

                <!-- Capacity Badge -->
                <UBadge
                  :color="getCapacityInfo(perfume.capacity).color"
                  variant="subtle"
                  class="absolute top-2 left-2"
                >
                  {{ getCapacityInfo(perfume.capacity).label }}
                </UBadge>
              </div>

              <!-- Content Section -->
              <div class="space-y-3 mt-4">
                <!-- Title -->
                <div>
                  <h3
                    class="font-semibold text-lg text-highlighted line-clamp-1"
                  >
                    {{ perfume.name }}
                  </h3>
                  <p class="text-xs text-muted">{{ perfume.slug }}</p>
                </div>

                <!-- Category & Brands -->
                <div class="flex flex-wrap items-center gap-2">
                  <UBadge
                    :color="getCategoryInfo(perfume.category).color"
                    variant="subtle"
                    size="xs"
                  >
                    {{ getCategoryInfo(perfume.category).label }}
                  </UBadge>

                  <UBadge
                    v-for="brand in perfume.brands || []"
                    :key="brand.slug"
                    color="neutral"
                    variant="subtle"
                    size="xs"
                  >
                    {{ brand.name }}
                  </UBadge>
                </div>

                <!-- Price -->
                <div class="pt-2 border-t border-gray-200 dark:border-gray-700">
                  <div v-if="perfume.discountPercent > 0" class="space-y-1">
                    <p class="text-lg font-bold text-success">
                      {{
                        getFinalPrice(
                          perfume.originalPrice,
                          perfume.discountPercent
                        ).toLocaleString("fa-IR")
                      }}
                      تومان
                    </p>
                    <p class="text-sm text-muted line-through">
                      {{ perfume.originalPrice.toLocaleString("fa-IR") }} تومان
                    </p>
                  </div>
                  <p v-else class="text-lg font-bold text-highlighted">
                    {{ perfume.originalPrice.toLocaleString("fa-IR") }} تومان
                  </p>
                </div>

                <!-- Additional Info -->
                <div class="flex items-center gap-3 text-xs text-muted pt-2">
                  <div class="flex items-center gap-1">
                    <UIcon name="i-lucide-star" class="size-4" />
                    <span>{{ perfume.rating || 0 }}</span>
                  </div>
                  <div class="flex items-center gap-1">
                    <UIcon name="i-lucide-message-circle" class="size-4" />
                    <span>{{ perfume.reviews || 0 }} نظر</span>
                  </div>
                  <div class="flex items-center gap-1">
                    <UIcon name="i-lucide-droplet" class="size-4" />
                    <span>{{ perfume.capacity }} ml</span>
                  </div>
                </div>

                <!-- Action Buttons -->
                <div class="grid grid-cols-2 gap-2 pt-3">
                  <UButton
                    color="primary"
                    variant="outline"
                    icon="i-lucide-edit"
                    block
                    @click="editPerfume(perfume)"
                  >
                    ویرایش
                  </UButton>

                  <UButton
                    color="error"
                    variant="outline"
                    icon="i-lucide-trash"
                    block
                    @click="deletePerfume(perfume)"
                  >
                    حذف
                  </UButton>
                </div>
              </div>
            </UCard>
          </div>

          <template #footer>
            <div class="flex items-center justify-between text-sm text-muted">
              <span>{{ filteredData.length }} مورد نمایش داده شده</span>
              <span>از مجموع {{ stats.total }} عطر</span>
            </div>
          </template>
        </UCard>
      </div>
    </div>
  </div>
</template>
