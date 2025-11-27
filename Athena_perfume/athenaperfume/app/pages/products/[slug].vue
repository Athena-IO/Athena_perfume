<template>
  <UContainer class="py-6 sm:py-10">
    <!-- Product Exists -->
    <div v-if="product" class="max-w-4xl mx-auto space-y-8">

      <!-- Main Carousel Slider -->
      <UCarousel
        v-slot="{ item }"
        ref="carousel"
        :items="productImages"
        arrows
        dots
        class="w-full rounded-xl overflow-hidden"
        @select="onSelectImage"
      >
        <img
          :src="item"
          :alt="product.name"
          class="w-full h-80 object-cover rounded-lg"
        />
      </UCarousel>

      <!-- Thumbnail Images -->
      <div class="flex gap-3 justify-center">
        <div
          v-for="(image, index) in productImages"
          :key="index"
          class="cursor-pointer transition-all duration-200"
          :class="[
            activeImageIndex === index 
              ? 'ring-2 ring-primary opacity-100' 
              : 'opacity-50 hover:opacity-75'
          ]"
          @click="selectImage(index)"
        >
          <UCard class="rounded-lg overflow-hidden">
            <img
              :src="image"
              class="w-20 h-20 object-cover"
              :alt="`${product.name} - تصویر ${index + 1}`"
            />
          </UCard>
        </div>
      </div>

        <!-- Product Information -->
        <div class="space-y-6">

<!-- Title -->
<div class="text-center">
  <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
    {{ product.name }} مدل فلان
  </h1>
</div>

<!-- Price and Discount -->
<div class="flex items-center justify-center gap-4">
  <p class="text-2xl font-bold text-primary">
    {{ product.price }}
  </p>
  <p class="text-gray-400 line-through text-base">
    ۲,۷۰۰,۰۰۰ تومان
  </p>
  <UBadge color="error" variant="solid" size="md">
    ۷٪ تخفیف
  </UBadge>
</div>


          <!-- Rating and Stock -->
<div class="flex flex-col items-center gap-2 text-sm mt-4">
  <div class="flex items-center gap-2">
    <span class="text-yellow-500">⭐⭐⭐⭐⭐</span>
    <span class="font-bold text-gray-700 dark:text-gray-300">4.5</span>
    <span class="text-gray-500">(۱۲۴ نظر)</span>
  </div>

  <UBadge color="success" variant="soft">
    ✔ موجود در انبار
  </UBadge>
</div>


        <UDivider />

        <!-- Volume/Size Selection with RadioGroup (Smaller) -->
<div class="w-full text-center">
  <p class="text-sm font-semibold mb-3 text-gray-900 dark:text-white">
    انتخاب حجم موردنظر:
  </p>

  <URadioGroup
    v-model="selectedVolume"
    :items="volumeOptions"
    orientation="horizontal"
    color="primary"
    variant="card"
    size="xs"
    :ui="{ 
      fieldset: 'w-full flex justify-center',
      container: 'flex justify-center gap-3',
      item: 'w-24',                /* عرض ثابت برای یکدست شدن */
      base: 'justify-center',
      wrapper: 'w-full flex justify-center',
      label: 'w-full text-center text-xs'
    }"
  />
</div>


        <UDivider />
<!-- Quantity + Add to Cart -->
<!-- Quantity + Add to Cart -->
<div class="flex flex-col sm:flex-row items-center gap-2 sm:gap-3 justify-center">

  <!-- Quantity (Right in RTL) -->
  <UInputNumber
    v-model="qty"
    :min="1"
    :step="5"
    size="md"
    class="w-full sm:w-28 order-1 sm:order-1"
    :ui="{
      wrapper: 'border border-gray-300 dark:border-gray-700 rounded-lg flex items-center justify-between',
      base: 'text-center font-semibold',
      increment: 'rounded-none rounded-s-lg',
      decrement: 'rounded-none rounded-e-lg'
    }"
  />

  <!-- Add to Cart Button (Center) -->
  <UButton
    class="flex-1 sm:flex-none sm:w-40 order-2 text-center"
    color="primary"
    size="md"
    icon="i-lucide-shopping-cart"
    @click="addToCart"
  >
    افزودن به سبد خرید
  </UButton>

</div>


<!-- ۳ دکمه اطلاعات — همه پس‌زمینه‌دار، بدون سفید -->
<div class="grid grid-cols-2 gap-3 mt-4 w-full">
  <!-- ارسال رایگان — زرشکی روشن + هاور تیره‌تر -->
  <NuxtLink to="/shipping-info">
    <UButton
      block
      size="md"
      class="w-full justify-center text-sm font-semibold text-red-700 bg-red-50 hover:bg-red-100 dark:bg-red-950/40 dark:text-red-300 dark:hover:bg-red-900/60 transition-all duration-200"
    >
      ارسال رایگان
    </UButton>
  </NuxtLink>

  <!-- ضمانت اصالت — زرشکی روشن + هاور تیره‌تر -->
  <NuxtLink to="/warranty">
    <UButton
      block
      size="md"
      class="w-full justify-center text-sm font-semibold text-red-700 bg-red-50 hover:bg-red-100 dark:bg-red-950/40 dark:text-red-300 dark:hover:bg-red-900/60 transition-all duration-200"
    >
      ضمانت اصالت
    </UButton>
  </NuxtLink>
</div>

<!-- خرید اقساطی — سبز لوکس + هاور تیره‌تر -->
<NuxtLink to="/installment" class="block mt-3">
  <UButton
    block
    size="md"
    icon="i-lucide-credit-card"
    class="w-full justify-center text-sm font-bold text-green-700 bg-green-50 hover:bg-green-100 dark:bg-green-950/40 dark:text-green-300 dark:hover:bg-green-900/60 transition-all duration-200"
  >
    خرید اقساطی
  </UButton>
