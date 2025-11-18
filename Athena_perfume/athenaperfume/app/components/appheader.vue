<template>
  <UHeader>
    <template #title>
      <UHeader title="Athena Perfume" to="/" />
    </template>

    <UNavigationMenu :items="items" />

    <template #right>
      <UColorModeButton />

      <UTooltip text="Open on GitHub" :kbds="['meta', 'G']">
        <UButton
          color="neutral"
          variant="ghost"
          to="https://github.com/nuxt/ui"
          target="_blank"
          icon="i-simple-icons-github"
          aria-label="GitHub"
        />
      </UTooltip>
    </template>
  </UHeader>
</template>

<script setup lang="ts">
import type { NavigationMenuItem } from "@nuxt/ui";

const items = computed<NavigationMenuItem[]>(() => [
  {
    label: "تخفیف ها",
    to: "/docs/getting-started",
  },
  {
    label: "عطر مردانه",
    to: "/docs/components",
  },
  {
    label: "عطر زنانه",
    to: "https://go.nuxt.com/figma-ui",
    target: "_blank",
  },
  {
    label: "فروشگاه عطر",
    to: "https://github.com/nuxt/ui/releases",
    target: "_blank",
  },
]);
</script>
