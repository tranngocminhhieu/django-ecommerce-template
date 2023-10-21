// Update params in URL and go
function updateURL(param, value) {
    const url = new URL(window.location.href);
    url.searchParams.set(param, value);
    window.location.href = url.toString();
}

// Get the parent div and remove it
function removeParent(button, parentClass) {
    var parent = button.closest(`.${parentClass}`);
    if (parent) {
        parent.remove();
    }
}


// Get cookie value (from Django docs)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// Sign up with modal form
const signUpForm = document.getElementById('signup-tab');
if (signUpForm) {
    signUpForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const passwordInput = document.getElementById("su-password");
        const confirmPasswordInput = document.getElementById("su-password-confirm");
        const passwordMismatchMessage = document.getElementById("password-mismatch");
        const alertMessage = document.getElementById('signup-status-alert');

        if (passwordInput.value !== confirmPasswordInput.value) {
            passwordMismatchMessage.style.display = "block";
        } else {
            passwordMismatchMessage.style.display = "none";
        }

        try {
            const response = await fetch('/account/api/signup/', {
                method: "POST",
                body: new FormData(signUpForm),
                headers: {'X-CSRFToken': csrftoken}
            });

            const alertDiv = document.createElement('div');
            alertDiv.classList.add("alert", "alert-dismissible", "fade", "show");

            if (response.status === 201) {
                alertDiv.innerHTML = 'Signup successful!';
                alertDiv.classList.add("alert-success");
            } else {
                const data = await response.json();
                const errorMessage = Object.values(data).map(errors => errors.join(' ')).join(' ');
                alertDiv.innerHTML = errorMessage;
                alertDiv.classList.add("alert-danger");
            }

            alertDiv.innerHTML += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
            alertMessage.appendChild(alertDiv);
            alertMessage.style.display = "block";
        } catch (error) {
            console.error('Error:', error);
        }
    });
};


// Sign up with sign in page
const regForm = document.getElementById('reg-form');
if (regForm) {
    regForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const alertMessage = document.getElementById('reg-status-alert');

        try {
            const response = await fetch('/account/api/signup/', {
                method: "POST",
                body: new FormData(regForm),
                headers: {'X-CSRFToken': csrftoken}
            });

            const alertDiv = document.createElement('div');
            alertDiv.classList.add("alert", "alert-dismissible", "fade", "show");

            if (response.status === 201) {
                alertDiv.innerHTML = 'Signup successful!';
                alertDiv.classList.add("alert-success");
            } else {
                const data = await response.json();
                const errorMessage = Object.values(data).map(errors => errors.join(' ')).join(' ');
                alertDiv.innerHTML = errorMessage;
                alertDiv.classList.add("alert-danger");
            }

            alertDiv.innerHTML += '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
            alertMessage.appendChild(alertDiv);
            alertMessage.style.display = "block";
        } catch (error) {
            console.error('Error:', error);
        }
    });
};


// JWT sign in modal form
// const signInForm = document.getElementById('signin-tab');
// signInForm.addEventListener('submit', async (e) => {
//     e.preventDefault(); // Ngăn form submit mặc định
//
//     try {
//         const response = await fetch('/account/api/token/', {
//             method: 'POST',
//             body: new FormData(signInForm),
//             headers: {'X-CSRFToken': csrftoken}
//         });
//
//         if (response.status === 200) {
//             const data = await response.json();
//
//             // Lưu JWT access_token và refresh_token vào cookie
//             document.cookie = `access_token=${data.access}; path=/;`;
//             document.cookie = `refresh_token=${data.refresh}; path=/;`;
//
//             // Chuyển hướng hoặc thực hiện các hành động khác sau khi đăng nhập thành công
//             window.location.href = '/'; // Ví dụ: chuyển hướng đến home
//         } else {
//             // Xử lý lỗi khi đăng nhập không thành công
//             console.error('Login failed:', response.statusText);
//         }
//     } catch (error) {
//         console.error('Error:', error);
//     };
// });

