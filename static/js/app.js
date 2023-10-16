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
        const response = await fetch('/signup/api/signup/', {
            method: "POST",
            body: new FormData(signUpForm),
            headers: {'X-CSRFToken': csrftoken}
        });

        if (response.status === 201) {
            alertMessage.className = "alert alert-success alert-dismissible fade show mt-5";
            alertMessage.innerHTML = 'Signup successful!' +
                '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
            alertMessage.style.display = "block";
        } else {
            const data = await response.json();
            let errorMessage = '';
            for (const field in data) {
                if (data.hasOwnProperty(field)) {
                    errorMessage += `${data[field][0]} `;
                }
            }
            alertMessage.className = "alert alert-danger alert-dismissible fade show mt-5";
            alertMessage.innerHTML = errorMessage +
                '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>';
            alertMessage.style.display = "block";
        }
    } catch (error) {
        console.error('Error:', error);
    }
});

