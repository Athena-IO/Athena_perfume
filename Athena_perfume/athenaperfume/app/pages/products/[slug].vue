<template>
  <UContainer class="py-6 sm:py-10">
    <div v-if="product" class="max-w-7xl mx-auto">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <!-- RIGHT: Product Gallery -->
        <div class="lg:col-span-5 order-1 lg:order-3">
          <ProductGallery :images="productImages" />
        </div>

        <!-- MIDDLE: Product Information -->
        <div class="lg:col-span-4 order-2 lg:order-2 space-y-4">
          <ProductInformation :product="product" />
        </div>

        <!-- LEFT: Pricing & Cart Actions -->
        <div class="lg:col-span-3 order-3 lg:order-1">
          <UCard :ui="{ body: { padding: 'p-6 sm:p-8' } }">
            <div class="space-y-6">
              <!-- Stock & Brand Header -->
              <div class="flex items-center justify-between gap-2">
                <!-- اگر ظرفیت موقت > 0 -->
                <UBadge
                  v-if="currentCapacity > 0"
                  color="success"
                  variant="soft"
                  size="lg"
                >
                  <span class="flex items-center gap-1">
                    <span class="i-lucide-check-circle"></span>
                    موجود در انبار✔
                  </span>
                </UBadge>

                <!-- اگر ظرفیت موقت = 0 -->
                <UBadge
                  v-else
                  color="error"
                  variant="soft"
                  size="lg"
                >
                  موجودی این محصول به پایان رسیده است
                </UBadge>

                <UButton
                  color="gray"
                  variant="outline"
                  size="sm"
                  square
                  class="px-4"
                  @click="navigateToBrand"
                >
                  {{ product.brand || "برند" }}
                </UButton>
              </div>

              <!-- اگر ظرفیت موقت کمتر از 100 بود -->
              <div v-if="currentCapacity > 0 && currentCapacity < 100">
                <UBadge
                  color="warning"
                  variant="soft"
                  size="sm"
                  class="w-full justify-center"
                >
                  تعداد محدود: فقط {{ currentCapacity }} عدد موجود است
                </UBadge>
              </div>

              <UDivider />

              <!-- Price Section -->
              <div class="text-center space-y-3">
                <p class="text-3xl font-bold text-primary">
                  {{ formatPrice(finalPrice) }} تومان
                </p>

                <p
                  v-if="hasDiscount"
                  class="text-gray-400 line-through text-base"
                >
                  {{ formatPrice(originalPriceTotal) }} تومان
                </p>

                <UBadge
                  v-if="hasDiscount"
                  color="error"
                  variant="solid"
                  size="lg"
                >
                  {{ product.discountPercent }}٪ تخفیف
                </UBadge>
              </div>

              <UDivider />

              <!-- Volume Selection -->
              <div>
                <p class="text-base font-semibold mb-3 text-center">
                  انتخاب حجم:
                </p>
                <URadioGroup
                  v-model="selectedVolume"
                  :items="volumeOptions"
                  orientation="vertical"
                  color="primary"
                  variant="card"
                  size="sm"
                  :ui="{
                    fieldset: 'w-full',
                    container: 'flex flex-col gap-3',
                    item: 'w-full',
                    base: 'justify-center',
                    label: 'w-full text-center text-sm',
                  }"
                />
              </div>

              <UDivider />

              <!-- Add to Cart Button (Left) & Quantity (Right) -->
              <div class="flex items-end gap-3">
                <!-- Add to Cart Button (Left) -->
                <UButton
                  class="flex-1 py-1.5 px-2.5 text-xs"
                  color="primary"
                  icon="i-lucide-shopping-cart"
                  :disabled="currentCapacity === 0 || qty === 0"
                  @click="addToCart"
                >
                  افزودن به سبد خرید
                </UButton>

                <!-- Quantity (Right) -->
                <div class="flex-shrink-0 w-20">
                  <p class="text-xs font-semibold mb-1 text-center">تعداد:</p>
                  <UInputNumber
                    v-model="qty"
                    :min="currentCapacity === 0 ? 0 : 1"
                    :max="currentCapacity"
                    :step="5"
                    size="sm"
                    :disabled="currentCapacity === 0"
                    :ui="{
                      wrapper:
                        'border border-gray-300 dark:border-gray-700 rounded-lg flex items-center justify-between',
                      base: 'text-center font-semibold text-xs',
                      increment: 'rounded-none rounded-s-lg',
                      decrement: 'rounded-none rounded-e-lg',
                    }"
                  />
                </div>
              </div>

              <UDivider />

              <!-- Additional Actions -->
              <div class="space-y-3">
                <UButton block color="gray" variant="outline" size="md">
                  ارسال رایگان
                </UButton>
                <UButton block color="gray" variant="outline" size="md">
                  ضمانت اصالت
                </UButton>
                <UButton
                  block
                  color="gray"
                  variant="outline"
                  size="md"
                  icon="i-lucide-credit-card"
                >
                  خرید اقساطی
                </UButton>
              </div>
            </div>
          </UCard>
        </div>
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