const updateCart = async (data) => {
    console.log(data)

    const totalItemsSpans = document.getElementsByClassName('total-items');
    const totalAmountSpans = document.getElementsByClassName('total-amount');
    for (let i = 0; i < totalItemsSpans.length; i++) {
        totalItemsSpans[i].textContent = data['total_items']
    };
    for (let i = 0; i < totalAmountSpans.length; i++) {
        totalAmountSpans[i].textContent = `\$${data['total_amount']}`
    }


    const headerCartItemsDiv = document.getElementById('header-cart-items');
    headerCartItemsDiv.replaceChildren();

    for (let i = 0; i < data['items'].length; i++) {
        let product = data['items'][i]['product']['name'];
        let slug = data['items'][i]['product']['slug'];
        let image = data['items'][i]['product']['image'];
        let price = data['items'][i]['product_variant']['price'];
        let quantity = data['items'][i]['quantity'];
        let version = data['items'][i]['product_variant']['version'];
        let color = data['items'][i]['product_variant']['color']['color_name'];
        let product_variant_id = data['items'][i]['product_variant_id']

        let item = `<div class="widget-cart-item p-2 border-bottom">
            <button aria-label="Remove" class="btn-close text-danger delete-from-cart" type="button" data-action="delete" data-variant="${product_variant_id}"><span aria-hidden="true">×</span></button>
            <div class="d-flex align-items-center"><a class="d-block flex-shrink-0" href="/products/${slug}/?version=${version}&amp;color=${color}">
                <img alt="Product" src="${image}" width="64"></a>
                <div class="ps-2">
                    <h6 class="widget-product-title"><a href="/products/${slug}/?version=${version}&amp;color=${color}">${product} (${version}, ${color})</a>
                    </h6>
                    <div class="widget-product-meta"><span class="text-accent me-2">\$${price}</span><span class="text-muted">x ${quantity}</span>
                    </div>
                </div>
            </div>
        </div>`

        headerCartItemsDiv.innerHTML += item
    };

    const deleteFromCartButtons = document.getElementsByClassName('delete-from-cart');

    for (let i = 0; i < deleteFromCartButtons.length; i++){

        deleteFromCartButtons[i].addEventListener('click', async (event) => {
            event.preventDefault()

            let action = event.currentTarget.getAttribute('data-action');
            let product_variant_id = event.currentTarget.getAttribute('data-variant');

            console.log("delete button", action, product_variant_id);

            await editCart(action, product_variant_id);
        });
    }




};

const editCart = async (action, product_variant_id) =>{

    console.log(action, product_variant_id);

    const response = await fetch('/orders/api/edit-cart/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'action': action,
            'product_variant_id': product_variant_id
        })
    });

    const data = await response.json()

    await updateCart(data)

}

const addToCartButtons = document.getElementsByClassName('add-to-cart');

for (let i = 0; i < addToCartButtons.length; i++) {
    addToCartButtons[i].addEventListener('click', async (event) => {
        event.preventDefault()

        let action = event.currentTarget.getAttribute('data-action');
        let product_variant_id = event.currentTarget.getAttribute('data-variant');

        await editCart(action, product_variant_id);
    });
}

const deleteFromCartButtons = document.getElementsByClassName('delete-from-cart');

for (let i = 0; i < deleteFromCartButtons.length; i++){

    deleteFromCartButtons[i].addEventListener('click', async (event) => {
        event.preventDefault()

        let action = event.currentTarget.getAttribute('data-action');
        let product_variant_id = event.currentTarget.getAttribute('data-variant');

        console.log("delete button", action, product_variant_id);

        await editCart(action, product_variant_id);
    });
}

