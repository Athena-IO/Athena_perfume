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
      <Ucard class="w-full">
        <template #header>صفحه ورود</template>
        <form @submit.prevent="handlelogin">
          <UFormField
            label="نام کاربری"
            name="userName"
            class="mb-4"
            :required="true"
            help="نام کاربری خود را وارد کنید"
          >
            <UInput
              type="text"
              placeholder="شماره تلفن"
              required
              v-model="number"
            />
          </UFormField>

          <UFormField
            label="رمز عبور"
            name="Password"
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
            >ورود</UButton
          >
        </form>
      </Ucard>
    </div>
  </div>
</template>

<script setup>
import { useAppToast } from "~/composables/useToast";
import { useRouter } from "vue-router";

const router = useRouter();
const Toast = useAppToast();

const number = ref("");
const password = ref("");
const pending = ref(false);

const handlelogin = async () => {
  pending.value = true;
  try {
    // ارسال درخواست به Django backend
    const res = await $fetch("http://127.0.0.1:8000/api/accounts/login/", {
      method: "POST",
      body: {
        identifier: number.value, // شماره یا ایمیل یا username
        password: password.value,
      },
    });

    // ذخیره توکن‌ها
    localStorage.setItem("access", res.access);
    localStorage.setItem("refresh", res.refresh);

    // پیام موفقیت
    Toast.toastSuccess({
      title: "ورود با موفقیت انجام شد",
      description: "خوش آمدید!",
    });

    // هدایت بر اساس نقش کاربر
    if (res.role === "admin") {
      router.push("/admin");
    } else {
      router.push("/");
    }
  } catch (err) {
    Toast.toastError({
      title: "ورود ناموفق بود",
      description:
        err?.data?.detail ||
        "رمز عبور یا شماره تلفن اشتباه است. دوباره امتحان کنید.",
    });
  } finally {
    pending.value = false;
  }
};
</script>
