<template>
  <UContainer class="py-6 sm:py-10">
    <div class="max-w-6xl mx-auto">
      <!-- Header -->
      <div class="mb-8">
        <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
          تکمیل خرید
        </h1>
        <p class="text-gray-500 dark:text-gray-400 mt-2">
          اطلاعات خود را وارد کنید و خرید را نهایی کنید
        </p>
      </div>

      <div class="grid lg:grid-cols-3 gap-6">
        <!-- Main Form Section -->
        <div class="lg:col-span-2 space-y-6">
          <!-- Cart Items -->
          <UCard>
            <template #header>
              <div class="flex items-center justify-between">
                <h2 class="text-lg font-semibold flex items-center gap-2">
                  <UIcon name="i-lucide-shopping-bag" class="size-5" />
                  سبد خرید شما ({{ cart.totalItems }} محصول)
                </h2>
                <UButton
                  color="neutral"
                  variant="ghost"
                  size="sm"
                  @click="$router.push('/')"
                >
                  ادامه خرید
                </UButton>
              </div>
            </template>

            <div class="space-y-4">
              <div
                v-for="item in cart.items"
                :key="`${item.id}-${item.selectedVolume}`"
                class="flex gap-4 p-4 border border-gray-200 dark:border-gray-800 rounded-lg hover:border-primary/50 transition-colors"
              >
                <!-- Product Image -->
                <div class="relative w-20 h-20 flex-shrink-0">
                  <img
                    :src="item.image"
                    :alt="item.title"
                    class="w-full h-full object-cover rounded-md"
                  />
                </div>

                <!-- Product Info -->
                <div class="flex-1 min-w-0">
                  <h3 class="font-semibold text-sm line-clamp-2 mb-1">
                    {{ item.title }}
                  </h3>
                  <div class="flex items-center gap-2 text-xs text-gray-500">
                    <span>حجم: {{ item.volumeLabel }}</span>
                    <span>•</span>
                    <span>تعداد: {{ item.qty }}</span>
                  </div>

                  <!-- Price -->
                  <div class="flex items-center gap-2 mt-2">
                    <span class="font-bold text-primary">
                      {{ formatPrice(item.price * item.qty) }} تومان
                    </span>
                    <span
                      v-if="
                        item.originalPrice && item.originalPrice > item.price
                      "
                      class="text-xs text-gray-400 line-through"
                    >
                      {{ formatPrice(item.originalPrice * item.qty) }} تومان
                    </span>
                  </div>
                </div>

                <!-- Remove Button -->
                <UButton
                  color="neutral"
                  variant="ghost"
                  size="sm"
                  icon="i-lucide-trash-2"
                  square
                  @click="cart.removeFromCart(item.id)"
                />
              </div>

              <!-- Empty State -->
              <div v-if="cart.items.length === 0" class="text-center py-12">
                <UIcon
                  name="i-lucide-shopping-cart"
                  class="size-16 text-gray-300 dark:text-gray-700 mx-auto mb-4"
                />
                <p class="text-gray-500">سبد خرید شما خالی است</p>
                <UButton class="mt-4" @click="$router.push('/')">
                  شروع خرید
                </UButton>
              </div>
            </div>
          </UCard>

          <!-- Shipping Information -->
          <UCard v-if="cart.items.length > 0">
            <template #header>
              <h2 class="text-lg font-semibold flex items-center gap-2">
                <UIcon name="i-lucide-map-pin" class="size-5" />
                اطلاعات ارسال
              </h2>
            </template>

            <UForm
              ref="formRef"
              :state="shippingForm"
              :validate="validateShipping"
              class="space-y-4"
              @submit="handleCheckout"
            >
              <div class="grid sm:grid-cols-2 gap-4">
                <UFormField label="نام" name="firstName" required>
                  <UInput
                    v-model="shippingForm.firstName"
                    placeholder="نام خود را وارد کنید"
                  />
                </UFormField>

                <UFormField label="نام خانوادگی" name="lastName" required>
                  <UInput
                    v-model="shippingForm.lastName"
                    placeholder="نام خانوادگی خود را وارد کنید"
                  />
                </UFormField>
              </div>

              <UFormField label="شماره تماس" name="phone" required>
                <UInput
                  v-model="shippingForm.phone"
                  type="tel"
                  placeholder="09123456789"
                  icon="i-lucide-phone"
                />
              </UFormField>

              <UFormField label="ایمیل" name="email">
                <UInput
                  v-model="shippingForm.email"
                  type="email"
                  placeholder="example@email.com"
                  icon="i-lucide-at-sign"
                />
              </UFormField>

              <div class="grid sm:grid-cols-2 gap-4">
                <UFormField label="استان" name="province" required>
                  <USelectMenu
                    v-model="shippingForm.province"
                    :items="provinces"
                    placeholder="انتخاب استان"
                  />
                </UFormField>

                <UFormField label="شهر" name="city" required>
                  <UInput v-model="shippingForm.city" placeholder="نام شهر" />
                </UFormField>
              </div>

              <UFormField label="آدرس کامل" name="address" required>
                <UTextarea
                  v-model="shippingForm.address"
                  :rows="3"
                  placeholder="آدرس کامل خود را وارد کنید..."
                />
              </UFormField>

              <UFormField label="کد پستی" name="postalCode" required>
                <UInput
                  v-model="shippingForm.postalCode"
                  placeholder="1234567890"
                  maxlength="10"
                />
              </UFormField>

              <UFormField label="توضیحات (اختیاری)" name="notes">
                <UTextarea
                  v-model="shippingForm.notes"
                  :rows="2"
                  placeholder="توضیحات تکمیلی..."
                />
              </UFormField>
            </UForm>
          </UCard>
        </div>

        <!-- Order Summary Sidebar -->
        <div class="lg:col-span-1">
          <div class="sticky top-6 space-y-4">
            <UCard>
              <template #header>
                <h2 class="text-lg font-semibold">خلاصه سفارش</h2>
              </template>

              <div class="space-y-3">
                <!-- Subtotal -->
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600 dark:text-gray-400">
                    مجموع محصولات
                  </span>
                  <span class="font-medium">
                    {{ formatPrice(subtotal) }} تومان
                  </span>
                </div>

                <!-- Original Total (before discount) -->
                <div
                  v-if="totalDiscount > 0"
                  class="flex justify-between text-sm"
                >
                  <span class="text-gray-600 dark:text-gray-400">
                    قیمت اصلی
                  </span>
                  <span class="font-medium text-gray-400 line-through">
                    {{ formatPrice(originalTotal) }} تومان
                  </span>
                </div>

                <!-- Discount -->
                <div
                  v-if="totalDiscount > 0"
                  class="flex justify-between text-sm text-success"
                >
                  <span>تخفیف</span>
                  <span class="font-medium">
                    -{{ formatPrice(totalDiscount) }} تومان
                  </span>
                </div>

                <!-- Shipping -->
                <div class="flex justify-between text-sm">
                  <span class="text-gray-600 dark:text-gray-400">
                    هزینه ارسال
                  </span>
                  <span
                    v-if="shippingCost === 0"
                    class="font-medium text-success"
                  >
                    رایگان
                  </span>
                  <span v-else class="font-medium">
                    {{ formatPrice(shippingCost) }} تومان
                  </span>
                </div>

                <UDivider />

                <!-- Total -->
                <div class="flex justify-between text-base font-bold">
                  <span>مجموع نهایی</span>
                  <span class="text-primary">
                    {{ formatPrice(finalTotal) }} تومان
                  </span>
                </div>

                <!-- Savings Badge -->
                <UBadge
                  v-if="totalDiscount > 0"
                  color="success"
                  variant="soft"
                  size="lg"
                  class="w-full justify-center"
                >
                  شما {{ formatPrice(totalDiscount) }} تومان صرفه‌جویی کردید!
                </UBadge>

                <!-- Free shipping notice -->
                <div
                  v-if="shippingCost > 0 && subtotal < 500000"
                  class="text-xs text-gray-500 bg-gray-50 dark:bg-gray-800 p-3 rounded-lg"
                >
                  <UIcon name="i-lucide-info" class="inline size-3" />
                  برای ارسال رایگان
                  {{ formatPrice(500000 - subtotal) }} تومان دیگر خرید کنید
                </div>
              </div>

              <template #footer>
                <UButton
                  block
                  size="lg"
                  icon="i-lucide-credit-card"
                  :disabled="cart.items.length === 0"
                  :loading="isProcessing"
                  @click="handleCheckout"
                >
                  پرداخت {{ formatPrice(finalTotal) }} تومان
                </UButton>

                <!-- Trust Badges -->
                <div
                  class="mt-4 pt-4 border-t border-gray-200 dark:border-gray-800"
                >
                  <div
                    class="space-y-2 text-xs text-gray-600 dark:text-gray-400"
                  >
                    <div class="flex items-center gap-2">
                      <UIcon
                        name="i-lucide-shield-check"
                        class="size-4 text-success"
                      />
                      <span>پرداخت ایمن</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <UIcon
                        name="i-lucide-truck"
                        class="size-4 text-primary"
                      />
                      <span>ارسال سریع</span>
                    </div>
                    <div class="flex items-center gap-2">
                      <UIcon
                        name="i-lucide-rotate-ccw"
                        class="size-4 text-info"
                      />
                      <span>7 روز ضمانت بازگشت</span>
                    </div>
                  </div>
                </div>
              </template>
            </UCard>

            <!-- Coupon Code -->
            <UCard>
              <template #header>
                <h3 class="text-sm font-semibold">کد تخفیف</h3>
              </template>

              <div class="flex gap-2">
                <UInput
                  v-model="couponCode"
                  placeholder="کد تخفیف را وارد کنید"
                  class="flex-1"
                  :disabled="couponApplied"
                />
                <UButton
                  v-if="!couponApplied"
                  variant="outline"
                  @click="applyCoupon"
                >
                  اعمال
                </UButton>
                <UButton
                  v-else
                  color="success"
                  variant="soft"
                  icon="i-lucide-check"
                  @click="removeCoupon"
                >
                  حذف
                </UButton>
              </div>
            </UCard>
          </div>
        </div>
      </div>
    </div>
  </UContainer>
