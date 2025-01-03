from flask import Flask, url_for, redirect, render_template, request
import os
from os import path
from flask_sqlalchemy import SQLAlchemy
from db import db
from db.models import users
from flask_login import LoginManager

from lab1 import lab1
from lab2 import lab2
from lab3 import lab3
from lab4 import lab4
from lab5 import lab5
from lab6 import lab6
from lab7 import lab7
from lab8 import lab8
from lab9 import lab9
from rgz import rgz

app = Flask(__name__)

login_manager = LoginManager()
login_manager.login_view = 'lab8.login'
login_manager.init_app(app)

@login_manager.user_loader
def load_users(login_id):
    return users.query.get(int(login_id))

app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'super-secret-key')
app.config['DB_TYPE'] = os.getenv('DB_TYPE', 'postgres')

if app.config['DB_TYPE'] == 'postgres':
    db_name = 'irina_kaluzhskaya_orm'
    db_user = 'irina_kaluzhskaya_orm'
    db_password = '123'
    host_ip = '127.0.0.1'
    host_port = 5432

    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{db_user}:{db_password}@{host_ip}:{host_port}/{db_name}'
else:
    dir_path = path.dirname(path.realpath(__file__))
    db_path = path.join(dir_path, "irina_kaluzhskaya_orm.db")
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///{db_path}'

db.init_app(app)

app.register_blueprint(lab1)
app.register_blueprint(lab2)
app.register_blueprint(lab3)
app.register_blueprint(lab4)
app.register_blueprint(lab5)
app.register_blueprint(lab6)
app.register_blueprint(lab7)
app.register_blueprint(lab8)
app.register_blueprint(lab9)
app.register_blueprint(rgz)


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
                <img src='""" + url_for('static', filename='/lab1/404.jpg') + """'>
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
                <li><a href="''' + url_for('lab4.lab') + '''">Четвертая лабораторная</a></li>
                <li><a href="''' + url_for('lab5.lab') + '''">Пятая лабораторная</a></li>
                <li><a href="''' + url_for('lab6.main') + '''">Шестая лабораторная</a></li>
                <li><a href="''' + url_for('lab7.main') + '''">Седьмая лабораторная</a></li>
                <li><a href="''' + url_for('lab8.lab') + '''">Восьмая лабораторная</a></li>
                <li><a href="''' + url_for('lab9.lab') + '''">Девятая лабораторная</a></li>
                <li><a href ="/rgz">РГЗ</a></li>
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