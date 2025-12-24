<!-- layouts/admin.vue -->
<template>
  <UDashboardGroup>
    <UDashboardSidebar collapsible resizable>
      <!-- Header with account info -->
      <template #header="{ collapsed }">
        <div v-if="!collapsed" class="flex items-center gap-3">
          <UAvatar src="https://github.com/benjamincanac.png" size="sm" />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate">Admin Name</p>
            <p class="text-xs text-muted truncate">admin@example.com</p>
          </div>
        </div>
        <UAvatar v-else src="https://github.com/benjamincanac.png" size="sm" />
      </template>

      <!-- Navigation Menu -->
      <template #default="{ collapsed }">
        <UNavigationMenu
          :collapsed="collapsed"
          :items="menuItems"
          orientation="vertical"
          highlight
          color="primary"
        />
      </template>

      <!-- Footer with dark mode toggle and logout -->
      <template #footer="{ collapsed }">
        <div class="space-y-2">
          <!-- Dark Mode Toggle -->
          <UColorModeButton
            :label="collapsed ? undefined : 'تغییر تم'"
            variant="ghost"
            block
          />

          <!-- Logout Button -->
          <UButton
            icon="i-lucide-log-out"
            :label="collapsed ? undefined : 'خروج'"
            color="error"
            variant="ghost"
            block
            @click="handleLogout"
          />
        </div>
      </template>
    </UDashboardSidebar>

    <!-- Main content area -->
    <UDashboardPanel grow>
      <template #header>
        <UDashboardNavbar :title="pageTitle">
          <!-- Add color mode button in navbar as well -->
          <template #right>
            <UColorModeButton />
          </template>
        </UDashboardNavbar>
      </template>

      <!-- Add a scrollable wrapper -->
      <div class="h-full overflow-y-auto">
        <slot />
      </div>
    </UDashboardPanel>
  </UDashboardGroup>
</template>

<script setup>
const route = useRoute();

// Page title based on current route
const pageTitle = computed(() => {
  const titles = {
    "/admin": "داشبورد",
    "/admin/products": "مدیریت محصولات",
    "/admin/products/add": "افزودن محصول",
    "/admin/orders": "سفارشات",
    "/admin/users": "کاربران",
    "/admin/settings": "تنظیمات",
  };
  return titles[route.path] || "پنل مدیریت";
});

// Menu items with routes
const menuItems = computed(() => [
  [
    {
      label: "داشبورد",
      icon: "i-lucide-layout-dashboard",
      to: "/admin",
      active: route.path === "/admin",
    },
    {
      label: "محصولات",
      icon: "i-lucide-package",
      badge: "45",
      defaultOpen: route.path.startsWith("/admin/products"),
      children: [
        {
          label: "همه محصولات",
          description: "مشاهده و مدیریت محصولات",
          icon: "i-lucide-list",
          to: "/admin/products",
        },
        {
          label: "افزودن محصول",
          description: "افزودن محصول جدید",
          icon: "i-lucide-plus-circle",
          to: "/admin/products/add",
        },
      ],
    },
    {
      label: "سفارشات",
      icon: "i-lucide-shopping-cart",
      to: "/admin/orders",
      badge: {
        label: "12",
        color: "error",
      },
      active: route.path === "/admin/orders",
    },
    {
      label: "کاربران",
      icon: "i-lucide-users",
      to: "/admin/users",
      active: route.path === "/admin/users",
    },
  ],
  [
    {
      label: "تنظیمات",
      icon: "i-lucide-settings",
      to: "/admin/settings",
      active: route.path === "/admin/settings",
    },
    {
      label: "راهنما",
      icon: "i-lucide-help-circle",
      to: "https://docs.example.com",
      target: "_blank",
    },
  ],
]);

const handleLogout = () => {
  // Add your logout logic here
  navigateTo("/login");
};
</script>