</template>

<script setup>
import { ref, computed } from "vue";
import { useCartStore } from "~/composables/stores/cart";
import { useRouter } from "vue-router";

const cart = useCartStore();
const router = useRouter();

// Shipping form state
const shippingForm = reactive({
  firstName: "",
  lastName: "",
  phone: "",
  email: "",
  province: "",
  city: "",
  address: "",
  postalCode: "",
  notes: "",
});

// Iranian provinces
const provinces = [
  "تهران",
  "اصفهان",
  "فارس",
  "خراسان رضوی",
  "آذربایجان شرقی",
  "مازندران",
  "گیلان",
  "البرز",
  "خوزستان",
  "قم",
  "کرمان",
  "همدان",
  "مرکزی",
];

// Coupon code
const couponCode = ref("");
const couponApplied = ref(false);
const couponDiscount = ref(0);
const isProcessing = ref(false);
const formRef = ref(null);

// Calculate subtotal (after product discounts)
const subtotal = computed(() => {
  return cart.items.reduce((sum, item) => {
    return sum + item.price * item.qty;
  }, 0);
});

// Calculate original total (before product discounts)
const originalTotal = computed(() => {
  return cart.items.reduce((sum, item) => {
    const price = item.originalPrice || item.price;
    return sum + price * item.qty;
  }, 0);
});

