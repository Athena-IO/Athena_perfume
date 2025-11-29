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
              {{ item.volumeLabel || item.selectedVolume + " میل" }}
            </p>
            <p class="font-bold text-primary mt-2">
              {{ formatPrice(item.price * item.qty) }}
            </p>
          </div>

          <div class="flex flex-col justify-between items-end gap-3">
            <div
              class="flex items-center gap-2 bg-white dark:bg-gray-900 rounded-lg"
            >
              <UButton
                icon="i-lucide-minus"
                size="xs"
                @click="decrement(item)"
              />
              <span class="w-10 text-center font-bold">{{ item.qty }}</span>
              <UButton
                icon="i-lucide-plus"
                size="xs"
                @click="cart.addToCart(item, 1)"
              />
            </div>
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
        <div class="flex justify-between text-lg font-bold">
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

const decrement = (item) => {
  if (item.qty > 1) {
    item.qty--;
  } else {
    cart.removeFromCart(item.id);
  }
};

const clearCart = () => {
  if (confirm("مطمئنی می‌خوای سبد رو کامل خالی کنی؟")) {
    cart.clearCart();
    toast.add({ title: "سبد خرید پاک شد", color: "success" });
  }
};
</script>
