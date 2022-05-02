from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
#from wtforms import validators
from wtforms.fields import SubmitField

app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'FSE_SECRET_KEY'

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)

   
class LightForm(FlaskForm):
    kitchenLightOn = SubmitField('Light on')
    kitchenLightOff = SubmitField('Light off')
    kitchenLight0 = SubmitField('0%')
    kitchenLight20 = SubmitField('20%')
    kitchenLight40 = SubmitField('40%')
    kitchenLight60 = SubmitField('60%')
    kitchenLight80 = SubmitField('80%')
    kitchenLight100 = SubmitField('100%')
    kitchenStatus = 'Light Off'

    lobbyLightOn = SubmitField('Light on')
    lobbyLightOff = SubmitField('Light off')
    loobyLight0 = SubmitField('0%')
    loobyLight20 = SubmitField('20%')
    loobyLight40 = SubmitField('40%')
    loobyLight60 = SubmitField('60%')
    loobyLight80 = SubmitField('80%')
    loobyLight100 = SubmitField('100%')
    loobyStatus = 'Lightoff Off'


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/light',  methods=['GET', 'POST'])

def light():
    form = LightForm()
    context = {
        'form': form,
    }

    if request.method=='POST' :
        if (form.kitchenLightOff.data):
            LightForm.kitchenStatus = "Light Off"

        elif (form.kitchenLightOn.data):
            LightForm.kitchenStatus = "Light On"

        elif (form.kitchenLight0.data):
            LightForm.kitchenStatus = "Light Off"

        elif(form.kitchenLight20.data):
            LightForm.kitchenStatus ="Light at 20%"

        elif(form.kitchenLight40.data):
            LightForm.kitchenStatus ="Light at 40%"

        elif(form.kitchenLight60.data):
            LightForm.kitchenStatus ="Light at 60%"

        elif(form.kitchenLight80.data):
            LightForm.kitchenStatus ="Light at 80%"

        elif(form.kitchenLight100.data):
            LightForm.kitchenStatus ="Light On"

        #lobby
        elif (form.lobbyLightOff.data):
            LightForm.loobyStatus = "Light Off"

        elif (form.lobbyLightOn.data):
            LightForm.loobyStatus = "Light On"

        elif (form.loobyLight0.data):
            LightForm.loobyStatus = "Light Off"

        elif(form.loobyLight20.data):
            LightForm.loobyStatus ="Light at 20%"

        elif(form.loobyLight40.data):
            LightForm.loobyStatus ="Light at 40%"

        elif(form.loobyLight60.data):
            LightForm.loobyStatus ="Light at 60%"

        elif(form.loobyLight80.data):
            LightForm.loobyStatus ="Light at 80%"

        elif(form.loobyLight100.data):
            LightForm.loobyStatus ="Light On"

        return render_template('light.html', **context)

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


if __name__ == '__main__':
    app.run()