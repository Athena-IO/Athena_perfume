<template>
  <div
    class="flex flex-col md:flex-row items-center justify-center min-h-screen w-full"
  >
    <!-- عکس -->
    <div class="hidden md:flex justify-center items-center w-1/2">
      <img
        src="https://vioralondon.com/wp-content/uploads/2023/10/Best-Autumn-Fragrances-For-Men-Main-Image-v2.jpg"
        alt="login"
        class="max-w-3xl rounded-2xl shadow-lg"
      />
    </div>

    <!-- کارت ورود -->
    <div class="w-full md:w-1/3 p-6">
      <Ucard class="w-full">
        <template #header>صفحه ورود</template>
        <form @submit.prevent="handlelogin">
          <UFormField
            label="نام کاربری"
            name="userName"
            class="mb-4"
            :required="true"
            help="نام کاربری خود را وارد کنید"
          >
            <UInput
              type="text"
              placeholder="شماره تلفن"
              required
              v-model="number"
            />
          </UFormField>

          <UFormField
            label="رمز عبور"
            name="Password"
            class="mb-4"
            :required="true"
            help="رمز عبور خود را وارد کنید"
          >
            <UInput
              type="password"
              placeholder="رمز عبور"
              required
              v-model="password"
            />
          </UFormField>

          <UButton type="submit" class="w-1/2 mt-2 justify-center"
            >ورود</UButton
          >
        </form>
      </Ucard>
    </div>
  </div>
</template>

<script setup>
import { useAppToast } from "~/composables/useToast";
const succes = ref(false);
const number = ref("");
const password = ref("");
const pending = ref(false);
const Toast = useAppToast();
</script>
