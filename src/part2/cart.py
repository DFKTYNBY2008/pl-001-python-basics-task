from typing import Final

from .crud import read_product, update_product
from .storage import (
    NAME_INDEX,
    PRICE_INDEX,
    QUANTITY_INDEX,
    Product,
)


type CartLine = tuple[int, int]

LINE_PRODUCT_ID_INDEX: Final = 0
LINE_QUANTITY_INDEX: Final = 1


def find_cart_line(cart: list[CartLine], product_id: int) -> int | None:
    for cart_ in cart:
        if cart_[LINE_PRODUCT_ID_INDEX] == product_id:
            return cart.index(cart_)
    return None


def add_to_cart(
    storage: list[Product],
    cart: list[CartLine],
    product_id: int,
    quantity: int,
) -> CartLine | None:
    product_person = read_product(storage, product_id)
    if not product_person:
        return None
    storage_quantity = product_person[QUANTITY_INDEX]
    if storage_quantity < quantity:
        print(
            f"not enough stock for product {product_id} : {product_person[QUANTITY_INDEX]} available, {quantity} requested"
        )
        return None

    fields_ = (
        product_person[NAME_INDEX],
        product_person[PRICE_INDEX],
        product_person[QUANTITY_INDEX] - quantity,
    )
    update_product(storage, product_id, fields_)

    line_index = find_cart_line(cart, product_id)
    if line_index is None:
        cartLine = (product_id, quantity)
        cart.append(cartLine)
        return cartLine
    old_quantity = cart[line_index][LINE_QUANTITY_INDEX]
    cartLine = (product_id, old_quantity + quantity)
    cart[line_index] = cartLine
    return cartLine


def remove_from_cart(
    storage: list[Product],
    cart: list[CartLine],
    product_id: int,
    quantity: int,
) -> CartLine | None:
    line_index = find_cart_line(cart, product_id)
    if line_index is None:
        print(f"product {product_id} is not in the cart")
        return None

    cart_quantity = cart[line_index][LINE_QUANTITY_INDEX]
    if cart_quantity < quantity:
        print(f"cart holds only {cart_quantity} unit(s) of product")
        print(f"{product_id}, cannot remove {quantity}")
        return None

    product_person = read_product(storage, product_id)
    if not product_person:
        return None

    fields_ = (
        product_person[NAME_INDEX],
        product_person[PRICE_INDEX],
        product_person[QUANTITY_INDEX] + quantity,
    )
    update_product(storage, product_id, fields_)

    new_cart_quantity = cart_quantity - quantity
    if new_cart_quantity == 0:
        del cart[line_index]
    else:
        cart[line_index] = (product_id, new_cart_quantity)
    return (product_id, new_cart_quantity)
