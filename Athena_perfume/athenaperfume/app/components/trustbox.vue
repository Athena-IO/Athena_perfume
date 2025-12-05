<template>
  <div class="min-h-screen">
    <!-- Hero Section -->
    <UContainer>
      <div class="py-12 sm:py-16 lg:py-20">
        <div class="text-center max-w-3xl mx-auto">
          <UBadge
            color="primary"
            variant="subtle"
            size="lg"
            class="mb-4"
          >
            سوالات متداول
          </UBadge>
          <h1 class="text-4xl sm:text-5xl lg:text-6xl font-bold text-gray-900 dark:text-white mb-6">
            سوالات شما، پاسخ‌های ما
          </h1>
          <p class="text-lg sm:text-xl text-gray-600 dark:text-gray-400">
            پاسخ سوالات رایج درباره محصولات، خدمات و نحوه خرید از فروشگاه عطر ما
          </p>
        </div>
      </div>
    </UContainer>

    <!-- FAQ Sections -->
    <UContainer>
      <div class="pb-20">
        <div class="grid gap-8 lg:gap-12">
          <!-- محصولات -->
          <div>
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 rounded-lg bg-primary/10">
                <UIcon name="i-lucide-package" class="size-6 text-primary" />
              </div>
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
                درباره محصولات
              </h2>
            </div>
            <UCard>
              <UAccordion
                :items="productQuestions"
                type="single"
                :ui="{
                  trigger: 'text-base py-4',
                  body: 'text-base text-gray-600 dark:text-gray-400 pb-4'
                }"
              >
                <template #body="{ item }">
                  <div v-html="item.content"></div>
                </template>
              </UAccordion>
            </UCard>
          </div>

          <!-- خرید و ارسال -->
          <div>
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 rounded-lg bg-success/10">
                <UIcon name="i-lucide-shopping-cart" class="size-6 text-success" />
              </div>
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
                خرید و ارسال
              </h2>
            </div>
            <UCard>
              <UAccordion
                :items="shippingQuestions"
                type="single"
                :ui="{
                  trigger: 'text-base py-4',
                  body: 'text-base text-gray-600 dark:text-gray-400 pb-4'
                }"
              >
                <template #body="{ item }">
                  <div v-html="item.content"></div>
                </template>
              </UAccordion>
            </UCard>
          </div>

          <!-- اصالت و کیفیت -->
          <div>
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 rounded-lg bg-warning/10">
                <UIcon name="i-lucide-shield-check" class="size-6 text-warning" />
              </div>
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
                اصالت و کیفیت
              </h2>
            </div>
            <UCard>
              <UAccordion
                :items="qualityQuestions"
                type="single"
                :ui="{
                  trigger: 'text-base py-4',
                  body: 'text-base text-gray-600 dark:text-gray-400 pb-4'
                }"
              >
                <template #body="{ item }">
                  <div v-html="item.content"></div>
                </template>
              </UAccordion>
            </UCard>
          </div>

          <!-- مرجوعی و گارانتی -->
          <div>
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 rounded-lg bg-error/10">
                <UIcon name="i-lucide-rotate-ccw" class="size-6 text-error" />
              </div>
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
                مرجوعی و گارانتی
              </h2>
            </div>
            <UCard>
              <UAccordion
                :items="returnQuestions"
                type="single"
                :ui="{
                  trigger: 'text-base py-4',
                  body: 'text-base text-gray-600 dark:text-gray-400 pb-4'
                }"
              >
                <template #body="{ item }">
                  <div v-html="item.content"></div>
                </template>
              </UAccordion>
            </UCard>
          </div>

          <!-- راهنمای انتخاب -->
          <div>
            <div class="flex items-center gap-3 mb-6">
              <div class="p-2 rounded-lg bg-info/10">
                <UIcon name="i-lucide-lightbulb" class="size-6 text-info" />
              </div>
              <h2 class="text-2xl font-bold text-gray-900 dark:text-white">
                راهنمای انتخاب عطر
              </h2>
            </div>
            <UCard>
              <UAccordion
                :items="guidanceQuestions"
                type="single"
                :ui="{
                  trigger: 'text-base py-4',
                  body: 'text-base text-gray-600 dark:text-gray-400 pb-4'
                }"
              >
                <template #body="{ item }">
                  <div v-html="item.content"></div>
                </template>
              </UAccordion>
            </UCard>
          </div>
        </div>
      </div>
    </UContainer>

    <!-- Contact CTA -->
    <div class="bg-gray-50 dark:bg-gray-900 border-t border-gray-200 dark:border-gray-800">
      <UContainer>
        <div class="py-12 sm:py-16">
          <UCard class="max-w-2xl mx-auto">
            <div class="text-center">
              <div class="inline-flex p-3 rounded-full bg-primary/10 mb-4">
                <UIcon name="i-lucide-help-circle" class="size-8 text-primary" />
              </div>
              <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                سوال دیگری دارید؟
              </h3>
              <p class="text-gray-600 dark:text-gray-400 mb-6">
                تیم پشتیبانی ما آماده پاسخگویی به سوالات شماست
              </p>
              <div class="flex flex-col sm:flex-row gap-3 justify-center">
                <UButton
                  to="/contact"
                  size="lg"
                  icon="i-lucide-mail"
                  color="primary"
                >
                  تماس با ما
                </UButton>
                <UButton
                  href="tel:02112345678"
                  size="lg"
                  icon="i-lucide-phone"
                  color="neutral"
                  variant="outline"
                >
                  تماس تلفنی
                </UButton>
              </div>
            </div>
          </UCard>
        </div>
      </UContainer>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

