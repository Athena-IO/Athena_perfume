<script setup>
import { h, resolveComponent } from "vue";
import { useClipboard } from "@vueuse/core";

const UBadge = resolveComponent("UBadge");
const UButton = resolveComponent("UButton");
const UDropdownMenu = resolveComponent("UDropdownMenu");
const UCheckbox = resolveComponent("UCheckbox");

const toast = useToast();
const router = useRouter();
const { copy } = useClipboard();

const {
  data: perfumes,
  refresh,
  pending,
} = await useFetch("/api/perfumes", {
  lazy: true,
});

const table = useTemplateRef("table");

// Filter states
const searchQuery = ref("");
const selectedCategory = ref("all");
const selectedBrands = ref([]);
const selectedSort = ref("none");

// Table columns definition
const columns = [
  {
    id: "select",
    header: ({ table }) =>
      h(UCheckbox, {
        modelValue: table.getIsSomePageRowsSelected()
          ? "indeterminate"
          : table.getIsAllPageRowsSelected(),
        "onUpdate:modelValue": (value) =>
          table.toggleAllPageRowsSelected(!!value),
        "aria-label": "انتخاب همه",
      }),
    cell: ({ row }) =>
      h(UCheckbox, {
        modelValue: row.getIsSelected(),
        "onUpdate:modelValue": (value) => row.toggleSelected(!!value),
        "aria-label": "انتخاب ردیف",
      }),
    enableSorting: false,
    enableHiding: false,
  },
  {
    accessorKey: "image",
    header: "تصویر",
    cell: ({ row }) => {
      return h("img", {
        src: row.getValue("image") || "/placeholder.png",
        alt: row.original.name,
        class: "size-12 rounded-lg object-cover",
      });
    },
    enableSorting: false,
  },
  {
    accessorKey: "name",
    header: "نام عطر",
    cell: ({ row }) => {
      return h("div", { class: "space-y-1" }, [
        h("p", { class: "font-medium text-highlighted" }, row.getValue("name")),
        h("p", { class: "text-xs text-muted" }, row.original.slug),
      ]);
    },
  },
  {
    accessorKey: "brands",
    header: "برند",
    cell: ({ row }) => {
      const brands = row.original.brands || [];
      if (brands.length === 0) return h("span", { class: "text-muted" }, "-");

      return h(
        "div",
        { class: "flex flex-wrap gap-1" },
        brands.map((brand) =>
          h(
            UBadge,
            {
              variant: "subtle",
              color: "neutral",
              size: "xs",
            },
            () => brand.name
          )
        )
      );
    },
  },
  {
    accessorKey: "category",
    header: "دسته‌بندی",
    cell: ({ row }) => {
      const categoryMap = {
        male: { label: "مردانه", color: "info" },
        female: { label: "زنانه", color: "secondary" },
        unisex: { label: "یونیسکس", color: "neutral" },
      };
      const cat = categoryMap[row.getValue("category")];

      return h(
        UBadge,
        {
          variant: "subtle",
          color: cat.color,
        },
        () => cat.label
      );
    },
  },
  {
    accessorKey: "capacity",
    header: "موجودی",
    cell: ({ row }) => {
      const capacity = row.getValue("capacity");
      let color = "success";
      let label = "موجود";

      if (capacity === 0) {
        color = "error";
        label = "ناموجود";
      } else if (capacity <= 5) {
        color = "warning";
        label = `${capacity} عدد`;
      } else {
        label = `${capacity} عدد`;
      }

      return h("div", { class: "flex items-center gap-2" }, [
        h(UBadge, { variant: "subtle", color }, () => label),
      ]);
    },
  },
  {
    accessorKey: "originalPrice",
    header: () => h("div", { class: "text-right" }, "قیمت"),
    cell: ({ row }) => {
      const price = Number(row.getValue("originalPrice"));
      const discount = row.original.discountPercent || 0;
      const finalPrice = price - (price * discount) / 100;

      return h("div", { class: "text-right" }, [
        discount > 0
          ? h("div", { class: "space-y-1" }, [
              h(
                "p",
                { class: "font-medium text-success" },
                `${finalPrice.toLocaleString("fa-IR")} تومان`
              ),
              h(
                "p",
                { class: "text-xs text-muted line-through" },
                `${price.toLocaleString("fa-IR")} تومان`
              ),
            ])
          : h(
              "p",
              { class: "font-medium" },
              `${price.toLocaleString("fa-IR")} تومان`
            ),
      ]);
    },
  },
  {
    id: "actions",
    enableHiding: false,
    cell: ({ row }) => {
      const items = [
        [
          {
            type: "label",
            label: "عملیات",
          },
        ],
        [
          {
            label: "ویرایش",
            icon: "i-lucide-edit",
            onSelect() {
              editPerfume(row.original);
            },
          },
          {
            label: "کپی ID",
            icon: "i-lucide-copy",
            onSelect() {
              copy(row.original.id);
              toast.add({
                title: "شناسه کپی شد!",
                color: "success",
                icon: "i-lucide-circle-check",
              });
            },
          },
        ],
        [
          {
            label: "حذف",
            icon: "i-lucide-trash",
            color: "error",
            onSelect() {
              deletePerfume(row.original);
            },
          },
        ],
      ];

      return h(
        "div",
        { class: "text-right" },
        h(
          UDropdownMenu,
          {
            content: { align: "end" },
            items,
            "aria-label": "منوی عملیات",
          },
          () =>
            h(UButton, {
              icon: "i-lucide-ellipsis-vertical",
              color: "neutral",
              variant: "ghost",
              class: "ml-auto",
              "aria-label": "عملیات",
            })
        )
      );
    },
  },
];

