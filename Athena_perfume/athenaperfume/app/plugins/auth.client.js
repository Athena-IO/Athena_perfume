// plugins/auth.client.js
import { useAuthStore } from '~/stores/auth'

export default defineNuxtPlugin(async () => {
  const authStore = useAuthStore();

  if (process.client) {
    await authStore.fetchCurrentUser();
  }
});
