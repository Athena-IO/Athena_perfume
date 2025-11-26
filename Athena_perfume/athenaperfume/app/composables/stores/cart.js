import { defineStore } from "pinia";

export const useCartStore = defineStore("cart", {
  state: () => ({
    items: [],
  }),

  persist: true,

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
}
,

    removeFromCart(id) {
      this.items = this.items.filter((i) => i.id !== id);
    },

    clearCart() {
      this.items = [];
    },

    total() {
      return this.items.reduce((sum, item) => sum + item.price * item.qty, 0);
    },
  },
});
