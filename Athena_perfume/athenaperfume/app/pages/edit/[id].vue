<script setup>
const route = useRoute();
const router = useRouter();
const toast = useToast();

const {
  data: perfume,
  pending,
  error,
} = await useFetch(`/api/perfumes/${route.params.id}`);

if (error.value) {
  toast.add({
    title: "خطا",
    description: "عطر مورد نظر یافت نشد",
    color: "error",
    icon: "i-lucide-x",
  });
  router.push("/perfume_gallery"); // یا هر صفحه‌ای که لیست عطرها هست
}
</script>

<template>
  <div v-if="pending" class="container mx-auto p-4 sm:p-6 max-w-6xl">
    <div class="flex items-center justify-center min-h-[400px]">
      <UIcon
        name="i-lucide-loader-2"
        class="size-8 animate-spin text-primary"
      />
    </div>
  </div>

  <PerfumeForm v-else-if="perfume" mode="edit" :perfume="perfume" />
</template>
