from decimal import Decimal

def calculate_price(product, quantity: int) -> int:
    """
    محاسبه قیمت نهایی هر واحد بر اساس تعداد
    """
    if quantity <= 0:
        raise ValueError("تعداد باید بیشتر از صفر باشد")

    # جستجوی قانون مناسب
    rules = product.pricing_rules.all()
    for rule in rules:
        if quantity >= rule.min_quantity:
            if rule.max_quantity is None or quantity <= rule.max_quantity:
                return int(rule.price_per_unit)

    # اگر هیچ قانونی نبود → قیمت پایه از volume_options
    if product.volume_options:
        return int(product.volume_options[0].get('price', 0))
    return 0