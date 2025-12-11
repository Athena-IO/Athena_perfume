<template>
  <USlideover v-model:open="isOpen" side="left" title="سبد خرید">
    <template #body>
      <!-- سبد خالی -->
      <div
        v-if="cart.items.length === 0"
        class="flex flex-col items-center justify-center h-full text-center px-6 py-12"
      >
        <UIcon
          name="i-lucide-shopping-cart"
          class="w-20 h-20 text-gray-400 mb-6"
        />
        <p class="text-xl font-bold mb-3">سبد خرید خالیه!</p>
        <p class="text-gray-500 mb-8">هنوز چیزی انتخاب نکردی</p>
        <UButton
          to="/products"
          color="primary"
          size="lg"
          @click="isOpen = false"
        >
          برو به فروشگاه
        </UButton>
      </div>

      <!-- لیست محصولات -->
      <div v-else class="space-y-4 pb-20">
        <div
          v-for="item in cart.items"
          :key="item.id"
          class="flex gap-4 p-4 bg-gray-50 dark:bg-gray-800 rounded-xl"
        >
          <img
            v-if="item.image"
            :src="item.image"
            class="w-20 h-20 rounded-lg object-cover"
          />
          <div class="flex-1">
            <h3 class="font-semibold text-sm">{{ item.title }}</h3>
<p class="text-xs text-gray-500 mt-1">
  حجم: {{ item.qty }} میل
</p>
            <p class="font-bold text-primary mt-2">
              {{ formatPrice(calculateItemTotal(item)) }} تومان
            </p>
          </div>

          <div class="flex flex-col justify-between items-end gap-3">
            <UInputNumber
              v-model="item.qty"
              :min="5"
              :step="5"
              size="xs"
              class="w-24"
              :max="Number(item.capacity) || undefined"  
              @update:model-value="updateQuantity(item)"
            />
            <UButton
              icon="i-lucide-trash-2"
              size="xs"
              color="error"
              variant="ghost"
              @click="cart.removeFromCart(item.id)"
            />
          </div>
        </div>
      </div>
    </template>

    <!-- فوتر -->
    <template #footer v-if="cart.items.length">
      <div class="w-full px-4 space-y-4 border-t pt-6">
        <!-- Total -->
        <div class="flex justify بین text-lg font-bold">
          <span>جمع کل:</span>
          <span class="text-primary"
            >{{ formatPrice(cart.totalPrice) }} تومان</span
          >
        </div>

        <!-- Buttons -->
        <div class="flex gap-3">
          <UButton block color="gray" variant="outline" @click="isOpen = false">
            ادامه خرید
          </UButton>
          <UButton block color="primary" to="/checkout" @click="isOpen = false">
            تسویه حساب
          </UButton>
        </div>

        <UButton block color="error" variant="ghost" @click="clearCart">
          پاک کردن سبد
        </UButton>
      </div>
    </template>
  </USlideover>
</template>

<script setup>
import { useCartStore } from "~/composables/stores/cart";

const isOpen = defineModel("open", { default: false });
const cart = useCartStore();
const toast = useToast();

const formatPrice = (price) => {
  const num =
    typeof price === "string"
      ? parseInt(price.replace(/[^0-9]/g, "")) || 0
      : price;
  return num.toLocaleString("fa-IR");
};

const calculateItemTotal = (item) => {
  return item.price * item.qty;
};

const updateQuantity = (item) => {
  // حداقل بر اساس step شما
  if (item.qty < 5) item.qty = 5;

  const capacity = Number(item.capacity) || 0;

  if (capacity > 0 && item.qty > capacity) {
    // اگر از ظرفیت بیشتر شد → برگشت به capacity و نمایش ارور
    item.qty = capacity;

    toast.add({
      title: "ظرفیت کافی نیست",
      description: `برای محصول «${item.title}» حداکثر ${capacity} عدد می‌توانید داشته باشید.`,
      color: "error",
    });
  }

  // اگر حجم بر اساس تعداد نمایش داده می‌شود
  if (item.selectedVolume) {
    item.totalVolume = item.qty;
  }
};

const clearCart = () => {
  if (confirm("مطمئنی می‌خوای سبد رو کامل خالی کنی؟")) {
    cart.clearCart();
    toast.add({ title: "سبد خرید پاک شد", color: "success" });
  }
};
</script>