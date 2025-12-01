// composables/useAuth.js
import { ref, computed } from "vue";

export const useAuth = () => {
  // اطلاعات کاربر رو جهانی نگه می‌داریم (بعد از رفرش هم بمونه)
  const user = useState("user", () => null);

  // وضعیت لاگین
  const isAuthenticated = computed(() => !!user.value);
  const isAdmin = computed(() => user.value?.role === "admin");

  // وقتی لاگین موفق شد اینو صدا بزن
  const setUser = (data) => {
    user.value = {
      id: data.id || data.user_id,
      username: data.username || data.email?.split("@")[0],
      fullName: data.full_name || data.name || data.username || "کاربر",
      email: data.email,
      phone: data.phone || data.mobile,
      role: data.role || data.is_admin ? "admin" : "customer",
      accessToken: data.access || data.access_token,
    };
  };

  // خروج از حساب
  const logout = () => {
    user.value = null;

    // پاک کردن کوکی‌ها
    const accessCookie = useCookie("access");
    const isAdminCookie = useCookie("isAdmin");
    const refreshCookie = useCookie("refresh");

    accessCookie.value = null;
    isAdminCookie.value = null;
    refreshCookie.value = null;

    // ریدایرکت به لاگین
    if (process.client) {
      navigateTo("/login");
    }
  };

  // چک کردن توکن و لود کاربر (اختیاری — بعداً توی پلاگین استفاده می‌شه)
  const fetchCurrentUser = async () => {
    const token = useCookie("access").value;
    if (!token) return;

    try {
      const userData = await $fetch("/api/accounts/me/", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUser(userData);
    } catch (err) {
      console.warn("توکن منقضی شده یا نامعتبر — لاگ‌اوت خودکار");
      logout();
    }
  };

  return {
    user: readonly(user),
    isAuthenticated,
    isAdmin,
    setUser,
    logout,
    fetchCurrentUser,
  };
};
