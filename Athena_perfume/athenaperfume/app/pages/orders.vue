<template>
  <div class="flex flex-col gap-6 p-6" dir="rtl">
    <!-- هدر با عنوان و آمار -->
    <div class="flex items-center justify-between">
      <div>
        <h1 class="text-2xl font-bold">مدیریت سفارشات</h1>
        <p class="text-muted">پیگیری و مدیریت سفارشات عطر</p>
      </div>
      
      <!-- کارت آمار هفتگی -->
      <UCard>
        <div class="text-center">
          <p class="text-sm text-muted">سفارشات این هفته</p>
          <p class="text-3xl font-bold text-primary">{{ weeklyOrdersCount }}</p>
        </div>
      </UCard>
    </div>

    <!-- بخش فیلترها -->
    <UCard>
      <div class="flex flex-wrap gap-4 items-end">
        <!-- جستجو بر اساس شناسه تراکنش -->
        <div class="flex-1 min-w-[250px]">
          <label class="text-sm font-medium mb-2 block">جستجو بر اساس شناسه تراکنش</label>
          <UInput
            v-model="searchTerm"
            icon="i-lucide-search"
            placeholder="جستجو بر اساس شناسه تراکنش..."
            class="w-full"
          />
        </div>

        <!-- فیلتر وضعیت ارسال -->
        <div class="min-w-[200px]">
          <label class="text-sm font-medium mb-2 block">وضعیت ارسال</label>
          <USelectMenu
            v-model="selectedStatus"
            :items="statusOptions"
            placeholder="همه وضعیت‌ها"
            icon="i-lucide-package"
          />
        </div>

        <!-- فیلتر بازه زمانی -->
        <div class="min-w-[200px]">
          <label class="text-sm font-medium mb-2 block">بازه زمانی</label>
          <USelectMenu
            v-model="selectedPeriod"
            :items="periodOptions"
            placeholder="انتخاب بازه"
            icon="i-lucide-calendar"
            class="w-full"
          />
        </div>

        <!-- دکمه پاک کردن فیلترها -->
        <UButton
          color="neutral"
          variant="outline"
          icon="i-lucide-x"
          @click="clearFilters"
        >
          پاک کردن فیلترها
        </UButton>
      </div>
    </UCard>

    <!-- جدول سفارشات -->
    <UCard>
      <UTable
        v-model:expanded="expanded"
        :data="filteredOrders"
        :columns="columns"
        :loading="loading"
        class="w-full"
      >
        <!-- ردیف گسترده شده - جزئیات سفارش -->
        <template #expanded="{ row }">
          <div class="p-4 bg-elevated/50 border-t border-default">
            <h4 class="font-semibold mb-3">اقلام سفارش:</h4>
            <div class="space-y-2">
              <div
                v-for="item in row.original.items"
                :key="item.id"
                class="flex items-center justify-between p-3 bg-default rounded-md"
              >
                <div class="flex items-center gap-3">
                  <UIcon name="i-lucide-package" class="text-primary" />
                  <div>
                    <p class="font-medium">{{ item.name }}</p>
                    <p class="text-sm text-muted">{{ item.size }}</p>
                  </div>
                </div>
                <div class="text-left">
                  <p class="font-medium">تعداد: {{ item.quantity }}</p>
                  <p class="text-sm text-muted">{{ formatPrice(item.price) }} تومان</p>
                </div>
              </div>
            </div>
          </div>
        </template>
      </UTable>
    </UCard>

    <!-- مدال جزئیات کامل سفارش -->
    <OrderDetailsModal
      v-model:open="isModalOpen"
      :order="selectedOrder"
      @update-status="handleUpdateStatus"
    />
  </div>
</template>

<script setup>
import { h, ref, computed, resolveComponent } from 'vue'

const UBadge = resolveComponent('UBadge')
const UButton = resolveComponent('UButton')
const UIcon = resolveComponent('UIcon')

