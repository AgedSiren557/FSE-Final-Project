from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'FSE_SECRET_KEY'


class LightForm(FlaskForm):
    lightOff = SubmitField('0%')
    lightMiddle = SubmitField('50%')
    lightOn = SubmitField('100%')


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/light',  methods=['GET', 'POST'])
def light():
    kitchenLight = LightForm()
    lobbyLight = LightForm()
    context = {
        'kitchen': kitchenLight,
        'lobby': lobbyLight,
    }
    return render_template('light.html', **context)


@app.route('/camera', methods = ['GET','POST'])
def camera():
    camera1 = LightForm()
    camera2 = LightForm()
    contex = {
        'camera1': camera1,
        'camera2': camera2,
    }
    return render_template('camera.html', **contex)


@app.route('/garage', methods = ['GET', 'POST'])
def garage():
    garagedoor = LightForm()
    context = {
        'garagedoor': garagedoor,
    }
    return render_template('garage.html', **context)


if __name__ == '__main__':
    app.run()