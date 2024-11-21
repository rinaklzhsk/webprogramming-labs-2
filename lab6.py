from flask import Blueprint, render_template, request, session

lab6 = Blueprint('lab6', __name__)

# Данные офисов
offices = []
for i in range(1, 11):
    offices.append({"number": i, "tenant": "", "price": 900 + i % 3 * 100})

# Главная страница
@lab6.route('/lab6/')
def main():
    # Передаём login пользователя в шаблон
    login = session.get('login', '')
    return render_template('lab6/lab6.html', login=login)

# JSON-RPC API
@lab6.route('/lab6/json-rpc-api/', methods=['POST'])
def api():
    data = request.json
    id = data['id']

    if data['method'] == 'info':
        # Отправляем список офисов
        return {
            'jsonrpc': '2.0',
            'result': offices,
            'id': id
        }

    login = session.get('login')
    if not login:
        return {
            'jsonrpc': '2.0',
            'error': {
                'code': 1,
                'message': 'Unauthorized'
            },
            'id': id
        }

    if data['method'] == 'user_total_cost':
        # Считаем общую стоимость бронирования для текущего пользователя
        total_cost = sum(office['price'] for office in offices if office['tenant'] == login)
        return {
            'jsonrpc': '2.0',
            'result': total_cost,
            'id': id
        }

    if data['method'] == 'booking':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 2,
                            'message': 'Already booked'
                        },
                        'id': id
                    }

                office['tenant'] = login
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    if data['method'] == 'cancellation':
        office_number = data['params']
        for office in offices:
            if office['number'] == office_number:
                if not office['tenant']:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 3,
                            'message': 'Not booked'
                        },
                        'id': id
                    }
                if office['tenant'] != login:
                    return {
                        'jsonrpc': '2.0',
                        'error': {
                            'code': 4,
                            'message': 'Вы не можете отменить чужое бронирование'
                        },
                        'id': id
                    }
                office['tenant'] = ''
                return {
                    'jsonrpc': '2.0',
                    'result': 'success',
                    'id': id
                }

    return {
        'jsonrpc': '2.0',
        'error': {
            'code': -32601,
            'message': 'Method not found'
        },
        'id': id
    }
