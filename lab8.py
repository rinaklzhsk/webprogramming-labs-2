from flask import Blueprint, render_template, request, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from db import db
from db.models import users, articles
from flask_login import login_user, login_required, current_user, logout_user

lab8 = Blueprint('lab8', __name__)

@lab8.route('/lab8/')
def lab():
    return render_template('lab8/lab8.html')


@lab8.route('/lab8/register/', methods = ['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('lab8/register.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    if not login_form or not password_form:
        return render_template('lab8/register.html', error='Заполните все поля')
    
    login_exists = users.query.filter_by(login = login_form).first()
    if login_exists:
        return render_template('lab8/register.html', 
                                error = 'Такой пользователь уже существует')

    password_hash = generate_password_hash(password_form)
    new_user = users(login = login_form, password = password_hash)
    db.session.add(new_user)
    db.session.commit()
    
    remember = 'remember' in request.form

    # Автоматический логин после регистрации
    login_user(new_user, remember=remember)

    return redirect('/lab8/')

    
@lab8.route('/lab8/login/', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('lab8/login.html')

    login_form = request.form.get('login')
    password_form = request.form.get('password')

    remember = 'remember' in request.form

    user = users.query.filter_by(login = login_form).first()

    if user:
        if check_password_hash(user.password, password_form):
            login_user(user, remember = remember)
            return redirect('/lab8/')

    return render_template('/lab8/login.html', 
                            error = 'Ошибка входа: логин и/или пароль неверны')


@lab8.route('/lab8/articles/')
@login_required
def article_list():
    # Извлекаем все статьи, которые принадлежат текущему пользователю
    user_articles = articles.query.filter_by(login_id=current_user.id).all()
    
    return render_template('lab8/articles_list.html', articles=user_articles)


@lab8.route('/lab8/logout/')
@login_required
def logout():
    logout_user()
    return redirect('/lab8/')


@lab8.route('/lab8/create/', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        article_text = request.form.get('article_text')

        if not title or not article_text:
            return render_template('lab8/create_article.html', error="Пожалуйста, заполните все поля")

        new_article = articles(
            title=title,
            article_text=article_text,
            login_id=current_user.id,
            is_favorite=False,  
            is_public=True,     
            likes=0
        )

        db.session.add(new_article)
        db.session.commit()

        return redirect('/lab8/articles/')  # Перенаправляем на список статей

    return render_template('lab8/create_article.html')
    

@lab8.route('/lab8/articles/delete/<int:article_id>/', methods=['POST'])
@login_required
def delete(article_id):
    article = articles.query.get(article_id)
    
    if article and article.login_id == current_user.id:
        db.session.delete(article)
        db.session.commit()
        return redirect('/lab8/articles/') 
    else:
        return "Статья не найдена или у вас нет прав на удаление этой статьи", 403


@lab8.route('/lab8/articles/edit/<int:article_id>/', methods=['GET', 'POST'])
@login_required
def edit(article_id):
    article = articles.query.get(article_id)

    if article and article.login_id == current_user.id:
        if request.method == 'POST':
            title = request.form.get('title')
            article_text = request.form.get('article_text')
            
            if not title or not article_text:
                return render_template('lab8/edit_article.html', article=article, error='Заполните все поля')

            # Обновляем данные статьи
            article.title = title
            article.article_text = article_text
            db.session.commit()

            return redirect(url_for('lab8.article_list'))  # Перенаправляем на страницу со списком статей

        # Если GET-запрос, показываем форму с текущими данными статьи
        return render_template('lab8/edit_article.html', article=article)
    
    else:
        return "Статья не найдена или у вас нет прав на редактирование этой статьи", 403