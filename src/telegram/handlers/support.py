from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from src.models.models import Users
from src.exceptions import server_exceptions


async def support(message: Message, state: FSMContext):
    try:
        user = Users.query.filter_by(tg_user_id=message.from_user.id).first()

        if user:
            await message.answer('Если тебе понадобилась помощь, я постараюсь помочь тебе.\n'
                                 '\n'
                                 '\n'
                                 'Как стать частью нашей команды?\n'
                                 'Ты можешь зарегистрироваться на нашем сайте: САЙТ'
                                 '\n'
                                 'Для вопросов по твоему заказу нажми на /order\n'
                                 'Там ты сможешь заказать:\n'
                                 '\n'
                                 '1. Необходимый товар для машины\n'
                                 '2. Проверить статус своего заказа\n'
                                 '\n')
        else:
            await message.answer('Сначала ты зарегистрируйся, а потом ты сможешь пользоваться нашей системой.')
    except Exception as e:
        print('SUPPORT: ', e)
        print(server_exceptions(400, 'Что-то пошло не так в support:\n'))