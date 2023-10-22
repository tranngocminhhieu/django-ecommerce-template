# Django E-commerce Template

This is a project from a Django course I took. I chose the E-commerce topic because it is familiar to us, and there will be many challenges in thinking about the model appropriately.

## Evolved features
1. Register.
2. Log in.
3. Add to cart.
4. Add to wishlist.
5. Apply discount code.
6. Choose a shipping method.
7. Buy now (clear wishlist and checkout current product).
8. Products have variants by color and version, grouped by category and brand.

## Errors
1. New members can not log in.
2. The order historical page's total price must be corrected.

## Further development direction
1. The icon should be red if the product variant is already on the wishlist.
2. On the product list page.
- Add to Cart and Add to Wishlist buttons should retrieve the product variant the user selected instead of the default variant.
- Handle customer filters with Ajax instead of reloading with new parameters.
3. Add a blog post feature
4. Allows users to make purchases without registering/logging (save information on local storage).
5. Discount code.
- Can only be used once per user.
- Add maximum used quantity.