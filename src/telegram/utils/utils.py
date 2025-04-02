def get_formatted_prompt(prompt: str, username: str, carinfo: str) -> str:
    """Функция, возвращающая промпт с полной информацией"""
    result = (
        prompt
        .replace("<username>", username)
        .replace("<carinfo>", carinfo)
    )
    return result