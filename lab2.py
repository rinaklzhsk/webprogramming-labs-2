from flask import Blueprint, url_for, redirect, render_template
lab2 = Blueprint('lab2',__name__)


@lab2.route('/lab2/a')
def a():
    return 'без слэша'


@lab2.route('/lab2/a/')
def a2():
    return 'со слэшем'


flower_list = [
    {'name':'роза','price': 200},
    {'name':'тюльпан', 'price': 170},
    {'name':'незабудка','price': 100},
    {'name':'ромашка','price': 100}
    ]


# Маршрут для отображения списка цветов
@lab2.route('/lab2/flowers')
def show_flowers():
    return render_template('flowers.html', flower_list=flower_list)


# Обработчик для удаления всех цветов
@lab2.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()
    return redirect(url_for('lab2.show_flowers'))


# Обработчик для удаления цветка по его индексу
@lab2.route('/lab2/del_flower/<int:flower_id>')
def del_flower(flower_id):
    # Проверка, существует ли цветок с таким индексом
    if 0 <= flower_id < len(flower_list):
        del flower_list[flower_id]  # Удаление цветка
        return redirect(url_for('lab2.show_flowers'))
    else:
        # Если цветок не найден, возвращаем 404
        abort(404)


# Обработчик для добавления нового цветка
@lab2.route('/lab2/add_flower', methods=['POST'])
def add_flower():
    name = request.form['name']
    price = request.form['price']
    # Добавляем новый цветок в список, проверяем наличие имени и цены
    if name and price.isdigit():
        flower_list.lab2end({'name': name, 'price': int(price)})
    return redirect(url_for('lab2.show_flowers'))


# Создаем маршрут для example
@lab2.route('/lab2/example')
def example():
    # определяем переменные
    name = 'Калужская Ирина'
    group = 'ФБИ-21'
    labnum = '2'
    course = '3 курс'
    fruits = [
        {'name': 'яблоки', 'price': 100}, 
        {'name': 'груши', 'price': 120},
        {'name': 'апельсины', 'price': 80},
        {'name': 'мандарины', 'price': 95},
        {'name': 'манго', 'price': 321}
    ]
    # передаем переменные для отображения в HTML
    return render_template('example.html', name=name, group=group, 
                            labnum=labnum, course=course, fruits=fruits)


@lab2.route('/lab2/')
def labtwo():
    return render_template('lab2.html')


@lab2.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)
    

# Основной маршрут для математических операций с двумя числами
@lab2.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    a=a
    b=b
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else "не делится на 0"
    power = a ** b
    return render_template('calculate.html', addition=addition, 
                           subtraction=subtraction, 
                           multiplication=multiplication, 
                           division=division, power=power, a=a, b=b)


# Маршрут, который перенаправляет с /lab2/calc/ на /lab2/calc/1/1
@lab2.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('lab2.calc', a=1, b=1))


# Маршрут, который перенаправляет с /lab2/calc/<int:a> на /lab2/calc/a/1
@lab2.route('/lab2/calc/<int:a>')
def calc_with_one(a):
    return redirect(url_for('lab2.calc', a=a, b=1))


# Список книг
books = [
    {"author": "Лев Толстой", "title": "Война и мир", "genre": "Роман", "pages": 1225},
    {"author": "Федор Достоевский", "title": "Преступление и наказание", "genre": "Роман", "pages": 671},
    {"author": "Александр Пушкин", "title": "Евгений Онегин", "genre": "Поэма", "pages": 224},
    {"author": "Антон Чехов", "title": "Вишневый сад", "genre": "Пьеса", "pages": 96},
    {"author": "Николай Гоголь", "title": "Мертвые души", "genre": "Поэма", "pages": 352},
    {"author": "Иван Тургенев", "title": "Отцы и дети", "genre": "Роман", "pages": 432},
    {"author": "Михаил Булгаков", "title": "Мастер и Маргарита", "genre": "Фантастический роман", "pages": 470},
    {"author": "Виктор Пелевин", "title": "Чапаев и Пустота", "genre": "Фантастика", "pages": 320},
    {"author": "Борис Акунин", "title": "Азазель", "genre": "Детектив", "pages": 288},
    {"author": "Аркадий и Борис Стругацкие", "title": "Пикник на обочине", "genre": "Фантастика", "pages": 224}
]


@lab2.route('/lab2/books')
def show_books():
    return render_template('books.html', books=books)


cats = [
    {"name": "Сиамская кошка", "description": "Известны своим стройным телом и ярко-голубыми глазами.", "image": "siamese.webp"},
    {"name": "Мейн-кун", "description": "Очень крупная порода кошек с густой шерстью и большими лапами.", "image": "mainecoon.webp"},
    {"name": "Бенгальская кошка", "description": "Активная кошка с пятнистым окрасом, похожая на дикого леопарда.", "image": "bengal.jpg"},
    {"name": "Британская короткошёрстная", "description": "Известна своим спокойным характером и плюшевой шерстью.", "image": "british.jpg"},
    {"name": "Моя кошка", "description": "Отличается игривостью, милостью и прожорливостью.", "image": "mycat.jpg"}
]


@lab2.route('/lab2/cats')
def show_cats():
    return render_template('cats.html',cats=cats)