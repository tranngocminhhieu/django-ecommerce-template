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
