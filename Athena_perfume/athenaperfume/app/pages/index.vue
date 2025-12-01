<template>
  <div class="w-full px-4 sm:px-6 lg:px-8">
    <div class="px-6 py-8">
      <BannerCarousel
        :banners="banners"
        height="medium"
        :autoplay="true"
        :autoplay-delay="7000"
      />
    </div>
    <div
      class="grid lg:grid-cols-2 grid-cols-1 items-center min-h-[70vh] gap-8"
    >
      <!-- بخش عکس با افکت مشابه اول -->
      <div class="pl-0 lg:pl-25 order-2 lg:order-1">
        <div class="relative group">
          <div
            class="absolute inset-0 bg-primary/15 rounded-3xl blur-3xl group-hover:blur-xl transition-all duration-700 -z-10"
          ></div>

          <img
            src="https://cdn.mos.cms.futurecdn.net/VzUqgr8pfbNcfXrpzeVBPE.jpg"
            alt="عطر لوکس"
            class="w-full h-auto rounded-lg shadow-lg object-cover group-hover:scale-[1.02] transition-transform duration-800"
            loading="lazy"
          />
        </div>
      </div>

      <!-- بخش متن -->
      <div class="flex flex-col gap-8 text-right order-1 lg:order-2" dir="rtl">
        <div class="pr-0 lg:pr-14 xl:pr-20 space-y-7">
          <h2
            class="text-5xl lg:text-6xl font-black leading-tight text-highlighted"
          >
            کیفیت دیدتان را <span class="text-primary">تغییر دهید</span>
          </h2>

          <p class="text-2xl lg:text-3xl font-bold text-default">
            رایحه مخصوص به خودتان را کشف کنید!
          </p>

          <p class="text-xl lg:text-2xl font-semibold text-toned">
            بهترین کیفیت! مناسب‌ترین قیمت!
          </p>
        </div>

        <!-- دکمه‌ها -->
        <div class="flex flex-wrap gap-5 mt-6 pr-0 lg:pr-14">
          <UButton
            to="/products?gender=male"
            color="primary"
            variant="solid"
            size="xl"
            class="px-16 py-5 text-xl font-bold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300"
          >
            مردانه
          </UButton>

          <UButton
            to="/products?gender=female"
            color="primary"
            variant="outline"
            size="xl"
            class="px-16 py-5 text-xl font-bold rounded-xl border-2 transform hover:scale-105 transition-all duration-300"
          >
            زنانه
          </UButton>
        </div>

        <!-- متن تشویقی -->
        <p class="text-sm lg:text-base text-muted pr-0 lg:pr-14 mt-4">
          بیش از ۵۰۰ رایحه اورجینال • ضمانت اصالت • ارسال رایگان
        </p>
      </div>
    </div>
  </div>

  <!-- Gender Category Boxes -->
  <div class="w-full px-4 sm:px-6 lg:px-8 mt-16">
    <div
      class="grid lg:grid-cols-2 grid-cols-1 gap-6 items-center min-h-[30vh]"
    >
      <!-- Box 1 - مردانه -->
      <ULink to="/men-products" class="group block h-full" raw>
        <UCard
          class="relative overflow-hidden h-full transition-all duration-300 group-hover:shadow-xl border-default"
        >
          <div class="relative h-[300px] lg:h-[400px]">
            <!-- Image -->
            <img
              src="https://hips.hearstapps.com/hmg-prod/images/mhlcologne-opener-0086-66ba5fbb0c4cf.jpg"
              alt="مردانه"
              class="w-full h-full object-cover"
            />

            <!-- Dark overlay on hover -->
            <div
              class="absolute inset-0 bg-black/20 group-hover:bg-black/50 transition-all duration-300"
            />

            <!-- Text -->
            <div class="absolute inset-0 flex items-center justify-center">
              <p
                class="text-white text-3xl font-bold z-10 transform group-hover:scale-110 transition-transform duration-300 drop-shadow-lg"
              >
                مردانه
              </p>
            </div>
          </div>
        </UCard>
      </ULink>

      <!-- Box 2 - زنانه -->
      <ULink to="/women-products" class="group block h-full" raw>
        <UCard
          class="relative overflow-hidden h-full transition-all duration-300 group-hover:shadow-xl border-default"
        >
          <div class="relative h-[300px] lg:h-[400px]">
            <!-- Image -->
            <img
              src="https://hips.hearstapps.com/hmg-prod/images/mhlcologne-opener-0086-66ba5fbb0c4cf.jpg"
              alt="زنانه"
              class="w-full h-full object-cover"
            />

            <!-- Dark overlay on hover -->
            <div
              class="absolute inset-0 bg-black/20 group-hover:bg-black/50 transition-all duration-300"
            />

            <!-- Text -->
            <div class="absolute inset-0 flex items-center justify-center">
              <p
                class="text-white text-3xl font-bold z-10 transform group-hover:scale-110 transition-transform duration-300 drop-shadow-lg"
              >
                زنانه
              </p>
            </div>
          </div>
        </UCard>
      </ULink>
    </div>
  </div>

  <!-- Product Categories & Carousel -->
  <div class="overflow-hidden mt-16">
    <div class="flex items-center justify-between p-6">
      <!-- Show all button on the left -->
      <div>
        <UButton
          @click="selectedCategory = 'all'"
          variant="ghost"
          color="neutral"
          size="xl"
          class="text-2xl"
          :class="
            selectedCategory === 'all'
              ? 'border-b-2 border-primary rounded-none'
              : ''
          "
        >
          نمایش همه
        </UButton>
      </div>

      <!-- Category buttons on the right -->
      <div class="flex gap-4">
        <UButton
          @click="selectedCategory = 'female'"
          variant="ghost"
          color="neutral"
          size="xl"
          class="text-2xl"
          :class="
            selectedCategory === 'female'
              ? 'border-b-2 border-primary rounded-none'
              : ''
          "
        >
          زنانه
        </UButton>
        <UButton
          @click="selectedCategory = 'male'"
          variant="ghost"
          color="neutral"
          size="xl"
          class="text-2xl"
          :class="
            selectedCategory === 'male'
              ? 'border-b-2 border-primary rounded-none'
              : ''
          "
        >
          مردانه
        </UButton>
      </div>
    </div>

    <!-- Carousel for products -->
    <div class="w-full px-16 sm:px-20 pb-12 relative">
      <UCarousel
        v-if="filteredProducts.length > 0"
        v-slot="{ item }"
        :items="filteredProducts"
        :ui="{
          root: 'w-full relative',
          viewport: 'w-full overflow-hidden',
          container: 'flex gap-4',
          item: 'flex-shrink-0 basis-full sm:basis-1/2 md:basis-1/3 lg:basis-1/4',
          dots: 'mt-6',
          prev: 'absolute -left-12 top-1/2 -translate-y-1/2 z-10',
          next: 'absolute -right-12 top-1/2 -translate-y-1/2 z-10',
        }"
        :prev="{
          color: 'primary',
          variant: 'solid',
          size: 'lg',
          square: true,
        }"
        :next="{
          color: 'primary',
          variant: 'solid',
          size: 'lg',
          square: true,
        }"
        loop
        arrows
        dots
        :slides-to-scroll="1"
      >
        <ProductCard :product="item" />
      </UCarousel>
    </div>
  </div>

  <!-- Hero Section -->
  <section class="min-h-screen backdrop-blur-sm py-16 px-4">
    <div class="mx-auto max-w-7xl">
      <div
        class="grid lg:grid-cols-2 grid-cols-1 items-center gap-8 lg:gap-12 min-h-[75vh]"
      >
        <!-- عکس -->
        <div class="order-2 lg:order-1 -ml-4 lg:-ml-12 xl:-ml-20">
          <div class="relative group">
            <div
              class="absolute inset-0 bg-primary/15 rounded-3xl blur-3xl group-hover:blur-xl transition-all duration-700 -z-10"
            ></div>

            <img
              src="https://cdn.mos.cms.futurecdn.net/VzUqgr8pfbNcfXrpzeVBPE.jpg"
              alt="عطر لوکس"
              class="w-full lg:w-[108%] xl:w-[112%] h-auto rounded-3xl shadow-2xl object-cover group-hover:scale-[1.02] transition-transform duration-800"
              loading="lazy"
            />
          </div>
        </div>

        <!-- متن -->
        <div
          class="order-1 lg:order-2 flex flex-col gap-8 text-right pr-4 lg:pr-0"
          dir="rtl"
        >
          <div class="space-y-6 lg:pr-20">
            <h2
              class="text-5xl lg:text-6xl font-black leading-tight text-highlighted"
            >
              کیفیت دیدتان را <span class="text-primary">تغییر دهید</span>
            </h2>

            <p class="text-2xl lg:text-3xl font-bold text-default">
              رایحه مخصوص به خودتان را کشف کنید!
            </p>

            <p class="text-xl lg:text-2xl font-semibold text-toned">
              بهترین کیفیت! مناسب‌ترین قیمت!
            </p>
          </div>

          <div class="flex justify-center lg:justify-start mt-8 lg:pr-20">
            <UButton
              to="/products"
              color="primary"
              variant="solid"
              size="xl"
              class="relative overflow-hidden group/btn px-20 py-7 text-2xl font-bold rounded-2xl shadow-2xl transform hover:scale-105 transition-all duration-500"
            >
              <span
                class="absolute inset-0 w-full h-full bg-white dark:bg-white/20 opacity-0 group-hover/btn:opacity-30 translate-x-[-100%] group-hover/btn:translate-x-full transition-transform duration-1000 skew-x-12"
              ></span>

              <span class="relative z-10 flex items-center gap-3">
                کشف مجموعه عطرها
                <UIcon name="i-heroicons-arrow-left" class="w-7 h-7" />
              </span>
            </UButton>
          </div>

          <p class="text-sm text-muted mt-6 lg:pr-20">
            بیش از ۵۰۰ رایحه اورجینال با ضمانت اصالت
          </p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const selectedCategory = ref("all");

