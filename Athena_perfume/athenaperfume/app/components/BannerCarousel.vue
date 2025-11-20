<template>
  <div v-if="banners?.length" class="relative w-full">
    <UCarousel
      ref="carousel"
      v-slot="{ item }"
      :items="banners"
      :ui="{
        viewport: 'rounded-lg overflow-hidden',
        item: 'basis-full relative',
        prev: 'absolute left-4 top-1/2 -translate-y-1/2 z-30 bg-black/60 text-white p-3 rounded-full shadow-xl opacity-70 hover:opacity-100 hover:bg-black/80 transition-all duration-300',
        next: 'absolute right-4 top-1/2 -translate-y-1/Commits:absolute right-4 top-1/2 -translate-y-1/2 z-30 bg-black/60 text-white p-3 rounded-full shadow-xl opacity-70 hover:opacity-100 hover:bg-black/80 transition-all duration-300',
        indicators: 'absolute bottom-6 left-1/2 -translate-x-1/2 z-30 flex gap-3',
        indicator: 'bg-white/70 hover:bg-white w-3 h-3 rounded-full transition-all duration-300'
      }"
      loop
      arrows
      indicators
      :autoplay="autoplayOptions"
    >
      <!-- اسلاید -->
      <div :class="heightClass" class="w-full relative overflow-hidden rounded-lg">
        <NuxtLink
          :to="item.url"
          :target="item.external ? '_blank' : '_self'"
          class="block w-full h-full"
        >
          <img
            :src="item.image"
            :alt="item.alt"
            class="w-full h-full object-cover hover:scale-105 transition-transform duration-700 ease-out"
            draggable="false"
            @mouseenter="showTooltip($event, item.hoverText)"
            @mousemove="moveTooltip"
            @mouseleave="hideTooltip"
          />
        </NuxtLink>
      </div>
    </UCarousel>

    <!-- Tooltip -->
    <Teleport to="body">
      <div
        v-if="tooltip.show"
        :style="{ left: tooltip.x + 'px', top: tooltip.y + 'px' }"
        class="fixed z-[9999] -translate-x-1/2 -translate-y-full -mt-2 px-4 py-2 bg-black/90 text-white text-sm rounded-lg pointer-events-none whitespace-nowrap backdrop-blur-sm"
      >
        {{ tooltip.text }}
        <div class="absolute left-1/2 -bottom-1 -translate-x-1/2 w-0 h-0 border-l-8 border-l-transparent border-r-8 border-r-transparent border-t-8 border-t-black/90"></div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
const props = defineProps({
  banners: { type: Array, default: () => [] },
  height: { type: String, default: 'medium' },
  autoplay: { type: Boolean, default: true },
  autoplayDelay: { type: Number, default: 5000 }
})

const heightClass = computed(() => ({
  small: 'h-48 sm:h-64',
  medium: 'h-64 sm:h-80 md:h-96',
  large: 'h-80 sm:h-96 md:h-[500px]',
  auto: 'aspect-[16/9]'
})[props.height])

// محاسبه autoplay با pauseOnHover
const autoplayOptions = computed(() => 
  props.autoplay ? { delay: props.autoplayDelay, pauseOnHover: true } : false
)

const tooltip = reactive({ show: false, text: '', x: 0, y: 0 })

const showTooltip = (e, text) => {
  if (text) {
    tooltip.show = true
    tooltip.text = text
    tooltip.x = e.clientX
    tooltip.y = e.clientY
  }
}

const moveTooltip = (e) => {
  if (tooltip.show) {
    tooltip.x = e.clientX
    tooltip.y = e.clientY
  }
}

const hideTooltip = () => {
  tooltip.show = false
  tooltip.text = ''
}
</script>