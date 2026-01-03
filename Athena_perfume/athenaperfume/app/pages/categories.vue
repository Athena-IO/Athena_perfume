<template>
  <UContainer>
    <h1 class="font-bold text-2xl mb-4">مدیریت دسته‌بندی‌ها</h1>
    <UCard>
      <template #header>
        <h3 class="font-semibold text-lg">افزودن دسته‌بندی جدید</h3>
      </template>
      <div class="flex items-center gap-2 mb-4">
        <UInput v-model="newLabel" placeholder="عنوان دسته‌بندی (فارسی)" />
        <UInput v-model="newValue" placeholder="شناسه انگلیسی (مثال: male)" />
        <UInput v-model="newDescription" placeholder="توضیح (اختیاری)" />
        <UButton color="primary" @click="addNewCategory">افزودن</UButton>
      </div>
      <UAlert v-if="error" color="danger" class="mb-2">{{ error }}</UAlert>
      <UList>
        <UTemplate v-for="cat in categories" :key="cat.value">
          <li class="py-2 border-b"> <strong>{{ cat.label }}</strong> <span class="text-xs text-gray-500">({{ cat.value }})</span> - {{ cat.description }} </li>
        </UTemplate>
      </UList>
    </UCard>
  </UContainer>
</template>

<script setup>
import { ref } from 'vue';
import { useCategories } from '~/composables/useCategories.js';

const { categories, addCategory } = useCategories();

const newLabel = ref('');
const newValue = ref('');
const newDescription = ref('');
const error = ref('');

function addNewCategory() {
  if (!newLabel.value || !newValue.value) {
    error.value = 'عنوان و شناسه انگلیسی هر دو الزامی است';
    return;
  }
  addCategory({
    label: newLabel.value,
    value: newValue.value,
    description: newDescription.value,
  });
  error.value = '';
  newLabel.value = '';
  newValue.value = '';
  newDescription.value = '';
}
</script>