// وضعیت‌ها
const searchTerm = ref('')
const selectedStatus = ref(null)
const selectedPeriod = ref({ label: 'همه زمان‌ها', value: 'all' })
const expanded = ref({})
const loading = ref(false)
const isModalOpen = ref(false)
const selectedOrder = ref(null)

// گزینه‌های فیلتر
const statusOptions = [
  { label: 'همه وضعیت‌ها', value: null, icon: 'i-lucide-list' },
  { label: 'ارسال نشده', value: 'not_sent', icon: 'i-lucide-circle-x' },
  { label: 'در راه', value: 'on_the_way', icon: 'i-lucide-truck' },
  { label: 'ارسال شده', value: 'sent', icon: 'i-lucide-circle-check' }
]

const periodOptions = [
  { label: 'همه زمان‌ها', value: 'all' },
  { label: 'امروز', value: 'today' },
  { label: 'این هفته', value: 'week' },
  { label: 'این ماه', value: 'month' },
  { label: '۷ روز گذشته', value: '7days' },
  { label: '۳۰ روز گذشته', value: '30days' }
]

// داده‌های نمونه
const orders = ref([
  {
    id: '1',
    transactionId: 'TXN001',
    customerName: 'علی احمدی',
    email: 'ali@example.com',
    phone: '۰۹۱۲۳۴۵۶۷۸۹',
    address: 'تهران، خیابان ولیعصر، پلاک ۱۲۳',
    postalCode: '۱۴۳۵۶۷۸۹۰۱',
    city: 'تهران',
    province: 'تهران',
    date: new Date().toISOString(),
    deliveryStatus: 'sent',
    paymentMethod: 'آنلاین',
    paymentStatus: 'پرداخت شده',
    notes: 'لطفا قبل از ساعت ۵ عصر تحویل دهید',
    items: [
      { id: '1', name: 'شانل شماره ۵', size: '۵۰ میلی‌لیتر', quantity: 2, price: 1200000 },
      { id: '2', name: 'دیور ساواژ', size: '۱۰۰ میلی‌لیتر', quantity: 1, price: 1500000 }
    ],
    totalValue: 3900000
  },
  {
    id: '2',
    transactionId: 'TXN002',
    customerName: 'سارا محمدی',
    email: 'sara@example.com',
    phone: '۰۹۱۲۳۴۵۶۷۸۸',
    address: 'تهران، خیابان انقلاب، کوچه شهید رستگار، پلاک ۴۵',
    postalCode: '۱۴۳۵۶۷۸۹۰۲',
    city: 'تهران',
    province: 'تهران',
    date: new Date(Date.now() - 86400000).toISOString(),
    deliveryStatus: 'on_the_way',
    paymentMethod: 'کارت به کارت',
    paymentStatus: 'پرداخت شده',
    notes: '',
    items: [
      { id: '3', name: 'تام فورد بلک ارکید', size: '۵۰ میلی‌لیتر', quantity: 1, price: 1800000 }
    ],
    totalValue: 1800000
  },
  {
    id: '3',
    transactionId: 'TXN003',
    customerName: 'رضا کریمی',
    email: 'reza@example.com',
    phone: '۰۹۱۲۳۴۵۶۷۸۷',
    address: 'اصفهان، خیابان چهارباغ، کوچه باغ گلدسته، پلاک ۷۸',
    postalCode: '۸۱۴۵۶۷۸۹۰۱',
    city: 'اصفهان',
    province: 'اصفهان',
    date: new Date(Date.now() - 172800000).toISOString(),
    deliveryStatus: 'not_sent',
    paymentMethod: 'در محل',
    paymentStatus: 'پرداخت نشده',
    notes: 'زنگ درب خراب است، لطفا تماس بگیرید',
    items: [
      { id: '4', name: 'گوچی بلوم', size: '۵۰ میلی‌لیتر', quantity: 3, price: 1100000 },
      { id: '5', name: 'ورساچه اروس', size: '۱۰۰ میلی‌لیتر', quantity: 1, price: 950000 }
    ],
    totalValue: 4250000
  },
  {
    id: '4',
    transactionId: 'TXN004',
    customerName: 'مریم حسینی',
    email: 'maryam@example.com',
    phone: '۰۹۱۲۳۴۵۶۷۸۶',
    address: 'شیراز، بلوار زند، خیابان فلسطین، پلاک ۲۳۴',
    postalCode: '۷۱۴۵۶۷۸۹۰۱',
    city: 'شیراز',
    province: 'فارس',
    date: new Date(Date.now() - 259200000).toISOString(),
    deliveryStatus: 'sent',
    paymentMethod: 'آنلاین',
    paymentStatus: 'پرداخت شده',
    notes: '',
    items: [
      { id: '6', name: 'ایو سن لوران بلک اوپیوم', size: '۹۰ میلی‌لیتر', quantity: 1, price: 1300000 }
    ],
    totalValue: 1300000
  },
  {
    id: '5',
    transactionId: 'TXN005',
    customerName: 'حسین رضایی',
    email: 'hossein@example.com',
    phone: '۰۹۱۲۳۴۵۶۷۸۵',
    address: 'مشهد، بلوار وکیل آباد، کوچه شهید بهشتی، پلاک ۱۵۶',
    postalCode: '۹۱۴۵۶۷۸۹۰۱',
    city: 'مشهد',
    province: 'خراسان رضوی',
    date: new Date(Date.now() - 432000000).toISOString(),
    deliveryStatus: 'on_the_way',
    paymentMethod: 'کارت به کارت',
    paymentStatus: 'پرداخت شده',
    notes: '',
    items: [
      { id: '7', name: 'باربری بریت', size: '۱۰۰ میلی‌لیتر', quantity: 2, price: 850000 }
    ],
    totalValue: 1700000
  },
  {
    id: '6',
    transactionId: 'TXN006',
    customerName: 'نازنین امیری',
    email: 'nazanin@example.com',
    phone: '۰۹۱۲۳۴۵۶۷۸۴',
    address: 'تبریز، خیابان آزادی، کوچه گلستان، پلاک ۸۹',
    postalCode: '۵۱۴۵۶۷۸۹۰۱',
    city: 'تبریز',
    province: 'آذربایجان شرقی',
    date: new Date(Date.now() - 604800000).toISOString(),
    deliveryStatus: 'not_sent',
    paymentMethod: 'آنلاین',
    paymentStatus: 'پرداخت شده',
    notes: 'کادو پیچ بشه لطفا',
    items: [
      { id: '8', name: 'پرادا کندی', size: '۵۰ میلی‌لیتر', quantity: 1, price: 950000 },
      { id: '9', name: 'مارک جیکوبز دیزی', size: '۱۰۰ میلی‌لیتر', quantity: 2, price: 1050000 }
    ],
    totalValue: 3050000
  }
])

