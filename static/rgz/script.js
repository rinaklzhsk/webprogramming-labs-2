document.addEventListener('DOMContentLoaded', function () {
    const registerForm = document.querySelector('form');
    if (registerForm) {
        registerForm.addEventListener('submit', function (event) {
            const login = document.getElementById('login').value;
            const password = document.getElementById('password').value;

            if (!/^[a-zA-Z0-9]+$/.test(login)) {
                alert('Логин должен содержать только латинские буквы и цифры.');
                event.preventDefault();
            }

            if (!/^[a-zA-Z0-9]+$/.test(password)) {
                alert('Пароль должен содержать только латинские буквы и цифры.');
                event.preventDefault();
            }
        });
    }
});
