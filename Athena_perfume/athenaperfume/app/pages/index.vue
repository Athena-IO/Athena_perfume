<template>
  <div class="text-red-500">hello</div>

  <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6">
    <ProductCard
      v-for="product in products"
      :key="product.id"
      :product="product"
    />
  </div>
</template>
<script setup>
const products = [
  {
    id: 1,
    name: "Product Name",
    image: "/images/product1.jpg",
    rating: 4.5,
    price: 29.99,
  },
];
</script>
