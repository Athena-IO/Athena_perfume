// middleware/auth.js
export default defineNuxtRouteMiddleware((to, from) => {
  // فقط در کلاینت اجرا بشه
  if (import.meta.server) return;

  const access = useCookie("access").value;
  const publicPages = ["/", "/login", "/about", "/contact"];
  const isPublic = publicPages.includes(to.path);

  if (!access && !isPublic) {
    return navigateTo("/login");
  }
});