// Your products array (make sure it has at least 8 items)
const products = ref([
  {
    id: 4,
    slug: "dior-sauvage-4",
    name: "دیور ساواج",
    price: 2500000,
    discountPercent: 10,
    rating: 4.5,
    reviews: 128,
    image: "https://picsum.photos/400/400?perfume=4",
    category: "male",
    badge: { text: "جدید", color: "primary" },
  },

  {
    id: 5,
    slug: "chanel-bleu-5",
    name: "شنل بلو د شنل",
    price: 3200000,
    discountPercent: 15,
    rating: 4.7,
    reviews: 210,
    image: "https://picsum.photos/400/400?perfume=5",
    category: "male",
    badge: { text: "پرفروش", color: "success" },
  },

  {
    id: 6,
    slug: "lancome-la-vie-6",
    name: "لانکوم لا ویه است بله",
    price: 1980000,
    discountPercent: 8,
    rating: 4.2,
    reviews: 74,
    image: "https://picsum.photos/400/400?perfume=6",
    category: "female",
    badge: { text: "ویژه", color: "warning" },
  },

  {
    id: 7,
    slug: "versace-eros-7",
    name: "ورساچه اروس",
    price: 2600000,
    discountPercent: 12,
    rating: 4.3,
    reviews: 91,
    image: "https://picsum.photos/400/400?perfume=7",
    category: "male",
    badge: { text: "تخفیف‌دار", color: "error" },
  },

  {
    id: 8,
    slug: "ysl-libre-8",
    name: "ایو سن لورن لیبره",
    price: 3000000,
    discountPercent: 5,
    rating: 4.6,
    reviews: 52,
    image: "https://picsum.photos/400/400?perfume=8",
    category: "female",
    badge: { text: "پیشنهادی", color: "primary" },
  },

  {
    id: 9,
    slug: "creed-aventus-9",
    name: "کرید اونتوس",
    price: 2850000,
    discountPercent: 18,
    rating: 4.8,
    reviews: 184,
    image: "https://picsum.photos/400/400?perfume=9",
    category: "male",
    badge: { text: "پرفروش", color: "success" },
  },

  {
    id: 10,
    slug: "burberry-her-10",
    name: "بربری هر",
    price: 1750000,
    discountPercent: 7,
    rating: 4.1,
    reviews: 35,
    image: "https://picsum.photos/400/400?perfume=10",
    category: "female",
    badge: { text: "اقتصادی", color: "gray" },
  },

  {
    id: 11,
    slug: "tomford-black-orchid-11",
    name: "تام فورد بلک اورکید",
    price: 2300000,
    discountPercent: 9,
    rating: 4.4,
    reviews: 147,
    image: "https://picsum.photos/400/400?perfume=11",
    category: "unisex",
    badge: { text: "کلاسیک", color: "warning" },
  },
]);

const banners = ref([
  {
    id: 1,
    image: "https://picsum.photos/1920/600?random=1",
    url: "/collection/summer",
    alt: "تخفیف تابستانه",
    hoverText: "مشاهده کلکسیون تابستان",
  },
  {
    id: 2,
    image: "https://picsum.photos/1920/600?random=2",
    url: "/new-arrivals",
    alt: "محصولات جدید",
    hoverText: "محصولات جدید را ببینید",
  },
  {
    id: 3,
    image: "https://picsum.photos/1920/600?random=3",
    url: "/brands/dior",
    external: false,
    alt: "برند دیور",
    hoverText: "مشاهده عطرهای دیور",
  },
  {
    id: 4,
    image: "https://picsum.photos/1920/600?random=4",
    url: "https://example.com/special-offer",
    external: true,
    alt: "پیشنهاد ویژه",
    hoverText: "پیشنهاد ویژه - کلیک کنید",
  },
]);

// Filter products based on selected category
const filteredProducts = computed(() => {
  if (selectedCategory.value === "all") {
    return products.value;
  }
  return products.value.filter((p) => p.category === selectedCategory.value);
});
</script>
