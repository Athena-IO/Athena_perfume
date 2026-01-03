import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)

  const isAuthenticated = computed(() => !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const userInfo = computed(() => user.value)

  const setUser = (userData) => {
    user.value = {
      id: userData.id || userData.user_id,
      username: userData.username || userData.email?.split('@')[0],
      fullName: userData.full_name || userData.name || userData.username || 'کاربر',
      email: userData.email,
      phone: userData.phone || userData.mobile,
      role: userData.role || userData.is_admin ? 'admin' : 'customer',
      accessToken: userData.access || userData.access_token,
    };
  };

  const logout = () => {
    user.value = null;

    // Clear cookies
    const accessCookie = useCookie('access');
    const isAdminCookie = useCookie('isAdmin');
    const refreshCookie = useCookie('refresh');

    accessCookie.value = null;
    isAdminCookie.value = null;
    refreshCookie.value = null;

    // Redirect to login
    if (process.client) {
      navigateTo('/login');
    }
  };

  const fetchCurrentUser = async () => {
    const token = useCookie('access').value;
    if (!token) return;

    try {
      const userData = await $fetch('/api/accounts/me/', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      setUser(userData);
    } catch (err) {
      console.warn('Token expired or invalid - auto logout');
      logout();
    }
  };

  return {
    user,
    isAuthenticated,
    isAdmin,
    userInfo,
    setUser,
    logout,
    fetchCurrentUser,
  };
}, {
  persist: true,
});
