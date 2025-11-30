<template>
  <div class="space-y-4 w-full">
    <!-- Main Carousel -->
    <UCarousel
      ref="carousel"
      :items="images"
      arrows
      dots
      class="w-full rounded-xl overflow-hidden"
      @select="onCarouselSelect"
    >
      <template #default="{ item }">
        <img :src="item" class="w-full h-80 object-cover rounded-lg" />
      </template>
    </UCarousel>

    <!-- Thumbnails -->
    <div class="flex gap-3 justify-center">
      <div
        v-for="(img, i) in images"
        :key="i"
        class="cursor-pointer transition-all duration-200"
        :class="[
          activeIndex === i
            ? 'ring-2 ring-primary opacity-100'
            : 'opacity-50 hover:opacity-75',
        ]"
        @click="selectSlide(i)"
      >
        <UCard class="rounded-lg overflow-hidden">
          <img :src="img" class="w-20 h-20 object-cover" />
        </UCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const props = defineProps({
  images: {
    type: Array,
    required: true,
  },
});

const activeIndex = ref(0);
const carousel = ref(null);

// When user scrolls in the Carousel
function onCarouselSelect(index) {
  activeIndex.value = index;
}

// When clicking on a thumbnail
function selectSlide(index) {
  activeIndex.value = index;
  carousel.value?.emblaApi?.scrollTo(index);
}
</script>
