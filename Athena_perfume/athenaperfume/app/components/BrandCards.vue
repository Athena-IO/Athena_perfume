<!-- components/BrandCards.vue -->
<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <UCard
      v-for="brand in brands"
      :key="brand.id"
      class="flex flex-col items-center text-center"
    >
      <div class="w-24 h-24 rounded-full overflow-hidden border border-default mb-3">
        <img
          :src="brand.image"
          :alt="brand.name"
          class="w-full h-full object-cover"
        >
      </div>

      <div class="font-medium mb-1">
        {{ brand.name }}
      </div>

      <div class="text-xs text-muted mb-3">
        /product_brand/{{ brand.slug }}
      </div>

      <div class="flex gap-2">
        <UButton
          size="xs"
          variant="outline"
          icon="i-lucide-eye"
          @click="$emit('view', brand)"
        >
          Details
        </UButton>
        <UButton
          size="xs"
          color="error"
          variant="ghost"
          icon="i-lucide-trash-2"
          @click="$emit('delete', brand)"
        />
      </div>
    </UCard>
  </div>
</template>

<script setup>
defineProps({
  brands: {
    type: Array,
    required: true
  }
})

defineEmits(['view', 'delete'])
</script>