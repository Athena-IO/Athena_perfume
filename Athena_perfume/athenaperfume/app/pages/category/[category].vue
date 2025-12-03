<script setup>
import ProductList from "~/components/ProductList.vue";
import { useRoute } from "vue-router";

const route = useRoute();
const category = route.params.category || "all";
</script>

<template>
  <ProductList :category="category" />
</template>
