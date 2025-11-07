// middleware/admin-only.js
export default defineNuxtRouteMiddleware((to, from) => {
  if (process.server) return;

  const accessToken = useCookie("access").value;
  const isAdmin = useCookie("isAdmin").value === "true";

  if (!accessToken) {
    return navigateTo("/login");
  }

  if (!isAdmin) {
    return navigateTo("/");
  }
});
