from flask import Blueprint, render_template, request, make_response, redirect
lab3 = Blueprint('lab3',__name__)


@lab3.route('/lab3/')
def lab():
    name = request.cookies.get('name','Аноним')
    name_color = request.cookies.get('name_color')
    age = request.cookies.get('age', 'неизвестный')
    return render_template('lab3/lab3.html', name=name, name_color=name_color, age=age)


@lab3.route('/lab3/cookie')
def cookie():
    resp = make_response(redirect('/lab3/'))
    resp.set_cookie('name', 'Alex', max_age=5)
    resp.set_cookie('age','20')
    resp.set_cookie('name_color','magenta')
    return resp


@lab3.route('/lab3/del_cookie')
def del_cookie():
    resp = make_response(redirect('/lab3/'))
    resp.delete_cookie('name')
    resp.delete_cookie('age')
    resp.delete_cookie('name_color')
    return resp


@lab3.route('/lab3/form1')
def form1():
    errors = {}
    user = request.args.get('user')
    if user == '':
        errors['user'] = 'Заполните поле!'

    age = request.args.get('age')
    if age == '':
        errors['age'] = 'Заполните поле!'

    sex = request.args.get('sex')
    return render_template('lab3/form1.html', user=user, age=age, sex=sex, errors=errors)


@lab3.route('/lab3/order')
def order():
    return render_template('lab3/order.html')


@lab3.route('/lab3/pay')
def pay():
    price = 0
    drink = request.args.get('drink')
    if drink == 'coffee':
        price = 120
    elif drink == 'black-tea':
        price = 80
    else:
        price = 70

    if request.args.get('milk') == 'on':
        price += 30
    if request.args.get('sugar') == 'on':
        price += 10

    return render_template('lab3/pay.html', price=price)


@lab3.route('/lab3/success')
def success():
    price = request.args.get('price')
    return render_template('/lab3/success.html', price=price)


#  стр 42
@lab3.route('/lab3/settings')
def settings():
    color = request.args.get('color')
    bg_color = request.args.get('bg_color')
    font_size = request.args.get('font_size')
    font_style = request.args.get('font_style')

    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, font_size=font_size, font_style=font_style))

    if color:
        resp = make_response(redirect('/lab3/settings'))
        resp.set_cookie('color', color)

    if bg_color:  
        resp.set_cookie('bg_color', bg_color)

    if font_size:
        resp.set_cookie('font_size', font_size)

    if font_style:
        resp.set_cookie('font_style', font_style)
        return resp

    color = request.cookies.get('color')
    bg_color = request.cookies.get('bg_color')
    font_size = request.cookies.get('font_size', '16')
    font_style = request.cookies.get('font_style', 'normal')

    resp = make_response(render_template('lab3/settings.html', color=color, bg_color=bg_color, 
                        font_size=font_size, font_style=font_style))
    return resp
    

@lab3.route('/lab3/ticket')
def ticket():
    ticket = 0
    FIO = request.args.get('FIO')
    age = request.args.get('age', 0)
    shelf = request.args.get('shelf')
    linen = request.args.get('linen')
    baggage = request.args.get('baggage')
    placefrom = request.args.get('placefrom')
    placeto = request.args.get('placeto')
    date = request.args.get('date')
    belay = request.args.get('belay')

    if int(age) < 18:
        ticket += 700
        ticket_type = "Детский билет"
    else:
        ticket += 1000
        ticket_type = "Взрослый билет"
    if shelf == 'lower' or shelf == 'lower-side':
        ticket += 100
    if linen == 'withlinen':
        ticket += 75
    if baggage == 'withbaggage':
        ticket += 250
    if belay == 'withbelay':
        ticket += 150
    return render_template('lab3/ticket.html', FIO=FIO, age=age, 
                ticket=ticket, shelf=shelf, linen=linen, 
                baggage=baggage, belay=belay, ticket_type=ticket_type, 
                placefrom=placefrom, placeto=placeto, date=date)
