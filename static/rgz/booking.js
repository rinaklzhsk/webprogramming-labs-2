document.addEventListener('DOMContentLoaded', function () {
    const seatsContainer = document.querySelector('.seats');
    const bookingForm = document.getElementById('booking-form');
    const confirmButton = document.getElementById('confirm-booking');
    const selectedSeats = new Set(); // Хранит выбранные места

    if (seatsContainer && bookingForm) {
        seatsContainer.addEventListener('click', function (event) {
            console.log('Клик по контейнеру мест');
            const seatButton = event.target.closest('button');
            if (!seatButton) {
                console.log('Кнопка не найдена');
                return;
            }
            if (seatButton.disabled) {
                console.log('Кнопка отключена'); 
                return;
            }

            const seatNumber = seatButton.dataset.seat; 
            const seatCheckbox = bookingForm.querySelector(`input[value="${seatNumber}"]`);

            if (selectedSeats.has(seatNumber)) {
                // Если место уже выбрано, снимаем выбор
                selectedSeats.delete(seatNumber);
                seatButton.classList.remove('selected');
                seatCheckbox.checked = false;
            } else {
                // Если место не выбрано, добавляем его
                if (selectedSeats.size >= 5) {
                    alert('Вы можете выбрать не более 5 мест.');
                    return;
                }
                selectedSeats.add(seatNumber);
                seatButton.classList.add('selected');
                seatCheckbox.checked = true;
            }

            // Активируем или деактивируем кнопку подтверждения
            if (confirmButton) {
                confirmButton.disabled = selectedSeats.size === 0;
            }

            console.log('Выбранные места:', Array.from(selectedSeats));
        });

        // Обработка отправки формы
        bookingForm.addEventListener('submit', function (event) {
            if (selectedSeats.size === 0) {
                event.preventDefault();
                alert('Выберите хотя бы одно место.');
            }
        });
    }
});