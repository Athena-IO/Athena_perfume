<template>
  <UInputNumber 
    v-model="count"
    :min="1"
    size="sm"
    color="neutral"
    variant="subtle"
    :increment="{ variant: 'ghost', size: 'xs' }"
    :decrement="{ variant: 'ghost', size: 'xs' }"
    class="w-32"
  />
</template>

<script setup>
const props = defineProps({
  modelValue: { type: Number, required: true },
});

const emit = defineEmits(["update:modelValue"]);

const count = computed({
  get: () => props.modelValue,
  set: (val) => emit("update:modelValue", val),
});
</script>
