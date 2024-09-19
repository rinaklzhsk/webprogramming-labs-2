from flask import Flask, url_for, redirect
app = Flask(__name__)

@app.errorhandler(404)
def not_found(err):
    return "нет такой страницы", 404
# функция start() срабатывает и на «/», и на «/web».

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
        <!-- Заголовок -->
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
    <body>
        <h1>Это первая лабораторная работа</h1>
    </body>
</html>
'''