document.addEventListener("DOMContentLoaded", async () => {
    const userLevel = document.getElementById("level");
    const userExperience = document.getElementById("experience");
    const myCar = document.getElementById("my-car");
    const washStatus = document.getElementById("wash-status");

    const tg = window.Telegram.WebApp;
    const tgUserId = tg.initDataUnsafe?.user?.id;

    try {
        const res = await fetch(`/game/garage/wash/status?telegram_id=${tgUserId}`);
        const data = await res.json();

        if (data.status === "fail") {
            alert(data.message);
            window.location.href = "/errors/400";
            return;
        } else {
            washStatus.innerText = data.message;
        }

        if (data.next_wash_at) {
            // Преобразуем строку времени в объект Date
            const nextWashTime = new Date(data.next_wash_at);
            // Начинаем отсчёт с момента следующей мойки
            startCountdownTimer(nextWashTime);
        }

        myCar.addEventListener("click", async () => {
            try {
                const response = await fetch("/game/garage/wash", {
                    method: "PATCH",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ tg_user_id: tgUserId }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    alert(errorData.data.message || "Ошибка при мытье");
                    return;
                }

                const result = await response.json();
                alert(result.data.message);

                // Обновить таймер после мойки
                if (result.washed) {
                    const nextWash = new Date(result.data.last_wash_car_time);
                    nextWash.setHours(nextWash.getHours() + 6); // добавляем 6 часов
                    startCountdownTimer(nextWash); // перезапускаем таймер
                }
            } catch (err) {
                console.error(err);
                alert("Произошла ошибка при мытье автомобиля");
            }
        });
    } catch (err) {
        console.error(err);
        alert("Ошибка загрузки статуса");
        window.location.href = "/errors/400";
    }

    async function startCountdownTimer(endTime) {
        const getLevel = await fetch(`/game/level/${tgUserId}`);

        if (!getLevel.ok) {
            alert("Ошибка при получении уровня");
            return;
        }

        const levelData = await getLevel.json();

        userLevel.innerHTML = `<strong>Уровень:</strong> ${levelData.level}`;
        userExperience.innerHTML = `<strong>Опыт:</strong> ${levelData.experience}`;

        function updateTimer() {
            const now = new Date();
            const diff = endTime - now;

            if (diff <= 0) {
                washStatus.innerText = "Автомобиль снова грязный! Пора его помыть 🧽";
                clearInterval(timer);
                return;
            }

            const hours = Math.floor(diff / (1000 * 60 * 60));
            const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
            const seconds = Math.floor((diff % (1000 * 60)) / 1000);

            // Обновляем статус с оставшимся временем
            washStatus.innerText = `🚿 Следующая мойка доступна через ${hours}ч ${minutes}м ${seconds}с`;
        }

        updateTimer(); // Обновим сразу при загрузке
        const timer = setInterval(updateTimer, 1000); // Обновление каждую секунду
    }
});
