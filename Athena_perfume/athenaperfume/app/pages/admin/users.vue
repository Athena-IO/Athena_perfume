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
  middleware: "admin-only",
});
import { useToast } from "#ui/composables/useToast";
import { useRouter } from "vue-router";

const toast = useToast();
const router = useRouter();

// --- داده‌ها ---
const admins = ref([]);
const loading = ref(true);
const showModal = ref(false);
const selectedId = ref(null);
const password = ref("");
const error = ref("");

// رمز امنیتی (در پروداکشن از .env استفاده کن)
const SECURITY_PASSWORD = "admin1234"; // یا: process.env.SECURITY_PASSWORD

// --- دریافت ادمین‌ها ---
const fetchAdmins = async () => {
  loading.value = true;
  try {
    const access = useCookie("access").value;
    if (!access) return router.push("/login");

    const users = await $fetch("http://127.0.0.1:8000/api/accounts/users/", {
      headers: { Authorization: `Bearer ${access}` },
    });

    // فقط ادمین‌ها + فقط فیلدهای لازم
    admins.value = users
      .filter((u) => u.role === "admin")
      .map((u) => ({
        id: u.id,
        username: u.username,
        email: u.email,
      }));
  } catch (err) {
    toast.add({
      title: "خطا",
      description: "دریافت ادمین‌ها ناموفق بود.",
      color: "error",
    });
  } finally {
    loading.value = false;
  }
};

// --- مودال حذف ---
const openDelete = (id) => {
  selectedId.value = id;
  password.value = "";
  error.value = "";
  showModal.value = true;
};

const closeModal = () => {
  showModal.value = false;
  selectedId.value = null;
};

const confirmDelete = async () => {
  if (password.value !== SECURITY_PASSWORD) {
    error.value = "رمز اشتباه است";
    return;
  }

  try {
    const access = useCookie("access").value;
    await $fetch(
      `http://127.0.0.1:8000/api/accounts/users/${selectedId.value}/`,
      {
        method: "DELETE",
        headers: { Authorization: `Bearer ${access}` },
      }
    );

    toast.add({
      title: "حذف شد",
      description: "ادمین با موفقیت حذف شد.",
      color: "success",
    });
    closeModal();
    fetchAdmins();
  } catch {
    toast.add({
      title: "خطا",
      description: "حذف ناموفق بود.",
      color: "error",
    });
  }
};

// لود اولیه
onMounted(() => {
  fetchAdmins();
});
</script>