// ثابتِ حجم‌ها
const volumeOptions = [
  { label: "۵ میل", value: 5 },
  { label: "۱۵ میل", value: 15 },
  { label: "۲۵ میل", value: 25 },
  { label: "۱۰۰ میل", value: 100 },
];

const selectedVolume = ref(5);
const qty = ref(1);

// محصولات (مثال)
const slug = route.params.slug;
const products = [
  {
    id: 4,
    slug: "dior-sauvage-4",
    name: "دیور ساواج",
    originalPrice: 2500000,
    discountPercent: 10,
    capacity: 250, // ظرفیت
    image:
      "https://liliome.com/wp-content/uploads/2016/04/Dior-Sauvage-1.jpg?v=1680545729",
    information: {
      gender: "مردانه",
      brand: "Dior",
      similar: "Bleu de Chanel",
      type: "Eau de Toilette",
      season: "چهار فصل (بهترین برای تابستان)",
      volume: "100ml / 200ml",
    },
  },
  {
    id: 5,
    slug: "chanel-bleu-5",
    name: "شنل بلو د شنل",
    originalPrice: 3200000,
    discountPercent: 15,
    capacity: 80,
    image: "https://liliome.ir/wp-content/uploads/2015/12/6-1.jpg",
    information: {
      gender: "مردانه",
      brand: "Chanel",
      similar: "Dior Sauvage",
      type: "Eau de Parfum",
      season: "چهار فصل",
      volume: "100ml / 150ml",
    },
  },
  {
    id: 6,
    slug: "lancome-la-vie-6",
    name: "لانکوم لا ویه است بله",
    originalPrice: 1980000,
    discountPercent: 8,
    capacity: 0, // ناموجود
    image:
      "https://hamedsps.ir/wp-content/uploads/2023/04/%D9%84%D9%88%DB%8C%D9%87-%D8%A8%D9%84.jpg",
    information: {
      gender: "زنانه",
      brand: "Lancôme",
      similar: "Armani Si",
      type: "Eau de Parfum",
      season: "پاییز و زمستان",
      volume: "75ml / 100ml",
    },
  },
  {
    id: 7,
    slug: "versace-eros-7",
    name: "ورساچه اروس",
    originalPrice: 2600000,
    discountPercent: 12,
    capacity: 150,
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYNzQWBYJkEtxw5kCcSyHGKnEVOugmqPf2qg&s",
    information: {
      gender: "مردانه",
      brand: "Versace",
      similar: "Invictus by Paco Rabanne",
      type: "Eau de Toilette",
      season: "زمستان / پاییز",
      volume: "100ml / 200ml",
    },
  },
  {
    id: 8,
    slug: "ysl-libre-8",
    name: "ایو سن لورن لیبره",
    originalPrice: 3000000,
    discountPercent: 5,
    capacity: 60,
    image:
      "https://liliome.com/wp-content/uploads/2019/08/Yves-Saint-Laurent-Libre-1.jpg",
    information: {
      gender: "زنانه",
      brand: "YSL",
      similar: "Mon Paris",
      type: "Eau de Parfum",
      season: "چهار فصل",
      volume: "90ml",
    },
  },
  {
    id: 9,
    slug: "creed-aventus-9",
    name: "کرید اونتوس",
    originalPrice: 2850000,
    discountPercent: 18,
    capacity: 300,
    image: "https://liliome.ir/wp-content/uploads/2016/12/3-76.jpg",

    information: {
      gender: "مردانه",
      brand: "Creed",
      similar: "Mont Blanc Explorer",
      type: "Eau de Parfum",
      season: "چهار فصل (بهترین برای بهار)",
      volume: "100ml / 120ml",
    },
  },
  {
    id: 10,
    slug: "burberry-her-10",
    name: "بربری هر",
    originalPrice: 1750000,
    discountPercent: 7,
    capacity: 40,
    image:
      "https://www.roha-shop.com/wp-content/uploads/2022/08/%D8%A8%D8%A7%D8%B1%D8%A8%D8%B1%DB%8C-%D9%87%D8%B1-01.jpg",
    information: {
      gender: "زنانه",
      brand: "Burberry",
      similar: "Ariana Grande Cloud",
      type: "Eau de Parfum",
      season: "بهار و تابستان",
      volume: "100ml",
    },
  },
  {
    id: 11,
    slug: "tomford-black-orchid-11",
    name: "تام فورد بلک اورکید",
    originalPrice: 2300000,
    discountPercent: 9,
    capacity: 90,
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTE-LsGMChiT5p8uw2tsRiBoO29qJotnXihyg&s",
    information: {
      gender: "یونیسکس",
      brand: "Tom Ford",
      similar: "Narciso Rodriguez For Her",
      type: "Eau de Parfum",
      season: "پاییز و زمستان",
      volume: "100ml / 150ml",
    },
  },
];

