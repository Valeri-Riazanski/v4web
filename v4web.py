from DBcm import UseDataBase
from flask import Flask, render_template, request, session
from vsearch import search4letters
from checker import check_logged_in
import datetime

app = Flask(__name__)
app.config['dbconfig'] = {'host': '127.0.0.1',
                          'user': 'kot',
                          'database': 'vDB',
                          'password': 'Jrc5xVdptXZo', }

_date = datetime.date.isoformat(datetime.date.today())


@app.route('/')
def aut():
    return render_template('login.html',
                           the_title="Welcome on board", )


@app.route('/reentry')
def reentry():
    if 'logged_in' in session:
        return render_template('logged_in.html',
                               message='You are now logged in as ')
    return render_template('login.html',
                           the_title="Welcome on board", )


@app.route('/login', methods=['POST'])
def do_login():
    session['logged_in'] = True
    login = request.form['login']
    user_name = _date + '  ' + login
    return render_template('logged_in.html',
                           the_title='Welcome to search!',
                           the_user_name=user_name, )


def get_user_name():
    return 'Data ' + request.form['login']


@app.route('/entry')
def entry_page():
    return render_template('entry.html',
                           the_title='Welcome to search!',
                           the_user_name='user_name', )


@app.route('/logout')
def do_logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return render_template('log_out.html',
                           the_title='You are now logged out')


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
                               the_user_name='user_name',
                               the_title='View Log',
                               the_row_titles=titles,
                               the_data=contents, )


app.secret_key = 'YouWillNeverGuessMySecretKey'

if __name__ == '__main__':
    app.run(debug=True)
