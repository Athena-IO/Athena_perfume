<template>
  <div class="flex flex-col md:flex-row md:mt-25 min-h-screen w-full">
    <!-- کارت ورود -->
    <div class="w-full p-6">
      <Ucard class="w-full items-center justify-center flex">
        <template #header>صفحه ثبت نام</template>
        <form @submit.prevent="handlesignup">
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
          <div class="space-y-2">
            <UFormField
              label="رمز عبور"
              name="password"
              class="mb-4"
              :required="true"
              help="رمز عبور خود را وارد کنید"
            >
              <UInput
                v-model="password"
                placeholder="Password"
                :type="show ? 'text' : 'password'"
                :ui="{ trailing: 'pe-1' }"
              >
                <template #trailing>
                  <UButton
                    color="neutral"
                    variant="link"
                    size="sm"
                    :icon="show ? 'i-lucide-eye-off' : 'i-lucide-eye'"
                    :aria-label="show ? 'Hide password' : 'Show password'"
                    :aria-pressed="show"
                    aria-controls="password"
                    @click="show = !show"
                  />
                </template>
              </UInput>
            </UFormField>
          </div>
          <u-input-menu
            v-model="role"
            :items="items"
            color="warning"
            highlight
          />

          <UButton
            :loading="pending"
            :disabled="pending"
            type="submit"
            class="w-1/2 mt-2 justify-center"
            >ثبت کاربر</UButton
          >
        </form>
      </Ucard>
    </div>
  </div>
  <div class=""></div>
</template>

<script setup>
import { useAppToast } from "~/composables/useToast";
import { useRouter } from "vue-router";

const router = useRouter();
const Toast = useAppToast();
const show = ref(false);
const number = ref("");
const password = ref("");
const pending = ref(false);
const items = ref(["admin", "user"]);
const role = ref("user");

const handlesignup = async () => {
  pending.value = true;
  try {
    // ارسال درخواست به Django backend
    const res = await $fetch("http://127.0.0.1:8000/api/accounts/login/", {
      method: "POST",
      body: {
        identifier: number.value, // شماره یا ایمیل یا username
        password: password.value,
        role: role.value,
      },
    });

    // ذخیره توکن‌ها
    localStorage.setItem("access", res.access);
    localStorage.setItem("refresh", res.refresh);

    // پیام موفقیت
    Toast.toastSuccess({
      title: "کاربر با موفقیت اضافه شد",
      description: "خوش آمدید",
    });

    // هدایت بر اساس نقش کاربر
    if (res.role === "admin") {
      router.push("/admin");
    } else {
      router.push("/");
    }
  } catch (err) {
    Toast.toastError({
      title: "ثبت کاربر ناموفق بود",
      description: err?.data?.detail || "کاربر با این نام وجود دارد",
    });
  } finally {
    pending.value = false;
  }
};
</script>
<style>
/* Hide the password reveal button in Edge */
::-ms-reveal {
  display: none;
}
</style>