const product = products.find((p) => p.slug === slug);

// 🔹 ظرفیت موقت که UI از آن استفاده می‌کند
const currentCapacity = ref(0);

// ✅ تابع همگام‌سازی ظرفیت و qty با سبد خرید
function syncFromCart() {
  if (!product) {
    currentCapacity.value = 0;
    qty.value = 0;
    return;
  }

  const existing = cart.items.find((i) => i.productId === product.id);

  const baseCapacity = product.capacity ?? 0;
  const alreadyInCart = existing?.qty ?? 0;

  // ظرفیت باقی‌مانده بعد از موارد موجود در سبد
  currentCapacity.value = Math.max(baseCapacity - alreadyInCart, 0);

  if (currentCapacity.value === 0) {
    qty.value = 0;
  } else {
    // اگر قبلاً در سبد بود، همان مقدار (تا حد ظرفیت)
    const desired = alreadyInCart > 0 ? alreadyInCart : qty.value || 1;
    qty.value = Math.min(desired, currentCapacity.value);
  }
}

// 🔸 اولین بار، هنگام لود صفحه
syncFromCart();

// وقتی حجم عوض شد:
// 1) qty را با همان مقدار تنظیم کن
// 2) اگر از ظرفیت بیشتر بود، به ظرفیت محدود کن
watch(
  selectedVolume,
  (v) => {
    if (currentCapacity.value === 0) {
      qty.value = 0;
      return;
    }
    qty.value = Math.min(v, currentCapacity.value);
  },
  { immediate: true }
);

// اگر کاربر qty را دستی بالا ببرد، بیشتر از currentCapacity نشود
watch(
  qty,
  (v) => {
    if (currentCapacity.value === 0) {
      qty.value = 0;
      return;
    }
    if (v > currentCapacity.value) qty.value = currentCapacity.value;
    if (v < 1) qty.value = 1;
  }
);

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
  if (!product || currentCapacity.value === 0) return;

  // اگر 18 است و 21 ظرفیت مانده، اینجا می‌شود 21
  const safeQty = Math.min(qty.value, currentCapacity.value);

  // qty را به مقدار امن تنظیم کن (مثلاً 21)
  qty.value = safeQty;

  cart.addToCart(
    {
      ...product,
      finalPrice: discountedSingle.value,
      originalPrice: product.originalPrice,
      selectedVolume: selectedVolume.value,
    },
    safeQty
  );

  // بعد از افزودن به سبد، از ظرفیت موقت کم می‌کنیم
  currentCapacity.value = Math.max(currentCapacity.value - safeQty, 0);
  if (currentCapacity.value === 0) qty.value = 0;
}

// 🔁 هر تغییری در سبد را گوش بده و دوباره ظرفیت را آپدیت کن
watch(
  () => cart.items,
  () => {
    syncFromCart();
  },
  { deep: true }
);
</script>