// Calculate total discount from products
const totalDiscount = computed(() => {
  return originalTotal.value - subtotal.value + couponDiscount.value;
});

// Shipping cost calculation (free for orders over 500,000)
const shippingCost = computed(() => {
  return subtotal.value >= 500000 ? 0 : 50000;
});

// Final total
const finalTotal = computed(() => {
  return subtotal.value + shippingCost.value - couponDiscount.value;
});

// Format price helper
const formatPrice = (price) => {
  return new Intl.NumberFormat("fa-IR").format(Math.round(price));
};

// Validation function
const validateShipping = (state) => {
  const errors = [];

  if (!state.firstName?.trim()) {
    errors.push({ name: "firstName", message: "نام الزامی است" });
  }

  if (!state.lastName?.trim()) {
    errors.push({ name: "lastName", message: "نام خانوادگی الزامی است" });
  }

  if (!state.phone?.trim()) {
    errors.push({ name: "phone", message: "شماره تماس الزامی است" });
  } else if (!/^09\d{9}$/.test(state.phone)) {
    errors.push({
      name: "phone",
      message: "شماره تماس معتبر نیست (مثال: 09123456789)",
    });
  }

  if (state.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(state.email)) {
    errors.push({ name: "email", message: "ایمیل معتبر نیست" });
  }

  if (!state.province) {
    errors.push({ name: "province", message: "انتخاب استان الزامی است" });
  }

  if (!state.city?.trim()) {
    errors.push({ name: "city", message: "نام شهر الزامی است" });
  }

  if (!state.address?.trim()) {
    errors.push({ name: "address", message: "آدرس کامل الزامی است" });
  } else if (state.address.trim().length < 10) {
    errors.push({
      name: "address",
      message: "آدرس باید حداقل 10 کاراکتر باشد",
    });
  }

  if (!state.postalCode?.trim()) {
    errors.push({ name: "postalCode", message: "کد پستی الزامی است" });
  } else if (!/^\d{10}$/.test(state.postalCode)) {
    errors.push({ name: "postalCode", message: "کد پستی باید 10 رقم باشد" });
  }

  return errors;
};

