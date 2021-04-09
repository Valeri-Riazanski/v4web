from flask import session, render_template
from functools import wraps


# func это функция, расположенная в строке ниже, после декоратора в модуле simple_webapp.py
# page1, page2, page3
def check_logged_in(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)
        return render_template('log_out.html',
                               the_title='You are logged out')

    return wrapper
