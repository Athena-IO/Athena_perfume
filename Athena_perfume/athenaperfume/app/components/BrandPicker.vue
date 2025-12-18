<!-- components/BrandSelectModal.vue -->
<template>
  <Transition
    enter-active-class="transition-opacity duration-200 ease-out"
    enter-from-class="opacity-0"
    enter-to-class="opacity-100"
    leave-active-class="transition-opacity duration-150 ease-in"
    leave-from-class="opacity-100"
    leave-to-class="opacity-0"
  >
    <div
      v-if="modelValue"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4"
    >
      <div class="bg-white dark:bg-gray-900 rounded-lg shadow-xl max-w-3xl w-full max-h-[80vh] overflow-hidden flex flex-col">
        <header class="flex items-center justify-between px-4 py-3 border-b border-default">
          <h2 class="text-lg font-semibold">انتخاب برند</h2>
          <UButton
            icon="i-lucide-x"
            variant="ghost"
            size="sm"
            @click="$emit('update:modelValue', false)"
          />
        </header>

        <div class="p-4 overflow-y-auto">
          <div v-if="loading" class="text-center py-8 text-muted">
            در حال بارگذاری برندها...
          </div>

          <div v-else-if="brands.length === 0" class="text-center py-8 text-muted">
            برندی ثبت نشده است.
          </div>

          <div v-else class="grid grid-cols-2 md:grid-cols-4 gap-4">
            <button
              v-for="brand in brands"
              :key="brand.id"
              type="button"
              class="flex flex-col items-center p-3 rounded-lg border border-default hover:border-primary hover:bg-primary/5 transition"
              @click="selectBrand(brand)"
            >
              <div class="w-16 h-16 rounded-full overflow-hidden border border-default mb-2">
                <img
                  :src="brand.image"
                  :alt="brand.name"
                  class="w-full h-full object-cover"
                >
              </div>
              <span class="text-sm font-medium">{{ brand.name }}</span>
              <span class="text-[11px] text-muted mt-1">
                /product_brand/{{ brand.slug }}
              </span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </Transition>
</template>

<script setup>
import { onMounted } from 'vue'
import { useBrands } from '~/composables/useBrands'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:modelValue', 'select'])

const { brands, loading, fetchBrands } = useBrands()

onMounted(() => {
  fetchBrands()
})

function selectBrand(brand) {
  emit('select', brand)
  emit('update:modelValue', false)
}
</script>