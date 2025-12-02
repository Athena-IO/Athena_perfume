<template>
  <UContainer class="py-6 sm:py-10">
    <div v-if="product" class="max-w-4xl mx-auto space-y-8">
      <ProductGallery :images="productImages" />

      <!-- Product Info -->
      <div class="space-y-6">
        <!-- Title -->
        <div class="text-center">
          <h1
            class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white"
          >
            {{ product.name }}
          </h1>
        </div>

        <!-- Price + Discount -->
        <div class="flex items-center justify-center gap-4">
          <!-- Final price -->
          <p class="text-2xl font-bold text-primary">
            {{ formatPrice(finalPrice) }} تومان
          </p>

          <!-- Original × qty -->
          <p v-if="hasDiscount" class="text-gray-400 line-through text-base">
            {{ formatPrice(originalPriceTotal) }} تومان
          </p>

          <!-- Discount badge -->
          <UBadge v-if="hasDiscount" color="error" variant="solid" size="md">
            {{ product.discountPercent }}٪ تخفیف
          </UBadge>
        </div>

        <!-- Rating + Stock -->
        <div class="flex flex-col items-center gap-2 text-sm mt-4">
          <div class="flex items-center gap-2">
            <span class="text-yellow-500">⭐⭐⭐⭐⭐</span>
            <span class="font-bold text-gray-700 dark:text-gray-300">4.5</span>
            <span class="text-gray-500">(۱۲۴ نظر)</span>
          </div>
          <UBadge color="success" variant="soft">✔ موجود در انبار</UBadge>
        </div>

        <UDivider />

        <!-- Volume Selection -->
        <div class="w-full text-center">
          <p class="text-sm font-semibold mb-3">انتخاب حجم:</p>

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
              item: 'w-24',
              base: 'justify-center',
              label: 'w-full text-center text-xs',
            }"
          />
        </div>

        <UDivider />

        <!-- Qty + Add to Cart -->
        <div
          class="flex flex-col sm:flex-row items-center gap-2 sm:gap-3 justify-center"
        >
          <!-- Qty (goes right side in RTL) -->
          <UInputNumber
            v-model="qty"
            :min="1"
            :step="5"
            size="md"
            class="w-full sm:w-28 order-1 sm:order-1"
            :ui="{
              wrapper:
                'border border-gray-300 dark:border-gray-700 rounded-lg flex items-center justify-between',
              base: 'text-center font-semibold',
              increment: 'rounded-none rounded-s-lg',
              decrement: 'rounded-none rounded-e-lg',
            }"
          />

          <!-- Add to Cart -->
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

        <!-- Additional Buttons -->
        <div class="grid grid-cols-2 gap-3 mt-3 w-full">
          <UButton block color="gray" variant="outline">ارسال رایگان</UButton>
          <UButton block color="gray" variant="outline">ضمانت اصالت</UButton>
        </div>

        <UButton
          block
          color="gray"
          size="md"
          variant="outline"
          icon="i-lucide-credit-card"
          class="mt-3"
        >
          خرید اقساطی
        </UButton>

        <!-- Extra Info -->
        <UCard>
          <div class="space-y-3 text-sm">
            <div class="flex items-start gap-2">
              <span class="i-lucide-truck text-primary"></span>
              <div>
                <p class="font-medium">ارسال رایگان</p>
                <p class="text-gray-500 text-xs">
                  برای سفارش‌های بالای ۵۰۰,۰۰۰ تومان
                </p>
              </div>
            </div>
            <UDivider />
            <div class="flex items-start gap-2">
              <span class="i-lucide-shield-check text-primary"></span>
              <div>
                <p class="font-medium">گارانتی اصالت کالا</p>
                <p class="text-gray-500 text-xs">۷ روز ضمانت بازگشت</p>
              </div>
            </div>
          </div>
        </UCard>
      </div>
    </div>

    <!-- Product Not Found -->
    <UCard v-else variant="outline">
      <div class="text-center py-12">
        <span
          class="i-lucide-package-x text-6xl text-gray-400 mb-4 block"
        ></span>
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

// حجم‌ها
const volumeOptions = [
  { label: "۳ میل", value: 3 },
  { label: "۶ میل", value: 6 },
  { label: "۱۲ میل", value: 12 },
  { label: "۱۰۰ میل", value: 100 },
];

