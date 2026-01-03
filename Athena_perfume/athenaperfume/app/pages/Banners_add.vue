<!-- pages/admin/banners.vue -->
<template>
  <div class="container mx-auto px-4 py-8 max-w-6xl">
    <div class="mb-8">
      <h1 class="text-3xl font-bold mb-2">Banner Management</h1>
      <p class="text-muted">Manage up to 4 banners for your homepage carousel</p>
    </div>

    <!-- Add New Banner Form -->
    <UCard class="mb-8">
      <template #header>
        <div class="flex items-center justify-between">
          <h2 class="text-xl font-semibold">Add New Banner</h2>
          <UBadge :color="bannersStore.banners.length >= 4 ? 'error' : 'success'">
            {{ bannersStore.banners.length }}/4 Banners
          </UBadge>
        </div>
      </template>

      <div class="space-y-4">
        <!-- Image Upload -->
        <div>
          <label class="block text-sm font-medium mb-2">Banner Image *</label>
          <UFileUpload
            v-model="form.image"
            accept="image/*"
            icon="i-lucide-image"
            label="Drop your banner image here"
            description="PNG, JPG or WebP (Recommended: 1920x600px)"
            class="min-h-48"
          />
          
          <!-- Image Preview -->
          <div v-if="form.image" class="mt-4">
            <p class="text-sm font-medium mb-2">Preview:</p>
            <div class="relative w-full h-48 rounded-lg overflow-hidden border border-default">
              <img
                :src="createPreviewUrl(form.image)"
                :alt="form.name || 'Preview'"
                class="w-full h-full object-cover"
              >
            </div>
          </div>
        </div>

        <!-- Name Input -->
        <div>
          <label class="block text-sm font-medium mb-2">Banner Name *</label>
          <UInput
            v-model="form.name"
            placeholder="e.g., Summer Sale 2024"
            size="lg"
          />
          <p class="text-xs text-muted mt-1">Used for accessibility and identification</p>
        </div>

        <!-- Link Input -->
        <div>
          <label class="block text-sm font-medium mb-2">Link (Optional)</label>
          <UInput
            v-model="form.link"
            placeholder="e.g., /products/sale"
            size="lg"
          />
          <p class="text-xs text-muted mt-1">Where users go when they click the banner</p>
        </div>

        <!-- Add Button -->
        <div class="flex justify-end pt-4">
          <UButton
            label="Add Banner"
            icon="i-lucide-plus"
            size="lg"
            :loading="isAdding"
            :disabled="bannersStore.banners.length >= 4 || !form.image || !form.name"
            @click="addBanner"
          />
        </div>
      </div>
    </UCard>

    <!-- Current Banners -->
    <div>
      <h2 class="text-xl font-semibold mb-4">Current Banners</h2>

      <div v-if="bannersStore.loading" class="text-center py-12">
        <UIcon name="i-lucide-loader-2" class="animate-spin text-4xl text-muted" />
        <p class="text-muted mt-2">Loading banners...</p>
      </div>

      <div v-else-if="bannersStore.banners.length === 0" class="text-center py-12 border border-dashed border-default rounded-lg">
        <UIcon name="i-lucide-image-off" class="text-4xl text-muted mb-2" />
        <p class="text-muted">No banners added yet</p>
      </div>

      <div v-else class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <UCard
          v-for="banner in bannersStore.banners"
          :key="banner.id"
          class="relative"
        >
          <template #header>
            <div class="flex items-center justify-between">
              <h3 class="font-semibold truncate">{{ banner.name }}</h3>
              <UButton
                icon="i-lucide-trash-2"
                color="error"
                variant="ghost"
                size="sm"
                @click="removeBanner(banner.id)"
              />
            </div>
          </template>

          <!-- Banner Preview -->
          <div class="space-y-3">
            <div class="relative w-full h-40 rounded-lg overflow-hidden border border-default group">
              <img
                :src="banner.image"
                :alt="banner.name"
                class="w-full h-full object-cover transition-transform group-hover:scale-105"
              >
              
              <!-- Hover overlay -->
              <div class="absolute inset-0 bg-black/60 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                <UIcon name="i-lucide-eye" class="text-white text-2xl" />
              </div>
            </div>

            <!-- Banner Info -->
            <div class="space-y-1">
              <div class="flex items-center text-sm">
                <UIcon name="i-lucide-tag" class="mr-2 text-muted" />
                <span class="text-muted">Name:</span>
                <span class="ml-2 font-medium">{{ banner.name }}</span>
              </div>
              
              <div v-if="banner.link" class="flex items-center text-sm">
                <UIcon name="i-lucide-link" class="mr-2 text-muted" />
                <span class="text-muted">Link:</span>
                <ULink :to="banner.link" class="ml-2 truncate">
                  {{ banner.link }}
                </ULink>
              </div>
              
              <div v-else class="flex items-center text-sm">
                <UIcon name="i-lucide-link-off" class="mr-2 text-muted" />
                <span class="text-muted">No link attached</span>
              </div>
            </div>
          </div>
        </UCard>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useBannersStore } from '~/stores/banners'

const toast = useToast()

const isAdding = ref(false)

const form = reactive({
  image: null,
  name: '',
  link: ''
})

// Pinia store
const bannersStore = useBannersStore()

// Add banner
async function addBanner() {
  if (bannersStore.banners.length >= 4) {
    toast.add({
      title: 'Maximum Reached',
      description: 'You can only have up to 4 banners. Please remove one to add a new banner.',
      color: 'error',
      timeout: 5000
    })
    return
  }

  if (!form.image || !form.name) {
    toast.add({
      title: 'Validation Error',
      description: 'Please provide an image and name',
      color: 'error'
    })
    return
  }

  isAdding.value = true

  try {
    const formData = new FormData()
    formData.append('image', form.image)
    formData.append('name', form.name)
    formData.append('link', form.link || '')

    await bannersStore.addBanner(formData)

    // Reset form
    form.image = null
    form.name = ''
    form.link = ''

    toast.add({
      title: 'Success',
      description: 'Banner added successfully',
      color: 'success'
    })
  } catch (error) {
    toast.add({
      title: 'Error',
      description: error?.message || 'Failed to add banner',
      color: 'error'
    })
  } finally {
    isAdding.value = false
  }
}

// Remove banner
async function removeBanner(id) {
  try {
    await bannersStore.removeBanner(id)

    toast.add({
      title: 'Success',
      description: 'Banner removed successfully',
      color: 'success'
    })
  } catch (error) {
    toast.add({
      title: 'Error',
      description: 'Failed to remove banner',
      color: 'error'
    })
  }
}

function createPreviewUrl(file) {
  return URL.createObjectURL(file)
}

onMounted(() => {
  bannersStore.fetchBanners()
})
</script>
