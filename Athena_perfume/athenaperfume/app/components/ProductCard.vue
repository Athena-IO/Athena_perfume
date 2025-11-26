<template>
<NuxtLink
  v-if="product && product.slug"
  :to="`/products/${product.slug}`"
  class="block border rounded-lg overflow-hidden hover:shadow-lg transition-shadow"
>
    <!-- Product Image -->
    <div class="relative aspect-square bg-gray-100">
      <img 
        :src="product.image" 
        :alt="product.name"
        class="w-full h-full object-cover hover:scale-105 transition-transform duration-300"
      />
      
      <!-- Optional: Badge for discount/new items -->
      <div v-if="product.badge" class="absolute top-2 right-2">
        <UBadge :color="product.badge.color" variant="solid">
          {{ product.badge.text }}
        </UBadge>
      </div>
    </div>
    
    <!-- Product Info -->
    <div class="p-4">
      <!-- Rating -->
      <div class="flex items-center gap-1 mb-2">
        <UIcon name="i-lucide-star" class="text-yellow-400 w-4 h-4 fill-yellow-400" />
        <span class="text-sm font-medium">{{ product.rating }}</span>
        <span class="text-sm text-gray-500">({{ product.reviews || 0 }})</span>
      </div>
      
      <!-- Product Name -->
      <h3 class="font-semibold mb-2 line-clamp-2 text-gray-900 dark:text-white">
        {{ product.name }}
      </h3>
      
      <!-- Price -->
      <div class="flex items-center gap-2">
        <p class="text-lg font-bold text-primary">{{ product.price }}</p>
        <p v-if="product.oldPrice" class="text-sm text-gray-400 line-through">
          {{ product.oldPrice }}
        </p>
      </div>
    </div>
  </NuxtLink>
</template>

<script setup>
defineProps({
  product: {
    type: Object,
    required: true,
    default: () => ({})
  }
})
</script>
