// composables/stores/cart.js   ← همون فایل قبلیت رو کامل جایگزین کن
import { defineStore } from "pinia";

export const useCartStore = defineStore("cart", {
  state: () => ({
    items: [],
  }),

  persist: true,

  // اینجا مهمه! total رو از actions ببرمی‌داریم و می‌ذاریم داخل getters
  getters: {
    // تعداد کل آیتم‌ها
    totalItems: (state) => state.items.reduce((sum, i) => sum + (i.qty || 0), 0),

    // جمع کل قیمت
    total: (state) => state.items.reduce((sum, item) => {
      const price = typeof item.price === "string"
        ? parseInt(item.price.replace(/[^0-9]/g, "")) || 0
        : item.price || 0;
      return sum + price * (item.qty || 0);
    }, 0),

    // اگه بعداً خواستی totalPrice هم داشته باشی
    totalPrice: (state) => state.total,
  },

  actions: {
    addToCart(product, qty = 1) {
      const existing = this.items.find(i => i.id === product.id);
      if (existing) {
        existing.qty += qty;
      } else {
        this.items.push({
          id: product.id,
          title: product.name,
          price: product.price,
          qty
        });
      }
    },

    removeFromCart(id) {
      this.items = this.items.filter((i) => i.id !== id);
    },

    clearCart() {
      this.items = [];
    },
  },
});