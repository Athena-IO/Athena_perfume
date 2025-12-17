// composables/useSearch.js
export function useSearch(queryRef) {
  // When a ref is used inside `query` and added to `watch`,
  // useFetch will refetch when it changes.[useFetch watch](https://stackoverflow.com/questions/78633662)
  const { data, pending, error } = useFetch('/api/search', {
    method: 'GET',
    query: { q: queryRef },
    watch: [queryRef],
  })

  const results = computed(() => (data.value && data.value.items) || [])

  return { results, pending, error }
}