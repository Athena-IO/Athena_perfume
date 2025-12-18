// composables/useBanners.js
export function useBanners() {
  // useState so the banners can be shared across pages/components
  const banners = useState('banners', () => [])
  const loading = ref(false)

  async function fetchBanners() {
    loading.value = true
    try {
      const { data } = await useFetch('/api/banners')
      banners.value = data.value || []
    } 
    catch (error) {
    toast.add({
      title: 'Error',
      description: 'Failed to load banners',
      color: 'error'
    })
    loading.value = false
}
  finally {
      loading.value = false
    }
  }

  return { banners, loading, fetchBanners }
}