<template>
  <div class="min-h-screen flex flex-col">
    <appheader />

    <main class="flex-1 w-full max-w-none mx-auto px-4">
      <slot />
    </main>
    <app-footer />
  </div>
</template>
