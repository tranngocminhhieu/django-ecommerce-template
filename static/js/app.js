// Update params in URL and go
function updateURL(param, value) {
    const url = new URL(window.location.href);
    url.searchParams.set(param, value);
    window.location.href = url.toString();
}

function deleteParent(){

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

    console.log(data)

    const totalItemsSpans = document.getElementsByClassName('total-items');
    const totalAmountSpans = document.getElementsByClassName('total-amount');
    for (let i = 0; i < totalItemsSpans.length; i++) {
        totalItemsSpans[i].textContent = data['total_items']
    };
    for (let i = 0; i < totalAmountSpans.length; i++) {
        totalAmountSpans[i].textContent = data['total_amount']
    }


    const headerCartItemsDiv = document.getElementById('header-cart-items');
    headerCartItemsDiv.replaceChildren();

    for (let i = 0; i < data['items'].length; i++) {
        let product = data['items'][i]['product']['name'];
        let slug = data['items'][i]['product']['slug'];
        let image = data['items'][i]['product']['image'];
        let price = data['items'][i]['price'];
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
                    <div class="widget-product-meta"><span class="text-accent me-2">${price}</span><span class="text-muted">x ${quantity}</span>
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