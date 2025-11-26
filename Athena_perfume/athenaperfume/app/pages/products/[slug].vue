<template>
  <UContainer class="py-8 sm:py-12">
    <div v-if="product" class="max-w-7xl mx-auto">
      <!-- Grid Layout for Product -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 lg:gap-12">
        <!-- Product Image -->
        <div class="flex justify-center lg:justify-end">
          <UCard class="overflow-hidden">
            <img 
              :src="product.image" 
              :alt="product.name"
              class="w-full max-w-md h-auto object-cover rounded-lg"
            />
          </UCard>
        </div>

        <!-- Product Details -->
        <div class="flex flex-col justify-center space-y-6">
          <!-- Title & Price -->
          <div class="space-y-3">
            <h1 class="text-3xl sm:text-4xl font-bold text-gray-900 dark:text-white">
              {{ product.name }}
            </h1>
            <p class="text-2xl sm:text-3xl font-semibold text-primary">
              {{ product.price }}
            </p>
          </div>

          <!-- Divider -->
          <div class="border-t border-gray-200 dark:border-gray-700"></div>

          <!-- Quantity & Add to Cart -->
          <div class="space-y-4">
            <div>
              <label class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                تعداد
              </label>
              <QuantityBox v-model="qty" />
            </div>

            <UButton
              color="primary"
              variant="solid"
              size="xl"
              block
              icon="i-lucide-shopping-cart"
              @click="cart.addToCart(product, qty)"
            >
              افزودن به سبد خرید
            </UButton>
          </div>

          <!-- Additional Info (Optional) -->
          <div class="pt-4 space-y-2 text-sm text-gray-600 dark:text-gray-400">
            <p class="flex items-center gap-2">
              <span class="i-lucide-check-circle text-success"></span>
              موجود در انبار
            </p>
            <p class="flex items-center gap-2">
              <span class="i-lucide-truck text-info"></span>
              ارسال رایگان برای خریدهای بالای ۵۰۰,۰۰۰ تومان
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Product Not Found -->
    <UCard v-else variant="outline">
      <div class="text-center py-12">
        <span class="i-lucide-package-x text-6xl text-gray-400 dark:text-gray-600 mb-4"></span>
        <p class="text-xl text-gray-600 dark:text-gray-400">محصول پیدا نشد</p>
      </div>
    </UCard>
  </UContainer>
</template>

<script setup>
import { ref } from "vue";
import { useRoute } from "vue-router";
import { useCartStore } from "~/composables/stores/cart";

const route = useRoute();
const cart = useCartStore();

// مقدار اولیه تعداد
const qty = ref(1);

// دریافت محصول بر اساس slug
const slug = route.params.slug;

const products = [
  { id: 1, slug: "nike-air-max-1", name: "کفش ورزشی نایک ایر مکس", price: "۲,۵۰۰,۰۰۰ تومان", image: "https://picsum.photos/400/400?random=1" },
  { id: 2, slug: "nike-air-max-2", name: "کفش ورزشی نایک ایر مکس", price: "۲,۵۰۰,۰۰۰ تومان", image: "https://picsum.photos/400/400?random=2" },
  { id: 3, slug: "nike-air-max-3", name: "کفش ورزشی نایک ایر مکس", price: "۲,۵۰۰,۰۰۰ تومان", image: "https://picsum.photos/400/400?random=3" },
  { id: 4, slug: "nike-air-max-4", name: "کفش ورزشی نایک ایر مکس", price: "۲,۵۰۰,۰۰۰ تومان", image: "https://picsum.photos/400/random=4" },
  { id: 5, slug: "nike-air-max-5", name: "کفش ورزشی نایک ایر مکس", price: "۲,۵۰۰,۰۰۰ تومان", image: "https://picsum.photos/400/400?random=5" },
];

const product = products.find((p) => p.slug === slug);
</script>
