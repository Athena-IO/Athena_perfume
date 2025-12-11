export const useCartStore = defineStore("cart", {
  state: () => ({
    items: [],
  }),

  persist: true,

  getters: {
    totalItems: (state) => state.items.length,

    total: (state) =>
      state.items.reduce((sum, item) => {
        const price = Number(item.price) || 0;
        return sum + price * (item.qty || 0);
      }, 0),

    totalPrice: (state) => state.total,
  },

  actions: {
    addToCart(product, qty = 1) {
      const existing = this.items.find((i) => i.productId === product.id);

      if (existing) {
        existing.qty += qty;
        existing.totalVolume =
          (existing.totalVolume || existing.selectedVolume || 0) +
          (product.selectedVolume || 0);
      } else {
        this.items.push({
          id: product.id,
          productId: product.id,
          title: product.name,
          price: product.finalPrice,
          originalPrice: product.originalPrice,
          selectedVolume: product.selectedVolume,
          totalVolume: product.selectedVolume,
          image: product.image,
          qty,
          // ✅ ظرفیت محصول را هم نگه می‌داریم
          capacity: product.capacity,
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