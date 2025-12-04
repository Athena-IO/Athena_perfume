<template>
  <UHeader>
    <!-- لوگو -->
    <template #title>
      <NuxtLink to="/" class="font-black text-xl flex items-center gap-3">
        <UIcon name="i-lucide-droplet" class="w-7 h-7 text-primary" />
        Athena Perfume
      </NuxtLink>
    </template>

    <!-- منوی اصلی -->
    <UNavigationMenu :items="navItems" />

    <!-- سمت راست: تم + کاربر + سبد خرید -->
    <template #right>
      <UColorModeButton />

      <!-- بخش احراز هویت کاربر -->
      <div v-if="isAuthenticated">
        <UDropdownMenu :items="userMenuItems">
          <UButton
            color="neutral"
            variant="ghost"
            size="md"
            :label="user?.fullName || 'کاربر'"
            icon="i-lucide-user"
          />
        </UDropdownMenu>
      </div>

      <!-- دکمه ورود برای کاربران غیر لاگین -->
      <div v-else>
        <UButton
          color="primary"
          variant="soft"
          size="md"
          label="ورود / ثبت‌نام"
          icon="i-lucide-log-in"
          to="/login"
        />
      </div>

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
import { useCartStore } from "~/composables/stores/cart";
import { useAuth } from "~/composables/useAuth";

const cartStore = useCartStore();
const cartOpen = ref(false);

// احراز هویت
const { user, isAuthenticated, isAdmin, logout } = useAuth();

// تعداد کل آیتم‌ها (با چک امن)
const totalItems = computed(() => {
  return cartStore.items.length;
});

// منوی کاربر
const userMenuItems = computed(() => {
  const items = [
    [
      {
        label: user.value?.fullName || "کاربر",
        icon: "i-lucide-user",
        type: "label",
      },
    ],
    [
      {
        label: "پروفایل",
        icon: "i-lucide-user-circle",
        to: "/profile",
      },
      {
        label: "سفارش‌های من",
        icon: "i-lucide-shopping-bag",
        to: "/orders",
      },
      {
        label: "تنظیمات",
        icon: "i-lucide-settings",
        to: "/settings",
      },
    ],
  ];

  // اگر ادمین است، منوی پنل ادمین اضافه شود
  if (isAdmin.value) {
    items.push([
      {
        label: "پنل مدیریت",
        icon: "i-lucide-shield",
        to: "/admin",
        color: "primary",
      },
    ]);
  }

  // دکمه خروج
  items.push([
    {
      label: "خروج از حساب",
      icon: "i-lucide-log-out",
      color: "error",
      onSelect: () => {
        logout();
      },
    },
  ]);

  return items;
});

// منوی اصلی
const navItems = [
  { label: "تخفیف‌ها", to: "/category/discounts" },
  { label: "عطر مردانه", to: "/category/male" },
  { label: "عطر زنانه", to: "/category/female" },
  { label: "فروشگاه", to: "/products" },
];
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
