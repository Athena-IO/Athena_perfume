// plugins.creds
export default defineNuxtPlugin(async () => {
  const { fetchCurrentUser } = useAuth();

  if (process.client) {
    await fetchCurrentUser();
  }
});
