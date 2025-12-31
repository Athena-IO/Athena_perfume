export function useBrands() {
  const brands = useState("brands", () => []);
  const loading = ref(false);

  async function fetchBrands() {
    loading.value = true;
    try {
      const { data } = await useFetch("/api/products/brands");
      brands.value = data.value || [];
    } finally {
      loading.value = false;
    }
  }

  async function addBrand(formData) {
    await $fetch("/api/products/brands", {
      method: "POST",
      body: formData,
    });
    // re-fetch from DB so list is always in sync
    await fetchBrands();
  }

  async function deleteBrand(id) {
    await $fetch(`/api/products/brands/${id}`, {
      method: "DELETE",
    });
    // optionally also refetch here:
    // await fetchBrands()
    brands.value = brands.value.filter((b) => b.id !== id);
  }

  return {
    brands,
    loading,
    fetchBrands,
    addBrand,
    deleteBrand,
  };
}
