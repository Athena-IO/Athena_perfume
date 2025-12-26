<template>
  <div class="p-6">
    <UCard>
      <template #header>
        <div class="flex justify-between items-center gap-4">
          <h2 class="text-xl font-bold">لیست کاربران</h2>

          <!-- Search and Filter Section -->
          <div class="flex gap-2 items-center">
            <!-- Search by ID -->
            <div class="w-48">
              <UInput
                v-model="searchId"
                type="number"
                placeholder="جستجو با شناسه (ID)..."
                icon="i-heroicons-magnifying-glass"
                size="sm"
              />
            </div>

            <!-- Role Filter -->
            <USelectMenu
              v-model="selectedRole"
              :items="roleOptions"
              value-key="value"
              size="sm"
              class="w-40"
            />
          </div>
        </div>
      </template>

      <UTable
        :data="paginatedUsers"
        :columns="columns"
        :empty-state="{
          icon: 'i-heroicons-users',
          label: 'کاربری با این مشخصات یافت نشد',
        }"
      >
        <template #role-cell="{ row }">
          <UBadge
            :color="row.original.role === 'admin' ? 'primary' : 'neutral'"
            variant="subtle"
            size="sm"
          >
            {{ row.original.role }}
          </UBadge>
        </template>

        <template #actions-cell="{ row }">
          <UButton
            color="error"
            variant="ghost"
            size="xs"
            icon="i-heroicons-trash"
            @click="openDelete(row.original.id)"
          />
        </template>
      </UTable>

      <!-- Pagination -->
      <template #footer>
        <div class="flex justify-between items-center px-4 py-3">
          <div class="text-sm text-muted">
            نمایش {{ startIndex + 1 }} تا {{ endIndex }} از
            {{ totalItems }} کاربر
          </div>
          <UPagination
            v-model:page="currentPage"
            :total="totalItems"
            :items-per-page="pageSize"
          />
        </div>
      </template>
    </UCard>

    <!-- Modal for Delete -->
    <UModal
      v-model:open="showModal"
      title="حذف کاربر"
      :ui="{
        title: 'text-error',
        footer: 'justify-end',
      }"
    >
      <template #body>
        <div class="space-y-4">
          <p>
            آیا مطمئنید می‌خواهید کاربر
            <strong class="text-highlighted">{{
              allUsers.find((u) => u.id === selectedId)?.username
            }}</strong>
            با شناسه
            <strong class="text-highlighted">{{ selectedId }}</strong> را حذف
            کنید؟
          </p>

          <UFormField label="رمز امنیتی">
            <UInput
              v-model="password"
              type="password"
              placeholder="رمز را وارد کنید (مثلاً admin1234)"
            />
          </UFormField>

          <div v-if="error" class="text-error text-sm">
            {{ error }}
          </div>
        </div>
      </template>

      <template #footer>
        <UButton variant="outline" color="neutral" @click="closeModal">
          لغو
        </UButton>
        <UButton color="error" :disabled="!password" @click="confirmDelete">
          تایید حذف
        </UButton>
      </template>
    </UModal>
  </div>
</template>

<script setup>
const toast = useToast();

const searchId = ref("");
const selectedRole = ref("all");
const showModal = ref(false);
const selectedId = ref(null);
const password = ref("");
const error = ref("");

// Pagination
const currentPage = ref(1);
const pageSize = ref(20);

const SECURITY_PASSWORD = "admin1234";

// گزینه‌های فیلتر نقش
const roleOptions = [
  { label: "همه", value: "all" },
  { label: "فقط ادمین‌ها", value: "admin" },
  { label: "فقط کاربران", value: "user" },
];

// تعریف ستون‌ها
const columns = [
  {
    id: "id",
    accessorKey: "id",
    header: "شناسه",
  },
  {
    id: "username",
    accessorKey: "username",
    header: "نام کاربری",
  },
  {
    id: "email",
    accessorKey: "email",
    header: "ایمیل",
  },
  {
    id: "role",
    accessorKey: "role",
    header: "نقش",
  },
  {
    id: "actions",
    header: "عملیات",
  },
];

