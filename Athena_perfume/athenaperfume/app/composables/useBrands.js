// composables/useBrands.js
export function useBrands() {
  const brands = useState('brands', () => [])
  const loading = ref(false)

  async function fetchBrands() {
    loading.value = true
    try {
      const { data } = await useFetch('/api/brands')
      brands.value = data.value || []
    } finally {
      loading.value = false
    }
  }

  async function addBrand(formData) {
    // formData: FormData with name, slug, image, etc.
    const created = await $fetch('/api/brands', {
      method: 'POST',
      body: formData
    })
    brands.value.push(created)
    return created
  }

  async function deleteBrand(id) {
    await $fetch(`/api/brands/${id}`, {
      method: 'DELETE'
    })
    brands.value = brands.value.filter(b => b.id !== id)
  }

  return {
    brands,
    loading,
    fetchBrands,
    addBrand,
    deleteBrand
  }
}