// SEO Meta
useHead({
  title: "سوالات متداول - فروشگاه عطر",
  meta: [
    {
      name: "description",
      content:
        "پاسخ سوالات متداول درباره خرید عطر، اصالت محصولات، نحوه ارسال و گارانتی",
    },
  ],
});

// درباره محصولات
const productQuestions = ref([
  {
    label: "محصولات شما اصل هستند؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">بله، تمامی محصولات ما 100% اصل و اورجینال هستند و مستقیماً از نمایندگی‌های معتبر و برندهای اصلی تهیه می‌شوند.</p>
      <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
        <li>واردات مستقیم از کشورهای اصلی</li>
        <li>دارای بارکد و هولوگرام اصالت</li>
        <li>گارانتی بازگشت وجه در صورت عدم اصالت</li>
      </ul>
    `,
  },
  {
    label: "چه برندهایی دارید؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">ما طیف وسیعی از برندهای معتبر جهانی را عرضه می‌کنیم:</p>
      <ul class="list-disc list-inside space-y-1 text-gray-600 dark:text-gray-400">
        <li><strong>برندهای لوکس:</strong> Dior, Chanel, Tom Ford, Creed</li>
        <li><strong>برندهای پرطرفدار:</strong> Versace, Burberry, YSL, Lancôme</li>
        <li><strong>عطرهای نیچ:</strong> Maison Francis Kurkdjian, Byredo</li>
      </ul>
    `,
  },
  {
    label: "تفاوت ادوپرفیوم با ادوتویلت چیست؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">تفاوت اصلی در غلظت اسانس و ماندگاری است:</p>
      <div class="space-y-3">
        <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <p class="font-semibold text-gray-900 dark:text-white mb-1">ادوپرفیوم (EDP)</p>
          <p class="text-sm">غلظت 15-20% - ماندگاری 6-8 ساعت - مناسب برای شب</p>
        </div>
        <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <p class="font-semibold text-gray-900 dark:text-white mb-1">ادوتویلت (EDT)</p>
          <p class="text-sm">غلظت 5-15% - ماندگاری 4-6 ساعت - مناسب برای روز</p>
        </div>
      </div>
    `,
  },
  {
    label: "عطرها حجم‌های مختلف دارند؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">بله، ما حجم‌های مختلفی ارائه می‌دهیم:</p>
      <ul class="list-disc list-inside space-y-1 text-gray-600 dark:text-gray-400">
        <li>حجم 30 میلی‌لیتر - مناسب امتحان</li>
        <li>حجم 50 میلی‌لیتر - استاندارد</li>
        <li>حجم 100 میلی‌لیتر - اقتصادی</li>
        <li>حجم 150+ میلی‌لیتر - ویژه</li>
      </ul>
    `,
  },
]);

