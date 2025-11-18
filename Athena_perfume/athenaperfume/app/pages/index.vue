<template>
  <div class="w-full px-4 sm:px-6 lg:px-8">
    <div class="grid lg:grid-cols-2 grid-cols-1 items-center min-h-[70vh]">
      <div class="pl-25">
        <img
          src="https://cdn.mos.cms.futurecdn.net/VzUqgr8pfbNcfXrpzeVBPE.jpg"
          alt=""
          class="w-full h-auto rounded-lg"
        />
      </div>

      <div class="flex flex-col gap-6 text-right items-start pr-56" dir="rtl">
        <h2 class="text-4xl font-bold">کیفیت دیدتان را تغییر دهید</h2>
        <p class="text-xl font-bold">رایحه مخصوص به خودتان را کشف کنید!</p>
        <p class="text-xl font-bold">بهترین کیفیت! مناسب ترین قیمت!</p>

        <div class="flex gap-4 mt-4 pr-15">
          <UButton
            color="primary"
            variant="solid"
            size="xl"
            class="px-12 py-4 text-lg"
            >مردانه</UButton
          >
          <UButton
            color="neutral"
            variant="outline"
            size="xl"
            class="px-12 py-4 text-lg"
            >زنانه</UButton
          >
        </div>
      </div>
    </div>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-4 gap-6 p-6">
    <ProductCard
      v-for="product in products"
      :key="product.id"
      :product="product"
    />
  </div>
</template>
<script setup>
const products = [
  {
    id: 1,
    name: "Product Name",
    image: "/images/product1.jpg",
    rating: 4.5,
    price: 29.99,
  },
];
</script>
