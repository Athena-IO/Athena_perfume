<script setup>
const route = useRoute();
const brand = route.params.brand;
</script>

<template>
  <ProductList :brand="brand" />
</template>
