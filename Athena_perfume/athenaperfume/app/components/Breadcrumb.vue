<!-- components/Breadcrumb.vue -->
<template>
  <UBreadcrumb :items="breadcrumbItems" separator-icon="i-lucide-slash" />
</template>

<script setup>
const route = useRoute()

const labelMap = {
  products: 'محصولات',
  product_brand: 'برند',
  male: 'مردانه',
  female: 'زنانه',
}

const breadcrumbItems = computed(() => {
  // Start with home
  const items = [
    {
      label: 'خانه',
      to: '/'
    }
  ]

  // Get path segments
  const segments = route.path.split('/').filter(Boolean)
  
  // Build breadcrumb items from URL
  let currentPath = ''
  segments.forEach((seg, index) => {
    currentPath += '/' + seg
    const isLast = index === segments.length - 1
    
    items.push({
      label: labelMap[seg] ?? decodeURIComponent(seg),
      // Only add 'to' if it's not the last item (last item becomes span automatically)
      ...(isLast ? {} : { to: currentPath })
    })
  })

  return items
})
</script>