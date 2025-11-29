import { defineStore } from "pinia";

export const useCartStore = defineStore("cart", {
  state: () => ({
    items: [],
  }),

  persist: true,

  getters: {
    totalItems: (state) =>
      state.items.reduce((sum, i) => sum + (i.qty || 0), 0),

    total: (state) =>
      state.items.reduce((sum, item) => {
        const price = Number(item.price) || 0;
        return sum + price * (item.qty || 0);
      }, 0),

    totalPrice: (state) => state.total,
  },

  actions: {
    addToCart(product, qty = 1) {
      const existing = this.items.find(
        (i) =>
          i.id === product.id && i.selectedVolume === product.selectedVolume
      );
      if (existing) {
        existing.qty += qty;
      } else {
        this.items.push({
          id: product.id,
          title: product.name,
          price: product.finalPrice, // قیمت بعد تخفیف
          originalPrice: product.originalPrice, // قیمت قبل تخفیف
          selectedVolume: product.selectedVolume,
          volumeLabel: product.volumeLabel,
          image: product.image,
          qty,
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
