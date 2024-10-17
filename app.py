from flask import Flask, url_for, redirect, render_template, request
from lab1 import lab1
from lab2 import lab2
from lab3 import lab3

app = Flask(__name__)
app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)


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


# Главная страница с адресами '/'
# корень сайта
@app.route('/')
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
                <li><a href="''' + url_for('lab1.lab') + '''">Первая лабораторная</a></li>
                <li><a href="''' + url_for('lab2.labtwo') + '''">Вторая лабораторная</a></li>
                <li><a href="''' + url_for('lab3.lab') + '''">Третья лабораторная</a></li>
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