from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3',__name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name','Аноним')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age', 'неизвестный')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age','20')
    resp.set_cookie('name_color','magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('/lab3/success.html', price=price)


@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_style=font_style))

    if color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)

    if bg_color:  
        resp.set_cookie('bg_color', bg_color)

    if font_size:
        resp.set_cookie('font_size', font_size)

    if font_style:
        resp.set_cookie('font_style', font_style)
        return resp

    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size', '16')
    font_style = request.cookies.get('font_style', 'normal')

    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, 
                        font_size=font_size, font_style=font_style))
    return resp
    

@lab3.route('/lab3/ticket')
def ticket():
    ticket = 0
    FIO = request.args.get('FIO')
    age = request.args.get('age', 0)
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    placefrom = request.args.get('placefrom')
    placeto = request.args.get('placeto')
    date = request.args.get('date')
    belay = request.args.get('belay')

    if int(age) < 18:
        ticket += 700
        ticket_type = "Детский билет"
    else:
        ticket += 1000
        ticket_type = "Взрослый билет"
    if shelf == 'lower' or shelf == 'lower-side':
        ticket += 100
    if linen == 'withlinen':
        ticket += 75
    if baggage == 'withbaggage':
        ticket += 250
    if belay == 'withbelay':
        ticket += 150
    return render_template('lab3/ticket.html', FIO=FIO, age=age, 
                ticket=ticket, shelf=shelf, linen=linen, 
                baggage=baggage, belay=belay, ticket_type=ticket_type, 
                placefrom=placefrom, placeto=placeto, date=date)


@lab3.route('/lab3/del_settings')
def del_settings():
    resp = make_response(redirect('/lab3/settings'))
    resp.set_cookie('color') 
    resp.set_cookie('bg_color')
    resp.set_cookie('font_size')
    resp.set_cookie('font_style')
    return resp


books = [
    {"title": "Война и мир", "price": 450, "author": "Лев Толстой", "genre": "Роман"},
    {"title": "Преступление и наказание", "price": 380, "author": "Федор Достоевский", "genre": "Роман"},
    {"title": "Мастер и Маргарита", "price": 550, "author": "Михаил Булгаков", "genre": "Роман"},
    {"title": "1984", "price": 300, "author": "Джордж Оруэлл", "genre": "Антиутопия"},
    {"title": "Оно", "price": 600, "author": "Стивен Кинг", "genre": "Хоррор"},
    {"title": "Гарри Поттер и философский камень", "price": 400, "author": "Дж.К. Роулинг", "genre": "Фэнтези"},
    {"title": "Алиса в стране чудес", "price": 250, "author": "Льюис Кэрролл", "genre": "Фэнтези"},
    {"title": "Гордость и предубеждение", "price": 350, "author": "Джейн Остин", "genre": "Роман"},
    {"title": "Улисс", "price": 700, "author": "Джеймс Джойс", "genre": "Роман"},
    {"title": "Бойцовский клуб", "price": 320, "author": "Чак Паланик", "genre": "Роман"},
    {"title": "Путь к дому", "price": 480, "author": "Елена Королева", "genre": "Психология"},
    {"title": "Маленький принц", "price": 200, "author": "Антуан де Сент-Экзюпери", "genre": "Сказка"},
    {"title": "Граф Монте-Кристо", "price": 650, "author": "Александр Дюма", "genre": "Приключения"},
    {"title": "О дивный новый мир", "price": 290, "author": "Олдос Хаксли", "genre": "Антиутопия"},
    {"title": "Фауст", "price": 500, "author": "Гете", "genre": "Драма"},
    {"title": "Три товарища", "price": 370, "author": "Эрих Мария Ремарк", "genre": "Роман"},
    {"title": "Шантарам", "price": 450, "author": "Грегори Дэвид Робертс", "genre": "Приключения"},
    {"title": "Путь мирного воина", "price": 300, "author": "Дэн Миллман", "genre": "Философия"},
    {"title": "Алхимик", "price": 280, "author": "Пауло Коэльо", "genre": "Философия"},
    {"title": "Сумерки", "price": 330, "author": "Стефани Майер", "genre": "Фэнтези"}
]

# Главная страница с формой и результатами поиска
@lab3.route('/lab3/books', methods=['GET', 'POST'])
def books_view():
    if request.method == 'POST':
        try:
            min_price = float(request.form.get('min_price', 0))
            max_price = float(request.form.get('max_price', float('inf')))
        except ValueError:
            min_price = 0
            max_price = float('inf')

        # Фильтруем книги, цена которых в указанном диапазоне
        filtered_books = [book for book in books if min_price <= book["price"] <= max_price]
        return render_template('lab3/books.html', books=filtered_books, min_price=min_price, max_price=max_price)
    
    return render_template('lab3/books.html', books=None)