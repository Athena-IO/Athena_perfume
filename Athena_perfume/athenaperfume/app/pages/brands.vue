<!-- pages/admin/brands.vue -->
<template>
  <div class="container mx-auto px-4 py-8 max-w-6xl">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Brand Management</h1>
      <p class="text-muted">
        Add brands with logo and generate links like /product_brand/[brand]
      </p>
    </div>

    <!-- Add Brand -->
    <UCard class="mb-8">
      <template #header>
        <h2 class="text-xl font-semibold">Add New Brand</h2>
      </template>

      <div class="space-y-4">
        <!-- Image -->
        <div>
          <label class="block text-sm font-medium mb-2">Brand Image *</label>
          <UFileUpload
            v-model="form.image"
            accept="image/*"
            icon="i-lucide-image"
            label="Drop your brand image here"
            description="PNG, JPG or WebP"
            class="min-h-32"
          />
        </div>

        <!-- Name -->
        <div>
          <label class="block text-sm font-medium mb-2">Brand Name *</label>
          <UInput v-model="form.name" placeholder="e.g., Nike" size="lg" />
        </div>

        <!-- Slug (editable) -->
        <div>
          <label class="block text-sm font-medium mb-2">Slug *</label>
          <UInput v-model="form.slug" placeholder="e.g., nike" size="lg" />
          <p class="text-xs text-muted mt-1">
            Link will be: <code>/product_brand/{{ form.slug }}</code>
          </p>
        </div>

        <div class="flex justify-end pt-4">
          <UButton
            label="Add Brand"
            icon="i-lucide-plus"
            size="lg"
            :loading="isAdding"
            :disabled="!form.image || !form.name || !form.slug"
            @click="handleAddBrand"
          />
        </div>
      </div>
    </UCard>

    <!-- Existing brands -->
    <div>
      <h2 class="text-xl font-semibold mb-4">Current Brands</h2>

      <div v-if="brandsStore.loading" class="text-center py-12">
        <UIcon
          name="i-lucide-loader-2"
          class="animate-spin text-4xl text-muted"
        />
        <p class="text-muted mt-2">Loading brands...</p>
      </div>

      <div
        v-else-if="brandsStore.brands.length === 0"
        class="text-center py-12 border border-dashed border-default rounded-lg"
      >
        <UIcon name="i-lucide-image-off" class="text-4xl text-muted mb-2" />
        <p class="text-muted">No brands added yet</p>
      </div>

      <div v-else>
        <BrandCards
          :brands="brandsStore.brands"
          @view="viewBrand"
          @delete="confirmDeleteBrand"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { useBrandsStore } from '~/stores/brands'

const toast = useToast();
const router = useRouter();

// Pinia store
const brandsStore = useBrandsStore();

const isAdding = ref(false);

const form = reactive({
  image: null,
  name: "",
  slug: "",
});

// auto-generate slug from name if slug is empty
watch(
  () => form.name,
  (val) => {
    if (!form.slug) {
      form.slug = val
        .trim()
        .toLowerCase()
        .replace(/\s+/g, "-")
        .replace(/[^a-z0-9-]/g, "");
    }
  }
);

async function handleAddBrand() {
  if (!form.image || !form.name || !form.slug) {
    toast.add({
      title: "Validation Error",
      description: "Please provide an image, name and slug",
      color: "error",
    });
    return;
  }

  isAdding.value = true;
  try {
    const formData = new FormData();
    formData.append("image", form.image);
    formData.append("name", form.name);
    formData.append("slug", form.slug);

    await brandsStore.addBrand(formData);

    form.image = null;
    form.name = "";
    form.slug = "";

    toast.add({
      title: "Success",
      description: "Brand added successfully",
      color: "success",
    });
  } catch (error) {
    toast.add({
      title: "Error",
      description: error?.message || "Failed to add brand",
      color: "error",
    });
  } finally {
    isAdding.value = false;
  }
}

function viewBrand(brand) {
  router.push(`/product_brand/${brand.slug}`);
}

async function confirmDeleteBrand(brand) {
  try {
    await brandsStore.deleteBrand(brand.id);
    toast.add({
      title: "Success",
      description: "Brand removed successfully",
      color: "success",
    });
  } catch (error) {
    toast.add({
      title: "Error",
      description: "Failed to remove brand",
      color: "error",
    });
  }
}

onMounted(() => {
  brandsStore.fetchBrands();
});
</script>
