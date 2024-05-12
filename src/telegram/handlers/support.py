from aiogram.types import Message
from src.models.models import Users
from src.db.db_app import app


async def support(message: Message):
    try:
        with app.app_context():
            user = Users.get_current(message.from_user.id)

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
                await message.answer('Сначала требуется пройти регистрацию, '
                                     'только потом ты сможешь пользоваться нашей системой.')
    except Exception as e:
        await message.answer('Кажется, произошла какая-то ошибка.\n'
                             'Стараемся разобраться с этим, извините за неудобства...')
        print('SUPPORT: ', e)