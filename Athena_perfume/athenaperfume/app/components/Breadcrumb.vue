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
  const items = [{ label: 'خانه', to: '/' }]

  const segments = route.path.split('/').filter(Boolean)

  let currentPath = ''
  segments.forEach((seg, index) => {
    currentPath += '/' + seg
    const isLast = index === segments.length - 1

    items.push({
      label: labelMap[seg] ?? decodeURIComponent(seg),
      ...(isLast ? {} : { to: currentPath })
    })
  })

  return items
})
</script>