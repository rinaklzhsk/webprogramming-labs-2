from flask import Blueprint, render_template, request, redirect

lab7 = Blueprint('lab7', __name__)

# Главная страница
@lab7.route('/lab7/')
def main():
    return render_template('lab7/index.html')


films = [
    {
        "title": "Hide and Seek",
        "title_ru": "Игра в прятки",
        "year": 2005,
        "description": "Отец-вдовец отчаянно пытается пробиться \
                        к своей 9-летней дочери, создавшей себе подлого маниакального \
                        воображаемого друга, одержимого идеей мести отцу. Однако \
                        воображаемые друзья могут войти и в реальную жизнь…"
    },

    {
        "title": "mother!",
        "title_ru": "мама!",
        "year": 2017,
        "description": "Отношения молодой пары оказываются под угрозой, когда, \
                        нарушая безмятежное существование супругов, в их дом заявляются незваные\
                        гости."
    },

    {
        "title": "What We Do in the Shadows",
        "title_ru": "Реальные упыри",
        "year": 2014,
        "description": "История жизни Виаго, Дикона и Владислава — трёх соседей и \
                        по совместительству бессмертных вампиров, которые всего лишь пытаются выжить \
                        в современном мире, где есть арендная плата, фейсконтроль в ночных клубах, \
                        губительный солнечный свет и другие неприятности."
    },

    {
        "title": "The Shining",
        "title_ru": "Сияние",
        "year": 1980,
        "description": "Джек Торренс с женой и сыном приезжает в элегантный отдалённый \
                        отель, чтобы работать смотрителем во время мертвого сезона. Торренс здесь раньше \
                        никогда не бывал. Или это не совсем так? Ответ лежит во мраке, сотканном из \
                        преступного кошмара."
    },

    {
        "title": "Pearl",
        "title_ru": "Пэрл",
        "year": 2022,
        "description": "1918 год. В мире бушует Первая мировая война и пандемия «испанки», \
                        а на техасской ферме мается девушка Пэрл. Она мечтает вырваться из этой глухомани и \
                        стать танцовщицей, но вместо этого вынуждена подчиняться строгой матери, ухаживать за \
                        парализованным отцом и покорно дожидаться мужа с фронта. Когда Пэрл узнаёт, что в \
                        ближайшем городке будет проходить прослушивание на вакансию в танцевальной труппе, \
                        она решает попасть туда любой ценой."
    }
]

@lab7.route('/lab7/rest-api/films/', methods=['GET'])
def get_films():
    return films


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['GET'])
def get_film(id):
    if 0 <= id < len(films):
        return films[id]
    else:
        return redirect('app/not_found')


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['DELETE'])
def del_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Film not found"}, 404
    del films[id]
    return '', 204


@lab7.route('/lab7/rest-api/films/<int:id>', methods=['PUT'])
def put_film(id):
    if id < 0 or id >= len(films):
        return {"error": "Film not found"}, 404
    film = request.get_json()
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    films[id] = film
    return films[id]

@lab7.route('/lab7/rest-api/films/', methods=['POST'])
def add_film():
    film = request.get_json()
    if film['description'] == '':
        return {'description': 'Заполните описание'}, 400
    films.append(film)
    id = {'id': len(films) - 1}
    return id

