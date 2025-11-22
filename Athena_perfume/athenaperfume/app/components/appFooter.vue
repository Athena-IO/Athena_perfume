<template>
  <footer class="bg-white border-t border-gray-200">
    <UContainer class="py-12 lg:py-16">
      <div
        class="grid grid-cols-2 lg:grid-cols-4 gap-10 lg:gap-16 text-center lg:text-right"
      >
        <!-- ۱. لوگو و اطلاعات تماس (سمت چپ در دسکتاپ) -->
        <div class="space-y-6 lg:col-span-1 order-1">
          <div class="flex flex-col items-center lg:items-start gap-4">
            <!-- لوگو + اسم سایت -->
            <div class="flex items-center gap-3">
              <img src="" alt="لوگو" class="w-12 h-12" />
              <span class="font-bold text-lg">اسم سایت</span>
            </div>
            <p class="text-xs text-gray-500">
              بهترین عطرها، رقابتی‌ترین قیمت‌ها
            </p>
          </div>

          <div class="space-y-3 text-sm text-gray-600">
            <p class="font-semibold">تلفن ۲۴/۷:</p>
            <p class="font-mono">021-333-4445678</p>
            <p class="font-mono">021-333-4445679</p>

            <div
              class="flex items-center justify-center lg:justify-start gap-2 mt-4"
            >
              <UIcon name="i-heroicons-map-pin" class="w-5 h-5 text-primary" />
              <p class="text-xs">
                تهران، خیابان ولیعصر، پلاک ۱۲۳، طبقه ۶، واحد ۶۰۸
              </p>
            </div>
          </div>
        </div>

        <!-- ۲. پشتیبانی مشتریان -->
        <div class="space-y-4 order-3 lg:order-2">
          <h3 class="font-bold text-gray-900">پشتیبانی مشتریان</h3>
          <ul class="space-y-3 text-sm text-gray-600">
            <li>
              <NuxtLink to="/contact" class="hover:text-primary transition"
                >تماس با ما</NuxtLink
              >
            </li>
            <li>
              <NuxtLink to="/faq" class="hover:text-primary transition"
                >سوالات متداول</NuxtLink
              >
            </li>
            <li>
              <NuxtLink to="/shipping" class="hover:text-primary transition"
                >راهنمای ارسال</NuxtLink
              >
            </li>
            <li>
              <NuxtLink to="/return" class="hover:text-primary transition"
                >شرایط بازگشت کالا</NuxtLink
              >
            </li>
          </ul>
        </div>

        <!-- ۳. ویژه‌ها -->
        <div class="space-y-4 order-4 lg:order-3">
          <h3 class="font-bold text-gray-900">ویژه‌ها</h3>
          <ul class="space-y-3 text-sm text-gray-600">
            <li>
              <NuxtLink to="/bestsellers" class="hover:text-primary transition"
                >پرفروش‌ترین‌ها</NuxtLink
              >
            </li>
            <li>
              <NuxtLink to="/new" class="hover:text-primary transition"
                >جدیدترین عطرها</NuxtLink
              >
            </li>
            <li>
              <NuxtLink to="/discount" class="hover:text-primary transition"
                >تخفیف‌های ویژه</NuxtLink
              >
            </li>
            <li>
              <NuxtLink to="/gift" class="hover:text-primary transition"
                >هدیه سازمانی</NuxtLink
              >
            </li>
          </ul>
        </div>

        <!-- ۴. دسته‌بندی‌ها -->
        <div class="space-y-4 order-2 lg:order-4">
          <h3 class="font-bold text-gray-900">دسته‌بندی‌ها</h3>
          <ul class="space-y-3 text-sm text-gray-600">
            <li>
              <NuxtLink to="/men" class="hover:text-primary transition"
                >عطر مردانه</NuxtLink
              >
            </li>
            <li>
              <NuxtLink to="/women" class="hover:text-primary transition"
                >عطر زنانه</NuxtLink
              >
            </li>
            <li>
              <NuxtLink to="/unisex" class="hover:text-primary transition"
                >یونیسکس</NuxtLink
              >
            </li>
            <li>
              <NuxtLink to="/miniature" class="hover:text-primary transition"
                >مینیاتوری</NuxtLink
              >
            </li>
          </ul>
        </div>
      </div>

      <!-- خط جداکننده و پایین‌ترین بخش -->
      <div class="mt-12 pt-8 border-t border-gray-200">
        <div
          class="flex flex-col lg:flex-row items-center justify-between gap-6"
        >
          <!-- کپی‌رایت -->
          <p class="text-xs text-gray-500 order-2 lg:order-1">
            © {{ new Date().getFullYear() }} اسم سایت - تمامی حقوق محفوظ است
          </p>

          <!-- شبکه‌های اجتماعی -->
          <div class="flex items-center gap-6 order-1 lg:order-2">
            <UButton
              icon="i-simple-icons-telegram"
              size="lg"
              color="neutral"
              variant="ghost"
              to="https://t.me/yourchannel"
              target="_blank"
              aria-label="Telegram"
            />
            <UButton
              icon="i-simple-icons-instagram"
              size="lg"
              color="neutral"
              variant="ghost"
              to="https://instagram.com/yourpage"
              target="_blank"
              aria-label="Instagram"
            />
            <UButton
              icon="i-simple-icons-whatsapp"
              size="lg"
              color="neutral"
              variant="ghost"
              to="https://wa.me/989123456789"
              target="_blank"
              aria-label="WhatsApp"
            />
          </div>
        </div>
      </div>
    </UContainer>
  </footer>
</template>

<script setup lang="ts">
import type { FooterColumn } from "@nuxt/ui";

const columns: FooterColumn[] = [
  {
    label: "پشتیبانی مشتریان",
    children: [
      {
        label: "تماس با ما",
        to: "/contact",
      },
      {
        label: "سوالات متداول",
        to: "/faq",
      },
      {
        label: "راهنمای خرید",
        to: "/guide",
      },
    ],
  },
  {
    label: "درباره ما",
    children: [
      {
        label: "تاریخچه",
        to: "/about",
      },
      {
        label: "تیم ما",
        to: "/team",
      },
    ],
  },
  {
    label: "اطلاعات قانونی",
    children: [
      {
        label: "قوانین و مقررات",
        to: "/terms",
      },
      {
        label: "حریم خصوصی",
        to: "/privacy",
      },
    ],
  },
];
</script>
