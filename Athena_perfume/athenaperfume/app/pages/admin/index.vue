<!-- pages/admin/index.vue -->
<template>
  <div class="p-6" dir="rtl">
    <h1 class="text-2xl font-bold mb-6" style="color: #1a0a0c">داشبورد</h1>

    <!-- Stats Cards with Comparison -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
      <!-- Revenue Card -->
      <UCard class="custom-card-bg">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UIcon
                name="i-lucide-trending-up"
                class="size-5"
                style="color: #1a0a0c"
              />
              <span style="color: #1a0a0c">درآمد</span>
            </div>
            <UBadge
              :color="revenueChange >= 0 ? 'success' : 'error'"
              variant="subtle"
            >
              <UIcon
                :name="
                  revenueChange >= 0
                    ? 'i-lucide-arrow-up'
                    : 'i-lucide-arrow-down'
                "
                class="size-3 ml-1"
              />
              {{ Math.abs(revenueChange) }}%
            </UBadge>
          </div>
        </template>
        <div>
          <p class="text-3xl font-bold" style="color: #1a0a0c">
            {{ formatCurrency(currentRevenue) }}
          </p>
          <p class="text-sm mt-1" style="color: #1a0a0c">
            مقایسه با ماه قبل: {{ formatCurrency(previousRevenue) }}
          </p>
        </div>
      </UCard>

      <!-- Orders Card -->
      <UCard class="custom-card-bg">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UIcon
                name="i-lucide-shopping-cart"
                class="size-5"
                style="color: #1a0a0c"
              />
              <span style="color: #1a0a0c">سفارشات</span>
            </div>
            <UBadge
              :color="ordersChange >= 0 ? 'success' : 'error'"
              variant="subtle"
            >
              <UIcon
                :name="
                  ordersChange >= 0
                    ? 'i-lucide-arrow-up'
                    : 'i-lucide-arrow-down'
                "
                class="size-3 ml-1"
              />
              {{ Math.abs(ordersChange) }}%
            </UBadge>
          </div>
        </template>
        <div>
          <p class="text-3xl font-bold" style="color: #1a0a0c">
            {{ currentOrders }}
          </p>
          <p class="text-sm mt-1" style="color: #1a0a0c">
            مقایسه با ماه قبل: {{ previousOrders }}
          </p>
        </div>
      </UCard>

      <!-- Users Card -->
      <UCard class="custom-card-bg">
        <template #header>
          <div class="flex items-center justify-between">
            <div class="flex items-center gap-2">
              <UIcon
                name="i-lucide-users"
                class="size-5"
                style="color: #1a0a0c"
              />
              <span style="color: #1a0a0c">کاربران</span>
            </div>
            <UBadge
              :color="usersChange >= 0 ? 'success' : 'error'"
              variant="subtle"
            >
              <UIcon
                :name="
                  usersChange >= 0 ? 'i-lucide-arrow-up' : 'i-lucide-arrow-down'
                "
                class="size-3 ml-1"
              />
              {{ Math.abs(usersChange) }}%
            </UBadge>
          </div>
        </template>
        <div>
          <p class="text-3xl font-bold" style="color: #1a0a0c">
            {{ currentUsers.toLocaleString("fa-IR") }}
          </p>
          <p class="text-sm mt-1" style="color: #1a0a0c">
            مقایسه با ماه قبل: {{ previousUsers.toLocaleString("fa-IR") }}
          </p>
        </div>
      </UCard>
    </div>

    <!-- Top Perfumes and Monthly Revenue Side by Side -->
    <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-6">
      <!-- Top Perfumes Section -->
      <UCard class="custom-card-bg">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon
              name="i-lucide-flame"
              class="size-5"
              style="color: #1a0a0c"
            />
            <span class="font-semibold" style="color: #1a0a0c"
              >پرفروش‌ترین عطرها</span
            >
          </div>
        </template>

        <div class="space-y-4">
          <div
            v-for="(perfume, index) in topPerfumes"
            :key="perfume.id"
            class="flex items-center justify-between p-3 rounded-lg hover:opacity-90 transition-colors custom-item-bg"
          >
            <div class="flex items-center gap-3">
              <div
                class="flex items-center justify-center w-8 h-8 rounded-full font-bold"
                style="background-color: #3b0510; color: white"
              >
                {{ index + 1 }}
              </div>
              <div>
                <p class="font-medium" style="color: #1a0a0c">
                  {{ perfume.name }}
                </p>
                <p class="text-sm" style="color: #1a0a0c">
                  {{ perfume.brand }}
                </p>
              </div>
            </div>
            <div class="text-left">
              <p class="font-semibold" style="color: #1a0a0c">
                {{ perfume.soldCount }} فروش
              </p>
              <p class="text-sm" style="color: #1a0a0c">
                {{ formatCurrency(perfume.revenue) }}
              </p>
            </div>
          </div>
        </div>
      </UCard>

      <!-- Monthly Revenue Chart -->
      <UCard class="custom-card-bg">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon
              name="i-lucide-bar-chart-3"
              class="size-5"
              style="color: #1a0a0c"
            />
            <span class="font-semibold" style="color: #1a0a0c"
              >درآمد ماهانه</span
            >
          </div>
        </template>

        <div class="h-64 flex items-end justify-between gap-2 p-4">
          <div
            v-for="month in monthlyRevenue"
            :key="month.month"
            class="flex-1 flex flex-col items-center gap-2"
          >
            <div class="w-full rounded-t-lg relative group custom-chart-bg">
              <div
                class="w-full rounded-t-lg transition-all duration-300 hover:opacity-80"
                :style="{
                  height: `${(month.amount / maxRevenue) * 200}px`,
                  backgroundColor: '#3B0510',
                }"
              >
                <div
                  class="absolute -top-8 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity px-2 py-1 rounded text-xs whitespace-nowrap"
                  style="background-color: #3b0510; color: white"
                >
                  {{ formatCurrency(month.amount) }}
                </div>
              </div>
            </div>
            <span class="text-xs" style="color: #1a0a0c">{{
              month.month
            }}</span>
          </div>
        </div>
      </UCard>
    </div>

    <!-- Latest Sold Products -->
    <UCard class="custom-card-bg">
      <template #header>
        <div class="flex items-center gap-2">
          <UIcon name="i-lucide-clock" class="size-5" style="color: #1a0a0c" />
          <span class="font-semibold" style="color: #1a0a0c"
            >آخرین محصولات فروخته شده</span
          >
        </div>
      </template>

      <UTable
        :data="latestSoldProducts"
        :columns="columns"
        class="min-h-[300px]"
      />
    </UCard>
  </div>
