<template>
  <div
    class="flex flex-col md:flex-row items-center justify-center min-h-screen w-full"
  >
    <!-- عکس -->
    <div class="hidden md:flex justify-center items-center w-1/2">
      <img
        src="https://vioralondon.com/wp-content/uploads/2023/10/Best-Autumn-Fragrances-For-Men-Main-Image-v2.jpg"
        alt="login"
        class="max-w-3xl rounded-2xl shadow-lg"
      />
    </div>

    <!-- کارت ورود -->
    <div class="w-full md:w-1/3 p-6">
      <UCard class="w-full">
        <template #header>صفحه ورود</template>
        <form @submit.prevent="handleLogin">
          <UFormField
            label="شناسه ورود"
            name="identifier"
            class="mb-4"
            :required="true"
            help="شماره تلفن، ایمیل یا نام کاربری"
          >
            <UInput
              type="text"
              placeholder="مثال: 09123456789"
              required
              v-model="identifier"
            />
          </UFormField>

          <UFormField
            label="رمز عبور"
            name="password"
            class="mb-4"
            :required="true"
            help="رمز عبور خود را وارد کنید"
          >
            <UInput
              type="password"
              placeholder="رمز عبور"
              required
              v-model="password"
            />
          </UFormField>

          <UButton
            :loading="pending"
            :disabled="pending"
            type="submit"
            class="w-1/2 mt-2 justify-center"
          >
            ورود
          </UButton>
        </form>
      </UCard>
    </div>
  </div>
</template>

<script setup>
import { useAppToast } from "~/composables/useToast";
import { useRouter } from "vue-router";

const router = useRouter();
const toast = useAppToast();

const identifier = ref("");
const password = ref("");
const pending = ref(false);

// کوکی‌ها با زمان انقضا
const accessCookie = useCookie("access", { maxAge: 60 * 60 * 24 }); // 1 روز
const refreshCookie = useCookie("refresh", { maxAge: 60 * 60 * 24 * 7 }); // 7 روز
const isAdminCookie = useCookie("isAdmin", { maxAge: 60 * 60 * 24 }); // 1 روز

const handleLogin = async () => {
  pending.value = true;
  try {
    const res = await $fetch("http://127.0.0.1:8000/api/accounts/login/", {
      method: "POST",
      body: {
        identifier: identifier.value,
        password: password.value,
      },
    });

    // ذخیره توکن‌ها در کوکی
    accessCookie.value = res.access;
    refreshCookie.value = res.refresh;
    isAdminCookie.value = res.role === "admin" ? "true" : "false";

    // پیام موفقیت
    toast.toastSuccess({
      title: "ورود موفق",
      description: "خوش آمدید!",
    });

    // هدایت بر اساس نقش
    router.push(res.role === "admin" ? "/admin" : "/");
  } catch (err) {
    toast.toastError({
      title: "ورود ناموفق",
      description: err?.data?.detail || "اطلاعات ورود اشتباه است.",
    });
  } finally {
    pending.value = false;
  }
};
</script>
