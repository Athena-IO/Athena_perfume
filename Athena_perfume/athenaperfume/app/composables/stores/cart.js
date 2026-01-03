import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore("cart", () => {
  const items = ref([])

  const totalItems = computed(() => items.value.length)

  const total = computed(() =>
    items.value.reduce((sum, item) => {
      const price = Number(item.price) || 0;
      return sum + price * (item.qty || 0);
    }, 0)
  )

  const totalPrice = computed(() => total.value)

  const addToCart = (product, qty = 1) => {
    const existing = items.value.find((i) => i.productId === product.id);

    if (existing) {
      existing.qty += qty;
      existing.totalVolume =
        (existing.totalVolume || existing.selectedVolume || 0) +
        (product.selectedVolume || 0);
    } else {
      items.value.push({
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
  }

  const removeFromCart = (id) => {
    items.value = items.value.filter((i) => i.id !== id);
  }

  const updateQuantity = (itemId, newQty) => {
    const item = items.value.find((i) => i.id === itemId);
    if (item && newQty >= 1) {
      item.qty = newQty;
    }
  }

  const clearCart = () => {
    items.value = [];
  }

  return {
    items,
    totalItems,
    total,
    totalPrice,
    addToCart,
    removeFromCart,
    updateQuantity,
    clearCart,
  }
}, {
  persist: true,
})