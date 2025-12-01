// middleware/auth.js
export default defineNuxtRouteMiddleware((to, from) => {
  // فقط در سمت کلاینت اجرا بشه (مهم!)
  if (import.meta.server) return;

  const access = useCookie("access").value;

  if (access && (to.path === "/login" || to.path === "/register")) {
    return navigateTo("/");
  }
  // ====================================================================

  // صفحاتی که همه می‌تونن ببینن (حتی بدون لاگین)
  const publicPages = [
    "/",
    "/login",
    "/register",
    "/about",
    "/contact",
    "/products",
    "/discounts",
    "/men",
    "/women",
  ];

  // اگر صفحه عمومی باشه یا با /product/ شروع بشه → اجازه بده
  const isPublic =
    publicPages.includes(to.path) ||
    to.path.startsWith("/product/") ||
    to.path.startsWith("/category/");

  // اگر لاگین نکرده و داره می‌ره یه صفحه خصوصی → ببرش لاگین
  if (!access && !isPublic) {
    return navigateTo("/login");
  }

  // در همه حالات دیگه → اجازه بده بره
});
