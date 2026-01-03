import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useBannersStore = defineStore('banners', () => {
  const banners = ref([])
  const loading = ref(false)
  const error = ref(null)

  const getBannerById = (id) => {
    return banners.value.find(banner => banner.id === id);
  };

  const bannerOptions = computed(() => {
    return banners.value.map(banner => ({
      label: banner.name,
      value: banner.id,
      description: banner.link || 'No link',
    }));
  });

  const fetchBanners = async () => {
    loading.value = true;
    error.value = null;

    try {
      const { data } = await useFetch('/api/banners');
      banners.value = data.value || [];
    } catch (err) {
      error.value = err;
      console.error('Error fetching banners:', err);
      // If API fails, use fallback banners
      banners.value = [
        {
          id: 1,
          image: "https://picsum.photos/1920/600?random=1",
          url: "/products",
          alt: "مجموعه محصولات",
          name: "مجموعه محصولات",
          link: "/products"
        },
        {
          id: 2,
          image: "https://picsum.photos/1920/600?random=2",
          url: "/brands",
          alt: "برندها",
          name: "برندها",
          link: "/brands"
        }
      ];
    } finally {
      loading.value = false;
    }
  };

  const addBanner = async (formData) => {
    try {
      const created = await $fetch('/api/banners', {
        method: 'POST',
        body: formData,
      });
      banners.value.push(created);
    } catch (err) {
      error.value = err;
      throw err;
    }
  };

  const removeBanner = async (id) => {
    try {
      await $fetch(`/api/banners/${id}`, {
        method: 'DELETE',
      });
      banners.value = banners.value.filter((b) => b.id !== id);
    } catch (err) {
      error.value = err;
      throw err;
    }
  };

  const updateBanner = (updatedBanner) => {
    const index = banners.value.findIndex(b => b.id === updatedBanner.id);
    if (index !== -1) {
      banners.value[index] = { ...banners.value[index], ...updatedBanner };
    }
  };

  return {
    banners,
    loading,
    error,
    getBannerById,
    bannerOptions,
    fetchBanners,
    addBanner,
    removeBanner,
    updateBanner,
  };
});