// In Cart page
const updateCartButton = document.getElementById('update-cart');
if (updateCartButton) {
    updateCartButton.addEventListener('click', async (event) => {
        event.preventDefault()

        let payload = []

        const cartItems = document.getElementsByClassName('cart-item');
        for (let i = 0; i < cartItems.length; i++) {
            let variant = cartItems[i].getAttribute('data-variant');

            let quantityInput = cartItems[i].getElementsByClassName('quantity');

            let quantity = quantityInput[0].value;

            let item = {"product_variant_id": parseInt(variant), "quantity": parseInt(quantity)};

            payload.push(item)

        };

        console.log(payload)

        const response = await fetch('/orders/api/update-cart/', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        await updateCart(data)
    })
};

const cartToCheckoutButton = document.getElementById('cart-to-checkout');
if (cartToCheckoutButton) {
    cartToCheckoutButton.addEventListener('click', async (event) => {
        event.preventDefault()
        const checkoutURL = cartToCheckoutButton.getAttribute('href');

        let orderComment = document.getElementById('order-comment');

        if (orderComment) {

            const response = await fetch('/orders/api/update-draft-order/', {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/json'},
                body: JSON.stringify({"comment": orderComment.value})
            });

            console.log(response);

            if (response.ok === true) {
                window.location.href = checkoutURL;
            };

        } else {
            window.location.href = checkoutURL;
        };

    });
};

// In Checkout page
const detailsToShippingButtons = document.getElementsByClassName('details-to-shipping');
for (let i = 0; i < detailsToShippingButtons.length; i++) {
    detailsToShippingButtons[i].addEventListener('click', async (event) => {
        event.preventDefault();

        const href = detailsToShippingButtons[i].getAttribute('href');

        const addressForm = document.getElementById('shipping-address');

        const formData = new FormData(addressForm);

        let payload = {}

        formData.forEach((value, key) => payload[key] = value);

        const response = await fetch('/orders/api/update-draft-order/', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        console.log(response);

        if (response.ok === true) {
            window.location.href = href;
        };

    });
};


// In Checkout > Shipping page
const shippingToPaymentButtons = document.getElementsByClassName('shipping-to-payment');
for (let i = 0; i < shippingToPaymentButtons.length; i++) {
    shippingToPaymentButtons[i].addEventListener('click', async (event) => {
        event.preventDefault();

        const href = shippingToPaymentButtons[i].getAttribute('href');

        const shippingForm = document.getElementById('shipping-method');

        const formData = new FormData(shippingForm);

        let payload = {}

        formData.forEach((value, key) => payload[key] = value);

        const response = await fetch('/orders/api/update-draft-order/', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        console.log(response);

        if (response.ok === true) {
            window.location.href = href;
        };

    });
};

// In Checkout > Payment
const paymentToReviewButtons = document.getElementsByClassName('payment-to-review');
for (let i = 0; i < paymentToReviewButtons.length; i++) {
    paymentToReviewButtons[i].addEventListener('click', async (event) => {
        event.preventDefault();

        const href = paymentToReviewButtons[i].getAttribute('href');

        const response = await fetch('/orders/api/update-draft-order/', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/json'},
            body: JSON.stringify({"payment_method": "COD"})
        });

        console.log(response);

        if (response.ok === true) {
            window.location.href = href;
        };

    });
};

// In Account > Wishlist
const editWishlist = async (action, product_variant_id) =>{

    console.log(action, product_variant_id);

    const response = await fetch('/orders/api/edit-wishlist/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            'action': action,
            'product_variant_id': product_variant_id
        })
    });

    const data = await response.json()

    const wishlistCountSpans = document.getElementsByClassName('wishlist-count');
    for (let i = 0; i < wishlistCountSpans.length; i++) {
        wishlistCountSpans[i].textContent = data['total_items']
    };

};


const deleteFromWishlistButtons = document.getElementsByClassName('delete-from-wishlist');
for (let i = 0; i < deleteFromWishlistButtons.length; i++){

    deleteFromWishlistButtons[i].addEventListener('click', async (event) => {
        event.preventDefault()

        let action = event.currentTarget.getAttribute('data-action');
        let product_variant_id = event.currentTarget.getAttribute('data-variant');

        await editWishlist(action, product_variant_id);

        removeParent(deleteFromWishlistButtons[i], 'wishlist-item');

    });
};

