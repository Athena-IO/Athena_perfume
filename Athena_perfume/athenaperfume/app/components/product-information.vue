<template>
  <UCard>
    <div class="space-y-4">
      <!-- Title -->
      <div>
        <h1 class="text-xl sm:text-2xl font-bold text-gray-900 dark:text-white">
          {{ product.name }}
        </h1>
      </div>

      <UDivider />

      <!-- Rating -->
      <div class="flex items-center justify-between text-sm">
        <div class="flex items-center gap-2">
          <span class="text-yellow-500">⭐⭐⭐⭐⭐</span>
          <span class="font-bold text-gray-700 dark:text-gray-300">{{ rating }}</span>
          <span class="text-gray-500">({{ reviewCount }} نظر)</span>
        </div>
      </div>

      <UDivider />

      <!-- Gender -->
      <div
        v-if="product.information?.gender"
        class="flex items-center justify-between text-sm"
      >
        <p class="text-gray-600 dark:text-gray-400">
          {{ product.information.gender }}
        </p>
        <div class="flex items-center gap-2">
          <span class="i-lucide-user text-primary"></span>
          <p class="font-medium">جنسیت</p>
        </div>
      </div>

      <UDivider v-if="product.information?.gender" />

      <!-- Brand -->
      <div
        v-if="product.information?.brand"
        class="flex items-center justify-between text-sm"
      >
        <p class="text-gray-600 dark:text-gray-400">
          {{ product.information.brand }}
        </p>
        <div class="flex items-center gap-2">
          <span class="i-lucide-tag text-primary"></span>
          <p class="font-medium">برند</p>
        </div>
      </div>

      <UDivider v-if="product.information?.brand" />

      <!-- Type -->
      <div
        v-if="product.information?.type"
        class="flex items-center justify-between text-sm"
      >
        <p class="text-gray-600 dark:text-gray-400">
          {{ product.information.type }}
        </p>
        <div class="flex items-center gap-2">
          <span class="i-lucide-droplet text-primary"></span>
          <p class="font-medium">نوع</p>
        </div>
      </div>

      <UDivider v-if="product.information?.type" />

      <!-- Season -->
      <div
        v-if="product.information?.season"
        class="flex items-center justify-between text-sm"
      >
        <p class="text-gray-600 dark:text-gray-400">
          {{ product.information.season }}
        </p>
        <div class="flex items-center gap-2">
          <span class="i-lucide-calendar text-primary"></span>
          <p class="font-medium">فصل</p>
        </div>
      </div>

      <UDivider v-if="product.information?.season" />

      <!-- Volume -->
      <div
        v-if="product.information?.volume"
        class="flex items-center justify-between text-sm"
      >
        <p class="text-gray-600 dark:text-gray-400">
          {{ product.information.volume }}
        </p>
        <div class="flex items-center gap-2">
          <span class="i-lucide-flask-conical text-primary"></span>
          <p class="font-medium">حجم</p>
        </div>
      </div>

      <UDivider v-if="product.information?.volume" />

      <!-- Similar -->
      <div
        v-if="product.information?.similar"
        class="flex items-center justify-between text-sm"
      >
        <p class="text-gray-600 dark:text-gray-400">
          {{ product.information.similar }}
        </p>
        <div class="flex items-center gap-2">
          <span class="i-lucide-sparkles text-primary"></span>
          <p class="font-medium">مشابه</p>
        </div>
      </div>

      <UDivider v-if="product.information?.similar" />

      <!-- Shipping Info -->
      <div class="flex items-center justify-between text-sm">
        <div>
          <p class="text-gray-500 text-xs">
            {{ shippingText }}
          </p>
        </div>
        <div class="flex items-center gap-2">
          <span class="i-lucide-truck text-primary"></span>
          <p class="font-medium">ارسال رایگان</p>
        </div>
      </div>

      <UDivider />

      <!-- Warranty -->
      <div class="flex items-center justify-between text-sm">
        <div>
          <p class="text-gray-500 text-xs">{{ warrantyText }}</p>
        </div>
        <div class="flex items-center gap-2">
          <span class="i-lucide-shield-check text-primary"></span>
          <p class="font-medium">گارانتی اصالت کالا</p>
        </div>
      </div>
    </div>
  </UCard>
</template>

<script setup lang="ts">
interface ProductInfo {
  name: string;
  information?: {
    gender?: string;
    brand?: string;
    type?: string;
    season?: string;
    volume?: string;
    similar?: string;
  };
}

interface Props {
  product: ProductInfo;
  rating?: number | string;
  reviewCount?: number | string;
  shippingText?: string;
  warrantyText?: string;
}

const props = withDefaults(defineProps<Props>(), {
  rating: '4.5',
  reviewCount: '۱۲۴',
  shippingText: 'برای سفارش‌های بالای ۵۰۰,۰۰۰ تومان',
  warrantyText: '۷ روز ضمانت بازگشت'
});
</script>