// خرید و ارسال
const shippingQuestions = ref([
  {
    label: "نحوه سفارش چگونه است؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">سفارش دادن بسیار آسان است:</p>
      <ol class="list-decimal list-inside space-y-2 text-gray-600 dark:text-gray-400">
        <li>محصول مورد نظر را به سبد خرید اضافه کنید</li>
        <li>مشخصات و آدرس خود را وارد کنید</li>
        <li>روش پرداخت را انتخاب کنید</li>
        <li>سفارش خود را نهایی کنید</li>
      </ol>
      <p class="mt-3 text-sm">پس از تایید، کد پیگیری برای شما ارسال می‌شود.</p>
    `,
  },
  {
    label: "هزینه ارسال چقدر است؟",
    icon: "i-lucide-circle-help",
    content: `
      <div class="space-y-3">
        <div class="p-3 bg-green-50 dark:bg-green-900/20 rounded-lg border border-green-200 dark:border-green-800">
          <p class="font-semibold text-green-900 dark:text-green-400 mb-1">
            🎉 ارسال رایگان
          </p>
          <p class="text-sm text-green-700 dark:text-green-300">
            برای سفارشات بالای 2 میلیون تومان در سراسر کشور
          </p>
        </div>
        <p class="text-gray-600 dark:text-gray-400">
          برای سفارشات زیر 2 میلیون تومان:<br>
          • تهران و کرج: 50,000 تومان<br>
          • شهرستان‌ها: 80,000 تومان
        </p>
      </div>
    `,
  },
  {
    label: "مدت زمان ارسال چقدر است؟",
    icon: "i-lucide-circle-help",
    content: `
      <ul class="space-y-2 text-gray-600 dark:text-gray-400">
        <li>📦 <strong>تهران و کرج:</strong> 1-2 روز کاری</li>
        <li>📦 <strong>شهرهای بزرگ:</strong> 2-4 روز کاری</li>
        <li>📦 <strong>سایر شهرها:</strong> 3-7 روز کاری</li>
        <li class="pt-2 text-sm">
          ⏰ سفارشات قبل از ساعت 12 ظهر همان روز ارسال می‌شوند
        </li>
      </ul>
    `,
  },
  {
    label: "روش‌های پرداخت چیست؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">ما روش‌های مختلفی برای پرداخت داریم:</p>
      <ul class="space-y-2 text-gray-600 dark:text-gray-400">
        <li>💳 پرداخت آنلاین (کلیه کارت‌های بانکی)</li>
        <li>💵 پرداخت در محل (تهران و کرج)</li>
        <li>🏦 واریز به حساب بانکی</li>
        <li>📱 درگاه‌های پرداخت معتبر</li>
      </ul>
      <p class="mt-3 text-sm bg-blue-50 dark:bg-blue-900/20 p-3 rounded-lg border border-blue-200 dark:border-blue-800">
        🔒 تمام تراکنش‌ها با استانداردهای امنیتی بالا انجام می‌شود
      </p>
    `,
  },
]);

