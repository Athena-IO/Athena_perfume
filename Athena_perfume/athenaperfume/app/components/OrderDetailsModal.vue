<template>
  <UModal v-model:open="isOpen" :ui="{ width: 'sm:max-w-4xl' }">
    <template #content>
      <div class="p-6" dir="rtl" v-if="order">
        <!-- هدر مدال -->
        <div class="flex items-center justify-between mb-6 pb-4 border-b border-default">
          <div>
            <h2 class="text-2xl font-bold">جزئیات سفارش</h2>
            <p class="text-sm text-muted mt-1">شناسه تراکنش: {{ order.transactionId }}</p>
          </div>
          <UButton
            color="neutral"
            variant="ghost"
            icon="i-lucide-x"
            square
            @click="isOpen = false"
          />
        </div>

        <!-- محتوای مدال -->
        <div class="space-y-6">
          <!-- وضعیت سفارش و دکمه تغییر وضعیت -->
          <UCard>
            <div class="flex items-center justify-between">
              <div class="flex items-center gap-4">
                <div>
                  <p class="text-sm text-muted mb-1">وضعیت فعلی:</p>
                  <UBadge
                    :color="getStatusConfig(order.deliveryStatus).color"
                    variant="subtle"
                    size="lg"
                    class="text-base"
                  >
                    {{ getStatusConfig(order.deliveryStatus).label }}
                  </UBadge>
                </div>
              </div>

              <!-- دکمه تغییر وضعیت -->
              <div v-if="order.deliveryStatus === 'not_sent'">
                <UButton
                  color="primary"
                  icon="i-lucide-truck"
                  @click="updateToInProgress"
                  :loading="isUpdating"
                >
                  ثبت و ارسال به "در حال ارسال"
                </UButton>
              </div>
              <div v-else-if="order.deliveryStatus === 'on_the_way'">
                <UButton
                  color="success"
                  icon="i-lucide-circle-check"
                  @click="updateToSent"
                  :loading="isUpdating"
                >
                  تایید تحویل
                </UButton>
              </div>
              <div v-else>
                <UBadge color="success" variant="soft" size="lg">
                  <UIcon name="i-lucide-package-check" class="ml-1" />
                  تحویل داده شده
                </UBadge>
              </div>
            </div>
          </UCard>

          <!-- اطلاعات مشتری -->
          <UCard>
            <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
              <UIcon name="i-lucide-user" class="text-primary" />
              اطلاعات مشتری
            </h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-muted">نام مشتری</p>
                <p class="font-medium">{{ order.customerName }}</p>
              </div>
              <div>
                <p class="text-sm text-muted">شماره تماس</p>
                <p class="font-medium">{{ order.phone }}</p>
              </div>
              <div>
                <p class="text-sm text-muted">ایمیل</p>
                <p class="font-medium">{{ order.email }}</p>
              </div>
              <div>
                <p class="text-sm text-muted">تاریخ سفارش</p>
                <p class="font-medium">{{ formatDate(order.date) }}</p>
              </div>
            </div>
          </UCard>

          <!-- آدرس تحویل -->
          <UCard>
            <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
              <UIcon name="i-lucide-map-pin" class="text-primary" />
              آدرس تحویل
            </h3>
            <div class="space-y-3">
              <div class="grid grid-cols-2 gap-4">
                <div>
                  <p class="text-sm text-muted">استان</p>
                  <p class="font-medium">{{ order.province }}</p>
                </div>
                <div>
                  <p class="text-sm text-muted">شهر</p>
                  <p class="font-medium">{{ order.city }}</p>
                </div>
              </div>
              <div>
                <p class="text-sm text-muted">آدرس کامل</p>
                <p class="font-medium">{{ order.address }}</p>
              </div>
              <div>
                <p class="text-sm text-muted">کد پستی</p>
                <p class="font-medium font-mono">{{ order.postalCode }}</p>
              </div>
            </div>
          </UCard>

          <!-- اقلام سفارش -->
          <UCard>
            <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
              <UIcon name="i-lucide-shopping-bag" class="text-primary" />
              اقلام سفارش ({{ order.items.length }} قلم)
            </h3>
            <div class="space-y-3">
              <div
                v-for="item in order.items"
                :key="item.id"
                class="flex items-center justify-between p-4 bg-elevated/50 rounded-lg"
              >
                <div class="flex items-center gap-3">
                  <div class="w-12 h-12 rounded-lg bg-primary/10 flex items-center justify-center">
                    <UIcon name="i-lucide-package" class="text-primary text-xl" />
                  </div>
                  <div>
                    <p class="font-medium">{{ item.name }}</p>
                    <p class="text-sm text-muted">حجم: {{ item.size }}</p>
                  </div>
                </div>
                <div class="text-left">
                  <p class="font-medium">تعداد: {{ item.quantity }}</p>
                  <p class="text-sm text-muted">{{ formatPrice(item.price) }} تومان</p>
                  <p class="text-sm font-semibold text-primary">
                    جمع: {{ formatPrice(item.price * item.quantity) }} تومان
                  </p>
                </div>
              </div>
            </div>

            <!-- جمع کل -->
            <div class="mt-4 pt-4 border-t border-default flex justify-between items-center">
              <p class="text-lg font-semibold">مبلغ کل سفارش:</p>
              <p class="text-2xl font-bold text-primary">
                {{ formatPrice(order.totalValue) }} تومان
              </p>
            </div>
          </UCard>

          <!-- اطلاعات پرداخت -->
          <UCard>
            <h3 class="text-lg font-semibold mb-4 flex items-center gap-2">
              <UIcon name="i-lucide-credit-card" class="text-primary" />
              اطلاعات پرداخت
            </h3>
            <div class="grid grid-cols-2 gap-4">
              <div>
                <p class="text-sm text-muted">روش پرداخت</p>
                <p class="font-medium">{{ order.paymentMethod }}</p>
              </div>
              <div>
                <p class="text-sm text-muted">وضعیت پرداخت</p>
                <UBadge
                  :color="order.paymentStatus === 'پرداخت شده' ? 'success' : 'warning'"
                  variant="subtle"
                >
                  {{ order.paymentStatus }}
                </UBadge>
              </div>
            </div>
          </UCard>

          <!-- یادداشت‌ها -->
          <UCard v-if="order.notes">
            <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
              <UIcon name="i-lucide-sticky-note" class="text-primary" />
              یادداشت‌های سفارش
            </h3>
            <div class="p-3 bg-warning/10 rounded-lg border border-warning/20">
              <p class="text-sm">{{ order.notes }}</p>
            </div>
          </UCard>
        </div>

        <!-- فوتر مدال -->
        <div class="mt-6 pt-4 border-t border-default flex justify-end gap-3">
          <UButton
            color="neutral"
            variant="outline"
            @click="isOpen = false"
          >
            بستن
          </UButton>
          <UButton
            color="primary"
            icon="i-lucide-printer"
            @click="printOrder"
          >
            چاپ سفارش
          </UButton>
        </div>
      </div>
    </template>
  </UModal>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  open: Boolean,
  order: Object
})

