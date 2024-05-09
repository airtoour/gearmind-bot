from flask import Blueprint, render_template, redirect, url_for, request


car = Blueprint('car', __name__, template_folder='templates')

@car.route('/', methods=['GET', 'POST'])
def register_car():
    message = None

    if request.method == 'POST':
        brand = request.form.get('brand')
        model = request.form.get('model')
        car_gen = request.form.get('gen')