// توابع کمکی
function formatPrice(price) {
  return price.toLocaleString('fa-IR')
}

function formatDate(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString('fa-IR', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

function openOrderDetails(order) {
  selectedOrder.value = order
  isModalOpen.value = true
}

// ستون‌های جدول
const columns = [
  {
    id: 'expand',
    header: '',
    cell: ({ row }) => h(UButton, {
      'color': 'neutral',
      'variant': 'ghost',
      'icon': 'i-lucide-chevron-down',
      'square': true,
      'aria-label': 'گسترش',
      'ui': {
        leadingIcon: ['transition-transform', row.getIsExpanded() ? 'duration-200 rotate-180' : '']
      },
      'onClick': () => row.toggleExpanded()
    })
  },
  {
    accessorKey: 'transactionId',
    header: 'شناسه تراکنش',
    cell: ({ row }) => h('div', { class: 'font-mono font-medium' }, row.getValue('transactionId'))
  },
  {
    accessorKey: 'customerName',
    header: 'نام مشتری',
    cell: ({ row }) => row.getValue('customerName')
  },
  {
    accessorKey: 'date',
    header: 'تاریخ سفارش',
    cell: ({ row }) => formatDate(row.getValue('date'))
  },
  {
    accessorKey: 'deliveryStatus',
    header: 'وضعیت ارسال',
    cell: ({ row }) => {
      const status = row.getValue('deliveryStatus')
      const statusConfig = {
        not_sent: { color: 'error', label: 'ارسال نشده' },
        on_the_way: { color: 'warning', label: 'در راه' },
        sent: { color: 'success', label: 'ارسال شده' }
      }
      
      const config = statusConfig[status]
      
      return h(UBadge, {
        color: config.color,
        variant: 'subtle'
      }, () => config.label)
    }
  },
  {
    accessorKey: 'items',
    header: 'اقلام',
    cell: ({ row }) => {
      const items = row.getValue('items')
      const totalQuantity = items.reduce((sum, item) => sum + item.quantity, 0)
      return h('div', { class: 'text-center' }, `${totalQuantity} قلم`)
    }
  },
  {
    accessorKey: 'totalValue',
    header: () => h('div', { class: 'text-left' }, 'مبلغ کل'),
    cell: ({ row }) => {
      const value = row.getValue('totalValue')
      return h('div', { class: 'text-left font-semibold text-primary' }, 
        `${formatPrice(value)} تومان`
      )
    }
  },
  {
    id: 'actions',
    header: 'عملیات',
    cell: ({ row }) => h(UButton, {
      color: 'primary',
      variant: 'outline',
      size: 'sm',
      icon: 'i-lucide-eye',
      onClick: () => openOrderDetails(row.original)
    }, () => 'نمایش بیشتر')
  }
]

// محاسبه: سفارشات فیلتر شده
const filteredOrders = computed(() => {
  let result = orders.value

  if (searchTerm.value) {
    result = result.filter(order =>
      order.transactionId.toLowerCase().includes(searchTerm.value.toLowerCase())
    )
  }

  if (selectedStatus.value && selectedStatus.value.value !== null) {
    result = result.filter(order => order.deliveryStatus === selectedStatus.value.value)
  }

  if (selectedPeriod.value && selectedPeriod.value.value !== 'all') {
    const now = new Date()
    
    result = result.filter(order => {
      const date = new Date(order.date)
      
      switch (selectedPeriod.value.value) {
        case 'today':
          return date.toDateString() === now.toDateString()
        case 'week': {
          const weekStart = new Date(now)
          weekStart.setDate(weekStart.getDate() - weekStart.getDay())
          return date >= weekStart
        }
        case 'month':
          return date.getMonth() === now.getMonth() && date.getFullYear() === now.getFullYear()
        case '7days': {
          const sevenDaysAgo = new Date(now)
          sevenDaysAgo.setDate(sevenDaysAgo.getDate() - 7)
          return date >= sevenDaysAgo
        }
        case '30days': {
          const thirtyDaysAgo = new Date(now)
          thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30)
          return date >= thirtyDaysAgo
        }
        default:
          return true
      }
    })
  }

  return result
})

// محاسبه: تعداد سفارشات هفتگی
const weeklyOrdersCount = computed(() => {
  const now = new Date()
  const weekStart = new Date(now)
  weekStart.setDate(weekStart.getDate() - weekStart.getDay())
  
  return orders.value.filter(order => {
    const orderDate = new Date(order.date)
    return orderDate >= weekStart
  }).length
})

// توابع
function clearFilters() {
  searchTerm.value = ''
  selectedStatus.value = null
  selectedPeriod.value = { label: 'همه زمان‌ها', value: 'all' }
}

function handleUpdateStatus(orderId, newStatus) {
  const order = orders.value.find(o => o.id === orderId)
  if (order) {
    order.deliveryStatus = newStatus
  }
}
</script>