const selectedVolume = ref(3);
const qty = ref(3);

// وقتی حجم عوض شد qty = حجم
watch(selectedVolume, (v) => {
  qty.value = v;
});

// محصولات (مثال)
const slug = route.params.slug;
const products = [
  {
    id: 4,
    slug: "dior-sauvage-4",
    name: "دیور ساواج",
    originalPrice: 2500000,
    discountPercent: 10,
    image:
      "https://liliome.com/wp-content/uploads/2016/04/Dior-Sauvage-1.jpg?v=1680545729",
  },
  {
    id: 5,
    slug: "chanel-bleu-5",
    name: "شنل بلو د شنل",
    originalPrice: 3200000,
    discountPercent: 15,
    image: "https://liliome.ir/wp-content/uploads/2015/12/6-1.jpg",
  },
  {
    id: 6,
    slug: "lancome-la-vie-6",
    name: "لانکوم لا ویه است بله",
    originalPrice: 1980000,
    discountPercent: 8,
    image:
      "https://hamedsps.ir/wp-content/uploads/2023/04/%D9%84%D9%88%DB%8C%D9%87-%D8%A8%D9%84.jpg",
  },
  {
    id: 7,
    slug: "versace-eros-7",
    name: "ورساچه اروس",
    originalPrice: 2600000,
    discountPercent: 12,
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYNzQWBYJkEtxw5kCcSyHGKnEVOugmqPf2qg&s",
  },
  {
    id: 8,
    slug: "ysl-libre-8",
    name: "ایو سن لورن لیبره",
    originalPrice: 3000000,
    discountPercent: 5,
    image:
      "https://liliome.com/wp-content/uploads/2019/08/Yves-Saint-Laurent-Libre-1.jpg",
  },
  {
    id: 9,
    slug: "creed-aventus-9",
    name: "کرید اونتوس",
    originalPrice: 2850000,
    discountPercent: 18,
    image: "https://liliome.ir/wp-content/uploads/2016/12/3-76.jpg",
  },
  {
    id: 10,
    slug: "burberry-her-10",
    name: "بربری هر",
    originalPrice: 1750000,
    discountPercent: 7,
    image:
      "https://www.roha-shop.com/wp-content/uploads/2022/08/%D8%A8%D8%A7%D8%B1%D8%A8%D8%B1%DB%8C-%D9%87%D8%B1-01.jpg",
  },
  {
    id: 11,
    slug: "tomford-black-orchid-11",
    name: "تام فورد بلک اورکید",
    originalPrice: 2300000,
    discountPercent: 9,
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTE-LsGMChiT5p8uw2tsRiBoO29qJotnXihyg&s",
  },
];

const product = products.find((p) => p.slug === slug);

// ⭐ قیمت بعد از تخفیف (یک عدد)
const discountedSingle = computed(() => {
  if (!product) return 0;
  return (
    product.originalPrice -
    (product.originalPrice * product.discountPercent) / 100
  );
});

// ⭐ قیمت قبل از تخفیف × qty
const originalPriceTotal = computed(() => {
  return product ? product.originalPrice * qty.value : 0;
});

// ⭐ قیمت بعد تخفیف × qty
const finalPrice = computed(() => {
  return discountedSingle.value * qty.value;
});

// آیا تخفیف دارد؟
const hasDiscount = computed(() => product?.discountPercent > 0);

// فرمت قیمت
const formatPrice = (price) => new Intl.NumberFormat("fa-IR").format(price);

// تصاویر اسلایدر
const productImages = computed(() => {
  if (!product) return [];
  return [
    product.image,
    `https://picsum.photos/640/640?random=${product.id}-2`,
    `https://picsum.photos/640/640?random=${product.id}-3`,
    `https://picsum.photos/640/640?random=${product.id}-4`,
  ];
});

// سبد خرید
function addToCart() {
  cart.addToCart(
    {
      ...product,
      finalPrice: discountedSingle.value, // ⭐ قیمت تک بعد تخفیف
      originalPrice: product.originalPrice, // ⭐ قیمت قبل تخفیف
      selectedVolume: selectedVolume.value,
      volumeLabel: volumeOptions.find((v) => v.value === selectedVolume.value)
        ?.label,
    },
    qty.value
  );
}
</script>
