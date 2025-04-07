document.addEventListener("DOMContentLoaded", () => {
    const tg = window.Telegram.WebApp;
    const user_id = tg.initDataUnsafe.user?.id;

    const playButton = document.getElementById("play");
    const createButton = document.getElementById("create");

    if (createButton) {
        document.getElementById("create")?.addEventListener("click", async () => {
            const user_car_id = await fetch(`/cars/${user_id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json"
                }
            });

            const create_game = await fetch("/game/create", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: user_id,
                    car_id: user_car_id
                })
            });

            if (create_game.redirected) {
                window.location.href = create_game.url;
            }
        });
    }

    if (playButton) {
        playButton.addEventListener("click", () => {
            // Показать уровень и опыт
            document.getElementById("level").style.display = "block";
            document.getElementById("experience").style.display = "block";

            // Скрыть кнопку "Играть"
            playButton.style.display = "none";

            // Получить user_id из переменной шаблона
            const user_id = "{{ user_id }}";  // Убедись, что user_id передается правильно в шаблоне

            // Ждем некоторое время, чтобы изменения DOM были видны
            setTimeout(() => {
                // После показа информации — редирект
                window.location.href = `/game/${user_id}`;
            }, 500);  // Задержка в 500 мс
        });
    }
)};