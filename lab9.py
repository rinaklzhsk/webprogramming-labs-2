from flask import Blueprint, render_template, request, redirect, url_for

lab9 = Blueprint('lab9', __name__)

# Страница с формой для ввода имени
@lab9.route('/lab9/', methods=['GET', 'POST'])
def lab():
    if request.method == 'POST':
        name = request.form['name']
        return redirect(url_for('lab9.age', name=name))  # Перенаправляем на страницу для ввода возраста
    return render_template('lab9/index.html')


# Страница с формой для ввода возраста
@lab9.route('/lab9/age/<name>', methods=['GET', 'POST'])
def age(name):
    if request.method == 'POST':
        age = request.form['age']
        return redirect(url_for('lab9.gender', name=name, age=age))  # Перенаправляем на страницу для ввода пола
    return render_template('lab9/age.html', name=name)


# Страница с формой для ввода пола
@lab9.route('/lab9/gender/<name>/<age>', methods=['GET', 'POST'])
def gender(name, age):
    if request.method == 'POST':
        gender = request.form['gender']
        return redirect(url_for('lab9.preference', name=name, age=age, gender=gender))  # Перенаправляем на страницу с вопросом
    return render_template('lab9/gender.html', name=name, age=age)


# Страница с вопросом о предпочтениях (вкусное/красивое)
@lab9.route('/lab9/preference/<name>/<age>/<gender>', methods=['GET', 'POST'])
def preference(name, age, gender):
    if request.method == 'POST':
        preference = request.form['preference']
        return redirect(url_for('lab9.sub_preference', name=name, age=age, gender=gender, preference=preference))  # Перенаправляем на подкатегорию
    return render_template('lab9/preference.html', name=name, age=age, gender=gender)


# Страница с подкатегорией (сладкое/соленое или что-то другое)
@lab9.route('/lab9/sub_preference/<name>/<age>/<gender>/<preference>', methods=['GET', 'POST'])
def sub_preference(name, age, gender, preference):
    if request.method == 'POST':
        sub_preference = request.form['sub_preference']
        return redirect(url_for('lab9.congratulations', name=name, age=age, gender=gender, preference=preference, sub_preference=sub_preference))  # Перенаправляем на поздравление
    return render_template('lab9/sub_preference.html', name=name, age=age, gender=gender, preference=preference)


# Страница с поздравлением и картинкой
@lab9.route('/lab9/congratulations/<name>/<age>/<gender>/<preference>/<sub_preference>')
def congratulations(name, age, gender, preference, sub_preference):
    # Вставка правильного окончания в зависимости от пола
    pronoun = 'быстро вырос, был умным и красивым' if gender == 'male' else 'быстро выросла, была умной и красивой'

    # Подготовка текста и подарка в зависимости от выбора
    if preference == 'delicious' and sub_preference == 'sweet':
        gift = "мешочек конфет"
        image = "candies.jpg"
        message = f"Поздравляю тебя, {name}, желаю, чтобы ты {pronoun}. Вот тебе подарок — {gift}."
    elif preference == 'delicious' and sub_preference == 'savory':
        gift = "соленое угощение"
        image = "salty.jpg"
        message = f"Поздравляю тебя, {name}, желаю, чтобы ты {pronoun}. Вот тебе подарок — {gift}."
    elif preference == 'beautiful' and sub_preference == 'myself':
        gift = "красивое украшение"
        image = "decoration.jpg"
        message = f"Поздравляю тебя, {name}, желаю, чтобы ты {pronoun}. Вот тебе подарок — {gift}."
    else:
        gift = "красивое что-то"
        image = "light.jpg"
        message = f"Поздравляю тебя, {name}, желаю, чтобы ты {pronoun}. Вот тебе подарок — {gift}."

    return render_template('lab9/congratulations.html', message=message, image=image)

