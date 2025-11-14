<template>
  <UCard
    class="cursor-pointer hover:shadow-lg transition-shadow"
    @click="navigateToProduct"
  >
    <!-- Product Image -->
    <img
      :src="product.image"
      :alt="product.name"
      class="w-full h-48 object-cover rounded-t-lg"
    />

    <!-- Product Info -->
    <div class="p-4 space-y-2">
      <!-- Product Name -->
      <h3 class="font-semibold text-lg truncate">{{ product.name }}</h3>

      <!-- Star Rating -->
      <div class="flex items-center gap-1">
        <span v-for="star in 5" :key="star" class="text-yellow-400">
          {{ star <= product.rating ? "★" : "☆" }}
        </span>
        <span class="text-sm text-gray-600 ml-2">({{ product.rating }})</span>
      </div>

      <!-- Price -->
      <p class="text-xl font-bold text-primary">${{ product.price }}</p>
    </div>
  </UCard>
</template>

<script setup>
const props = defineProps({
  product: {
    type: Object,
    required: true,
  },
});

const navigateToProduct = () => {
  navigateTo(`/products/${props.product.id}`);
};
</script>
