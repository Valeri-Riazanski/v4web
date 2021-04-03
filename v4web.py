from DBcm import UseDataBase
from flask import Flask, render_template, request, session
from vsearch import search4letters
from checker import check_logged_in

app = Flask(__name__)
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'kot',
                          'database': 'vDB',
                          'password': 'Jrc5xVdptXZo', }


@app.route('/')
def aut():
    title = "Welcome on board"
    return render_template('login.html',
                           the_title=title,)


@app.route('/login', methods=['POST'])
def do_login():
    render_template('login.html',
                     )
    session['logged_in'] = True
    login = request.form['login']
    message = 'You are now logged in as ' + login
    return render_template('entry.html',
                           the_title='Welcome to search4letters!',
                           the_message=message, )


@app.route('/entry')
def entry_page():
    return render_template('entry.html',
                           the_title='Welcome to search4letters!')


@app.route('/logout')
def do_logout() -> str:
    session.pop('logged_in')
    return 'You are now logged out'


def log_request(req: 'flask_request', res: str) -> None:
    with UseDataBase(app.config['dbconfig']) as cursor:
        _SQL = """insert into log
        (phrase, letters, ip, browser_string, results)
         values
        (%s, %s, %s, %s, %s)"""
        cursor.execute(_SQL, (req.form['phrase'],
                              req.form['letters'],
                              req.remote_addr,
                              req.user_agent.browser,
                              res,))


@app.route('/search4', methods=['POST'])
def do_search():
    phrase = request.form['phrase']
    letters = request.form['letters']
    title = 'Here are your results:'
    results = str(search4letters(phrase, letters))
    log_request(request, results)
    return render_template('results.html',
                           the_title=title,
                           the_phrase=phrase,
                           the_letters=letters,
                           the_results=results, )


@app.route('/viewlog')
@check_logged_in
def view_the_log():
    with UseDataBase(app.config['dbconfig']) as cursor:
        _SQL = """select phrase, letters, ip, browser_string, results
                from log"""
        cursor.execute(_SQL)
        contents = cursor.fetchall()
        titles = ('Phrase', 'Letters', 'Remote_addr', 'User_agent', 'Results')
        return render_template('viewlog.html',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents, )


app.secret_key = 'YouWillNeverGuessMySecretKey'

if __name__ == '__main__':
    app.run(debug=True)