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
    <div class="grid lg:grid-cols-2 grid-cols-1 items-center min-h-[70vh]">
      <div class="pl-25">
        <img
          src="https://cdn.mos.cms.futurecdn.net/VzUqgr8pfbNcfXrpzeVBPE.jpg"
          alt=""
          class="w-full h-auto rounded-lg"
        />
      </div>

      <div class="flex flex-col gap-6 text-right items-start pr-56" dir="rtl">
        <h2 class="text-4xl font-bold">کیفیت دیدتان را تغییر دهید</h2>
        <p class="text-xl font-bold">رایحه مخصوص به خودتان را کشف کنید!</p>
        <p class="text-xl font-bold">بهترین کیفیت! مناسب ترین قیمت!</p>

        <div class="flex gap-4 mt-4 pr-15">
          <UButton
            color="primary"
            variant="solid"
            size="xl"
            class="px-12 py-4 text-lg"
            >مردانه</UButton
          >
          <UButton
            color="neutral"
            variant="outline"
            size="xl"
            class="px-12 py-4 text-lg"
            >زنانه</UButton
          >
        </div>
      </div>
    </div>
  </div>
  <div class="w-full px-4 sm:px-6 lg:px-8">
    <div
      class="grid lg:grid-cols-2 grid-cols-1 gap-6 items-center min-h-[30vh]"
    >
      <!-- Box 1 -->
      <ULink to="/men-products" class="group block h-full" raw>
        <UCard
          class="relative overflow-hidden h-full transition-all duration-300 group-hover:shadow-xl"
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
                class="text-white text-3xl font-bold z-10 transform group-hover:scale-110 transition-transform duration-300"
              >
                مردانه
              </p>
            </div>
          </div>
        </UCard>
      </ULink>

      <!-- Box 2 -->
      <ULink to="/women-products" class="group block h-full" raw>
        <UCard
          class="relative overflow-hidden h-full transition-all duration-300 group-hover:shadow-xl"
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
                class="text-white text-3xl font-bold z-10 transform group-hover:scale-110 transition-transform duration-300"
              >
                زنانه
              </p>
            </div>
          </div>
        </UCard>
      </ULink>
    </div>
  </div>
  <div class="overflow-hidden">
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
              ? 'border-b-2 border-black dark:border-white rounded-none'
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
              ? 'border-b-2 border-black dark:border-white rounded-none'
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
              ? 'border-b-2 border-black dark:border-white rounded-none'
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
          next: 'absolute -right-12 top-1/2 -translate-y-1/2 z-10'
        }"
        :prev="{ 
          color: 'primary', 
          variant: 'solid',
          size: 'lg',
          square: true
        }"
        :next="{ 
          color: 'primary', 
          variant: 'solid',
          size: 'lg',
          square: true
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
</template>

<script setup>
const selectedCategory = ref('all')

// Your products array (make sure it has at least 8 items)
const products = ref([
  {
    id: 1,
    name: 'کفش ورزشی نایک ایر مکس',
    price: '۲,۵۰۰,۰۰۰ تومان',
    oldPrice: '۳,۰۰۰,۰۰۰ تومان', // optional
    rating: 4.5,
    reviews: 128, // optional
    image: 'https://picsum.photos/400/400?random=1',
    category: 'male',
    badge: { text: 'جدید', color: 'primary' } // optional
  },
 {
    id: 1,
    name: 'کفش ورزشی نایک ایر مکس',
    price: '۲,۵۰۰,۰۰۰ تومان',
    oldPrice: '۳,۰۰۰,۰۰۰ تومان', // optional
    rating: 4.5,
    reviews: 128, // optional
    image: 'https://picsum.photos/400/400?random=1',
    category: 'male',
    badge: { text: 'جدید', color: 'primary' } // optional
  },
 {
    id: 1,
    name: 'کفش ورزشی نایک ایر مکس',
    price: '۲,۵۰۰,۰۰۰ تومان',
    oldPrice: '۳,۰۰۰,۰۰۰ تومان', // optional
    rating: 4.5,
    reviews: 128, // optional
    image: 'https://picsum.photos/400/400?random=1',
    category: 'male',
    badge: { text: 'جدید', color: 'primary' } // optional
  },
 {
    id: 1,
    name: 'کفش ورزشی نایک ایر مکس',
    price: '۲,۵۰۰,۰۰۰ تومان',
    oldPrice: '۳,۰۰۰,۰۰۰ تومان', // optional
    rating: 4.5,
    reviews: 128, // optional
    image: 'https://picsum.photos/400/400?random=1',
    category: 'male',
    badge: { text: 'جدید', color: 'primary' } // optional
  },
 {
    id: 1,
    name: 'کفش ورزشی نایک ایر مکس',
    price: '۲,۵۰۰,۰۰۰ تومان',
    oldPrice: '۳,۰۰۰,۰۰۰ تومان', // optional
    rating: 4.5,
    reviews: 128, // optional
    image: 'https://picsum.photos/400/400?random=1',
    category: 'male',
    badge: { text: 'جدید', color: 'primary' } // optional
  },])
  const banners = ref([
  {
    id: 1,
    image: 'https://picsum.photos/1920/600?random=1',
    url: '/collection/summer',
    alt: 'تخفیف تابستانه',
    hoverText: 'مشاهده کلکسیون تابستان' // Text shown on cursor hover
  },
  {
    id: 2,
    image: 'https://picsum.photos/1920/600?random=2',
    url: '/new-arrivals',
    alt: 'محصولات جدید',
    hoverText: 'محصولات جدید را ببینید'
  },
  {
    id: 3,
    image: 'https://picsum.photos/1920/600?random=3',
    url: '/brands/dior',
    external: false,
    alt: 'برند دیور',
    hoverText: 'مشاهده عطرهای دیور'
  },
  {
    id: 4,
    image: 'https://picsum.photos/1920/600?random=4',
    url: 'https://example.com/special-offer',
    external: true,
    alt: 'پیشنهاد ویژه',
    hoverText: 'پیشنهاد ویژه - کلیک کنید'
  }
])

// Filter products based on selected category
const filteredProducts = computed(() => {
  if (selectedCategory.value === 'all') {
    return products.value
  }
  return products.value.filter(p => p.category === selectedCategory.value)
})

</script>
