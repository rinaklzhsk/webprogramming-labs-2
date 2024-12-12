from flask import Blueprint, render_template, request, session, current_app
import psycopg2
from psycopg2.extras import RealDictCursor
from os import path
import sqlite3

lab6 = Blueprint('lab6', __name__)

# Функции для работы с базой данных
def db_connect():
    if current_app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host = '127.0.0.1',
            database = 'irina_kaluzhskaya_knowledge_base',
            user = 'irina_kaluzhskaya_knowledge_base',
            password = '123'
        )
        cur = conn.cursor(cursor_factory=RealDictCursor)
    else:
        dir_path = path.dirname(path.realpath(__file__))
        db_path = path.join(dir_path, "database.db")
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()

    return conn, cur


def db_close(conn, cur):
    conn.commit()
    cur.close()
    conn.close()

# Главная страница
@lab6.route('/lab6/')
def main():
    login = session.get('login', '')
    return render_template('lab6/lab6.html', login=login)

# JSON-RPC API для работы с офисами
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    method = data.get('method')
    id = data.get('id')
    conn, cur = db_connect()

    try:
        # Получение списка офисов с сортировкой по номеру
        if method == 'info':
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM offices ORDER BY number ASC;")  # Сортировка по номеру офиса
            else:
                cur.execute("SELECT * FROM offices ORDER BY number ASC;")
            offices = cur.fetchall()
            return {
                'jsonrpc': '2.0',
                'result': [
                    {"number": office["number"], "tenant": office["tenant"], "price": office["price"]}
                    for office in offices
                ],
                'id': id
            }

        # Проверка авторизации
        login = session.get('login')
        if not login:
            return {
                'jsonrpc': '2.0',
                'error': {'code': 1, 'message': 'Пожалуйста, авторизуйтесь'},
                'id': id
            }

        # Расчет общей стоимости бронирования
        if method == 'user_total_cost':
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT SUM(price) AS total FROM offices WHERE tenant = %s;", (login,))
            else:
                cur.execute("SELECT SUM(price) AS total FROM offices WHERE tenant = ?;", (login,))
            result = cur.fetchone()
            total_cost = result["total"] if result["total"] else 0
            return {
                'jsonrpc': '2.0',
                'result': total_cost,
                'id': id
            }

        # Бронирование офиса
        if method == 'booking':
            office_number = data['params']
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM offices WHERE number = %s;", (office_number,))
            else:
                cur.execute("SELECT * FROM offices WHERE number = ?;", (office_number,))
            office = cur.fetchone()

            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {'code': 2, 'message': 'Офис не найден'},
                    'id': id
                }
            if office["tenant"]:
                return {
                    'jsonrpc': '2.0',
                    'error': {'code': 3, 'message': 'Уже забронировано!'},
                    'id': id
                }

            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE offices SET tenant = %s WHERE number = %s;", (login, office_number))
            else:
                cur.execute("UPDATE offices SET tenant = ? WHERE number = ?;", (login, office_number))
            conn.commit()
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }

        # Отмена бронирования офиса
        if method == 'cancellation':
            office_number = data['params']
            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("SELECT * FROM offices WHERE number = %s;", (office_number,))
            else:
                cur.execute("SELECT * FROM offices WHERE number = ?;", (office_number,))
            office = cur.fetchone()

            if not office:
                return {
                    'jsonrpc': '2.0',
                    'error': {'code': 2, 'message': 'Office not found'},
                    'id': id
                }
            if office["tenant"] != login:
                return {
                    'jsonrpc': '2.0',
                    'error': {'code': 3, 'message': 'Вы не можете отменить чужое бронирование!'},
                    'id': id
                }

            if current_app.config['DB_TYPE'] == 'postgres':
                cur.execute("UPDATE offices SET tenant = NULL WHERE number = %s;", (office_number,))
            else:
                cur.execute("UPDATE offices SET tenant = NULL WHERE number = ?;", (office_number,))
            conn.commit()
            return {
                'jsonrpc': '2.0',
                'result': 'success',
                'id': id
            }

        # Метод не найден
        return {
            'jsonrpc': '2.0',
            'error': {'code': -32601, 'message': 'Method not found'},
            'id': id
        }
    finally:
        db_close(conn, cur)
