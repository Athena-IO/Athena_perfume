// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-07-15",
  devtools: { enabled: true },
  modules: ["@nuxt/ui",'@pinia/nuxt'],
  colorMode: {
    preference: "light", // default value of $colorMode.preference
  },

  css: ["~/assets/css/main.css"],
  vite: { plugins: [tailwindcss()] },
  routeRules: {
    // همه درخواست‌های /api/** رو به Django پروکسی کن
    "/api/**": {
      proxy: "http://127.0.0.1:8000/api/**",
    },
  },
});