// اصالت و کیفیت
const qualityQuestions = ref([
  {
    label: "چگونه از اصل بودن محصولات اطمینان حاصل کنم؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">ما چندین راه برای اطمینان از اصالت ارائه می‌دهیم:</p>
      <ul class="list-disc list-inside space-y-2 text-gray-600 dark:text-gray-400">
        <li>بارکد اصلی روی بسته‌بندی</li>
        <li>هولوگرام و سریال نامبر برند</li>
        <li>فاکتور رسمی همراه محصول</li>
        <li>امکان استعلام از سایت رسمی برند</li>
        <li>گارانتی بازگشت 100% وجه</li>
      </ul>
    `,
  },
  {
    label: "نحوه نگهداری عطر چگونه است؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">برای حفظ کیفیت عطر این نکات را رعایت کنید:</p>
      <div class="space-y-2">
        <div class="flex items-start gap-2">
          <span class="text-green-600 dark:text-green-400">✓</span>
          <p>در جای خنک و تاریک نگهداری شود</p>
        </div>
        <div class="flex items-start gap-2">
          <span class="text-green-600 dark:text-green-400">✓</span>
          <p>از تماس مستقیم با نور خورشید دوری کند</p>
        </div>
        <div class="flex items-start gap-2">
          <span class="text-green-600 dark:text-green-400">✓</span>
          <p>درب آن را همیشه بسته نگه دارید</p>
        </div>
        <div class="flex items-start gap-2">
          <span class="text-red-600 dark:text-red-400">✗</span>
          <p>در حمام یا مکان‌های مرطوب نگذارید</p>
        </div>
      </div>
    `,
  },
  {
    label: "تاریخ انقضا دارند؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">بله، عطرها معمولاً 3-5 سال عمر دارند:</p>
      <ul class="space-y-2 text-gray-600 dark:text-gray-400">
        <li>📅 عطرهای بسته نشده: 3-5 سال</li>
        <li>📅 عطرهای باز شده: 1-2 سال</li>
        <li>🌡️ نگهداری صحیح عمر را افزایش می‌دهد</li>
      </ul>
      <p class="mt-3 text-sm">
        تمام محصولات ما دارای حداقل 2 سال تا تاریخ انقضا هستند.
      </p>
    `,
  },
]);

// مرجوعی و گارانتی
const returnQuestions = ref([
  {
    label: "شرایط مرجوعی محصول چیست؟",
    icon: "i-lucide-circle-help",
    content: `
      <div class="space-y-3">
        <p class="font-semibold text-gray-900 dark:text-white">
          شما می‌توانید در شرایط زیر محصول را مرجوع کنید:
        </p>
        <ul class="space-y-2 text-gray-600 dark:text-gray-400">
          <li>✅ تا 7 روز پس از دریافت</li>
          <li>✅ بسته‌بندی دست نخورده باشد</li>
          <li>✅ سلفون و پلمپ محصول سالم باشد</li>
          <li>✅ فاکتور خرید همراه باشد</li>
        </ul>
        <div class="p-3 bg-amber-50 dark:bg-amber-900/20 rounded-lg border border-amber-200 dark:border-amber-800">
          <p class="text-sm text-amber-900 dark:text-amber-400">
            ⚠️ توجه: محصولات باز شده قابل بازگشت نیستند
          </p>
        </div>
      </div>
    `,
  },
  {
    label: "گارانتی اصالت کالا چگونه است؟",
    icon: "i-lucide-circle-help",
    content: `
      <div class="space-y-3">
        <p class="mb-2 font-semibold text-gray-900 dark:text-white">
          ما 100% اصالت کالا را تضمین می‌کنیم:
        </p>
        <div class="p-4 bg-primary/10 rounded-lg border border-primary/20">
          <p class="font-semibold text-primary mb-2">🛡️ گارانتی بازگشت وجه</p>
          <p class="text-sm">
            در صورت عدم اصالت محصول، 100% وجه پرداختی شما بازگردانده می‌شود
          </p>
        </div>
        <ul class="list-disc list-inside space-y-1 text-gray-600 dark:text-gray-400">
          <li>بدون هیچ پرسش اضافی</li>
          <li>بازگشت وجه ظرف 24 ساعت</li>
          <li>هزینه ارسال برعهده ماست</li>
        </ul>
      </div>
    `,
  },
  {
    label: "اگر محصول آسیب دیده برسد چه کنم؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">در صورت دریافت محصول آسیب دیده:</p>
      <ol class="list-decimal list-inside space-y-2 text-gray-600 dark:text-gray-400">
        <li>بلافاصله با پشتیبانی تماس بگیرید</li>
        <li>عکس از آسیب دیدگی بگیرید</li>
        <li>بسته را باز نکنید</li>
        <li>ما جایگزین ارسال می‌کنیم یا وجه برمی‌گردانیم</li>
      </ol>
      <p class="mt-3 text-sm bg-green-50 dark:bg-green-900/20 p-3 rounded-lg">
        📞 پشتیبانی 24/7: 021-12345678
      </p>
    `,
  },
]);