// In Products
const editFromWishlistButtons = document.getElementsByClassName('edit-wishlist');
for (let i = 0; i < editFromWishlistButtons.length; i++){

    editFromWishlistButtons[i].addEventListener('click', async (event) => {
        event.preventDefault()

        let action = event.currentTarget.getAttribute('data-action');
        let product_variant_id = event.currentTarget.getAttribute('data-variant');

        await editWishlist(action, product_variant_id);

        if (action === 'add') {
            editFromWishlistButtons[i].setAttribute('data-action', 'delete');
        } else {
            editFromWishlistButtons[i].setAttribute('data-action', 'add');
        };

    });
};

const priceSliders = document.getElementsByClassName('range-slider');
for (let i = 0; i < priceSliders.length; i++) {
    let rangeSliderUi = priceSliders[i].querySelector('.range-slider-ui');
    let rangeSlierValueMin = priceSliders[i].querySelector('.range-slider-value-min');
    let rangeSlierValueMax = priceSliders[i].querySelector('.range-slider-value-max');

    rangeSliderUi.noUiSlider.on('change', () => {
        let valueMin = rangeSlierValueMin.value;
        let valueMax = rangeSlierValueMax.value;

        const url = new URL(window.location.href);
        url.searchParams.set('min_price', valueMin);
        url.searchParams.set('max_price', valueMax);

        window.location.href = url.toString();
    });

    rangeSlierValueMax.addEventListener('change', () => {
        let valueMax = rangeSlierValueMax.value;
        updateURL('max_price', valueMax);
    });

    rangeSlierValueMin.addEventListener('change', () => {
        let valueMin = rangeSlierValueMin.value;
        updateURL('min_price', valueMin);
    });

};

// In all
const buyNowButtons = document.getElementsByClassName('buy-now');
for (let i = 0; i < buyNowButtons.length; i++) {
    buyNowButtons[i].addEventListener('click', async (event) => {
        let product_variant_id = buyNowButtons[i].getAttribute('data-variant');
        let quantity = buyNowButtons[i].getAttribute('data-quantity');

        let payload = [{"product_variant_id": parseInt(product_variant_id), "quantity": parseInt(quantity)}]

        let response = await fetch('/orders/api/update-cart/', {
            method: 'POST',
            headers: {'X-CSRFToken': csrftoken, 'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });

        if (response.ok === true) {
            window.location.href = '/orders/checkout/';
        };

    });
};

// In single Product
const quantitySelect = document.getElementById('quantity');
const buyNowButton = document.getElementById('buy-now');
if (quantitySelect && buyNowButton) {
    quantitySelect.addEventListener('change', () => {
        let quantity = quantitySelect.value;
        buyNowButton.setAttribute('data-quantity', parseInt(quantity));
    });
};

//
const brandCheckBoxes = document.getElementsByClassName('brand-checkbox');
for (let i = 0; i < brandCheckBoxes.length; i++) {
    brandCheckBoxes[i].addEventListener('change', () => {

        const url = new URL(window.location.href);
        const brandValue = brandCheckBoxes[i].value;

        if (brandCheckBoxes[i].checked) {
            url.searchParams.append('brand', brandValue);
            window.location.href = url.toString();

        } else {
            const brandParams = url.searchParams.getAll('brand');
            const updatedBrandParams = brandParams.filter(brand => brand !== brandValue);
            url.searchParams.delete('brand');
            updatedBrandParams.forEach(brand => url.searchParams.append('brand', brand));
            window.location.href = url.toString();
        }
    })
}


// Keep scroll position when refresh in the same page
// Reference https://stackoverflow.com/a/58743412/19919470
document.addEventListener("DOMContentLoaded", () => {
    const scrollPosition = localStorage.getItem('scrollPosition');
    const scrollPathName = localStorage.getItem('scrollPathName');
    if (scrollPosition && scrollPathName && scrollPathName === window.location.pathname) {
        window.scrollTo(0, scrollPosition);
    }
});

window.onbeforeunload = () => {
    localStorage.setItem('scrollPosition', window.scrollY);
    localStorage.setItem('scrollPathName', window.location.pathname);
};