const emit = defineEmits(['update:open', 'update-status'])

const isUpdating = ref(false)

const isOpen = computed({
  get: () => props.open,
  set: (value) => emit('update:open', value)
})

function getStatusConfig(status) {
  const configs = {
    not_sent: { color: 'error', label: 'ارسال نشده' },
    on_the_way: { color: 'warning', label: 'در حال ارسال' },
    sent: { color: 'success', label: 'تحویل داده شده' }
  }
  return configs[status] || configs.not_sent
}

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

async function updateToInProgress() {
  isUpdating.value = true
  
  // شبیه‌سازی فراخوانی API
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // فراخوانی واقعی API:
  // try {
  //   await $fetch(`/api/orders/${props.order.id}/status`, {
  //     method: 'PATCH',
  //     body: { status: 'on_the_way' }
  //   })
  // } catch (error) {
  //   console.error(error)
  // }
  
  emit('update-status', props.order.id, 'on_the_way')
  isUpdating.value = false
}

async function updateToSent() {
  isUpdating.value = true
  
  // شبیه‌سازی فراخوانی API
  await new Promise(resolve => setTimeout(resolve, 1000))
  
  // فراخوانی واقعی API:
  // try {
  //   await $fetch(`/api/orders/${props.order.id}/status`, {
  //     method: 'PATCH',
  //     body: { status: 'sent' }
  //   })
  // } catch (error) {
  //   console.error(error)
  // }
  
  emit('update-status', props.order.id, 'sent')
  isUpdating.value = false
}

function printOrder() {
  // می‌توانید یک صفحه چاپ سفارشی ایجاد کنید
  window.print()
}
</script>
