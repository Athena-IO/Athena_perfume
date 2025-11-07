<template>
  <div class="flex flex-col md:flex-row md:mt-25 min-h-screen w-full">
    <!-- کارت ثبت‌نام -->
    <div class="w-full p-6">
      <UCard class="w-full items-center justify-center flex">
        <template #header>صفحه ثبت نام</template>
        <form @submit.prevent="handleSignup">
          <!-- شماره تلفن -->
          <UFormField
            label="شماره تلفن"
            name="phone"
            class="mb-4"
            :required="true"
            help="مثلاً: 09123456789"
          >
            <UInput
              type="tel"
              placeholder="09123456789"
              required
              v-model="phone"
            />
          </UFormField>

          <!-- رمز عبور با نمایش/مخفی -->
          <UFormField
            label="رمز عبور"
            name="password"
            class="mb-4"
            :required="true"
            help="حداقل ۸ کاراکتر، شامل عدد و حروف"
          >
            <UInput
              v-model="password"
              :type="showPassword ? 'text' : 'password'"
              placeholder="رمز عبور"
              :ui="{ trailing: 'pe-1' }"
            >
              <template #trailing>
                <UButton
                  color="neutral"
                  variant="link"
                  size="sm"
                  :icon="showPassword ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                  :aria-label="showPassword ? 'مخفی کردن' : 'نمایش رمز'"
                  @click="showPassword = !showPassword"
                />
              </template>
            </UInput>
          </UFormField>

          <!-- انتخاب نقش (فقط ادمین ببینه) -->
          <UFormField v-if="isAdmin" label="نقش کاربر" name="role" class="mb-4">
            <UInputMenu
              v-model="role"
              :items="roleItems"
              color="warning"
              highlight
            />
          </UFormField>

          <!-- دکمه ثبت -->
          <UButton
            :loading="pending"
            :disabled="pending"
            type="submit"
            class="w-1/2 mt-2 justify-center"
          >
            ثبت کاربر
          </UButton>
        </form>
      </UCard>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: "admin-only",
});

import { useAppToast } from "~/composables/useToast";
import { useRouter } from "vue-router";

const router = useRouter();
const toast = useAppToast();

// فرم
const phone = ref("");
const password = ref("");
const pending = ref(false);
const showPassword = ref(false);

// نقش
const role = ref("user");
const roleItems = ref([
  { label: "کاربر عادی", value: "user" },
  { label: "ادمین", value: "admin" },
]);

// کوکی‌ها
const accessCookie = useCookie("access", { maxAge: 60 * 60 * 24 });
const refreshCookie = useCookie("refresh", { maxAge: 60 * 60 * 24 * 7 });
const isAdminCookie = useCookie("isAdmin", { maxAge: 60 * 60 * 24 });

// آیا کاربر فعلی ادمین است؟
const isAdmin = computed(() => isAdminCookie.value === "true");

// تابع ثبت‌نام
const handleSignup = async () => {
  pending.value = true;

  // اعتبارسنجی ساده
  if (!/^09[0-9]{9}$/.test(phone.value)) {
    toast.toastError({ title: "خطا", description: "شماره تلفن معتبر نیست." });
    pending.value = false;
    return;
  }
  if (password.value.length < 8) {
    toast.toastError({
      title: "خطا",
      description: "رمز عبور باید حداقل ۸ کاراکتر باشد.",
    });
    pending.value = false;
    return;
  }

  try {
    const res = await $fetch("http://127.0.0.1:8000/api/accounts/register/", {
      method: "POST",
      body: {
        phone: phone.value,
        password: password.value,
        // فقط ادمین بتونه نقش admin انتخاب کنه
        role: isAdmin.value ? role.value : "user",
      },
    });

    // اگر کاربر جدید ادمین باشه، توکن بده (اختیاری)
    if (res.access && res.refresh) {
      accessCookie.value = res.access;
      refreshCookie.value = res.refresh;
      isAdminCookie.value = res.role === "admin" ? "true" : "false";
    }

    toast.toastSuccess({
      title: "موفقیت",
      description: "کاربر با موفقیت ایجاد شد.",
    });

    router.push("/admin");
  } catch (err) {
    const message =
      err?.data?.detail || err?.data?.phone?.[0] || "خطا در ثبت‌نام";
    toast.toastError({ title: "خطا", description: message });
  } finally {
    pending.value = false;
  }
};
</script>

<style>
::-ms-reveal {
  display: none;
}
</style>
