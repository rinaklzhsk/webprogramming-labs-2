from flask import Blueprint, url_for, redirect
lab1 = Blueprint('lab1',__name__)


# Маршрут для первой лабораторной
@lab1.route('/lab1/')
def lab():
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
                <a href="/lab1/berserk">Берсерк</a>
            </li>
        </body>
    </html>
    '''


@lab1.route("/lab1/web")
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


@lab1.route("/lab1/author")
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
@lab1.route('/lab1/oak')
def oak():
    path = url_for("static", filename="lab1/oak.jpg")
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


@lab1.route('/lab1/counter')
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
@lab1.route('/lab1/reset_counter')
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


@lab1.route("/lab1/info")
def info():
    return redirect("/lab1/author")


# Маршрут с текстом и изображением, а также с заголовками Content-Language и нестандартными заголовками
@lab1.route('/lab1/berserk')
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
            <img src="''' + url_for('static', filename='lab1/berserk.png') + '''">
        </body>
    </html>''', { 
    "Content-Language": "ru", 
    "Genre": "fantasy manga", 
    "Author": "Kentaro Miura" 
}