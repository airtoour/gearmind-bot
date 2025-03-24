from sqlalchemy import event, inspect
from db.models import Cars


@event.listens_for(Cars, "before_insert")
def add_full(mapper, connection, target):
    target.full = (
        f"{target.brand_name} {target.model_name} "
        f"{target.gen_name} {target.year} года с "
        f"пробегом {target.mileage} тыс. км"
    )


@event.listens_for(Cars, "before_update")
def auto_update_full(target):
    if inspect(target).modified:
        target.full = (
            f"{target.brand_name} {target.model_name} "
            f"{target.gen_name} {target.year} года с "
            f"пробегом {target.mileage} тыс. км"
        )
