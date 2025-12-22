<template>
  <NuxtLink
    v-if="product && product.slug"
    :to="`/products/${product.slug}`"
    class="group block border border-gray-200 dark:border-gray-800 rounded-xl overflow-hidden hover:shadow-xl hover:border-primary/50 dark:hover:border-primary/50 transition-all duration-300 bg-white dark:bg-gray-900"
  >
    <!-- Product Image -->
    <div
      class="relative aspect-square bg-gray-50 dark:bg-gray-800 overflow-hidden"
    >
      <img
        :src="product.image"
        :alt="product.name"
        class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
        :class="{ grayscale: isOutOfStock }"
      />

      <!-- Gradient overlay on hover -->
      <div
        class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
      />

      <!-- Out of Stock Badge -->
      <div v-if="isOutOfStock" class="absolute top-3 right-3 z-10">
        <UBadge
          color="red"
          variant="solid"
          size="md"
          class="shadow-lg backdrop-blur-sm"
        >
          ناموجود
        </UBadge>
      </div>

      <!-- Discount Badge (Dark Red) -->
      <div v-else-if="hasDiscount" class="absolute top-3 right-3 z-10">
        <div
          class="bg-red-900 text-white px-3 py-2 rounded-lg shadow-lg backdrop-blur-sm"
        >
          <div class="flex items-center gap-1">
            <UIcon name="i-lucide-percent" class="w-4 h-4" />
            <span class="text-sm font-bold">{{ discountPercent }}٪ تخفیف</span>
          </div>
        </div>
      </div>

      <!-- Badge for new items or other badges -->
      <div v-else-if="product.badge" class="absolute top-3 right-3 z-10">
        <UBadge
          :color="product.badge.color"
          variant="solid"
          size="md"
          class="shadow-lg backdrop-blur-sm"
        >
          {{ product.badge.text }}
        </UBadge>
      </div>
    </div>

    <!-- Product Info -->
    <div class="p-5 space-y-3">
      <!-- Rating & Reviews -->
      <div class="flex items-center gap-2">
        <div
          class="flex items-center gap-1 px-2 py-1 rounded-md bg-amber-50 dark:bg-amber-900/20"
        >
          <UIcon
            name="i-lucide-star"
            class="text-amber-500 w-4 h-4 fill-amber-500"
          />
          <span
            class="text-sm font-semibold text-amber-700 dark:text-amber-400"
            >{{ product.rating }}</span
          >
        </div>
        <span class="text-sm text-gray-500 dark:text-gray-400"
          >({{ product.reviews || 0 }} reviews)</span
        >
      </div>

      <!-- Product Name -->
      <h3
        class="font-semibold text-base line-clamp-2 text-gray-900 dark:text-white group-hover:text-primary transition-colors min-h-[3rem]"
      >
        {{ product.name }}
      </h3>

      <!-- Price Section (Available) -->
      <div
        v-if="!isOutOfStock"
        class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800"
      >
        <div class="flex items-baseline gap-2">
          <!-- قیمت جدید با رنگ قرمز تیره در صورت تخفیف -->
          <p
            class="text-xl font-bold"
            :class="
              hasDiscount ? 'text-red-900 dark:text-red-500' : 'text-primary'
            "
          >
            {{ formatPrice(finalPrice) }}
          </p>

          <!-- قیمت قبلی -->
          <p
            v-if="oldPrice"
            class="text-sm text-gray-400 dark:text-gray-500 line-through"
          >
            {{ formatPrice(oldPrice) }}
          </p>
        </div>

        <UButton
          icon="i-lucide-shopping-cart"
          color="primary"
          variant="soft"
          size="sm"
          square
          class="opacity-0 group-hover:opacity-100 transition-opacity duration-300"
        />
      </div>

      <!-- Out of Stock Section -->
      <div
        v-else
        class="flex items-center justify-center pt-2 border-t border-gray-100 dark:border-gray-800"
      >
        <div
          class="flex items-center gap-2 px-4 py-2 rounded-lg bg-red-50 dark:bg-red-900/20"
        >
          <UIcon name="i-lucide-package-x" class="text-red-500 w-5 h-5" />
          <span class="text-sm font-semibold text-red-600 dark:text-red-400">
            این محصول موجود نیست
          </span>
        </div>
      </div>

      <!-- Discount label -->
    </div>
  </NuxtLink>
</template>

<script setup>
const { product } = defineProps({
  product: {
    type: Object,
    required: true,
  },
});

// تبدیل قیمت به تومان فارسی
const formatPrice = (num) => {
  return num.toLocaleString("fa-IR") + " تومان";
};

// بررسی موجود بودن محصول
const isOutOfStock = computed(() => {
  return product.capacity === 0;
});

// بررسی وجود تخفیف
const hasDiscount = computed(() => {
  return product.discountPercent && product.discountPercent > 0;
});

// قیمت با تخفیف
const finalPrice = computed(() => {
  if (!product.discountPercent) return product.price;
  return product.price - (product.price * product.discountPercent) / 100;
});

// قیمت اصلی
const oldPrice = computed(() => {
  return product.discountPercent ? product.price : null;
});

// درصد تخفیف برای نمایش
const discountPercent = computed(() => product.discountPercent || 0);
</script>
