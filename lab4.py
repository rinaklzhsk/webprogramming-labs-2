from flask import Blueprint, render_template, request, redirect, session

lab4 = Blueprint('lab4',__name__)

@lab4.route('/lab4/')
def lab():
    return render_template('lab4/lab4.html')


@lab4.route('/lab4/div-form')
def div_form():
    return render_template('lab4/div-form.html')


@lab4.route('/lab4/div', methods = ['POST'])
def div():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/div.html', error='Оба поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x2 == 0:
        return render_template('lab4/div.html', error0='На ноль делить нельзя!')
    result = x1 / x2
    return render_template('lab4/div.html', x1=x1, x2=x2, result=result)


# сложение
@lab4.route('/lab4/addition-form')
def addition_form():
    return render_template('lab4/addition-form.html')


@lab4.route('/lab4/addition', methods = ['POST'])
def addition():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 0
    else:
        x1 = int(x1)
    if x2 == '':
        x2 = 0
    else:
        x2 = int(x2)
    result = x1 + x2
    return render_template('lab4/addition.html', x1=x1, x2=x2, result=result)


# умножение
@lab4.route('/lab4/multiplication-form')
def multiplication_form():
    return render_template('lab4/multiplication-form.html')


@lab4.route('/lab4/multiplication', methods = ['POST'])
def multiplication():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '':
        x1 = 1
    else:
        x1 = int(x1)
    if x2 == '':
        x2 = 1
    else:
        x2 = int(x2)
    result = x1 * x2
    return render_template('lab4/multiplication.html', x1=x1, x2=x2, result=result)


# вычитание
@lab4.route('/lab4/subtraction-form')
def subtraction_form():
    return render_template('lab4/subtraction-form.html')


@lab4.route('/lab4/subtraction', methods = ['POST'])
def subtraction():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/subtraction.html', error='Все поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    result = x1 - x2
    return render_template('lab4/subtraction.html', x1=x1, x2=x2, result=result)


# возведение в степень
@lab4.route('/lab4/power-form')
def power_form():
    return render_template('lab4/power-form.html')


@lab4.route('/lab4/power', methods = ['POST'])
def power():
    x1 = request.form.get('x1')
    x2 = request.form.get('x2')
    if x1 == '' or x2 == '':
        return render_template('lab4/power.html', error='Все поля должны быть заполнены!')
    x1 = int(x1)
    x2 = int(x2)
    if x1 == 0 and x2 == 0:
        return render_template('lab4/power.html', error0='Оба значения равны нулю!')
    result = x1 ** x2
    return render_template('lab4/power.html', x1=x1, x2=x2, result=result)

    
tree_count = 0

@lab4.route('/lab4/tree', methods = ['GET', 'POST'])
def tree():
    global tree_count
    if request.method == 'GET':
        return render_template('lab4/tree.html', tree_count=tree_count)

    operation = request.form.get('operation')

    if operation == 'cut':
        tree_count -= 1
    elif operation == 'plant':
        tree_count += 1

    return redirect('/lab4/tree')


users = [
    {'name': 'Alexander Hamilton','login': 'alex', 'password': '123', 'sex': 'мужской'},
    {'name': 'Bob Ross','login': 'bob', 'password': '555','sex': 'мужской'},
    {'name': 'Irina Kaluzhskaya','login': 'rina', 'password': '1912', 'sex': 'женский'},
    {'name': 'Mayya Matsekh','login': 'may', 'password': '0206', 'sex': 'женский'}
]

@lab4.route('/lab4/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'GET':
        if 'name' in session:
            authorized = True
            name = session['name']
        else:
            authorized=False
            name = ''
        return render_template('lab4/login.html', authorized=authorized, name=name)
    name = request.form.get('name')
    login = request.form.get('login')
    password = request.form.get('password')
    sex = request.form.get('sex')
    for user in users:
        if login == user['login'] and password == user['password'] and name == user['name'] and sex == user['sex']:
            session['name'] = name
            return redirect('/lab4/login')
    error = 'Некорректные данные'
    if name == '':
        error = 'Не указано имя пользователя'
    elif login == '':
        error = 'Не указан логин'
    elif password == '':
        error = 'Не указан пароль'
    return render_template('lab4/login.html', error=error, authorized=False, 
                            login=login, password=password, name=name, sex=sex)


@lab4.route('/lab4/logout', methods = ['POST'])
def logout():
    session.pop('name', None)
    return redirect('/lab4/login')


