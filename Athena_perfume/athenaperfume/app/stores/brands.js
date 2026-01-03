import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useBrandsStore = defineStore('brands', () => {
  const brands = ref([])
  const loading = ref(false)
  const error = ref(null)

  const getBrandById = (id) => {
    return brands.value.find(brand => brand.id === id);
  };

  const getBrandBySlug = (slug) => {
    return brands.value.find(brand => brand.slug === slug);
  };

  const brandOptions = computed(() => {
    return brands.value.map(brand => ({
      label: brand.name,
      value: brand.slug,
      description: brand.name,
    }));
  });

  const fetchBrands = async () => {
    loading.value = true;
    error.value = null;

    try {
      const { data } = await useFetch('/api/products/brands');
      brands.value = data.value || [];
    } catch (err) {
      error.value = err;
      console.error('Error fetching brands:', err);
    } finally {
      loading.value = false;
    }
  };

  const addBrand = async (formData) => {
    try {
      await $fetch('/api/products/brands', {
        method: 'POST',
        body: formData,
      });
      await fetchBrands(); // Re-fetch to sync
    } catch (err) {
      error.value = err;
      throw err;
    }
  };

  const deleteBrand = async (id) => {
    try {
      await $fetch(`/api/products/brands/${id}`, {
        method: 'DELETE',
      });
      brands.value = brands.value.filter((b) => b.id !== id);
    } catch (err) {
      error.value = err;
      throw err;
    }
  };

  const updateBrand = (updatedBrand) => {
    const index = brands.value.findIndex(b => b.id === updatedBrand.id);
    if (index !== -1) {
      brands.value[index] = { ...brands.value[index], ...updatedBrand };
    }
  };

  return {
    brands,
    loading,
    error,
    getBrandById,
    getBrandBySlug,
    brandOptions,
    fetchBrands,
    addBrand,
    deleteBrand,
    updateBrand,
  };
});
