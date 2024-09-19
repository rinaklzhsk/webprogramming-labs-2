from flask import Flask
app = Flask(__name__)

# функция start() срабатывает и на «/», и на «/web».
# @app.route("/")
@app.route("/web")
def web():
    # возвращает html-страницу
    return """<!doctype html>
        <html>
           <body>
               <h1>web-сервер на flask</h1>
           </body>
        </html>"""

@app.route("/author")
def author():
    name = "Калужская Ирина Витальевна"
    group = "ФБИ-21"
    faculty = "ФБ"

    return """<!doctype html>
        <html>
            <body>
                <p>Студент: """ + name + """</p>
                <p>Группа: """ + group + """</p>
                <p>Факульет: """ + faculty + """</p>
                <a href="/web">web</a>
            </body>
        </html>"""