// middleware/admin-only.global.js
export default defineNuxtRouteMiddleware((to, from) => {
  if (process.server) return;

  const access = useCookie("access").value;
  const isAdmin = useCookie("isAdmin").value === "true";

  if (!access) {
    return navigateTo("/login");
  }

  if (!isAdmin) {
    return navigateTo("/");
  }
});
