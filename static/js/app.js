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

// Sign up with sign in page
const regForm = document.getElementById('reg-form');
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