// Filter and search logic
const filteredData = computed(() => {
  if (!perfumes.value) return [];

  let filtered = perfumes.value;

  // Category filter
  if (selectedCategory.value !== "all") {
    filtered = filtered.filter((p) => p.category === selectedCategory.value);
  }

  // Brand filter
  if (selectedBrands.value.length > 0) {
    filtered = filtered.filter((p) =>
      p.brands?.some((b) => selectedBrands.value.includes(b.slug))
    );
  }

  // Search query
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase();
    filtered = filtered.filter(
      (p) =>
        p.name.toLowerCase().includes(query) ||
        p.slug.toLowerCase().includes(query) ||
        p.brands?.some((b) => b.name.toLowerCase().includes(query))
    );
  }

  // Sorting
  if (selectedSort.value === "price_low_high") {
    filtered = [...filtered].sort((a, b) => a.originalPrice - b.originalPrice);
  } else if (selectedSort.value === "price_high_low") {
    filtered = [...filtered].sort((a, b) => b.originalPrice - a.originalPrice);
  } else if (selectedSort.value === "capacity_low") {
    filtered = [...filtered].sort((a, b) => a.capacity - b.capacity);
  }

  return filtered;
});

// Row selection
const rowSelection = ref({});

// Actions
function editPerfume(perfume) {
  router.push(`/edit_perfume/${perfume.id}`);
}

async function deletePerfume(perfume) {
  if (!confirm(`آیا مطمئن هستید که می‌خواهید "${perfume.name}" را حذف کنید؟`)) {
    return;
  }

  try {
    await $fetch(`/api/perfumes/${perfume.id}`, {
      method: "DELETE",
    });

    toast.add({
      title: "عطر حذف شد",
      description: `${perfume.name} با موفقیت حذف شد`,
      color: "success",
      icon: "i-lucide-check",
    });

    refresh();
  } catch (error) {
    toast.add({
      title: "خطا در حذف",
      description: "مشکلی در حذف عطر پیش آمد",
      color: "error",
      icon: "i-lucide-x",
    });
  }
}

async function deleteSelected() {
  const selected =
    table.value?.tableApi?.getFilteredSelectedRowModel().rows || [];

  if (selected.length === 0) {
    toast.add({
      title: "هیچ موردی انتخاب نشده",
      color: "warning",
    });
    return;
  }

  if (
    !confirm(`آیا مطمئن هستید که می‌خواهید ${selected.length} عطر را حذف کنید؟`)
  ) {
    return;
  }

  try {
    await Promise.all(
      selected.map((row) =>
        $fetch(`/api/perfumes/${row.original.id}`, { method: "DELETE" })
      )
    );

    toast.add({
      title: "عطرها حذف شدند",
      description: `${selected.length} عطر با موفقیت حذف شد`,
      color: "success",
    });

    rowSelection.value = {};
    refresh();
  } catch (error) {
    toast.add({
      title: "خطا در حذف",
      color: "error",
    });
  }
}

