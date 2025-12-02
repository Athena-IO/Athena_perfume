<template>
  <div class="p-6">
    <UCard>
      <template #header>
        <h2 class="text-xl font-bold">لیست ادمین‌ها</h2>
      </template>

      <UTable
        :data="admins"
        :columns="[
          { id: 'username', key: 'username', label: 'نام کاربری' },
          { id: 'email', key: 'email', label: 'ایمیل' },
          { id: 'actions', label: 'عملیات' },
        ]"
        :loading="loading"
        :empty-state="{ icon: 'i-heroicons-users', label: 'ادمینی یافت نشد' }"
      >
        <template #actions-data="{ row }">
          <UButton
            color="red"
            size="xs"
            icon="i-heroicons-trash"
            @click="openDelete(row.id)"
          />
        </template>
      </UTable>
    </UCard>

    <!-- مودال حذف -->
    <UModal v-model="showModal" v-if="showModal">
      <UCard>
        <template #header>
          <h3 class="font-semibold">حذف ادمین</h3>
        </template>

        <p class="mb-4">
          آیا مطمئنید می‌خواهید ادمین
          <strong>{{
            admins.find((a) => a.id === selectedId)?.username
          }}</strong>
          را حذف کنید؟
        </p>

        <UFormField label="رمز امنیتی">
          <UInput
            v-model="password"
            type="password"
            placeholder="رمز را وارد کنید"
          />
        </UFormField>

        <div v-if="error" class="text-red-500 text-sm mt-1">{{ error }}</div>

        <template #footer>
          <div class="flex justify-end gap-2">
            <UButton variant="ghost" @click="closeModal">لغو</UButton>
            <UButton color="red" :disabled="!password" @click="confirmDelete">
              حذف
            </UButton>
          </div>
        </template>
      </UCard>
    </UModal>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: "admin-only", // این خودش با useAuth کار می‌کنه → کافیه!
});

import { useRouter } from "vue-router";

// useAuth رو وارد کن (حیاتی!)
import { useAuth } from "~/composables/useAuth";
const { user, isAuthenticated, isAdmin } = useAuth();

const toast = useToast();
const router = useRouter();

const admins = ref([]);
const loading = ref(true);
const showModal = ref(false);
const selectedId = ref(null);
const password = ref("");
const error = ref("");

const SECURITY_PASSWORD = "admin1234"; // بعداً از env

// فقط از useAuth استفاده کن، نه کوکی مستقیم!
const fetchAdmins = async () => {
  loading.value = true;

  // اگر لاگین نیست یا ادمین نیست → خود middleware قبلاً باید گرفته باشه
  // ولی برای اطمینان یه چک اضافه
  if (!isAuthenticated.value || !isAdmin.value) {
    router.push("/login");
    return;
  }

  try {
    const users = await $fetch("/api/accounts/users/", {
      headers: {
        Authorization: `Bearer ${useCookie("access").value}`, // فقط اینجا از کوکی استفاده کن
      },
    });

    admins.value = users
      .filter((u) => u.role === "admin")
      .map((u) => ({
        id: u.id,
        username: u.username,
        email: u.email,
      }));
  } catch (err) {
    console.error(err);
    toast.add({
      title: "خطا",
      description: "دریافت لیست ادمین‌ها ناموفق بود",
      color: "error",
    });
  } finally {
    loading.value = false;
  }
};

const confirmDelete = async () => {
  if (password.value !== SECURITY_PASSWORD) {
    error.value = "رمز امنیتی اشتباه است";
    return;
  }

  try {
    await $fetch(
      `http://127.0.0.1:8000/api/accounts/users/${selectedId.value}/`,
      {
        method: "DELETE",
        headers: { Authorization: `Bearer ${useCookie("access").value}` },
      }
    );

    toast.add({ title: "موفق", description: "ادمین حذف شد", color: "success" });
    closeModal();
    fetchAdmins();
  } catch (err) {
    toast.add({ title: "خطا", description: "حذف ناموفق بود", color: "error" });
  }
};

// فقط وقتی کاربر لود شد، دیتا رو بگیر
watchEffect(() => {
  if (isAuthenticated.value && isAdmin.value) {
    fetchAdmins();
  }
});
</script>
