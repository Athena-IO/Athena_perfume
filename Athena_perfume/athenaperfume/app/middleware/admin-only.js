// middleware/admin-only.js
export default defineNuxtRouteMiddleware((to, from) => {
  // فقط در کلاینت اجرا بشه
  if (import.meta.server) return;

  const access = useCookie("access").value;
  const isAdmin = useCookie("isAdmin").value === "true";

  if (!access) {
    return navigateTo("/login");
  }

  if (!isAdmin) {
    return navigateTo("/");
  }
});
