document.addEventListener("DOMContentLoaded", () => {
    const btn = document.getElementById("my-tasks");
    const panel = document.getElementById("task-panel");
    const list = document.getElementById("task-list");
    const closeBtn = document.getElementById("close-tasks");

    const telegram = window.Telegram.WebApp;
    telegram.ready();

    const telegramId = telegram.initDataUnsafe.user?.id;

    async function fetchTasks() {
        if (!telegramId) return;

        try {
            const res = await fetch(`/tasks/${telegramId}/all`);
            const tasks = await res.json();
            renderTasks(tasks);
            panel.classList.add("visible");
        } catch (err) {
            console.error("Ошибка загрузки заданий:", err);
        }
    }

    function renderTasks(tasks) {
        list.innerHTML = "";

        const grouped = tasks.reduce((acc, task) => {
            if (!acc[task.type]) {
                acc[task.type] = [];
            }
            acc[task.type].push(task);
            return acc;
        }, {});

        for (const type in grouped) {
            // Заголовок категории
            const groupHeader = document.createElement("h4");
            groupHeader.className = "task-group-title";
            groupHeader.textContent = type;
            list.appendChild(groupHeader);

            // Список задач внутри категории
            grouped[type].forEach(task => {
                const el = document.createElement("div");
                el.className = "task-item";
                el.innerHTML = `
                    <strong>${task.title}</strong><br>
                    <small>${task.description}</small><br>
                    <span>Прогресс: ${task.current_value}/${task.target_value}</span><br>
                    <span>Опыт: +${task.reward_xp}</span>
                `;
                list.appendChild(el);
            });
        }
    }

    btn.addEventListener("click", fetchTasks);
    closeBtn.addEventListener("click", () => {
        panel.classList.remove("visible");
    });
});