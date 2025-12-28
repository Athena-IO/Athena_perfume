<template>
  <div class="p-6">
    <!-- Stats Cards at Top -->
    <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6" dir="rtl">
      <!-- Total Customers -->
      <UCard class="custom-card-bg">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon
              name="i-heroicons-users"
              class="size-5"
              style="color: #1a0a0c"
            />
            <span style="color: #1a0a0c">کل مشتریان</span>
          </div>
        </template>
        <div>
          <p class="text-3xl font-bold" style="color: #1a0a0c">
            {{ allUsers.length }}
          </p>
          <p class="text-sm mt-1" style="color: #1a0a0c">
            تعداد کل کاربران ثبت شده
          </p>
        </div>
      </UCard>

      <!-- New Customers This Week -->
      <UCard class="custom-card-bg">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon
              name="i-heroicons-user-plus"
              class="size-5"
              style="color: #1a0a0c"
            />
            <span style="color: #1a0a0c">مشتریان جدید این هفته</span>
          </div>
        </template>
        <div>
          <p class="text-3xl font-bold" style="color: #1a0a0c">
            {{ newCustomersThisWeek }}
          </p>
          <p class="text-sm mt-1" style="color: #1a0a0c">
            کاربران ثبت نام شده در ۷ روز گذشته
          </p>
        </div>
      </UCard>

      <!-- Active Users (Recent Purchases) -->
      <UCard class="custom-card-bg">
        <template #header>
          <div class="flex items-center gap-2">
            <UIcon
              name="i-heroicons-shopping-bag"
              class="size-5"
              style="color: #1a0a0c"
            />
            <span style="color: #1a0a0c">کاربران فعال</span>
          </div>
        </template>
        <div>
          <p class="text-3xl font-bold" style="color: #1a0a0c">
            {{ activeUsers }}
          </p>
          <p class="text-sm mt-1" style="color: #1a0a0c">
            خرید در ۲ هفته تا ۱ ماه اخیر
          </p>
        </div>
      </UCard>
    </div>

    <!-- Users Table -->
    <div dir="rtl">
      <UCard class="custom-card-bg">
        <template #header>
          <div class="flex justify-between items-center gap-4">
            <h2 class="text-xl font-bold" style="color: #1a0a0c">
              لیست کاربران
            </h2>

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
          :ui="tableUI"
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

          <template #purchaseValue-cell="{ row }">
            <span class="font-medium" style="color: #1a0a0c">
              {{ formatCurrency(row.original.purchaseValue) }}
            </span>
          </template>

          <template #purchaseQuantity-cell="{ row }">
            <span class="font-medium" style="color: #1a0a0c">
              {{ row.original.purchaseQuantity }} عدد
            </span>
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
            <div class="text-sm" style="color: #1a0a0c">
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
    </div>

    <!-- Modal for Delete -->
    <UModal v-model:open="showModal" :ui="modalUI">
      <template #header>
        <h3 class="text-lg font-semibold" style="color: #3b0510">حذف کاربر</h3>
      </template>

      <template #body>
        <div class="space-y-4" dir="rtl">
          <p style="color: #1a0a0c">
            آیا مطمئنید می‌خواهید کاربر
            <strong style="color: #3b0510">{{
              allUsers.find((u) => u.id === selectedId)?.username
            }}</strong>
            با شناسه
            <strong style="color: #3b0510">{{ selectedId }}</strong> را حذف
            کنید؟
          </p>

          <UFormField label="رمز امنیتی">
            <UInput
              v-model="password"
              type="password"
              placeholder="رمز را وارد کنید (مثلاً admin1234)"
            />
          </UFormField>

          <div v-if="error" class="text-sm" style="color: #dc2626">
            {{ error }}
          </div>
        </div>
      </template>

      <template #footer>
        <div class="flex justify-end gap-2">
          <UButton variant="outline" color="neutral" @click="closeModal">
            لغو
          </UButton>
          <UButton color="error" :disabled="!password" @click="confirmDelete">
            تایید حذف
          </UButton>
        </div>
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

definePageMeta({
  layout: "admin",
});

// UI Customizations
const tableUI = {
  th: "text-right",
  td: "text-right",
};

const modalUI = {
  root: "bg-[#D8CFC4]",
  header: "bg-[#D8CFC4] border-b border-[#D8CFC4]",
  body: "bg-[#D8CFC4]",
  footer: "bg-[#D8CFC4] border-t border-[#D8CFC4]",
};

// Stats calculations
const newCustomersThisWeek = computed(() => {
  // Mock calculation - Replace with actual date filtering
  return 12;
});

const activeUsers = computed(() => {
  // Mock calculation - Users with purchases in last 2 weeks to 1 month
  return 28;
});

