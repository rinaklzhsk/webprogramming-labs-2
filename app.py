from flask import Flask, url_for, redirect, render_template
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return """<!doctype html>
        <html>
            <head>
                <title>Страница не найдена - 404</title>
                <style>
                    body {
                        font-family: Arial, sans-serif;
                        text-align: center;
                        background-color: #ffe4e1; 
                        margin: 0;
                        padding: 0;
                    }
                    h1 {
                        font-size: 48px;
                        margin-top: 50px;
                        color: #ff69b4;  
                    }
                    p {
                        font-size: 18px;
                        color: #c71585;  
                    }
                    img {
                        width: 300px;
                        height: auto;
                        margin-top: 20px;
                    }
                    a {
                        display: inline-block;
                        margin-top: 30px;
                        padding: 10px 20px;
                        background-color: #ff1493;
                        color: white;
                        text-decoration: none;
                        border-radius: 5px;
                    }
                    a:hover {
                        background-color: #db7093;
                    }
                </style>
            </head> 
            <body>
                <h1>404 - Страница не найдена</h1>
                <p>Кажется, что-то пошло не так. Эта страница не существует.</p>
                <img src='""" + url_for('static', filename='404.jpg') + """'>
                <p>Возможно, вы ошиблись в адресе. Попробуйте вернуться на главную.</p>
                <a href="/">На главную</a>
            </body>
        </html>""", 404