// راهنمای انتخاب
const guidanceQuestions = ref([
  {
    label: "چگونه عطر مناسب خودم را پیدا کنم؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">برای انتخاب عطر مناسب این موارد را در نظر بگیرید:</p>
      <div class="space-y-3">
        <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <p class="font-semibold mb-2">1️⃣ بر اساس شخصیت</p>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            پرانرژی: عطرهای سیتروس و فرش<br>
            آرام: عطرهای گلی و شرقی<br>
            باوقار: عطرهای وودی و مشکی
          </p>
        </div>
        <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <p class="font-semibold mb-2">2️⃣ بر اساس فصل</p>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            بهار/تابستان: عطرهای سبک و فرش<br>
            پاییز/زمستان: عطرهای گرم و سنگین
          </p>
        </div>
        <div class="p-3 bg-gray-50 dark:bg-gray-800 rounded-lg">
          <p class="font-semibold mb-2">3️⃣ بر اساس مناسبت</p>
          <p class="text-sm text-gray-600 dark:text-gray-400">
            روزانه: عطرهای ملایم<br>
            مهمانی: عطرهای شیک و ماندگار<br>
            ورزشی: عطرهای اسپرت
          </p>
        </div>
      </div>
    `,
  },
  {
    label: "تفاوت عطرهای مردانه و زنانه چیست؟",
    icon: "i-lucide-circle-help",
    content: `
      <div class="space-y-3">
        <div class="p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
          <p class="font-semibold text-blue-900 dark:text-blue-400 mb-2">
            👨 عطرهای مردانه
          </p>
          <p class="text-sm">
            معمولاً وودی، مشکی، اسپرت و با ماندگاری بالا
          </p>
        </div>
        <div class="p-3 bg-pink-50 dark:bg-pink-900/20 rounded-lg">
          <p class="font-semibold text-pink-900 dark:text-pink-400 mb-2">
            👩 عطرهای زنانه
          </p>
          <p class="text-sm">
            معمولاً گلی، میوه‌ای، شیرین و ملایم‌تر
          </p>
        </div>
        <div class="p-3 bg-purple-50 dark:bg-purple-900/20 rounded-lg">
          <p class="font-semibold text-purple-900 dark:text-purple-400 mb-2">
            👥 عطرهای یونیسکس
          </p>
          <p class="text-sm">
            مناسب هر دو جنسیت با نت‌های متعادل
          </p>
        </div>
      </div>
    `,
  },
  {
    label: "چطور عطر را درست استفاده کنم؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">نکات مهم در استفاده از عطر:</p>
      <div class="space-y-2">
        <div class="flex items-start gap-2">
          <span>✨</span>
          <p>روی نقاط پالسی بزنید (مچ دست، گردن، پشت گوش)</p>
        </div>
        <div class="flex items-start gap-2">
          <span>✨</span>
          <p>در فاصله 15-20 سانتی از پوست اسپری کنید</p>
        </div>
        <div class="flex items-start gap-2">
          <span>✨</span>
          <p>بعد از زدن عطر، مچ دست‌ها را به هم نمالید</p>
        </div>
        <div class="flex items-start gap-2">
          <span>✨</span>
          <p>بعد از حمام و روی پوست مرطوب استفاده کنید</p>
        </div>
        <div class="flex items-start gap-2">
          <span>✨</span>
          <p>برای ماندگاری بیشتر، روی لباس هم بزنید</p>
        </div>
      </div>
    `,
  },
  {
    label: "چگونه بین عطرهای مختلف انتخاب کنم؟",
    icon: "i-lucide-circle-help",
    content: `
      <p class="mb-3">پیشنهادات ما برای انتخاب بهتر:</p>
      <ul class="space-y-2 text-gray-600 dark:text-gray-400">
        <li>🎁 از سمپل استفاده کنید (رایگان با هر سفارش)</li>
        <li>💬 با مشاوران ما مشورت کنید</li>
        <li>⭐ نظرات کاربران را بخوانید</li>
        <li>📊 از فیلترهای سایت استفاده کنید</li>
        <li>🎯 بر اساس برند مورد علاقه جستجو کنید</li>
      </ul>
      <p class="mt-3 text-sm bg-primary/10 p-3 rounded-lg border border-primary/20">
        💡 می‌توانید سمپل چند عطر را با تخفیف سفارش دهید
      </p>
    `,
  },
]);
</script>
