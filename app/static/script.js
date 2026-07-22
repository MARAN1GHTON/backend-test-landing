document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById("contactForm");
    const submitBtn = document.getElementById("submitBtn");
    const btnText = document.querySelector(".btn-text");
    const spinner = document.getElementById("spinner");
    
    const alertBox = document.getElementById("alertBox");
    const alertMessage = document.getElementById("alertMessage");
    const aiResponseBox = document.getElementById("aiResponseBox");
    const aiReplyText = document.getElementById("aiReplyText");

    form.addEventListener("submit", async (e) => {
        e.preventDefault();

        // Скрытие предыдущих результатов и ошибок
        alertBox.className = "alert hide";
        aiResponseBox.classList.add("hide");

        // Показ спиннера, отключение кнопки
        submitBtn.disabled = true;
        btnText.textContent = "Отправка...";
        spinner.classList.remove("hide");

        // Сбор данных формы
        const formData = {
            name: document.getElementById("name").value,
            phone: document.getElementById("phone").value,
            email: document.getElementById("email").value,
            comment: document.getElementById("comment").value
        };

        try {
            // Отправка POST запроса на API
            const response = await fetch("/api/contact", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (response.ok) {
                // Успешный ответ
                form.reset();
                showAlert(data.message, "success");
                
                // Отображение ответа ИИ
                if (data.ai_analysis && data.ai_analysis.auto_reply) {
                    aiReplyText.textContent = data.ai_analysis.auto_reply;
                    aiResponseBox.classList.remove("hide");
                }
            } else {
                // Обработка ошибок (в т.ч. Rate Limit 429 или валидации 422)
                let errorMsg = data.detail || "Произошла неизвестная ошибка";
                
                // Ошибки валидации приходят в виде массива
                if (Array.isArray(data.detail)) {
                    errorMsg = data.detail.map(err => err.msg).join(", ");
                }
                
                showAlert(errorMsg, "error");
            }
        } catch (error) {
            console.error("Network error:", error);
            showAlert("Ошибка соединения с сервером.", "error");
        } finally {
            // Восстановление состояния кнопки
            submitBtn.disabled = false;
            btnText.textContent = "Отправить сообщение";
            spinner.classList.add("hide");
        }
    });

    // Функция для отображения оповещений
    function showAlert(message, type) {
        alertMessage.textContent = message;
        alertBox.className = `alert ${type}`;
    }
});
