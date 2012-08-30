r"""

    web
    ~~~

    Web application for generating poetry and annotating text.

"""

import flask


app = flask.Flask(__name__)
app.config.from_envvar('POEMY_SETTINGS', silent=True)
app.config['DEBUG'] = True


@app.route("/")
def index():
    return flask.render_template('index.html')


if __name__ == '__main__':
    app.run()
