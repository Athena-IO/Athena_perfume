<template>
  <UHeader>
    <!-- Logo -->
    <template #title>
      <NuxtLink to="/" class="font-black text-xl flex items-center gap-3">
        <UIcon name="i-lucide-droplet" class="w-7 h-7 text-primary" />
        Athena Perfume
      </NuxtLink>
    </template>

    <!-- Main nav - desktop -->
    <UNavigationMenu :items="navItems" class="hidden lg:flex" />

    <!-- Right side: search + theme + user + cart - desktop -->
    <template #right>
      <!-- Search button + popover (desktop) -->
      <div class="hidden lg:flex items-center gap-2">
        <UPopover 
          v-model:open="searchOpen" 
          :content="{ 
            align: 'end',
            side: 'bottom',
            sideOffset: 12
          }"
          :ui="{
            content: 'w-screen max-w-3xl'
          }"
        >
          <UButton
            icon="i-lucide-search"
            color="neutral"
            variant="ghost"
          />

          <template #content>
            <div class="p-4">
              <div class="flex items-center gap-2 mb-3">
                <UInput
                  v-model="search"
                  icon="i-lucide-search"
                  placeholder="Search perfumes..."
                  class="flex-1"
                  autofocus
                />
                <UButton
                  icon="i-lucide-x"
                  color="neutral"
                  variant="ghost"
                  @click="closeSearch"
                />
              </div>

              <div v-if="searchPending" class="text-sm text-muted">
                Searching...
              </div>
              <div v-else-if="searchError" class="flex flex-col items-center justify-center py-8 text-center">
                <UIcon name="i-lucide-search-x" class="w-12 h-12 text-muted mb-3" />
                <p class="text-sm font-medium text-muted">نتیجه‌ای یافت نشد</p>
                <p class="text-xs text-muted mt-1">لطفاً عبارت دیگری را جستجو کنید</p>
              </div>
              <div v-else>
                <div
                  v-if="!searchResults.length && search.length > 2"
                  class="flex flex-col items-center justify-center py-8 text-center"
                >
                  <UIcon name="i-lucide-search-x" class="w-12 h-12 text-muted mb-3" />
                  <p class="text-sm font-medium text-muted">نتیجه‌ای یافت نشد</p>
                  <p class="text-xs text-muted mt-1">لطفاً عبارت دیگری را جستجو کنید</p>
                </div>

                <div v-else class="space-y-1 max-h-96 overflow-auto">
                  <NuxtLink
                    v-for="item in searchResults"
                    :key="item.id"
                    :to="`/products/${item.slug}`"
                    class="flex items-center justify-between px-3 py-2 text-sm rounded-md hover:bg-muted transition-colors"
                    @click="closeSearch"
                  >
                    <span>{{ item.title }}</span>
                    <UIcon
                      name="i-lucide-arrow-right"
                      class="w-4 h-4 text-muted"
                    />
                  </NuxtLink>
                </div>
              </div>
            </div>
          </template>
        </UPopover>
      </div>

      <!-- Theme button - desktop -->
      <UColorModeButton class="hidden lg:flex" />

      <!-- User auth - desktop -->
      <div v-if="authStore.isAuthenticated" class="hidden lg:block">
        <UDropdownMenu :items="userMenuItems">
          <UButton
            color="neutral"
            variant="ghost"
            size="md"
            :label="authStore.userInfo && authStore.userInfo.fullName ? authStore.userInfo.fullName : 'کاربر'"
            icon="i-lucide-user"
          />
        </UDropdownMenu>
      </div>

      <!-- Login button - desktop -->
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

      <!-- Cart button - desktop -->
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

    <!-- Mobile body -->
    <template #body>
      <!-- Search in mobile -->
      <div class="px-2.5 mb-3">
        <UPopover 
          v-model:open="searchOpen"
          :content="{
            side: 'bottom',
            align: 'start',
            sideOffset: 8
          }"
          :ui="{
            content: 'w-[calc(100vw-2rem)]'
          }"
        >
          <UButton
            block
            color="neutral"
            variant="outline"
            icon="i-lucide-search"
          >
            Search
          </UButton>

          <template #content>
            <div class="p-3 max-h-80 overflow-auto">
              <div class="flex items-center gap-2 mb-3">
                <UInput
                  v-model="search"
                  icon="i-lucide-search"
                  placeholder="Search perfumes..."
                  class="flex-1"
                  autofocus
                />
                <UButton
                  icon="i-lucide-x"
                  color="neutral"
                  variant="ghost"
                  @click="closeSearch"
                />
              </div>

              <div v-if="searchPending" class="text-sm text-muted">
                Searching...
              </div>
              <div v-else-if="searchError" class="flex flex-col items-center justify-center py-6 text-center">
                <UIcon name="i-lucide-search-x" class="w-10 h-10 text-muted mb-2" />
                <p class="text-sm font-medium text-muted">نتیجه‌ای یافت نشد</p>
                <p class="text-xs text-muted mt-1">لطفاً عبارت دیگری را جستجو کنید</p>
              </div>
              <div v-else>
                <div
                  v-if="!searchResults.length && search.length > 2"
                  class="flex flex-col items-center justify-center py-6 text-center"
                >
                  <UIcon name="i-lucide-search-x" class="w-10 h-10 text-muted mb-2" />
                  <p class="text-sm font-medium text-muted">نتیجه‌ای یافت نشد</p>
                  <p class="text-xs text-muted mt-1">لطفاً عبارت دیگری را جستجو کنید</p>
                </div>

                <div v-else class="space-y-1 max-h-60 overflow-auto">
                  <NuxtLink
                    v-for="item in searchResults"
                    :key="item.id"
                    :to="`/products/${item.slug}`"
                    class="flex items-center justify-between px-3 py-2 text-sm rounded-md hover:bg-muted transition-colors"
                    @click="closeSearch"
                  >
                    <span>{{ item.title }}</span>
                    <UIcon
                      name="i-lucide-arrow-right"
                      class="w-4 h-4 text-muted"
                    />
                  </NuxtLink>
                </div>
              </div>
            </div>
          </template>
        </UPopover>
      </div>

      <!-- Main nav - mobile -->
      <UNavigationMenu
        :items="navItems"
        orientation="vertical"
        class="-mx-2.5 mb-4"
      />

      <UDivider class="my-4" />

      <!-- User in mobile -->
      <div v-if="authStore.isAuthenticated" class="space-y-2">
        <div class="px-2.5 py-2 text-sm font-medium text-muted">
          {{ authStore.userInfo && authStore.userInfo.fullName ? authStore.userInfo.fullName : "کاربر" }}
        </div>
        <UNavigationMenu
          :items="mobileUserMenuItems"
          orientation="vertical"
          class="-mx-2.5"
        />
      </div>

      <!-- Login in mobile -->
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

      <UDivider class="my-4" />

      <!-- Cart in mobile -->
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

  <!-- Cart drawer -->
  <CartSlideover v-model:open="cartOpen" />
