<script setup>
const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  // Already selected brands to prevent duplicates
  selectedBrands: {
    type: Array,
    default: () => [],
  },
});

const emit = defineEmits(["update:modelValue", "select"]);

const { brands, loading, fetchBrands } = useBrands();
const searchTerm = ref("");

const open = computed({
  get: () => props.modelValue,
  set: (value) => emit("update:modelValue", value),
});

// Fetch brands when modal opens
watch(open, (isOpen) => {
  if (isOpen && brands.value.length === 0) {
    fetchBrands();
  }
});

// Filter out already selected brands and apply search
const filteredBrands = computed(() => {
  let result = brands.value;

  // Filter out already selected brands
  const selectedIds = props.selectedBrands.map((b) => b.id);
  result = result.filter((brand) => !selectedIds.includes(brand.id));

  // Apply search filter
  if (searchTerm.value) {
    const search = searchTerm.value.toLowerCase();
    result = result.filter(
      (brand) =>
        brand.name.toLowerCase().includes(search) ||
        brand.slug.toLowerCase().includes(search)
    );
  }

  return result;
});

function selectBrand(brand) {
  // Emit only the necessary fields for the perfume form
  emit("select", {
    id: brand.id,
    name: brand.name,
    slug: brand.slug,
    image: brand.image,
  });
  searchTerm.value = "";
}
</script>

<template>
  <UModal
    v-model:open="open"
    title="انتخاب برند"
    description="برند مورد نظر را برای عطر انتخاب کنید"
    :ui="{ footer: 'justify-end' }"
  >
    <template #body>
      <div class="space-y-4">
        <!-- Search Input -->
        <UInput
          v-model="searchTerm"
          icon="i-lucide-search"
          placeholder="جستجوی برند..."
          size="lg"
        />

        <!-- Loading State -->
        <div
          v-if="loading"
          class="flex flex-col items-center justify-center py-12"
        >
          <UIcon
            name="i-lucide-loader-2"
            class="animate-spin text-4xl text-muted mb-2"
          />
          <p class="text-sm text-muted">در حال بارگذاری برندها...</p>
        </div>

        <!-- Empty State - No brands at all -->
        <div
          v-else-if="brands.length === 0"
          class="text-center py-12 border border-dashed border-default rounded-lg"
        >
          <UIcon name="i-lucide-image-off" class="text-4xl text-muted mb-2" />
          <p class="text-muted mb-3">هنوز برندی اضافه نشده است</p>
          <NuxtLink to="/admin/brands">
            <UButton
              label="افزودن برند جدید"
              icon="i-lucide-plus"
              size="sm"
              color="primary"
            />
          </NuxtLink>
        </div>

        <!-- Empty State - No search results or all selected -->
        <div
          v-else-if="filteredBrands.length === 0"
          class="text-center py-12 border border-dashed border-default rounded-lg"
        >
          <UIcon name="i-lucide-search-x" class="text-4xl text-muted mb-2" />
          <p class="text-muted">
            {{
              searchTerm
                ? "برندی با این جستجو پیدا نشد"
                : "همه برندها انتخاب شده‌اند"
            }}
          </p>
        </div>

        <!-- Brand List -->
        <div v-else class="space-y-2 max-h-96 overflow-y-auto">
          <button
            v-for="brand in filteredBrands"
            :key="brand.id"
            type="button"
            class="w-full flex items-center gap-3 p-3 rounded-lg border border-default hover:bg-elevated hover:border-primary/50 transition-all text-right group"
            @click="selectBrand(brand)"
          >
            <!-- Brand Image -->
            <div class="relative shrink-0">
              <img
                v-if="brand.image"
                :src="brand.image"
                :alt="brand.name"
                class="size-14 object-cover rounded-lg ring-1 ring-default"
              />
              <div
                v-else
                class="size-14 bg-elevated rounded-lg flex items-center justify-center ring-1 ring-default"
              >
                <UIcon name="i-lucide-image" class="size-6 text-muted" />
              </div>

              <!-- Hover overlay -->
              <div
                class="absolute inset-0 bg-primary/10 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity"
              />
            </div>

            <!-- Brand Info -->
            <div class="flex-1 min-w-0">
              <p
                class="font-semibold text-default truncate group-hover:text-primary transition-colors"
              >
                {{ brand.name }}
              </p>
              <p class="text-xs text-muted truncate mt-0.5">
                /product_brand/{{ brand.slug }}
              </p>
            </div>

            <!-- Add Icon -->
            <UIcon
              name="i-lucide-plus-circle"
              class="size-5 text-muted group-hover:text-primary shrink-0 transition-colors"
            />
          </button>
        </div>
      </div>
    </template>

    <template #footer="{ close }">
      <UButton
        label="بستن"
        color="neutral"
        variant="outline"
        icon="i-lucide-x"
        @click="close"
      />
    </template>
  </UModal>
</template>
