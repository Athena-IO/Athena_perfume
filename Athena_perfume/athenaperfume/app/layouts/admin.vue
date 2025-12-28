<template>
  <UDashboardGroup :ui="groupUI">
    <UDashboardSidebar collapsible resizable :ui="sidebarUI">
      <!-- Your sidebar content remains the same -->
      <template #header="{ collapsed }">
        <div v-if="!collapsed" class="flex items-center gap-3 p-3">
          <UAvatar src="https://github.com/benjamincanac.png" size="sm" />
          <div class="flex-1 min-w-0">
            <p class="text-sm font-medium truncate" style="color: #1a0a0c">
              نام ادمین
            </p>
            <p class="text-xs truncate" style="color: #1a0a0c">
              admin@example.com
            </p>
          </div>
        </div>
        <UAvatar v-else src="https://github.com/benjamincanac.png" size="sm" />
      </template>

      <template #default="{ collapsed }">
        <UNavigationMenu
          :collapsed="collapsed"
          :items="menuItems"
          orientation="vertical"
          highlight
          :ui="navigationUI"
        />
      </template>

      <template #footer="{ collapsed }">
        <div class="space-y-2 p-3">
          <UColorModeButton
            :label="collapsed ? undefined : 'تغییر تم'"
            variant="ghost"
            block
          />
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

    <UDashboardPanel grow :ui="panelUI">
      <template #header>
        <UDashboardNavbar :title="pageTitle" :ui="navbarUI">
          <template #right>
            <UColorModeButton />
          </template>
        </UDashboardNavbar>
      </template>

      <div class="h-full overflow-y-auto custom-scrollbar bg-white">
        <slot />
      </div>
    </UDashboardPanel>
  </UDashboardGroup>
</template>

<script setup>
const route = useRoute();

// Add this UI config to reverse the flex direction
const groupUI = {
  base: "flex-row-reverse", // This will put the sidebar on the right
};

// Rest of your existing UI customizations
const sidebarUI = {
  root: "bg-[#D8CFC4] border-[#D8CFC4]",
  body: "bg-[#D8CFC4]",
  header: "bg-[#D8CFC4] border-b border-[#D8CFC4]",
  footer: "bg-[#D8CFC4] border-t border-[#D8CFC4]",
};

const navigationUI = {
  root: "bg-[#D8CFC4]",
  item: {
    base: "text-[#1A0A0C] hover:bg-[#3B0510]/10",
    active: "bg-[#3B0510]/10 text-[#3B0510]",
    inactive: "text-[#1A0A0C]",
  },
};

const navbarUI = {
  root: "bg-[#D8CFC4] border-b border-[#D8CFC4]",
  title: "text-[#1A0A0C]",
};

const panelUI = {
  root: "bg-white",
  body: "bg-white",
};

// Your existing computed properties and functions...
const pageTitle = computed(() => {
  const titles = {
    "/admin": "داشبورد",
    "/admin/perfumes": "مدیریت عطرها",
    "/admin/perfumes/add": "افزودن عطر",
    "/admin/orders": "سفارشات",
    "/admin/users": "کاربران",
    "/admin/settings": "تنظیمات",
  };
  return titles[route.path] || "پنل مدیریت";
});

const menuItems = computed(() => [
  [
    {
      label: "داشبورد",
      icon: "i-lucide-layout-dashboard",
      to: "/admin",
      active: route.path === "/admin",
    },
    {
      label: "عطرها",
      icon: "i-lucide-sparkles",
      badge: "45",
      defaultOpen: route.path.startsWith("/admin/perfumes"),
      children: [
        {
          label: "همه عطرها",
          description: "مشاهده و مدیریت عطرها",
          icon: "i-lucide-list",
          to: "/admin/perfumes",
        },
        {
          label: "افزودن عطر",
          description: "افزودن عطر جدید",
          icon: "i-lucide-plus-circle",
          to: "/admin/perfumes/add",
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
  navigateTo("/login");
};
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #f5f5f5;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #d8cfc4;
  border-radius: 4px;
}

.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #3b0510;
}
</style>
