<template>
  <div class="flex flex-col md:flex-row md:mt-25 min-h-screen w-full">
    <div class="w-full p-6">
      <UCard class="w-full items-center justify-center flex">
        <template #header>ثبت نام کاربر جدید</template>
        <form @submit.prevent="handleSignup">
          <!-- شماره تلفن -->
          <UFormField label="شماره تلفن" class="mb-4" :required="true">
            <UInput
              type="tel"
              placeholder="09123456789"
              required
              v-model="phone"
            />
          </UFormField>

          <!-- رمز عبور -->
          <UFormField label="رمز عبور" class="mb-4" :required="true">
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
                  @click="showPassword = !showPassword"
                />
              </template>
            </UInput>
          </UFormField>

          <!-- انتخاب نقش -->
          <UFormField label="نقش کاربر" class="mb-4">
            <UInputMenu
              v-model="role"
              :items="roleItems"
              color="warning"
              highlight
            />
          </UFormField>

          <!-- دکمه -->
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
  middleware: "admin-only", // فقط ادمین‌ها وارد می‌شن
});

import { useAppToast } from "~/composables/useToast";
import { useRouter } from "vue-router";

const router = useRouter();
const toast = useAppToast();

const phone = ref("");
const password = ref("");
const pending = ref(false);
const showPassword = ref(false);
const role = ref("user");

const roleItems = ref([
  { label: "کاربر عادی", value: "user" },
  { label: "ادمین", value: "admin" },
]);

const handleSignup = async () => {
  pending.value = true;

  // اعتبارسنجی
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
        role: role.value, // حتی اگه کاربر عادی باشه، بک‌اند چک می‌کنه
      },
    });

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
