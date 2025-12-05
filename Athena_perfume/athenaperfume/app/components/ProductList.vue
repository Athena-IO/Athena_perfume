<template>
  <div class="p-6">
    <UContainer>
      <div class="flex flex-col lg:flex-row gap-6">
        <!-- فیلترها -->
        <aside class="lg:w-64 shrink-0">
          <ProductFilter
            :selectedCategory="selectedCategory"
            :selectedBrands="selectedBrands"
            :selectedSort="selectedSort"
            :filtered-count="filteredProducts.length"
            @update:category="selectedCategory = $event"
            @update:brands="selectedBrands = $event"
            @update:sort="selectedSort = $event"
          />
        </aside>

        <!-- لیست محصولات -->
        <div class="flex-1">
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <ProductCard
              v-for="product in filteredProducts"
              :key="product.id"
              :product="product"
            />
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
import { ref, computed, watch } from "vue";
import ProductFilter from "~/components/ProductFilter.vue";
import ProductCard from "~/components/ProductCard.vue";

const props = defineProps({
  category: {
    type: String,
    default: "all",
  },
  brand: {
    type: String,
    default: null,
  },
});

// Initialize with props
const selectedCategory = ref(props.category);
const selectedBrands = ref(props.brand ? [props.brand] : []);
const selectedSort = ref("none");

// Watch for prop changes and update local state
watch(
  () => props.category,
  (newCategory) => {
    selectedCategory.value = newCategory;
  },
  { immediate: true }
);

watch(
  () => props.brand,
  (newBrand) => {
    selectedBrands.value = newBrand ? [newBrand] : [];
  },
  { immediate: true }
);

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
    brand: "dior",
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
    brand: "chanel",
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
    brand: "lancome",
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
    brand: "versace",
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
    brand: "ysl",
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
    brand: "creed",
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
    brand: "burberry",
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
    brand: "tomford",
    badge: { text: "کلاسیک", color: "warning" },
  },
]);

const filteredProducts = computed(() => {
  let list = [...products.value];

  // Filter by category
  if (selectedCategory.value && selectedCategory.value !== "all") {
    list = list.filter((p) => p.category === selectedCategory.value);
  }

  // Filter by brands (multiple selection)
  if (selectedBrands.value.length > 0) {
    list = list.filter((p) => selectedBrands.value.includes(p.brand));
  }

  // Sort
  if (selectedSort.value === "price_low_high") {
    list.sort((a, b) => a.price - b.price);
  } else if (selectedSort.value === "price_high_low") {
    list.sort((a, b) => b.price - a.price);
  }

  return list;
});
</script>
