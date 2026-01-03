import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCategoriesStore = defineStore('categories', () => {
  const categories = ref([])
  const loading = ref(false)
  const error = ref(null)

  const getCategoryById = (id) => {
    return categories.value.find(cat => cat.id === id);
  };

  const getCategoryBySlug = (slug) => {
    return categories.value.find(cat => cat.slug === slug);
  };

  const categoryOptions = computed(() => {
    return categories.value.map(cat => ({
      label: cat.label || cat.name,
      value: cat.value || cat.slug,
      description: cat.description,
    }));
  });

  const fetchCategories = async () => {
    loading.value = true;
    error.value = null;

    try {
      const { data } = await useFetch('/api/categories');
      categories.value = data.value || [];
    } catch (err) {
      error.value = err;
      console.error('Error fetching categories:', err);
    } finally {
      loading.value = false;
    }
  };

  const addCategory = (category) => {
    if (category && !categories.value.find(c => c.slug === category.slug)) {
      categories.value.push(category);
    }
  };

  const updateCategory = (updatedCategory) => {
    const index = categories.value.findIndex(c => c.id === updatedCategory.id);
    if (index !== -1) {
      categories.value[index] = { ...categories.value[index], ...updatedCategory };
    }
  };

  const removeCategory = (categoryId) => {
    categories.value = categories.value.filter(c => c.id !== categoryId);
  };

  return {
    categories,
    loading,
    error,
    getCategoryById,
    getCategoryBySlug,
    categoryOptions,
    fetchCategories,
    addCategory,
    updateCategory,
    removeCategory,
  };
});
