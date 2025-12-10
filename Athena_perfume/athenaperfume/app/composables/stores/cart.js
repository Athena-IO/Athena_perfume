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
      // Create unique ID based on product ID and selected volume
      const uniqueId = `${product.id}-${product.selectedVolume}`;

      const existing = this.items.find((i) => i.uniqueId === uniqueId);

      if (existing) {
        existing.qty += qty;
      } else {
        this.items.push({
          id: uniqueId, // Unique ID for cart item
          productId: product.id, // Original product ID
          uniqueId: uniqueId, // For finding items
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

    updateQuantity(itemId, newQty) {
      const item = this.items.find((i) => i.id === itemId);
      if (item && newQty >= 1) {
        item.qty = newQty;
      }
    },

    clearCart() {
      this.items = [];
    },
  },
});
