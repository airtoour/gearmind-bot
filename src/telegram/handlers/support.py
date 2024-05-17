from aiogram.types import Message
from src.db.models.models import Users
from src.telegram.keyboards.inline.inline import to_signup

async def support(message: Message):
    markup = to_signup()
    try:
        user = Users.get_user_by_tg(message.from_user.id)

        if user:
            await message.answer(
                'Если тебе понадобилась помощь, я постараюсь помочь тебе.\n'
                '\n'
                '\n'
                'Как стать частью нашей команды?\n'
                'Ты можешь зарегистрироваться на нашем сайте по кнопке ниже.'
                '\n'
                'Для вопросов по твоему заказу нажми на /order\n'
                'Там ты сможешь заказать:\n'
                '\n'
                '1. Необходимый товар для машины\n'
                '2. Проверить статус своего заказа\n'
                '\n'
            )
        else:
            await message.answer(
                "Сначала требуется пройти регистрацию, "
                "только потом ты сможешь пользоваться нашей системой.", reply_markup=markup
            )
    except Exception as e:
        await message.answer(
            "Кажется, произошла какая-то ошибка.\n"
            "Стараемся разобраться с этим, извините за неудобства...")
        print('SUPPORT: ', e)