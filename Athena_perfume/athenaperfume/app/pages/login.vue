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
import { useAuthStore } from '~/stores/auth'

const identifier = ref("")
const password = ref("")
const pending = ref(false)

const authStore = useAuthStore()
const router = useRouter()
const route = useRoute() // read query (?redirectTo=/checkout)

const handleLogin = async () => {
  pending.value = true
  try {
    const res = await $fetch("/api/accounts/login/", {
      method: "POST",
      body: {
        identifier: identifier.value,
        password: password.value,
      },
    })

    const accessCookie = useCookie("access", { maxAge: 60 * 60 * 24 * 7 })
    accessCookie.value = res.access || res.access_token

    authStore.setUser(res.user || res)

    useAppToast().toastSuccess({
      title:
        "خوش آمدی " + (res.user?.full_name || res.user?.username || "کاربر"),
      description: "ورود با موفقیت انجام شد",
    })

    // If we came with ?redirectTo=/checkout (from cart), go there
    const redirectTo = route.query.redirectTo
    if (redirectTo) {
      return router.push(redirectTo)
    }

    // Otherwise, normal role-based redirect
    const role = res.user?.role || res.role
    router.push(role === "admin" ? "/admin" : "/")
  } catch (err) {
    console.error("خطای ورود:", err)

    let message = "مشکلی پیش آمد، دوباره تلاش کن"
    if (err && (err.status === 401 || err.status === 400)) {
      message = (err.data && err.data.detail) || "شناسه یا رمز عبور اشتباه است"
    } else if (err && err.status === 404) {
      message = "سرور پیدا نشد. بک‌اند اجرا شده؟"
    } else if (err && err.status >= 500) {
      message = "سرور مشکلی دارد، بعداً تلاش کن"
    }

    useAppToast().toastError({
      title: "ورود ناموفق",
      description: message,
    })
  } finally {
    pending.value = false
  }
}
</script>