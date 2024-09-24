from flask import Flask, url_for, redirect
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
def internal_server_error(e):
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