@app.route("/lab1/web")
def web():
    # возвращает html-страницу
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
           </body>
        </html>""",200,{
            # возвращается заголовок X-Server
            'X-Server': 'sample', 
            # выводит тест
            'Content-Type': 'text/plain; charset=utf-8'
        } 


@app.route("/lab1/author")
def author():
    name = "Калужская Ирина Витальевна"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факульет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""

# выдавает страницу с картинкой дуба
@app.route('/lab1/oak')
def oak():
    path = url_for("static", filename="oak.jpg")
    return '''
<!doctype html>
<html>
    <head>
        <link rel="stylesheet" href="''' + url_for("static", filename="lab1.css") + '''">
    </head>
    <body>
        <h1>Дуб</h1>
        <img src="''' + path + '''">
    </body>
</html>
'''

count = 0

@app.route('/lab1/counter')
def counter():
    global count
    count += 1
    return '''
<!doctype html>
<html>
    <body>
        Сколько раз вы сюда заходили: ''' + str(count) + '''
    </body>
</html>
''',  201

# Роут для сброса счетчика
@app.route('/lab1/reset_counter')
def reset_counter():
    global count
    count = 0
    return '''
<!doctype html>
<html>
    <body>
        <p>Счётчик был успешно очищен.</p>
        <a href="/lab1/counter">Вернуться к счётчику</a>
    </body>
</html>
''', 200

@app.route("/lab1/info")
def info():
    return redirect("/lab1/author")

# Главная страница с адресами '/' и '/index'
@app.route('/')
@app.route('/index')
def index():
    return '''
<!doctype html>
<html>
    <head>
        <title>НГТУ, ФБ, Лабораторные работы</title>
    </head>
    <body>
        <header>
            <h1>НГТУ, ФБ, WEB-программирование, часть 2. Список лабораторных</h1>
        </header>
        
        <ul>
            <li><a href="''' + url_for('lab1') + '''">Первая лабораторная</a></li>
        </ul>
        
        <footer style = "bottom: 0; position: fixed">
            <p>ФИО: Калужская Ирина Витальевна</p>
            <p>Группа: Группа ФБИ-21</p>
            <p>Курс: 3</p>
            <p>Год: 2024</p>
        </footer>
    </body>
</html>
'''

# Маршрут для первой лабораторной
@app.route('/lab1')
def lab1():
    return '''
<!doctype html>
<html>
    <head>
        <title>Лабораторная 1</title>
    </head>
    <body>
        <h1>Лабораторная 1</h1>
        <p>
            Flask — фреймворк для создания веб-приложений на языке программирования Python, 
            использующий набор инструментов Werkzeug, а также шаблонизатор Jinja2. 
            Относится к категории так называемых микрофреймворков — минималистичных каркасов 
            веб-приложений, сознательно предоставляющих лишь самые базовые возможности.
        </p>
        <p><a href="/">На главную</a></p>
        <h2>Список роутов</h2>
        <li>
            <a href="/lab1/web">Веб</a>
        </li>
        <li>
            <a href="/lab1/author">Автор</a>
        </li>
        <li>
            <a href="/lab1/oak">Дуб</a>
        </li>
        <li>
            <a href="/lab1/counter">Счетчик</a>
        </li>
        <li>
            <a href="/lab1/reset_counter">Ресет счетчика</a>
        </li>
        <li>
            <a href="/lab1/info">Инфо</a>
        </li>
        <li>
            <a href="/">Главная страница 1</a>
        </li>
        <li>
            <a href="/index">Главная страница 2</a>
        </li>
        <li>
            <a href="/lab1">Первая лабораторная</a>
        </li>
        <li>
            <a href="/error400">Ошибка 400</a>
        </li>
        <li>
            <a href="/error401">Ошибка 401</a>
        </li>
        <li>
            <a href="/error402">Ошибка 402</a>
        </li>
        <li>
            <a href="/error403">Ошибка 403</a>
        </li>
        <li>
            <a href="/error405">Ошибка 405</a>
        </li>
        <li>
            <a href="/error418">Ошибка 418</a>
        </li>
        <li>
            <a href="/cause_error">Вызов ошибки</a>
        </li>
        <li>
            <a href="/berserk">Берсерк</a>
        </li>
    </body>
</html>
'''

# Маршрут для кода 400 (Bad Request)
@app.route('/error400')
def error_400():
    return '''
<!doctype html>
<html>
    <body>
        <h1>400 - Bad Request</h1>
        <p>Сервер не может обработать ваш запрос.</p>
    </body>
</html>
''', 400

# Маршрут для кода 401 (Unauthorized)
@app.route('/error401')
def error_401():
    return '''
<!doctype html>
<html>
    <body>
        <h1>401 - Unauthorized</h1>
        <p>Доступ запрещен. Требуется авторизация.</p>
    </body>
</html>
''', 401

# Маршрут для кода 402 (Payment Required)
@app.route('/error402')
def error_402():
    return '''
<!doctype html>
<html>
    <body>
        <h1>402 - Payment Required</h1>
        <p>Требуется оплата для доступа к ресурсу.</p>
    </body>
</html>
''', 402

# Маршрут для кода 403 (Forbidden)
@app.route('/error403')
def error_403():
    return '''
<!doctype html>
<html>
    <body>
        <h1>403 - Forbidden</h1>
        <p>Доступ к ресурсу запрещен.</p>
    </body>
</html>
''', 403

# Маршрут для кода 405 (Method Not Allowed)
@app.route('/error405')
def error_405():
    return '''
<!doctype html>
<html>
    <body>
        <h1>405 - Method Not Allowed</h1>
        <p>Запрошенный метод не разрешен для этого ресурса.</p>
    </body>
</html>
''', 405

# Маршрут для кода 418 (I'm a teapot)
@app.route('/error418')
def error_418():
    return '''
<!doctype html>
<html>
    <body>
        <h1>418 - I'm a teapot</h1>
        <p>Я — чайник, и я не могу заварить кофе.</p>
    </body>
</html>
''', 418

# Маршрут, который вызывает ошибку на сервере
@app.route('/cause_error')
def cause_error():
    # Намеренная ошибка: деление на ноль
    return 1 / 0  # Это вызовет ошибку 500

# Перехватчик для ошибки 500 (Internal Server Error)
@app.errorhandler(500)
def internal_server_error(err):
    return '''
<!doctype html>
<html>
    <head>
        <title>Ошибка сервера - 500</title>
    </head> 
    <body>
        <h1>500 - Внутренняя ошибка сервера</h1>
        <p>На сервере произошла ошибка.</p>
        <a href="/">На главную</a>
    </body>
</html>
''', 500

# Маршрут с текстом и изображением, а также с заголовками Content-Language и нестандартными заголовками
@app.route('/berserk')
def berserk():
    return '''
    <!doctype html>
    <html lang="ru">
        <head>
            <title>Берсерк</title>
        </head>
        <body>
            <h1>Краткое содержание сюжета Берсерка</h1>
            <p>
            Это история воина по имени Гатс, который живет в мире, напоминающем Европу Средневековья. 
            В детстве он потерял свою семью и присоединился к банде наемников, где стал одним из лучших воинов. 
            Во время одной из битв Гатс встретил Гриффита, командира наемного отряда Сокола, и стал его лучшим другом.
            </p>
            <p>
            Однако в своей жажде власти и славы Гриффит предал своих товарищей, включая Гатса, и заключил сделку 
            с богом демонов, чтобы стать могущественным и узнать истинную природу мира.
            </p>
            <p>
            Гатс выжил в массакре и начал мстить своему бывшему другу, отправляясь в опасное путешествие по миру, 
            населенному демонами и другими опасными существами. Он путешествует в поисках силы и возможности отомстить Гриффиту.
            </p>
            <img src="''' + url_for('static', filename='berserk.png') + '''">
        </body>
    </html>''', { 
    "Content-Language": "ru", 
    "Genre": "fantasy manga", 
    "Author": "Kentaro Miura" 
}

@app.route('/lab2/a')
def a():
    return 'без слэша'

@app.route('/lab2/a/')
def a2():
    return 'со слэшем'

flower_list = ['роза','тюльпан','незабудка','ромашка']

# @app.route('/lab2/flowers/<int:flower_id>')
# def flowers(flower_id):
#     if flower_id >= len(flower_list):
#         return 'такого цветка нет', 404
#     else:
#         return "цветок: " + flower_list[flower_id]
    
# Улучшенный роут для вывода информации о цветке по ID
@app.route('/lab2/flowers/<int:flower_id>')
def get_flower_by_id(flower_id):
    if flower_id >= len(flower_list) or flower_id < 0:
        return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка</h1>
        <p>Такого цветка нет.</p>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </body>
</html>
''', 404

    return f'''
<!doctype html>
<html>
    <body>
        <h1>Цветок: {flower_list[flower_id]}</h1>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

# Обработчик для добавления цветка
@app.route('/lab2/add_flower/')
@app.route('/lab2/add_flower/<name>')
def add_flower(name=None):
    if not name:  # Проверка на отсутствие имени
        return '''
<!doctype html>
<html>
    <body>
        <h1>Ошибка</h1>
        <p>Вы не задали имя цветка.</p>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </body>
</html>
''', 400  # Возвращаем HTML с ошибкой 400

    flower_list.append(name)  # Добавляем цветок в список
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Добавлен новый цветок</h1>
        <p>Название нового цветка: {name}</p>
        <p>Всего цветов: {len(flower_list)}</p>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

# Роут для вывода всех цветов и их количества
@app.route('/lab2/flowers')
def show_flowers():
    return f'''
<!doctype html>
<html>
    <body>
        <h1>Список всех цветов</h1>
        <p>Всего цветов: {len(flower_list)}</p>
        <ul>
            {''.join(f'<li>{flower}</li>' for flower in flower_list)}
        </ul>
        <a href="/lab2/clear_flowers">Очистить список цветов</a>
    </body>
</html>
'''

# Роут для очистки списка цветов
@app.route('/lab2/clear_flowers')
def clear_flowers():
    flower_list.clear()  # Очищаем список цветов
    return '''
<!doctype html>
<html>
    <body>
        <h1>Список цветов очищен</h1>
        <a href="/lab2/flowers">Посмотреть все цветы</a>
    </body>
</html>
'''

# Создаем маршрут для example
@app.route('/lab2/example')
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

@app.route('/lab2/')
def lab2():
    return render_template('lab2.html')

@app.route('/lab2/filters')
def filters():
    phrase = "О <b>сколько</b> <u>нам</u> <i>открытий</i> чудных..."
    return render_template('filter.html', phrase=phrase)
    
# Основной маршрут для математических операций с двумя числами
@app.route('/lab2/calc/<int:a>/<int:b>')
def calc(a, b):
    addition = a + b
    subtraction = a - b
    multiplication = a * b
    division = a / b if b != 0 else "не делится на 0"
    power = a ** b

    return f'''
<!doctype html>
<html>
    <body>
        <h1>Расчёт с параметрами:</h1>
        <p>{a} + {b} = {addition}</p>
        <p>{a} - {b} = {subtraction}</p>
        <p>{a} * {b} = {multiplication}</p>
        <p>{a} / {b} = {division}</p>
        <p>{a}<sup>{b}</sup> = {power}</p>
    </body>
</html>
'''

# Маршрут, который перенаправляет с /lab2/calc/ на /lab2/calc/1/1
@app.route('/lab2/calc/')
def calc_default():
    return redirect(url_for('calc', a=1, b=1))

# Маршрут, который перенаправляет с /lab2/calc/<int:a> на /lab2/calc/a/1
@app.route('/lab2/calc/<int:a>')
def calc_with_one(a):
    return redirect(url_for('calc', a=a, b=1))