</template>

<script setup lang="ts">
import { h } from "vue";
import type { TableColumn } from "@nuxt/ui";

definePageMeta({
  layout: "admin",
});

// Mock data - Replace with your API calls
const currentRevenue = ref(125000000);
const previousRevenue = ref(98000000);
const currentOrders = ref(128);
const previousOrders = ref(95);
const currentUsers = ref(2341);
const previousUsers = ref(2150);

// Calculate percentage changes
const revenueChange = computed(() =>
  Math.round(
    ((currentRevenue.value - previousRevenue.value) / previousRevenue.value) *
      100
  )
);
const ordersChange = computed(() =>
  Math.round(
    ((currentOrders.value - previousOrders.value) / previousOrders.value) * 100
  )
);
const usersChange = computed(() =>
  Math.round(
    ((currentUsers.value - previousUsers.value) / previousUsers.value) * 100
  )
);

// Top perfumes data
const topPerfumes = ref([
  {
    id: 1,
    name: "عود شرقی",
    brand: "العربیه",
    soldCount: 145,
    revenue: 25000000,
  },
  { id: 2, name: "گل رز", brand: "پاریس", soldCount: 132, revenue: 22000000 },
  { id: 3, name: "وانیل", brand: "فرانسه", soldCount: 98, revenue: 18000000 },
  { id: 4, name: "چوب صندل", brand: "هند", soldCount: 87, revenue: 15000000 },
  { id: 5, name: "مشک", brand: "عربستان", soldCount: 76, revenue: 13000000 },
]);

