document.addEventListener("DOMContentLoaded", async () => {
    try {
        const tg = window.Telegram.WebApp;
        const tgId = tg.initDataUnsafe?.user?.id;

        const greeting = document.getElementById("greeting");
        const welcomeText = document.getElementById("welcome-text");
        const playButton = document.getElementById("play");
        const createButton = document.getElementById("create");

        // Проверка элементов
        if (!greeting || !playButton || !createButton) {
            alert("Ошибка: Элементы DOM не найдены!");
            return;
        }

        tg.expand();

        if (!tgId) {
            alert("Ошибка: TG ID не найден! Редирект на /errors/400");
            window.location.href = "/errors/400";
            return;
        }

        try {
            const profileInit = await fetch(`/game/init/${tgId}`);

            if (!profileInit.ok) {
                alert(`Ошибка профиля: ${profileInit.status}! Редирект на /errors/400`);
                window.location.href = "/errors/400";
                return;
            }

            const data = await profileInit.json();
            const userName = data.user_name?.trim() || tg.initDataUnsafe?.user?.first_name;

            greeting.innerText = `Добро пожаловать в GearGame, ${userName}!`;
            welcomeText.style.display = "block";

            if (data?.has_progress) {
                playButton.style.display = "inline-block";

                playButton.addEventListener("click", () => {
                    window.location.href = `/game/profile/${tgId}`;
                });
            } else {
                createButton.style.display = "inline-block";

                createButton.addEventListener("click", async () => {
                    try {
                        const carRes = await fetch(`/cars/${tgId}`);

                        if (!carRes.ok) {
                            alert(`Ошибка машины: ${carRes.status}`);
                            throw new Error("Car fetch failed");
                        }

                        const car_data = await carRes.json();

                        const car_id = car_data.id;
                        const user_id = car_data.user_id;

                        const createProfile = await fetch("/game/create", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ "user_id": user_id, "car_id": car_id })
                        });

                        const createProfileResult = await createProfile.json();

                        if (createProfile.ok || createProfile.redirected || createProfileResult.status == "ok") {
                            // Сообщение об успешно созданном профиле
                            alert(createProfileResult.message);

                            // Редирект на профиль
                            window.location.href = `/game/profile/${tgId}`;
                        } else {
                            alert(`Ошибка создания: ${createProfile.status}`);
                            window.location.href = "/errors/422";
                        }
                    } catch (err) {
                        alert(`Ошибка: ${err.message}`);
                        window.location.href = `/errors/500`;
                    }
                });
            }
        } catch (err) {
            alert(`Глобальная ошибка: ${err.message}`);
            window.location.href = `/errors/500`;
        }
    } catch (err) {
        // На случай, если упал даже Telegram WebApp
        console.error("Critical error:", err);
    }
});
