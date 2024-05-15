from src.db.repository.users import get_user_by_tg
from src.db.models.cars import Cars
from src.db.db import session

def car_register(brand: str,
                 model: str,
                 gen: str,
                 year: int,
                 tg_user_id: str):
    user = get_user_by_tg(tg_user_id)

    try:
        if user:
            user_car = Cars(
                brand_name = brand,
                model_name = model,
                gen_name = gen,
                year = year,
                user_id = user.user_id
            )
            session.add(user_car)
            session.commit()
            print('Машина успешно зарегистрирована в базе данных!')
    except Exception as e:
        session.rollback()
        print(e)
        raise e
    finally:
        session.close()