// Monthly revenue data
const monthlyRevenue = ref([
  { month: "فروردین", amount: 85000000 },
  { month: "اردیبهشت", amount: 92000000 },
  { month: "خرداد", amount: 78000000 },
  { month: "تیر", amount: 105000000 },
  { month: "مرداد", amount: 98000000 },
  { month: "شهریور", amount: 125000000 },
]);

const maxRevenue = computed(() =>
  Math.max(...monthlyRevenue.value.map((m) => m.amount))
);

// Latest sold products
interface SoldProduct {
  id: string;
  productName: string;
  customerName: string;
  date: string;
  quantity: number;
  price: number;
  status: "completed" | "pending" | "cancelled";
}

const latestSoldProducts = ref<SoldProduct[]>([
  {
    id: "1001",
    productName: "عود شرقی",
    customerName: "علی احمدی",
    date: new Date().toISOString(),
    quantity: 2,
    price: 3500000,
    status: "completed",
  },
  {
    id: "1002",
    productName: "گل رز",
    customerName: "فاطمه محمدی",
    date: new Date(Date.now() - 3600000).toISOString(),
    quantity: 1,
    price: 2800000,
    status: "completed",
  },
  {
    id: "1003",
    productName: "وانیل",
    customerName: "حسن رضایی",
    date: new Date(Date.now() - 7200000).toISOString(),
    quantity: 3,
    price: 5400000,
    status: "pending",
  },
  {
    id: "1004",
    productName: "چوب صندل",
    customerName: "مریم کریمی",
    date: new Date(Date.now() - 10800000).toISOString(),
    quantity: 1,
    price: 3200000,
    status: "completed",
  },
  {
    id: "1005",
    productName: "مشک",
    customerName: "رضا نوری",
    date: new Date(Date.now() - 14400000).toISOString(),
    quantity: 2,
    price: 4600000,
    status: "cancelled",
  },
]);

// Table columns
const UBadge = resolveComponent("UBadge");

const columns: TableColumn<SoldProduct>[] = [
  {
    accessorKey: "id",
    header: "شماره سفارش",
    cell: ({ row }) => `#${row.getValue("id")}`,
  },
  {
    accessorKey: "productName",
    header: "نام محصول",
  },
  {
    accessorKey: "customerName",
    header: "نام مشتری",
  },
  {
    accessorKey: "date",
    header: "تاریخ",
    cell: ({ row }) => {
      return new Date(row.getValue("date")).toLocaleString("fa-IR", {
        day: "numeric",
        month: "short",
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },
  {
    accessorKey: "quantity",
    header: "تعداد",
    cell: ({ row }) => `${row.getValue("quantity")} عدد`,
  },
  {
    accessorKey: "price",
    header: "قیمت",
    cell: ({ row }) => formatCurrency(row.getValue("price") as number),
  },
  {
    accessorKey: "status",
    header: "وضعیت",
    cell: ({ row }) => {
      const status = row.getValue("status") as string;
      const statusConfig = {
        completed: { label: "تکمیل شده", color: "success" as const },
        pending: { label: "در انتظار", color: "warning" as const },
        cancelled: { label: "لغو شده", color: "error" as const },
      };

      const config = statusConfig[status as keyof typeof statusConfig];
      return h(
        UBadge,
        {
          color: config.color,
          variant: "subtle",
        },
        () => config.label
      );
    },
  },
];

// Helper function to format currency
function formatCurrency(amount: number): string {
  return new Intl.NumberFormat("fa-IR", {
    style: "currency",
    currency: "IRR",
    maximumFractionDigits: 0,
  }).format(amount);
}

// TODO: Replace with actual API calls
// Example:
// const { data: stats } = await useFetch('/api/admin/stats')
// const { data: topPerfumes } = await useFetch('/api/admin/top-perfumes')
// const { data: monthlyRevenue } = await useFetch('/api/admin/monthly-revenue')
// const { data: latestSoldProducts } = await useFetch('/api/admin/latest-sales')
</script>

<style scoped>
.custom-card-bg {
  background-color: #d8cfc4;
}

.custom-item-bg {
  background-color: #e6ded3;
}

.custom-chart-bg {
  background-color: #e6ded3;
}
</style>