// Statistics
const stats = computed(() => {
  const data = perfumes.value || [];
  return {
    total: data.length,
    outOfStock: data.filter((p) => p.capacity === 0).length,
    lowStock: data.filter((p) => p.capacity > 0 && p.capacity <= 5).length,
    inStock: data.filter((p) => p.capacity > 5).length,
  };
});
</script>

<template>
  <div class="container mx-auto p-4 sm:p-6 max-w-7xl">
    <!-- Header -->
    <div class="mb-6 flex items-center justify-between">
      <div>
        <h1 class="text-2xl sm:text-3xl font-bold text-default">
          مدیریت عطرها
        </h1>
        <p class="text-sm text-muted mt-1">لیست و مدیریت عطرهای فروشگاه</p>
      </div>

      <UButton to="/add_perfume" color="primary" icon="i-lucide-plus" size="lg">
        افزودن عطر جدید
      </UButton>
    </div>

    <!-- Statistics Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
      <UCard>
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-lg bg-primary/10">
            <UIcon name="i-lucide-package" class="size-6 text-primary" />
          </div>
          <div>
            <p class="text-sm text-muted">کل عطرها</p>
            <p class="text-2xl font-bold text-highlighted">{{ stats.total }}</p>
          </div>
        </div>
      </UCard>

      <UCard>
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-lg bg-success/10">
            <UIcon name="i-lucide-check-circle" class="size-6 text-success" />
          </div>
          <div>
            <p class="text-sm text-muted">موجود</p>
            <p class="text-2xl font-bold text-success">{{ stats.inStock }}</p>
          </div>
        </div>
      </UCard>

      <UCard>
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-lg bg-warning/10">
            <UIcon name="i-lucide-alert-triangle" class="size-6 text-warning" />
          </div>
          <div>
            <p class="text-sm text-muted">کمبود موجودی</p>
            <p class="text-2xl font-bold text-warning">{{ stats.lowStock }}</p>
          </div>
        </div>
      </UCard>

      <UCard>
        <div class="flex items-center gap-3">
          <div class="p-3 rounded-lg bg-error/10">
            <UIcon name="i-lucide-x-circle" class="size-6 text-error" />
          </div>
          <div>
            <p class="text-sm text-muted">ناموجود</p>
            <p class="text-2xl font-bold text-error">{{ stats.outOfStock }}</p>
          </div>
        </div>
      </UCard>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-4 gap-6">
      <!-- Use the extracted filter component -->
      <div class="lg:col-span-1">
        <ProductFilter
          :selected-category="selectedCategory"
          :selected-brands="selectedBrands"
          :selected-sort="selectedSort"
          :filtered-count="filteredData.length"
          @update:category="selectedCategory = $event"
          @update:brands="selectedBrands = $event"
          @update:sort="selectedSort = $event"
        />
      </div>

      <!-- Main Table -->
      <div class="lg:col-span-3">
        <UCard>
          <template #header>
            <div
              class="flex flex-col sm:flex-row gap-3 items-start sm:items-center justify-between"
            >
              <!-- Search -->
              <UInput
                v-model="searchQuery"
                placeholder="جستجو بر اساس نام، برند یا اسلاگ..."
                icon="i-lucide-search"
                class="w-full sm:max-w-sm"
                size="md"
              />

              <!-- Bulk Actions -->
              <div class="flex items-center gap-2">
                <UButton
                  v-if="Object.keys(rowSelection).length > 0"
                  color="error"
                  variant="outline"
                  icon="i-lucide-trash"
                  size="sm"
                  @click="deleteSelected"
                >
                  حذف انتخاب‌شده‌ها
                </UButton>

                <UButton
                  color="neutral"
                  variant="outline"
                  icon="i-lucide-refresh-cw"
                  size="sm"
                  :loading="pending"
                  @click="refresh"
                >
                  بروزرسانی
                </UButton>
              </div>
            </div>
          </template>

          <!-- Table -->
          <UTable
            ref="table"
            v-model:row-selection="rowSelection"
            :data="filteredData"
            :columns="columns"
            :loading="pending"
            sticky
            class="min-h-[400px]"
          />

          <template #footer>
            <div class="flex items-center justify-between text-sm text-muted">
              <span>
                {{
                  table?.tableApi?.getFilteredSelectedRowModel().rows.length ||
                  0
                }}
                از {{ filteredData.length }} مورد انتخاب شده
              </span>
              <span> {{ filteredData.length }} مورد نمایش داده شده </span>
            </div>
          </template>
        </UCard>
      </div>
    </div>
  </div>
</template>