</NuxtLink>



        <!-- Additional Product Info -->
<UCard>
  <div class="flex items-center justify-center gap-8">
    <!-- First Section -->
    <div class="flex items-center gap-2">
      <span class="i-lucide-truck text-primary text-xl"></span>
      <div>
        <p class="font-medium">ارسال رایگان</p>
        <p class="text-gray-500 text-xs">برای سفارش‌های بالای ۵۰۰,۰۰۰ تومان</p>
      </div>
    </div>

    <!-- Vertical Divider -->
    <div class="h-12 w-px bg-gray-200"></div>

    <!-- Second Section -->
    <div class="flex items-center gap-2">
      <span class="i-lucide-shield-check text-primary text-xl"></span>
      <div>
        <p class="font-medium">گارانتی اصالت کالا</p>
        <p class="text-gray-500 text-xs">۷ روز ضمانت بازگشت وجه</p>
      </div>
    </div>
  </div>
</UCard>


 <UTabs :items="tabs" class="w-full mt-4">
    <template #description>
      <div class="p-4">
        <p>این یک توضیحات محصول است. می‌توانید اطلاعات دقیق درباره محصول را اینجا قرار دهید.</p>
      </div>
    </template>

    <template #specifications>
      <div class="p-4">
        <ul class="space-y-2">
          <li>مشخصه ۱: مقدار</li>
          <li>مشخصه ۲: مقدار</li>
          <li>مشخصه ۳: مقدار</li>
        </ul>
      </div>
    </template>

    <template #reviews>
      <div class="p-4">
        <p>نظرات کاربران درباره این محصول</p>
      </div>
    </template>
  </UTabs>

      </div>
    </div>

    <!-- Product Not Found -->
    <UCard v-else variant="outline">
      <div class="text-center py-12">
        <span class="i-lucide-package-x text-6xl text-gray-400 mb-4 block"></span>
        <p class="text-lg text-gray-600">محصول پیدا نشد</p>
      </div>
    </UCard>

  </UContainer>
</template>

<script setup>
import { ref, watch, computed } from "vue";
import { useRoute } from "vue-router";
import { useCartStore } from "~/composables/stores/cart";

const route = useRoute();
const cart = useCartStore();
const carousel = ref(null);

// Volume options with quantity values
const volumeOptions = [
  { label: '۳ میل', value: 3 },
  { label: '۶ میل', value: 6 },
  { label: '۱۲ میل', value: 12 },
  { label: '۱۰۰ میل', value: 100 }
];
const tabs = [
  {
    label: 'توضیحات',
    icon: 'i-lucide-file-text',
    slot: 'description'
  },
  {
    label: 'مشخصات',
    icon: 'i-lucide-list',
    slot: 'specifications'
  },
  {
    label: 'نظرات',
    icon: 'i-lucide-message-square',
    slot: 'reviews'
  }
]
// Selected volume (defaults to first option)
const selectedVolume = ref(3);

// Quantity - automatically updates when volume changes
const qty = ref(3);

// Watch for volume changes and update quantity
watch(selectedVolume, (newVolume) => {
  qty.value = newVolume;
});

// Active image index for carousel
const activeImageIndex = ref(0);

// Product data
const slug = route.params.slug;

const products = [
  { 
    id: 1, 
    slug: "nike-air-max-1", 
    name: "کفش ورزشی نایک ایر مکس", 
    price: "۲,۵۰۰,۰۰۰ تومان", 
    image: "https://picsum.photos/400/400?random=1" 
  },
  { 
    id: 2, 
    slug: "nike-air-max-2", 
    name: "کفش ورزشی نایک ایر مکس", 
    price: "۲,۵۰۰,۰۰۰ تومان", 
    image: "https://picsum.photos/400/400?random=2" 
  },
  { 
    id: 3, 
    slug: "nike-air-max-3", 
    name: "کفش ورزشی نایک ایر مکس", 
    price: "۲,۵۰۰,۰۰۰ تومان", 
    image: "https://picsum.photos/400/400?random=3" 
  },
  { 
    id: 4, 
    slug: "nike-air-max-4", 
    name: "کفش ورزشی نایک ایر مکس", 
    price: "۲,۵۰۰,۰۰۰ تومان", 
    image: "https://picsum.photos/400/400?random=4" 
  },
  { 
    id: 5, 
    slug: "nike-air-max-5", 
    name: "کفش ورزشی نایک ایر مکس", 
    price: "۲,۵۰۰,۰۰۰ تومان", 
    image: "https://picsum.photos/400/400?random=5" 
  },
];

const product = products.find((p) => p.slug === slug);

// Product images for carousel (main image + additional images)
const productImages = computed(() => {
  if (!product) return [];
  return [
    product.image,
    `https://picsum.photos/640/640?random=${product.id}-2`,
    `https://picsum.photos/640/640?random=${product.id}-3`,
    `https://picsum.photos/640/640?random=${product.id}-4`,
  ];
});

// Carousel handlers
function onSelectImage(index) {
  activeImageIndex.value = index;
}

function selectImage(index) {
  activeImageIndex.value = index;
  carousel.value?.emblaApi?.scrollTo(index);
}

// Add to cart with selected volume info
function addToCart() {
  cart.addToCart({
    ...product,
    selectedVolume: selectedVolume.value,
    volumeLabel: volumeOptions.find(v => v.value === selectedVolume.value)?.label
  }, qty.value);
}
</script>
