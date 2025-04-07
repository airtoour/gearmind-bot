document.addEventListener("DOMContentLoaded", () => {
    const tgUserId = extractTgUserIdFromURL();
    
    // Инициализация Telegram WebApp
    Telegram.WebApp.ready();
    Telegram.WebApp.expand();

    // Загрузка данных игры
    loadGameData();

    async function loadGameData() {
        try {
            const initData = Telegram.WebApp.initData;
            
            const response = await fetch(`/game/${tgUserId}`, {
                headers: {
                    "X-Telegram-InitData": initData
                }
            });

            if (!response.ok) {
                const error = await response.text();
                throw new Error(error);
            }

            const html = await response.text();
            document.body.innerHTML = html;
            
        } catch (error) {
            Telegram.WebApp.showAlert(`Ошибка: ${error.message}`);
            Telegram.WebApp.close();
        }
    }

    function extractTgUserIdFromURL() {
        const path = window.location.pathname.split('/');
        return parseInt(path[path.length - 1]);
    }
});
