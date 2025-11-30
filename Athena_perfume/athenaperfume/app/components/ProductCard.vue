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
      />

      <!-- Gradient overlay on hover -->
      <div
        class="absolute inset-0 bg-gradient-to-t from-black/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300"
      />

      <!-- Badge for discount/new items -->
      <div v-if="product.badge" class="absolute top-3 right-3 z-10">
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

      <!-- Price Section -->
      <div
        class="flex items-center justify-between pt-2 border-t border-gray-100 dark:border-gray-800"
      >
        <div class="flex items-baseline gap-2">
          <!-- قیمت جدید -->
          <p class="text-xl font-bold text-primary">
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

      <!-- Discount label -->
      <div v-if="oldPrice" class="flex items-center gap-1 text-xs text-success">
        <UIcon name="i-lucide-trending-down" class="w-3 h-3" />
        <span class="font-medium"> {{ discountPercent }}٪ تخفیف </span>
      </div>
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
