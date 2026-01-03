<template>
  <div class="p-4 sm:p-6">
    <UContainer>
      <div class="flex flex-col lg:flex-row gap-4 sm:gap-6">
        <!-- Desktop Filters -->
        <aside class="hidden lg:block lg:w-64 shrink-0">
          <ProductFilter />
        </aside>

        <!-- Main Content -->
        <div class="flex-1">
          <!-- Mobile Filter Button -->
          <div class="lg:hidden mb-4">
            <UDrawer
              v-model:open="isFilterOpen"
              direction="left"
              title="فیلترها"
            >
              <UButton
                label="نمایش فیلترها"
                icon="i-lucide-filter"
                color="neutral"
                variant="outline"
                block
              />

              <template #body>
                <ProductFilter />
              </template>

              <template #footer>
                <UButton
                  label="نمایش نتایج"
                  color="primary"
                  block
                  @click="isFilterOpen = false"
                />
              </template>
            </UDrawer>
          </div>

          <!-- Product Grid -->
          <div
            class="grid grid-cols-2 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-3 xl:grid-cols-4 gap-3 sm:gap-4 md:gap-6"
          >
            <ProductCard
              v-for="product in productsStore.paginatedProducts"
              :key="product.id"
              :product="product"
            />
          </div>

          <!-- Empty State -->
          <div v-if="productsStore.filteredProducts.length === 0" class="text-center py-12">
            <UIcon
              name="i-lucide-package-x"
              class="size-16 text-gray-400 mx-auto mb-4"
            />
            <p class="text-gray-600 dark:text-gray-400 text-lg">
              محصولی یافت نشد
            </p>
          </div>

          <!-- Pagination controls -->
          <div
            v-if="productsStore.totalPages > 1"
            class="flex justify-center mt-8 gap-2"
          >
            <UButton
              icon="i-lucide-arrow-right"
              color="neutral"
              variant="outline"
              :disabled="productsStore.currentPage === 1"
              @click="productsStore.prevPage()"
            />
            <UButton
              v-for="page in productsStore.totalPages"
              :key="page"
              :color="productsStore.currentPage === page ? 'primary' : 'neutral'"
              variant="outline"
              @click="productsStore.setCurrentPage(page)"
            >
              {{ page }}
            </UButton>
            <UButton
              icon="i-lucide-arrow-left"
              color="neutral"
              variant="outline"
              :disabled="productsStore.currentPage === productsStore.totalPages"
              @click="productsStore.nextPage()"
            />
          </div>
        </div>
      </div>
    </UContainer>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import ProductFilter from "~/components/ProductFilter.vue";
import ProductCard from "~/components/ProductCard.vue";
import { useProductsStore } from "~/stores/products.js";

const productsStore = useProductsStore();
const isFilterOpen = ref(false); // For mobile filter drawer

const props = defineProps({
  category: {
    type: String,
    default: "all",
  },
  brand: {
    type: String,
    default: null,
  },
});

onMounted(() => {
  productsStore.fetchAllProducts();
  // Set initial category and brand from props
  if (props.category) {
    productsStore.setSelectedCategory(props.category);
  }
  if (props.brand) {
    productsStore.setSelectedBrands([props.brand]);
  }
});

// Watch for prop changes and update store state
watch(
  () => props.category,
  (newCategory) => {
    productsStore.setSelectedCategory(newCategory);
  }
);

watch(
  () => props.brand,
  (newBrand) => {
    productsStore.setSelectedBrands(newBrand ? [newBrand] : []);
  }
);

</script>