// داده‌های نمونه - 50 کاربر برای تست pagination
const allUsers = ref([
  // Admins
  { id: 101, username: "ali_admin", email: "ali@example.com", role: "admin" },
  {
    id: 105,
    username: "reza_manager",
    email: "reza@example.com",
    role: "admin",
  },
  { id: 420, username: "admin_test", email: "test@example.com", role: "admin" },
  {
    id: 301,
    username: "mahdi_admin",
    email: "mahdi@example.com",
    role: "admin",
  },
  {
    id: 305,
    username: "hamid_admin",
    email: "hamid@example.com",
    role: "admin",
  },
  {
    id: 401,
    username: "zahra_admin",
    email: "zahra@example.com",
    role: "admin",
  },
  {
    id: 405,
    username: "hasan_admin",
    email: "hasan@example.com",
    role: "admin",
  },
  {
    id: 501,
    username: "maryam_admin",
    email: "maryam@example.com",
    role: "admin",
  },
  {
    id: 505,
    username: "javad_admin",
    email: "javad@example.com",
    role: "admin",
  },
  {
    id: 601,
    username: "fatemeh_admin",
    email: "fatemeh@example.com",
    role: "admin",
  },

  // Users
  { id: 210, username: "sara_user", email: "sara@example.com", role: "user" },
  {
    id: 315,
    username: "mohammad_user",
    email: "mohammad@example.com",
    role: "user",
  },
  { id: 525, username: "user_demo", email: "demo@example.com", role: "user" },
  { id: 201, username: "amir_user", email: "amir@example.com", role: "user" },
  { id: 202, username: "neda_user", email: "neda@example.com", role: "user" },
  { id: 203, username: "arash_user", email: "arash@example.com", role: "user" },
  {
    id: 204,
    username: "niloofar_user",
    email: "niloofar@example.com",
    role: "user",
  },
  { id: 205, username: "pouya_user", email: "pouya@example.com", role: "user" },
  {
    id: 206,
    username: "shirin_user",
    email: "shirin@example.com",
    role: "user",
  },
  {
    id: 207,
    username: "kamran_user",
    email: "kamran@example.com",
    role: "user",
  },
  { id: 208, username: "leila_user", email: "leila@example.com", role: "user" },
  {
    id: 209,
    username: "behnam_user",
    email: "behnam@example.com",
    role: "user",
  },
  {
    id: 211,
    username: "azadeh_user",
    email: "azadeh@example.com",
    role: "user",
  },
  {
    id: 212,
    username: "mehran_user",
    email: "mehran@example.com",
    role: "user",
  },
  { id: 213, username: "nasim_user", email: "nasim@example.com", role: "user" },
  {
    id: 214,
    username: "davood_user",
    email: "davood@example.com",
    role: "user",
  },
  { id: 215, username: "sogol_user", email: "sogol@example.com", role: "user" },
  { id: 216, username: "saeed_user", email: "saeed@example.com", role: "user" },
  {
    id: 217,
    username: "parisa_user",
    email: "parisa@example.com",
    role: "user",
  },
  { id: 218, username: "vahid_user", email: "vahid@example.com", role: "user" },
  { id: 219, username: "elnaz_user", email: "elnaz@example.com", role: "user" },
  { id: 220, username: "omid_user", email: "omid@example.com", role: "user" },
  { id: 221, username: "sima_user", email: "sima@example.com", role: "user" },
  {
    id: 222,
    username: "kourosh_user",
    email: "kourosh@example.com",
    role: "user",
  },
  { id: 223, username: "mina_user", email: "mina@example.com", role: "user" },
  { id: 224, username: "navid_user", email: "navid@example.com", role: "user" },
  {
    id: 225,
    username: "yasmin_user",
    email: "yasmin@example.com",
    role: "user",
  },
  { id: 226, username: "babak_user", email: "babak@example.com", role: "user" },
  {
    id: 227,
    username: "nazanin_user",
    email: "nazanin@example.com",
    role: "user",
  },
  { id: 228, username: "ramin_user", email: "ramin@example.com", role: "user" },
  {
    id: 229,
    username: "sepideh_user",
    email: "sepideh@example.com",
    role: "user",
  },
  {
    id: 230,
    username: "masoud_user",
    email: "masoud@example.com",
    role: "user",
  },
  {
    id: 231,
    username: "taraneh_user",
    email: "taraneh@example.com",
    role: "user",
  },
  {
    id: 232,
    username: "shahab_user",
    email: "shahab@example.com",
    role: "user",
  },
  {
    id: 233,
    username: "golnaz_user",
    email: "golnaz@example.com",
    role: "user",
  },
  { id: 234, username: "ehsan_user", email: "ehsan@example.com", role: "user" },
  {
    id: 235,
    username: "mahnaz_user",
    email: "mahnaz@example.com",
    role: "user",
  },
  {
    id: 236,
    username: "farshad_user",
    email: "farshad@example.com",
    role: "user",
  },
  {
    id: 237,
    username: "roxana_user",
    email: "roxana@example.com",
    role: "user",
  },
  {
    id: 238,
    username: "soheil_user",
    email: "soheil@example.com",
    role: "user",
  },
]);

// محاسبه لیست فیلتر شده
const filteredUsers = computed(() => {
  let filtered = allUsers.value;

  // فیلتر بر اساس نقش
  if (selectedRole.value && selectedRole.value !== "all") {
    filtered = filtered.filter((user) => user.role === selectedRole.value);
  }

  // فیلتر بر اساس شناسه
  if (searchId.value) {
    filtered = filtered.filter((user) =>
      user.id.toString().includes(searchId.value.toString())
    );
  }

  return filtered;
});

// محاسبات pagination
const totalItems = computed(() => filteredUsers.value.length);

const startIndex = computed(() => (currentPage.value - 1) * pageSize.value);

const endIndex = computed(() => {
  const end = startIndex.value + pageSize.value;
  return end > totalItems.value ? totalItems.value : end;
});

const paginatedUsers = computed(() => {
  return filteredUsers.value.slice(startIndex.value, endIndex.value);
});

// وقتی فیلتر تغییر کرد، به صفحه اول برگرد
watch([selectedRole, searchId], () => {
  currentPage.value = 1;
});

const openDelete = (id) => {
  selectedId.value = id;
  showModal.value = true;
  password.value = "";
  error.value = "";
};

const closeModal = () => {
  showModal.value = false;
  selectedId.value = null;
  password.value = "";
  error.value = "";
};

const confirmDelete = async () => {
  if (password.value !== SECURITY_PASSWORD) {
    error.value = "رمز امنیتی اشتباه است";
    return;
  }

  try {
    allUsers.value = allUsers.value.filter((u) => u.id !== selectedId.value);

    toast.add({
      title: "موفق",
      description: "کاربر با موفقیت حذف شد",
      color: "success",
      icon: "i-heroicons-check-circle",
    });
    closeModal();
  } catch (err) {
    toast.add({
      title: "خطا",
      description: "حذف ناموفق بود",
      color: "error",
      icon: "i-heroicons-exclamation-circle",
    });
  }
};
</script>
