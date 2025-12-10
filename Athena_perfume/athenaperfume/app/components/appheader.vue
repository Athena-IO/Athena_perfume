<template>
  <UHeader>
    <!-- لوگو -->
    <template #title>
      <NuxtLink to="/" class="font-black text-xl flex items-center gap-3">
        <UIcon name="i-lucide-droplet" class="w-7 h-7 text-primary" />
        Athena Perfume
      </NuxtLink>
    </template>

    <!-- منوی اصلی - فقط در دسکتاپ -->
    <UNavigationMenu :items="navItems" class="hidden lg:flex" />

    <!-- سمت راست: تم + کاربر + سبد خرید - فقط دسکتاپ -->
    <template #right>
      <!-- دکمه تم - فقط در دسکتاپ -->
      <UColorModeButton class="hidden lg:flex" />

      <!-- بخش احراز هویت کاربر - فقط دسکتاپ -->
      <div v-if="isAuthenticated" class="hidden lg:block">
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

      <!-- دکمه ورود برای کاربران غیر لاگین - فقط دسکتاپ -->
      <div v-else class="hidden lg:block">
        <UButton
          color="primary"
          variant="soft"
          size="md"
          label="ورود / ثبت‌نام"
          icon="i-lucide-log-in"
          to="/login"
        />
      </div>

      <!-- دکمه سبد خرید با تعداد آیتم - فقط دسکتاپ -->
      <div class="relative hidden lg:block">
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

    <!-- محتوای منوی موبایل -->
    <template #body>
      <!-- منوی اصلی به صورت عمودی -->
      <UNavigationMenu
        :items="navItems"
        orientation="vertical"
        class="-mx-2.5 mb-4"
      />

      <!-- فاصله‌انداز -->
      <UDivider class="my-4" />

      <!-- بخش کاربر در موبایل -->
      <div v-if="isAuthenticated" class="space-y-2">
        <div class="px-2.5 py-2 text-sm font-medium text-muted">
          {{ user?.fullName || "کاربر" }}
        </div>
        <UNavigationMenu
          :items="mobileUserMenuItems"
          orientation="vertical"
          class="-mx-2.5"
        />
      </div>

      <!-- دکمه ورود در موبایل برای کاربران غیر لاگین -->
      <div v-else class="px-2.5">
        <UButton
          color="primary"
          variant="soft"
          size="md"
          label="ورود / ثبت‌نام"
          icon="i-lucide-log-in"
          to="/login"
          block
        />
      </div>

      <!-- فاصله‌انداز -->
      <UDivider class="my-4" />

      <!-- دکمه سبد خرید در موبایل -->
      <div class="px-2.5">
        <UButton
          color="neutral"
          variant="outline"
          size="md"
          icon="i-lucide-shopping-cart"
          block
          @click="cartOpen = true"
        >
          <span class="flex items-center gap-2">
            <span>سبد خرید</span>
            <UBadge v-if="totalItems > 0" color="primary" size="xs">
              {{ totalItems }}
            </UBadge>
          </span>
        </UButton>
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

// منوی کاربر برای دسکتاپ (DropdownMenu)
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

// منوی کاربر برای موبایل (NavigationMenu)
const mobileUserMenuItems = computed(() => {
  const items = [
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
  ];

  if (isAdmin.value) {
    items.push({
      label: "پنل مدیریت",
      icon: "i-lucide-shield",
      to: "/admin",
    });
  }

  items.push({
    label: "خروج از حساب",
    icon: "i-lucide-log-out",
    click: () => logout(),
  });

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