// Format currency helper
const formatCurrency = (value) => {
  return new Intl.NumberFormat("fa-IR", {
    style: "currency",
    currency: "IRR",
    maximumFractionDigits: 0,
  }).format(value);
};

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
    id: "purchaseValue",
    accessorKey: "purchaseValue",
    header: "ارزش خرید",
  },
  {
    id: "purchaseQuantity",
    accessorKey: "purchaseQuantity",
    header: "تعداد خرید",
  },
  {
    id: "actions",
    header: "عملیات",
  },
];

// داده‌های نمونه با اطلاعات خرید
const allUsers = ref([
  // Admins
  {
    id: 101,
    username: "ali_admin",
    email: "ali@example.com",
    role: "admin",
    purchaseValue: 15000000,
    purchaseQuantity: 25,
  },
  {
    id: 105,
    username: "reza_manager",
    email: "reza@example.com",
    role: "admin",
    purchaseValue: 20000000,
    purchaseQuantity: 40,
  },
  {
    id: 420,
    username: "admin_test",
    email: "test@example.com",
    role: "admin",
    purchaseValue: 5000000,
    purchaseQuantity: 12,
  },
  {
    id: 301,
    username: "mahdi_admin",
    email: "mahdi@example.com",
    role: "admin",
    purchaseValue: 18000000,
    purchaseQuantity: 35,
  },
  {
    id: 305,
    username: "hamid_admin",
    email: "hamid@example.com",
    role: "admin",
    purchaseValue: 12000000,
    purchaseQuantity: 28,
  },
  {
    id: 401,
    username: "zahra_admin",
    email: "zahra@example.com",
    role: "admin",
    purchaseValue: 22000000,
    purchaseQuantity: 45,
  },
  {
    id: 405,
    username: "hasan_admin",
    email: "hasan@example.com",
    role: "admin",
    purchaseValue: 16000000,
    purchaseQuantity: 32,
  },
  {
    id: 501,
    username: "maryam_admin",
    email: "maryam@example.com",
    role: "admin",
    purchaseValue: 19000000,
    purchaseQuantity: 38,
  },
  {
    id: 505,
    username: "javad_admin",
    email: "javad@example.com",
    role: "admin",
    purchaseValue: 14000000,
    purchaseQuantity: 30,
  },
  {
    id: 601,
    username: "fatemeh_admin",
    email: "fatemeh@example.com",
    role: "admin",
    purchaseValue: 21000000,
    purchaseQuantity: 42,
  },

  // Users
  {
    id: 210,
    username: "sara_user",
    email: "sara@example.com",
    role: "user",
    purchaseValue: 3500000,
    purchaseQuantity: 8,
  },
  {
    id: 315,
    username: "mohammad_user",
    email: "mohammad@example.com",
    role: "user",
    purchaseValue: 4200000,
    purchaseQuantity: 10,
  },
  {
    id: 525,
    username: "user_demo",
    email: "demo@example.com",
    role: "user",
    purchaseValue: 2800000,
    purchaseQuantity: 6,
  },
  {
    id: 201,
    username: "amir_user",
    email: "amir@example.com",
    role: "user",
    purchaseValue: 5600000,
    purchaseQuantity: 14,
  },
  {
    id: 202,
    username: "neda_user",
    email: "neda@example.com",
    role: "user",
    purchaseValue: 3200000,
    purchaseQuantity: 7,
  },
  {
    id: 203,
    username: "arash_user",
    email: "arash@example.com",
    role: "user",
    purchaseValue: 4800000,
    purchaseQuantity: 11,
  },
  {
    id: 204,
    username: "niloofar_user",
    email: "niloofar@example.com",
    role: "user",
    purchaseValue: 6200000,
    purchaseQuantity: 15,
  },
  {
    id: 205,
    username: "pouya_user",
    email: "pouya@example.com",
    role: "user",
    purchaseValue: 3900000,
    purchaseQuantity: 9,
  },
  {
    id: 206,
    username: "shirin_user",
    email: "shirin@example.com",
    role: "user",
    purchaseValue: 5100000,
    purchaseQuantity: 12,
  },
  {
    id: 207,
    username: "kamran_user",
    email: "kamran@example.com",
    role: "user",
    purchaseValue: 4500000,
    purchaseQuantity: 10,
  },
  {
    id: 208,
    username: "leila_user",
    email: "leila@example.com",
    role: "user",
    purchaseValue: 3700000,
    purchaseQuantity: 8,
  },
  {
    id: 209,
    username: "behnam_user",
    email: "behnam@example.com",
    role: "user",
    purchaseValue: 5400000,
    purchaseQuantity: 13,
  },
  {
    id: 211,
    username: "azadeh_user",
    email: "azadeh@example.com",
    role: "user",
    purchaseValue: 2900000,
    purchaseQuantity: 6,
  },
  {
    id: 212,
    username: "mehran_user",
    email: "mehran@example.com",
    role: "user",
    purchaseValue: 4100000,
    purchaseQuantity: 9,
  },
  {
    id: 213,
    username: "nasim_user",
    email: "nasim@example.com",
    role: "user",
    purchaseValue: 6800000,
    purchaseQuantity: 16,
  },
  {
    id: 214,
    username: "davood_user",
    email: "davood@example.com",
    role: "user",
    purchaseValue: 3300000,
    purchaseQuantity: 7,
  },
  {
    id: 215,
    username: "sogol_user",
    email: "sogol@example.com",
    role: "user",
    purchaseValue: 5900000,
    purchaseQuantity: 14,
  },
  {
    id: 216,
    username: "saeed_user",
    email: "saeed@example.com",
    role: "user",
    purchaseValue: 4400000,
    purchaseQuantity: 10,
  },
  {
    id: 217,
    username: "parisa_user",
    email: "parisa@example.com",
    role: "user",
    purchaseValue: 3600000,
    purchaseQuantity: 8,
  },
  {
    id: 218,
    username: "vahid_user",
    email: "vahid@example.com",
    role: "user",
    purchaseValue: 5200000,
    purchaseQuantity: 12,
  },
  {
    id: 219,
    username: "elnaz_user",
    email: "elnaz@example.com",
    role: "user",
    purchaseValue: 2700000,
    purchaseQuantity: 5,
  },
  {
    id: 220,
    username: "omid_user",
    email: "omid@example.com",
    role: "user",
    purchaseValue: 4700000,
    purchaseQuantity: 11,
  },
  {
    id: 221,
    username: "sima_user",
    email: "sima@example.com",
    role: "user",
    purchaseValue: 3400000,
    purchaseQuantity: 7,
  },
  {
    id: 222,
    username: "kourosh_user",
    email: "kourosh@example.com",
    role: "user",
    purchaseValue: 6100000,
    purchaseQuantity: 15,
  },
  {
    id: 223,
    username: "mina_user",
    email: "mina@example.com",
    role: "user",
    purchaseValue: 3800000,
    purchaseQuantity: 9,
  },
  {
    id: 224,
    username: "navid_user",
    email: "navid@example.com",
    role: "user",
    purchaseValue: 5500000,
    purchaseQuantity: 13,
  },
  {
    id: 225,
    username: "yasmin_user",
    email: "yasmin@example.com",
    role: "user",
    purchaseValue: 4300000,
    purchaseQuantity: 10,
  },
  {
    id: 226,
    username: "babak_user",
    email: "babak@example.com",
    role: "user",
    purchaseValue: 3100000,
    purchaseQuantity: 6,
  },
  {
    id: 227,
    username: "nazanin_user",
    email: "nazanin@example.com",
    role: "user",
    purchaseValue: 5800000,
    purchaseQuantity: 14,
  },
  {
    id: 228,
    username: "ramin_user",
    email: "ramin@example.com",
    role: "user",
    purchaseValue: 4600000,
    purchaseQuantity: 11,
  },
  {
    id: 229,
    username: "sepideh_user",
    email: "sepideh@example.com",
    role: "user",
    purchaseValue: 3000000,
    purchaseQuantity: 6,
  },
  {
    id: 230,
    username: "masoud_user",
    email: "masoud@example.com",
    role: "user",
    purchaseValue: 5300000,
    purchaseQuantity: 12,
  },
  {
    id: 231,
    username: "taraneh_user",
    email: "taraneh@example.com",
    role: "user",
    purchaseValue: 4000000,
    purchaseQuantity: 9,
  },
  {
    id: 232,
    username: "shahab_user",
    email: "shahab@example.com",
    role: "user",
    purchaseValue: 6400000,
    purchaseQuantity: 15,
  },
  {
    id: 233,
    username: "golnaz_user",
    email: "golnaz@example.com",
    role: "user",
    purchaseValue: 3500000,
    purchaseQuantity: 8,
  },
  {
    id: 234,
    username: "ehsan_user",
    email: "ehsan@example.com",
    role: "user",
    purchaseValue: 5700000,
    purchaseQuantity: 13,
  },
  {
    id: 235,
    username: "mahnaz_user",
    email: "mahnaz@example.com",
    role: "user",
    purchaseValue: 4200000,
    purchaseQuantity: 10,
  },
  {
    id: 236,
    username: "farshad_user",
    email: "farshad@example.com",
    role: "user",
    purchaseValue: 2600000,
    purchaseQuantity: 5,
  },
  {
    id: 237,
    username: "roxana_user",
    email: "roxana@example.com",
    role: "user",
    purchaseValue: 6000000,
    purchaseQuantity: 14,
  },
  {
    id: 238,
    username: "soheil_user",
    email: "soheil@example.com",
    role: "user",
    purchaseValue: 4900000,
    purchaseQuantity: 11,
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

<style scoped>
.custom-card-bg {
  background-color: #d8cfc4;
}
</style>
