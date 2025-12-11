export const useCartStore = defineStore("cart", {
  state: () => ({
    items: [],
  }),

  persist: true,

  getters: {
    totalItems: (state) =>
      state.items.length,

    total: (state) =>
      state.items.reduce((sum, item) => {
        const price = Number(item.price) || 0;
        return sum + price * (item.qty || 0);
      }, 0),

    totalPrice: (state) => state.total,
  },

  actions: {
    addToCart(product, qty = 1) {
      // group only by product id
      const existing = this.items.find((i) => i.productId === product.id);

      if (existing) {
        // increase quantity
        existing.qty += qty;
        // optionally accumulate volume in some field
        existing.totalVolume =
          (existing.totalVolume || existing.selectedVolume || 0) +
          (product.selectedVolume || 0);
      } else {
        this.items.push({
          id: product.id, // use product id as cart item id
          productId: product.id,
          title: product.name,
          price: product.finalPrice,
          originalPrice: product.originalPrice,
          // store last selected volume or an accumulated one
          selectedVolume: product.selectedVolume,
          totalVolume: product.selectedVolume, // can use this for display
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
