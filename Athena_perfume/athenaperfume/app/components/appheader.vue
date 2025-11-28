<template>
  <UHeader>
    <!-- لوگو -->
    <template #title>
      <NuxtLink to="/" class="font-black text-xl flex items-center gap-3">
        <UIcon name="i-lucide-droplet"class="w-7 h-7 text-primary" />
        Athena Perfume
      </NuxtLink>
    </template>

    <!-- منوی اصلی -->
    <UNavigationMenu :items="navItems" />

    <!-- سمت راست: تم + سبد خرید -->
    <template #right>
      <UColorModeButton />

      <!-- دکمه سبد خرید با تعداد آیتم -->
      <div class="relative">
        <UButton
          color="neutral"
          variant="ghost"
          size="md"
          icon="i-lucide-shopping-cart"
          aria-label="سبد خرید"
          class="text-xl"
          @click="cartOpen = true"
        />

        <!-- تعداد آیتم‌ها روی دکمه -->
        <transition name="fade">
          <div
            v-if="totalItems > 0"
            class="absolute -top-2 -right-2 bg-primary text-white text-xs font-bold rounded-full w-6 h-6 flex items-center justify-center shadow-lg"
          >
            {{ totalItems }}
          </div>
        </transition>
      </div>

    </template>
  </UHeader>

  <!-- دراور سبد خرید -->
  <CartSlideover v-model:open="cartOpen" />
</template>

<script setup>
// بدون lang="ts" → فقط JavaScript خالص
import { useCartStore } from "~/composables/stores/cart"

const cartStore = useCartStore()
const cartOpen = ref(false)

// تعداد کل آیتم‌ها (با چک امن)
const totalItems = computed(() => {
  return cartStore.items.reduce((sum, item) => sum + (item.qty || 0), 0)
})

// منوی اصلی
const navItems = [
  { label: "تخفیف‌ها", to: "/discounts" },
  { label: "عطر مردانه", to: "/men" },
  { label: "عطر زنانه", to: "/women" },
  { label: "فروشگاه", to: "/products" }
]
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: all 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>