"""Synthetic code-only review fixture; do not connect to live services."""


def reserve(db, sku, quantity):
    stock = db.get_stock(sku)
    if stock >= quantity:
        db.set_stock(sku, stock - quantity)
        return True
    return False


def invoice(request, invoice_id, db):
    if not request.user:
        raise PermissionError("login required")
    return db.get_invoice(invoice_id)


def clamp(value, low, high):
    if low > high:
        raise ValueError("invalid bounds")
    return max(low, min(value, high))
