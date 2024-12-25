from flask import Blueprint, render_template, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, films
from flask_login import login_user, login_required, current_user, logout_user

rgz = Blueprint('rgz', __name__)

@rgz.route('/rgz/')
def main():
    return render_template('rgz/rgz.html')


@rgz.route('/rgz/register/', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return render_template('rgz/register.html', login=current_user.login, message='Вы не можете зарегистрироваться, находясь в аккаунте. Хотите выйти?')
    
    if request.method == 'GET':
        return render_template('rgz/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if login_form == '':
        return render_template('rgz/register.html', error='Заполните имя пользователя')

    if password_form == '':
        return render_template('rgz/register.html', error='Заполните пароль')

    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('rgz/register.html', error='Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()

    remember = 'remember' in request.form
    login_user(new_user, remember=remember)
    return render_template('rgz/rgz.html', login=login_form)


@rgz.route('/rgz/login/', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return render_template('rgz/rgz.html', login=current_user.login)
        
    if request.method == 'GET':
        return render_template('rgz/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if login_form == '':
        return render_template('rgz/login.html', error='Заполните имя пользователя')

    if password_form == '':
        return render_template('rgz/login.html', error='Заполните пароль')

    user = users.query.filter_by(login = login_form).first()
    remember = 'remember' in request.form
    
    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember=remember)
            return render_template('rgz/rgz.html', login=login_form)
    return render_template('rgz/login.html', error='Ошибка входа: логин и/или пароль неверны')


@rgz.route('/rgz/logout')
@login_required
def logout():
    logout_user()
    return redirect('/rgz/')


# films = [
#     {
#         "title": "Hide and Seek",
#         "title_ru": "Игра в прятки",
#         "year": 2005,
#         "description": "Отец-вдовец отчаянно пытается пробиться \
#                         к своей 9-летней дочери, создавшей себе подлого маниакального \
#                         воображаемого друга, одержимого идеей мести отцу. Однако \
#                         воображаемые друзья могут войти и в реальную жизнь…"
#     },

#     {
#         "title": "mother!",
#         "title_ru": "мама!",
#         "year": 2017,
#         "description": "Отношения молодой пары оказываются под угрозой, когда, \
#                         нарушая безмятежное существование супругов, в их дом заявляются незваные\
#                         гости."
#     },

#     {
#         "title": "What We Do in the Shadows",
#         "title_ru": "Реальные упыри",
#         "year": 2014,
#         "description": "История жизни Виаго, Дикона и Владислава — трёх соседей и \
#                         по совместительству бессмертных вампиров, которые всего лишь пытаются выжить \
#                         в современном мире, где есть арендная плата, фейсконтроль в ночных клубах, \
#                         губительный солнечный свет и другие неприятности."
#     },

#     {
#         "title": "The Shining",
#         "title_ru": "Сияние",
#         "year": 1980,
#         "description": "Джек Торренс с женой и сыном приезжает в элегантный отдалённый \
#                         отель, чтобы работать смотрителем во время мертвого сезона. Торренс здесь раньше \
#                         никогда не бывал. Или это не совсем так? Ответ лежит во мраке, сотканном из \
#                         преступного кошмара."
#     },

#     {
#         "title": "Pearl",
#         "title_ru": "Пэрл",
#         "year": 2022,
#         "description": "1918 год. В мире бушует Первая мировая война и пандемия «испанки», \
#                         а на техасской ферме мается девушка Пэрл. Она мечтает вырваться из этой глухомани и \
#                         стать танцовщицей, но вместо этого вынуждена подчиняться строгой матери, ухаживать за \
#                         парализованным отцом и покорно дожидаться мужа с фронта. Когда Пэрл узнаёт, что в \
#                         ближайшем городке будет проходить прослушивание на вакансию в танцевальной труппе, \
#                         она решает попасть туда любой ценой."
#     }
# ]


@rgz.route('/rgz/afisha/')
def afisha():
    films_list = films.query.all()
    return render_template('rgz/afisha.html',films=films_list)


@rgz.route('/rgz/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'GET':
        return render_template('rgz/create.html', login=current_user.login)

    title = request.form.get('title')
    film_text = request.form.get('film_text')

    if title == '' or film_text == '':
        return render_template('rgz/create.html', error='Заполните все поля')

    new_film = films(
        title=title, 
        film_text=film_text, 
        login_id=current_user.id)
    
    db.session.add(new_film)
    db.session.commit()
    return redirect('/rgz/afisha/')


@rgz.route('/rgz/edit/<int:films_id>', methods=['GET', 'POST'])
@login_required
def edit(films_id):
    film = films.query.get(films_id)

    if film and film.login_id == current_user.id:
        if request.method == 'POST':
            title = request.form.get('title')
            film_text = request.form.get('film_text')
            
            if not title or not film_text:
                return render_template('rgz/edit_films.html', film=film, error='Заполните все поля')

            film.title = title
            film.film_text = film_text
            db.session.commit()

            return redirect('/rgz/afisha/')
        return render_template('rgz/edit_films.html', film=film)


@rgz.route('/rgz/delete/<int:films_id>', methods=['POST'])
@login_required
def delete(films_id):
    film = films.query.filter_by(id=films_id).first() 

    if film and film.login_id == current_user.id:
        db.session.delete(film)
        db.session.commit()

    return redirect('/rgz/afisha/')