// middleware/auth.js
export default defineNuxtRouteMiddleware((to, from) => {
  // فقط در کلاینت چک کن
  if (process.server) return;

  const accessToken = useCookie("access").value;
  const publicPages = ["/", "/login", "/about", "/contact"];
  const isPublic = publicPages.includes(to.path);

  if (!accessToken && !isPublic) {
    return navigateTo("/login");
  }
});
