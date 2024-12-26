from flask import Flask, render_template, request, redirect, url_for, session, flash, current_app
from flask import Blueprint
import psycopg2
from psycopg2.extras import RealDictCursor
from werkzeug.security import generate_password_hash, check_password_hash
from os import path
import sqlite3


app = Flask(__name__)
app.secret_key = 'secret'  # Установите секретный ключ для сессий

rgz = Blueprint('rgz', __name__)

# Конфигурация базы данных
app.config['DB_TYPE'] = 'postgres' 
app.config['POSTGRES_HOST'] = '127.0.0.1'
app.config['POSTGRES_DB'] = 'rgz'
app.config['POSTGRES_USER'] = 'rgz'
app.config['POSTGRES_PASSWORD'] = '123'

def db_connect():
    if app.config['DB_TYPE'] == 'postgres':
        conn = psycopg2.connect(
            host=app.config['POSTGRES_HOST'],
            database=app.config['POSTGRES_DB'],
            user=app.config['POSTGRES_USER'],
            password=app.config['POSTGRES_PASSWORD']
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


@rgz.route('/rgz/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form['full_name']
        login = request.form['login']
        password = request.form['password']
        password_hash = generate_password_hash(password)

        conn, cur = db_connect()
        try:
            cur.execute('INSERT INTO users (full_name, login, password_hash) VALUES (%s, %s, %s)',
                        (full_name, login, password_hash))
            conn.commit()
            flash('Регистрация прошла успешно!', 'success')
            return redirect(url_for('rgz.login')) 
        except psycopg2.IntegrityError:
            flash('Логин уже занят. Попробуйте другой.', 'error')
        finally:
            db_close(conn, cur)

    return render_template('rgz/register.html')

@rgz.route('/rgz/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        conn, cur = db_connect()
        try:
            cur.execute('SELECT * FROM users WHERE login = %s', (login,))
            user = cur.fetchone()

            if user and check_password_hash(user['password_hash'], password):
                session['user_id'] = user['id']
                session['full_name'] = user['full_name']
                session['is_admin'] = user.get('is_admin', False)

                if session['is_admin']:
                    flash('Вы успешно вошли в систему как администратор!', 'success')
                else:
                    flash('Вы успешно вошли в систему!', 'success')

                return redirect(url_for('rgz.index'))
            else:
                flash('Неверный логин или пароль.', 'error')
        finally:
            db_close(conn, cur)

    return render_template('rgz/login.html')

@rgz.route('/rgz/logout')
def logout():
    session.clear()
    flash('Вы успешно вышли из системы.', 'success')
    return redirect(url_for('rgz.index'))

@rgz.route('/rgz')
def main_menu():
    is_admin = session.get('is_admin', False)
    return render_template('rgz/rgz.html', is_admin=is_admin)

@rgz.route('/rgz/index')
def index():
    conn, cur = db_connect()
    try:
        cur.execute('SELECT * FROM movies ORDER BY date, time')
        movies = cur.fetchall()
    finally:
        db_close(conn, cur)
    return render_template('rgz/index.html', movies=movies)

@rgz.route('/rgz/book/<int:movie_id>', methods=['POST'])
def book(movie_id):
    if 'user_id' not in session:
        flash('Сначала войдите в систему.', 'error')
        return redirect(url_for('rgz.login'))

    selected_seats = request.form.getlist('seats')
    if not selected_seats:
        flash('Выберите хотя бы одно место.', 'error')
        return redirect(url_for('rgz.movie', movie_id=movie_id))

    conn, cur = db_connect()
    try:
        for seat in selected_seats:
            # Проверяем, не занято ли место
            cur.execute('SELECT * FROM bookings WHERE movie_id = %s AND seat_number = %s', (movie_id, seat))
            if cur.fetchone():
                flash(f'Место {seat} уже занято.', 'error')
                continue

            # Бронируем место
            cur.execute('INSERT INTO bookings (user_id, movie_id, seat_number) VALUES (%s, %s, %s)',
                        (session['user_id'], movie_id, seat))
        conn.commit()
        flash('Места успешно забронированы!', 'success')
    except psycopg2.IntegrityError:
        flash('Ошибка при бронировании мест.', 'error')
    finally:
        db_close(conn, cur)

    return redirect(url_for('rgz.movie', movie_id=movie_id))

@rgz.route('/rgz/unbook/<int:movie_id>/<int:seat_number>', methods=['POST'])
def unbook(movie_id, seat_number):
    if 'user_id' not in session:
        flash('Сначала войдите в систему.', 'error')
        return redirect(url_for('rgz.login'))

    conn, cur = db_connect()
    try:
        # Проверяем, принадлежит ли бронь текущему пользователю
        cur.execute('SELECT * FROM bookings WHERE movie_id = %s AND seat_number = %s AND user_id = %s',
                    (movie_id, seat_number, session['user_id']))
        if not cur.fetchone():
            flash('Вы не можете отменить чужую бронь.', 'error')
            return redirect(url_for('rgz.movie', movie_id=movie_id))

        # Отменяем бронь
        cur.execute('DELETE FROM bookings WHERE movie_id = %s AND seat_number = %s AND user_id = %s',
                    (movie_id, seat_number, session['user_id']))
        conn.commit()
        flash('Бронь успешно отменена.', 'success')
    finally:
        db_close(conn, cur)

    return redirect(url_for('rgz.movie', movie_id=movie_id))

@rgz.route('/rgz/admin/add_movie', methods=['GET', 'POST'])
def admin_add_movie():
    if 'is_admin' not in session or not session['is_admin']:
        flash('Доступ запрещен. Требуются права администратора.', 'error')
        return redirect(url_for('rgz.index'))

    if request.method == 'POST':
        title = request.form['title']
        date = request.form['date']
        time = request.form['time']

        conn, cur = db_connect()
        try:
            cur.execute('INSERT INTO movies (title, date, time) VALUES (%s, %s, %s)',
                        (title, date, time))
            conn.commit()
            flash('Сеанс успешно добавлен.', 'success')
            return redirect(url_for('rgz.index'))
        finally:
            db_close(conn, cur)

    return render_template('rgz/add_movie.html')

@rgz.route('/rgz/movie/<int:movie_id>')
def movie(movie_id):
    conn, cur = db_connect()
    try:
        # Получаем информацию о фильме
        cur.execute('SELECT * FROM movies WHERE id = %s', (movie_id,))
        movie = cur.fetchone()

        # Получаем список бронированных мест для этого фильма
        cur.execute('SELECT * FROM bookings WHERE movie_id = %s', (movie_id,))
        bookings = cur.fetchall()

        if not movie:
            flash('Фильм не найден.', 'error')
            return redirect(url_for('rgz.index'))

    finally:
        db_close(conn, cur)

    return render_template('rgz/movie.html', movie=movie, bookings=bookings)

@rgz.route('/rgz/admin/delete_movie/<int:movie_id>', methods=['POST', 'GET'])
def delete_movie(movie_id):
    conn, cur = db_connect()
    try:
        cur.execute('DELETE FROM movies WHERE id = %s', (movie_id,))
        conn.commit()
        flash('Сеанс успешно удален.', 'success')
    finally:
        db_close(conn, cur)

    return redirect(url_for('rgz.index'))


from datetime import datetime

@rgz.route('/rgz/admin/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
def admin_edit_movie(movie_id):
    if 'is_admin' not in session or not session['is_admin']:
        flash('Доступ запрещен. Требуются права администратора.', 'error')
        return redirect(url_for('rgz.index'))

    conn, cur = db_connect()
    try:
        cur.execute('SELECT * FROM movies WHERE id = %s', (movie_id,))
        movie = cur.fetchone()

        if not movie:
            flash('Фильм не найден.', 'error')
            return redirect(url_for('rgz.index'))

        # Проверяем, прошел ли сеанс
        movie_datetime = datetime.combine(movie['date'], movie['time'])
        current_datetime = datetime.now()

        if movie_datetime < current_datetime:
            flash('Невозможно редактировать фильм, так как сеанс уже прошел.', 'error')
            return redirect(url_for('rgz.index'))

        if request.method == 'POST':
            title = request.form['title']
            date = request.form['date']
            time = request.form['time']

            # Обновляем данные фильма
            cur.execute('UPDATE movies SET title = %s, date = %s, time = %s WHERE id = %s',
                        (title, date, time, movie_id))
            conn.commit()

            flash('Фильм успешно обновлен.', 'success')
            return redirect(url_for('rgz.index'))

        return render_template('rgz/edit_movie.html', movie=movie)

    finally:
        db_close(conn, cur)