// Apply coupon
const applyCoupon = () => {
  if (!couponCode.value.trim()) {
    alert("لطفاً کد تخفیف را وارد کنید");
    return;
  }

  // Simulate coupon validation
  const code = couponCode.value.toUpperCase();

  if (code === "WELCOME10") {
    couponDiscount.value = Math.round(subtotal.value * 0.1); // 10% discount
    couponApplied.value = true;
    alert("کد تخفیف 10٪ با موفقیت اعمال شد!");
  } else if (code === "SAVE50K") {
    couponDiscount.value = 50000;
    couponApplied.value = true;
    alert("کد تخفیف 50,000 تومان با موفقیت اعمال شد!");
  } else {
    alert("کد تخفیف معتبر نیست");
  }
};

// Remove coupon
const removeCoupon = () => {
  couponCode.value = "";
  couponApplied.value = false;
  couponDiscount.value = 0;
};

// Handle checkout
const handleCheckout = async () => {
  // Validate form first
  const errors = validateShipping(shippingForm);

  if (errors.length > 0) {
    // Form will show errors automatically
    alert("لطفاً تمام فیلدهای الزامی را به درستی پر کنید");
    return;
  }

  if (cart.items.length === 0) {
    alert("سبد خرید شما خالی است");
    return;
  }

  isProcessing.value = true;

  try {
    // Simulate API call
    await new Promise((resolve) => setTimeout(resolve, 2000));

    // Create order object
    const order = {
      items: cart.items.map((item) => ({
        id: item.id,
        title: item.title,
        price: item.price,
        originalPrice: item.originalPrice,
        qty: item.qty,
        selectedVolume: item.selectedVolume,
        volumeLabel: item.volumeLabel,
        total: item.price * item.qty,
      })),
      shipping: { ...shippingForm },
      subtotal: subtotal.value,
      originalTotal: originalTotal.value,
      discount: totalDiscount.value,
      coupon: couponApplied.value
        ? {
            code: couponCode.value,
            discount: couponDiscount.value,
          }
        : null,
      shippingCost: shippingCost.value,
      total: finalTotal.value,
      orderNumber: `ORD-${Date.now()}`,
      createdAt: new Date().toISOString(),
    };

    console.log("Order Details:", order);

    // Here you would send to your backend
    // const response = await $fetch('/api/orders', {
    //   method: 'POST',
    //   body: order
    // })

    // Redirect to payment gateway
    alert(
      `سفارش شما با موفقیت ثبت شد!\nشماره سفارش: ${order.orderNumber}\n\nدر حال انتقال به درگاه پرداخت...`
    );

    // Clear cart after successful order
    cart.clearCart();

    // Redirect to success page or payment gateway
    // router.push(`/payment/${order.orderNumber}`)
    router.push("/");
  } catch (error) {
    console.error("Checkout error:", error);
    alert("خطا در ثبت سفارش. لطفاً دوباره تلاش کنید.");
  } finally {
    isProcessing.value = false;
  }
};
</script>
