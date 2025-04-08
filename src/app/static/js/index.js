document.addEventListener("DOMContentLoaded", async () => {
    const tg = window.Telegram.WebApp;
    const user_id = tg.initDataUnsafe?.user?.id;

    const greeting = document.getElementById("greeting");
    const playButton = document.getElementById("play");
    const createButton = document.getElementById("create");

    tg.expand();

    if (!user_id) {
        window.location.href = "/errors/400";
        return;
    }

    try {
        const res = await fetch(`/game/init/${user_id}`);
        const data = await res.json();

        if (data.user_name) {
            greeting.innerText = `Добро пожаловать, ${data.user_name}!`;
        }

        if (data.has_progress) {
            playButton.style.display = "inline-block";
            playButton.addEventListener("click", () => {
                window.location.href = `/game/profile/${user_id}`;
            });
        } else {
            createButton.style.display = "inline-block";
            createButton.addEventListener("click", async () => {
                try {
                    const carRes = await fetch(`/cars/${user_id}`);
                    const car_id = await carRes.json();

                    const createRes = await fetch("/game/create", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            user_id: user_id,
                            car_id: car_id
                        })
                    });

                    if (createRes.ok || createRes.redirected) {
                        window.location.href = `/game/profile/${user_id}`;
                    }
                } catch (err) {
                    window.location.href = `/errors/${carRes.status}`;
                }
            });
        }
    } catch (err) {
        window.location.href = `/errors/${res.status}`;
    }
});
