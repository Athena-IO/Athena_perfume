<template>
  <div class="p-6">
    <UContainer>
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- فیلترها -->
        <aside class="lg:w-64 shrink-0">
          <ProductFilter
            :selectedCategory="selectedCategory"
            :selectedSort="selectedSort"
            :filtered-count="filteredProducts.length"
            @update:category="selectedCategory = $event"
            @update:sort="selectedSort = $event"
          />
        </aside>

        <!-- لیست محصولات -->
        <div class="flex-1">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <UCard
              v-for="product in filteredProducts"
              :key="product.id"
              class="group hover:shadow-xl transition-all duration-300"
            >
              <!-- تصویر محصول -->
              <div class="relative overflow-hidden rounded-lg mb-4">
                <img
                  :src="product.image"
                  :alt="product.name"
                  class="w-full h-56 object-cover group-hover:scale-105 transition-transform duration-300"
                />

                <!-- بج -->
                <div class="absolute top-3 right-3">
                  <UBadge
                    :color="product.badge.color"
                    variant="solid"
                    size="sm"
                  >
                    {{ product.badge.text }}
                  </UBadge>
                </div>

                <!-- درصد تخفیف -->
                <div
                  v-if="product.discountPercent > 0"
                  class="absolute top-3 left-3"
                >
                  <UBadge color="error" variant="solid" size="sm">
                    {{ product.discountPercent }}% تخفیف
                  </UBadge>
                </div>
              </div>

              <!-- محتوای کارت -->
              <div class="space-y-3">
                <h3
                  class="font-bold text-lg text-gray-900 dark:text-white line-clamp-1"
                >
                  {{ product.name }}
                </h3>

                <!-- امتیاز و نظرات -->
                <div class="flex items-center gap-2 text-sm">
                  <div class="flex items-center gap-1">
                    <UIcon
                      name="i-lucide-star"
                      class="text-yellow-400 size-4"
                    />
                    <span class="font-medium">{{ product.rating }}</span>
                  </div>
                  <span class="text-gray-400">•</span>
                  <span class="text-gray-600 dark:text-gray-400">
                    {{ product.reviews }} نظر
                  </span>
                </div>

                <!-- قیمت -->
                <div class="flex items-center justify-between pt-2">
                  <div class="flex flex-col">
                    <span class="text-2xl font-bold text-primary">
                      {{ product.price.toLocaleString() }}
                    </span>
                    <span class="text-xs text-gray-500">تومان</span>
                  </div>
                </div>

                <!-- دکمه افزودن به سبد -->
                <UButton
                  block
                  color="primary"
                  size="lg"
                  trailing-icon="i-lucide-shopping-cart"
                  @click="addToCart(product)"
                >
                  افزودن به سبد
                </UButton>
              </div>
            </UCard>
          </div>

          <!-- پیام خالی -->
          <div v-if="filteredProducts.length === 0" class="text-center py-12">
            <UIcon
              name="i-lucide-package-x"
              class="size-16 text-gray-400 mx-auto mb-4"
            />
            <p class="text-gray-600 dark:text-gray-400 text-lg">
              محصولی یافت نشد
            </p>
          </div>
        </div>
      </div>
    </UContainer>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";
import ProductFilter from "~/components/ProductFilter.vue";

const selectedCategory = ref("all");
const selectedSort = ref("none");

const products = ref([
  {
    id: 4,
    slug: "dior-sauvage-4",
    name: "دیور ساواج",
    price: 2500000,
    discountPercent: 10,
    rating: 4.5,
    reviews: 128,
    image:
      "https://liliome.com/wp-content/uploads/2016/04/Dior-Sauvage-1.jpg?v=1680545729",
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
    image: "https://liliome.ir/wp-content/uploads/2015/12/6-1.jpg",
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
    image:
      "https://hamedsps.ir/wp-content/uploads/2023/04/%D9%84%D9%88%DB%8C%D9%87-%D8%A8%D9%84.jpg",
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
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYNzQWBYJkEtxw5kCcSyHGKnEVOugmqPf2qg&s",
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
    image:
      "https://liliome.com/wp-content/uploads/2019/08/Yves-Saint-Laurent-Libre-1.jpg",
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
    image: "https://liliome.ir/wp-content/uploads/2016/12/3-76.jpg",
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
    image:
      "https://www.roha-shop.com/wp-content/uploads/2022/08/%D8%A8%D8%A7%D8%B1%D8%A8%D8%B1%DB%8C-%D9%87%D8%B1-01.jpg",
    category: "female",
    badge: { text: "اقتصادی", color: "neutral" },
  },
  {
    id: 11,
    slug: "tomford-black-orchid-11",
    name: "تام فورد بلک اورکید",
    price: 2300000,
    discountPercent: 9,
    rating: 4.4,
    reviews: 147,
    image:
      "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTE-LsGMChiT5p8uw2tsRiBoO29qJotnXihyg&s",
    category: "unisex",
    badge: { text: "کلاسیک", color: "warning" },
  },
]);

// فیلترینگ + سورت
const filteredProducts = computed(() => {
  let list = [...products.value];

  if (selectedCategory.value !== "all") {
    list = list.filter((p) => p.category === selectedCategory.value);
  }

  if (selectedSort.value === "price_low_high") {
    list.sort((a, b) => a.price - b.price);
  } else if (selectedSort.value === "price_high_low") {
    list.sort((a, b) => b.price - a.price);
  }

  return list;
});

// افزودن به سبد خرید
const addToCart = (product) => {
  console.log("Added to cart:", product);
  // منطق افزودن به سبد خرید
};
</script>
