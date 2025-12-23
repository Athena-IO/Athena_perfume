<!-- pages/admin/index.vue -->
<template>
  <div class="p-6">
    <h1 class="text-2xl font-bold mb-6">داشبورد</h1>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-package" class="size-5" />
            <span>محصولات</span>
          </div>
        </template>
        <p class="text-3xl font-bold">45</p>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-shopping-cart" class="size-5" />
            <span>سفارشات</span>
          </div>
        </template>
        <p class="text-3xl font-bold">128</p>
      </UCard>

      <UCard>
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon name="i-lucide-users" class="size-5" />
            <span>کاربران</span>
          </div>
        </template>
        <p class="text-3xl font-bold">2,341</p>
      </UCard>
    </div>
  </div>
</template>