</template>


<script setup>
import { useCartStore } from "~/composables/stores/cart";
import { useAuthStore } from "~/stores/auth";
import { useSearch } from "~/composables/useSearch";

const cartStore = useCartStore();
const cartOpen = ref(false);

// Auth
const authStore = useAuthStore();

// Cart count
const totalItems = computed(() => cartStore.items.length);

// Search state
const searchOpen = ref(false);
const search = ref("");

// Composable using useFetch with reactive query and watch.[useFetch watch](https://stackoverflow.com/questions/78633662)
const {
  results: searchResults,
  pending: searchPending,
  error: searchError,
} = useSearch(search);

const closeSearch = () => {
  searchOpen.value = false;
  search.value = "";
};

// User menu (desktop)
const userMenuItems = computed(() => {
  const items = [
    [
      {
        label: authStore.userInfo && authStore.userInfo.fullName
          ? authStore.userInfo.fullName
          : "کاربر",
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

  if (authStore.isAdmin) {
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
        authStore.logout();
      },
    },
  ]);

  return items;
});

// User menu (mobile)
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

  if (authStore.isAdmin) {
    items.push({
      label: "پنل مدیریت",
      icon: "i-lucide-shield",
      to: "/admin",
    });
  }

  items.push({
    label: "خروج از حساب",
    icon: "i-lucide-log-out",
    click: () => authStore.logout(),
  });

  return items;
});

// Main nav
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
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>