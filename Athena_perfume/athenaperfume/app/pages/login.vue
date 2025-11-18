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
const identifier = ref("");
const password = ref("");
const pending = ref(false);

const accessCookie = useCookie("access", { maxAge: 60 * 60 * 24 });
const isAdminCookie = useCookie("isAdmin", { maxAge: 60 * 60 * 24 });

const handleLogin = async () => {
  pending.value = true;
  try {
    // آدرس دقیقاً همونی که سرور Django روش اجرا شده
    const res = await $fetch("/api/accounts/login/", {
      method: "POST",
      body: {
        identifier: identifier.value,
        password: password.value,
      },
      credentials: "include", // برای httpOnly cookie
    });

    accessCookie.value = res.access;
    isAdminCookie.value = res.role === "admin" ? "true" : "false";

    useAppToast().toastSuccess({
      title: "ورود موفق",
      description: "خوش آمدید!",
    });
    useRouter().push(res.role === "admin" ? "/admin" : "/");
  } catch (err) {
    console.error("خطای ورود:", err);

    let message = "مشکلی پیش اومد، دوباره تلاش کن";

    // ارورهای رایج و متن فارسی قشنگ
    if (err?.status === 401 || err?.status === 400) {
      message = err?.data?.detail || "شناسه یا رمز عبور اشتباهه";
    } else if (err?.status === 404) {
      message = "آدرس سرور پیدا نشد. بک‌اند رو اجرا کردی؟";
    } else if (err?.status >= 500) {
      message = "سرور مشکل داره، یه کم دیگه امتحان کن";
    } else if (!navigator.onLine) {
      message = "اینترنتت وصل نیست";
    }

    useAppToast().toastError({
      title: "ورود ناموفق",
      description: message,
    });
  } finally {
    pending.value = false;
  }
};
</script>
