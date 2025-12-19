<!-- components/BrandCards.vue -->
<template>
  <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
    <UCard
      v-for="brand in brands"
      :key="brand.id"
      :ui="{ body: 'flex flex-col items-center text-center gap-3 p-4 sm:p-6' }"
    >
      <UAvatar
        :src="brand.image"
        :alt="brand.name"
        size="3xl"
        class="ring-1 ring-border"
      />

      <div class="space-y-1">
        <p class="font-medium text-default">
          {{ brand.name }}
        </p>
        <p class="text-xs text-muted">
          /product_brand/{{ brand.slug }}
        </p>
      </div>

      <div class="flex gap-2 w-full mt-auto">
        <UButton
          size="xs"
          variant="outline"
          color="neutral"
          icon="i-lucide-eye"
          block
          @click="$emit('view', brand)"
        >
          Details
        </UButton>
        <UButton
          size="xs"
          color="error"
          variant="ghost"
          icon="i-lucide-trash-2"
          square
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
