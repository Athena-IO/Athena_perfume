import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useProductsStore = defineStore('products', () => {
  // State
  const allProducts = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Filter states
  const selectedCategory = ref('all')
  const selectedBrands = ref([])
  const selectedSort = ref('none')

  // Pagination
  const currentPage = ref(1)
  const pageSize = ref(20)

  // Getters
  const filteredProducts = computed(() => {
    let list = [...allProducts.value];

    // Filter by category
    if (selectedCategory.value && selectedCategory.value !== 'all') {
      list = list.filter((p) => p.category === selectedCategory.value);
    }

    // Filter by brands (multiple selection)
    if (selectedBrands.value.length > 0) {
      list = list.filter((p) => selectedBrands.value.includes(p.brand));
    }

    // Sort
    if (selectedSort.value === 'price_low_high') {
      list.sort((a, b) => a.price - b.price);
    } else if (selectedSort.value === 'price_high_low') {
      list.sort((a, b) => b.price - a.price);
    }

    return list;
  });

  const totalPages = computed(() => {
    return Math.ceil(filteredProducts.value.length / pageSize.value);
  });

  const paginatedProducts = computed(() => {
    const start = (currentPage.value - 1) * pageSize.value;
    const end = start + pageSize.value;
    return filteredProducts.value.slice(start, end);
  });

  const hasActiveFilters = computed(() => {
    return selectedCategory.value !== 'all' ||
           selectedBrands.value.length > 0 ||
           selectedSort.value !== 'none';
  });

  const getProductById = (id) => {
    return allProducts.value.find(product => product.id === id);
  };

  const getProductBySlug = (slug) => {
    return allProducts.value.find(product => product.slug === slug);
  };

  // Actions
  const fetchAllProducts = async () => {
    loading.value = true;
    error.value = null;

    try {
      // Try to fetch from API first
      const response = await useFetch('/api/products');
      if (response.data.value && response.data.value.length > 0) {
        allProducts.value = response.data.value;
      } else {
        // Fallback to hardcoded products if API is empty
        setFallbackProducts();
      }
    } catch (err) {
      // If API fails, use hardcoded products
      console.warn('API not available, using fallback products');
      setFallbackProducts();
    } finally {
      loading.value = false;
    }
  };

  const setFallbackProducts = () => {
    allProducts.value = [
        {
          id: 4,
          slug: 'dior-sauvage-4',
          name: 'دیور ساواج',
          price: 2500000,
          discountPercent: 10,
          capacity: 250,
          rating: 4.5,
          reviews: 128,
          image: 'https://liliome.com/wp-content/uploads/2016/04/Dior-Sauvage-1.jpg?v=1680545729',
          category: 'male',
          brand: 'dior',
          badge: { text: 'جدید', color: 'primary' },
          information: {
            gender: 'مردانه',
            brand: 'Dior',
            similar: 'Bleu de Chanel',
            type: 'Eau de Toilette',
            season: 'چهار فصل (بهترین برای تابستان)',
            volume: '100ml / 200ml',
          },
        },
        {
          id: 5,
          slug: 'chanel-bleu-5',
          name: 'شنل بلو د شنل',
          price: 3200000,
          discountPercent: 15,
          capacity: 80,
          rating: 4.7,
          reviews: 210,
          image: 'https://liliome.ir/wp-content/uploads/2015/12/6-1.jpg',
          category: 'male',
          brand: 'chanel',
          badge: { text: 'پرفروش', color: 'success' },
          information: {
            gender: 'مردانه',
            brand: 'Chanel',
            similar: 'Dior Sauvage',
            type: 'Eau de Parfum',
            season: 'چهار فصل',
            volume: '100ml / 150ml',
          },
        },
        {
          id: 6,
          slug: 'lancome-la-vie-6',
          name: 'لانکوم لا ویه است بله',
          price: 1980000,
          discountPercent: 8,
          capacity: 0,
          rating: 4.2,
          reviews: 74,
          image: 'https://hamedsps.ir/wp-content/uploads/2023/04/%D9%84%D9%88%DB%8C%D9%87-%D8%A8%D9%84.jpg',
          category: 'female',
          brand: 'lancome',
          badge: { text: 'ویژه', color: 'warning' },
          information: {
            gender: 'زنانه',
            brand: 'Lancôme',
            similar: 'Armani Si',
            type: 'Eau de Parfum',
            season: 'پاییز و زمستان',
            volume: '75ml / 100ml',
          },
        },
        {
          id: 7,
          slug: 'versace-eros-7',
          name: 'ورساچه اروس',
          price: 2600000,
          discountPercent: 12,
          capacity: 150,
          rating: 4.3,
          reviews: 91,
          image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSYNzQWBYJkEtxw5kCcSyHGKnEVOugmqPf2qg&s',
          category: 'male',
          brand: 'versace',
          badge: { text: 'تخفیف‌دار', color: 'error' },
          information: {
            gender: 'مردانه',
            brand: 'Versace',
            similar: 'Invictus by Paco Rabanne',
            type: 'Eau de Toilette',
            season: 'زمستان / پاییز',
            volume: '100ml / 200ml',
          },
        },
        {
          id: 8,
          slug: 'ysl-libre-8',
          name: 'ایو سن لورن لیبره',
          price: 3000000,
          discountPercent: 5,
          capacity: 60,
          rating: 4.6,
          reviews: 52,
          image: 'https://liliome.com/wp-content/uploads/2019/08/Yves-Saint-Laurent-Libre-1.jpg',
          category: 'female',
          brand: 'ysl',
          badge: { text: 'پیشنهادی', color: 'primary' },
          information: {
            gender: 'زنانه',
            brand: 'YSL',
            similar: 'Mon Paris',
            type: 'Eau de Parfum',
            season: 'چهار فصل',
            volume: '90ml',
          },
        },
        {
          id: 9,
          slug: 'creed-aventus-9',
          name: 'کرید اونتوس',
          price: 2850000,
          discountPercent: 18,
          capacity: 300,
          rating: 4.8,
          reviews: 184,
          image: 'https://liliome.ir/wp-content/uploads/2016/12/3-76.jpg',
          category: 'male',
          brand: 'creed',
          badge: { text: 'پرفروش', color: 'success' },
          information: {
            gender: 'مردانه',
            brand: 'Creed',
            similar: 'Mont Blanc Explorer',
            type: 'Eau de Parfum',
            season: 'چهار فصل (بهترین برای بهار)',
            volume: '100ml / 120ml',
          },
        },
        {
          id: 10,
          slug: 'burberry-her-10',
          name: 'بربری هر',
          price: 1750000,
          discountPercent: 7,
          capacity: 40,
          rating: 4.1,
          reviews: 35,
          image: 'https://www.roha-shop.com/wp-content/uploads/2022/08/%D8%A8%D8%A7%D8%B1%D8%A8%D8%B1%DB%8C-%D9%87%D8%B1-01.jpg',
          category: 'female',
          brand: 'burberry',
          badge: { text: 'اقتصادی', color: 'neutral' },
          information: {
            gender: 'زنانه',
            brand: 'Burberry',
            similar: 'Ariana Grande Cloud',
            type: 'Eau de Parfum',
            season: 'بهار و تابستان',
            volume: '100ml',
          },
        },
        {
          id: 11,
          slug: 'tomford-black-orchid-11',
          name: 'تام فورد بلک اورکید',
          price: 2300000,
          discountPercent: 9,
          capacity: 90,
          rating: 4.4,
          reviews: 147,
          image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTE-LsGMChiT5p8uw2tsRiBoO29qJotnXihyg&s',
          category: 'unisex',
          brand: 'tomford',
          badge: { text: 'کلاسیک', color: 'warning' },
          information: {
            gender: 'یونیسکس',
            brand: 'Tom Ford',
            similar: 'Narciso Rodriguez For Her',
            type: 'Eau de Parfum',
            season: 'پاییز و زمستان',
            volume: '100ml / 150ml',
          },
        },
      ];
  };

  // Filter actions
  const setSelectedCategory = (category) => {
    selectedCategory.value = category;
    currentPage.value = 1; // Reset to first page on filter change
  };

  const setSelectedBrands = (brands) => {
    selectedBrands.value = brands;
    currentPage.value = 1; // Reset to first page on filter change
  };

  const setSelectedSort = (sort) => {
    selectedSort.value = sort;
    currentPage.value = 1; // Reset to first page on filter change
  };

  // Pagination actions
  const setCurrentPage = (page) => {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page;
    }
  };

  const nextPage = () => {
    if (currentPage.value < totalPages.value) {
      currentPage.value++;
    }
  };

  const prevPage = () => {
    if (currentPage.value > 1) {
      currentPage.value--;
    }
  };

  // Filter reset
  const resetFilters = () => {
    selectedCategory.value = 'all';
    selectedBrands.value = [];
    selectedSort.value = 'none';
    currentPage.value = 1;
  };

  return {
    // State
    allProducts,
    loading,
    error,
    selectedCategory,
    selectedBrands,
    selectedSort,
    currentPage,
    pageSize,

    // Getters
    filteredProducts,
    totalPages,
    paginatedProducts,
    hasActiveFilters,

    // Actions
    fetchAllProducts,
    setFallbackProducts,
    setSelectedCategory,
    setSelectedBrands,
    setSelectedSort,
    setCurrentPage,
    nextPage,
    prevPage,
    resetFilters,

    // Helper functions
    getProductById,
    getProductBySlug,
  };
});
