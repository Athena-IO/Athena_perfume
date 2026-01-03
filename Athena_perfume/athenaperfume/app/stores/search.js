import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useSearchStore = defineStore('search', () => {
  const searchQuery = ref('')
  const results = ref([])
  const pending = ref(false)
  const error = ref(null)

  const hasResults = computed(() => results.value.length > 0)

  const search = async (query) => {
    if (!query?.trim()) {
      results.value = []
      return
    }

    pending.value = true
    error.value = null

    try {
      const { data, error: fetchError } = await useFetch('/api/search', {
        method: 'GET',
        query: { q: query.trim() }
      })

      if (fetchError.value) {
        throw fetchError.value
      }

      results.value = data.value?.items || []
    } catch (err) {
      error.value = err
      results.value = []
      console.error('Search error:', err)
    } finally {
      pending.value = false
    }
  }

  const clearResults = () => {
    results.value = []
    searchQuery.value = ''
    error.value = null
  }

  const setSearchQuery = (query) => {
    searchQuery.value = query
  }

  return {
    searchQuery,
    results,
    pending,
    error,
    hasResults,
    search,
    clearResults,
    setSearchQuery,
  }
})
