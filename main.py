# !/usr/bin/env python3
# ## ###############################################
# file: main.py
# main file for flask server execution
# Authors:
# Daniel Alberto Zarco Manzanares
# Octavio González Alcalá
# Carlos Colín Cosme
# Christian Otero García
# ## ###############################################

#from crypt import methods
from multiprocessing import context
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms.fields import SubmitField
from yeelight import Bulb
from garagedoor_hardware import openDoor,closeDoor

#configuration needed for flask, boostrap and wtf.fields
app = Flask(__name__, static_folder='static')
bootstrap = Bootstrap(app)
app.config['SECRET_KEY'] = 'FSE_SECRET_KEY'

@app.errorhandler(404)
def not_found(error):
    '''
    defining the 404 error for load htmls that doesn't exist into server
    :param error:
    :return: rendering error
    '''
    return render_template('404.html', error=error) # rendering 404.html


class LightForm(FlaskForm):
    '''
    defining LightForm class to use a Form
    using flask_wtf and bootstrap for implematation
    '''
    #Kitchen light state and buttons
    kitchenLightOn = SubmitField('Light on')
    kitchenLightOff = SubmitField('Light off')
    kitchenLight0 = SubmitField('0%')
    kitchenLight20 = SubmitField('20%')
    kitchenLight40 = SubmitField('40%')
    kitchenLight60 = SubmitField('60%')
    kitchenLight80 = SubmitField('80%')
    kitchenLight100 = SubmitField('100%')
    kitchenStatus = 'Light Off'
    #lobby light state and buttons
    lobbyLightOn = SubmitField('Light on')
    lobbyLightOff = SubmitField('Light off')
    loobyLight0 = SubmitField('0%')
    loobyLight20 = SubmitField('20%')
    loobyLight40 = SubmitField('40%')
    loobyLight60 = SubmitField('60%')
    loobyLight80 = SubmitField('80%')
    loobyLight100 = SubmitField('100%')
    loobyStatus = 'Lightoff Off'

#configuration required for the conection with yeelight API
kitchenBulb = Bulb("192.168.0.13")
lobbyBulb = Bulb("192.168.0.14")

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/light',  methods=['GET', 'POST'])
def light():
    '''
    function for render the camera.html and load into server
    :return: flask render of light.html
    '''
    form = LightForm()  #create the form
    context = { # context variables for light.html into flask
        'form': form,   
    }

    if request.method=='POST' :
        '''
        analize the form of the post, depending on the field selected
        will call the API with the respective indication
        and change the status of the light
        '''
        if (form.kitchenLightOff.data):     #check if ligh off of the kitchen was selected
            LightForm.kitchenStatus = "Light Off"   #set the status of the ligh as off
            kitchenBulb.turn_off()                  #using the API of yeelight to turn off the light

        elif (form.kitchenLightOn.data):
            LightForm.kitchenStatus = "Light On"
            kitchenBulb.turn_on()

        elif (form.kitchenLight0.data):
            LightForm.kitchenStatus = "Light Off"
            kitchenBulb.set_brightness(0)

        elif(form.kitchenLight20.data):
            LightForm.kitchenStatus ="Light at 20%"
            kitchenBulb.set_brightness(20)

        elif(form.kitchenLight40.data):
            LightForm.kitchenStatus ="Light at 40%"
            kitchenBulb.set_brightness(40)

        elif(form.kitchenLight60.data):
            LightForm.kitchenStatus ="Light at 60%"
            kitchenBulb.set_brightness(60)

        elif(form.kitchenLight80.data):
            LightForm.kitchenStatus ="Light at 80%"
            kitchenBulb.set_brightness(80)

        elif(form.kitchenLight100.data):
            LightForm.kitchenStatus ="Light On"
            kitchenBulb.set_brightness(100)

        #
        elif (form.lobbyLightOff.data):
            LightForm.loobyStatus = "Light Off"
            lobbyBulb.turn_off()

        elif (form.lobbyLightOn.data):
            LightForm.loobyStatus = "Light On"
            lobbyBulb.turn_on()

        elif (form.loobyLight0.data):
            LightForm.loobyStatus = "Light Off"
            lobbyBulb.set_brightness(0)

        elif(form.loobyLight20.data):
            LightForm.loobyStatus ="Light at 20%"
            lobbyBulb.set_brightness(20)

        elif(form.loobyLight40.data):
            LightForm.loobyStatus ="Light at 40%"
            lobbyBulb.set_brightness(40)

        elif(form.loobyLight60.data):
            LightForm.loobyStatus ="Light at 60%"
            lobbyBulb.set_brightness(60)

        elif(form.loobyLight80.data):
            LightForm.loobyStatus ="Light at 80%"
            lobbyBulb.set_brightness(80)

        elif(form.loobyLight100.data):
            LightForm.loobyStatus ="Light On"
            lobbyBulb.set_brightness(100)

        #redirect to the same template, and send the form with the status cheange
        return render_template('light.html', **context)

    #render light template, and send the form created
    return render_template('light.html', **context)    


@app.route('/camera', methods = ['GET','POST'])
def camera():
    '''
    function for render the camera.html and load into server
    :return: flask render of camera.html
    '''
    camera1 = LightForm() # creating a Lightform for camera 1 set load into server
    camera2 = LightForm() # creating a Lightform for camera 2 set load into server
    contex = { # context variables for camera.html into flask
        'camera1': camera1,
        'camera2': camera2,
    }
    return render_template('camera.html', **contex) # rendering camera.html

# functions to open and close door with two servomotors allocated into pins 12 and 13
openDoor(12)
openDoor(13)
closeDoor(12)
closeDoor(13)

@app.route('/garage', methods = ['GET', 'POST'])
def garage():
    '''
    function for render the garage.html and load into server
    :return: flask render of garage.html
    '''
    garagedoor = LightForm() # creating a Lightform for load into server
    context = {
        'garagedoor': garagedoor, # context variables for garage.html into flask
    }
    return render_template('garage.html', **context) # rendering garage.html


@app.route('/door', methods = ['GET', 'POST'])
def door():


    door = LightForm()
    context = {'door1': door}
    return render_template('door.html', **context)


if __name__ == '__main__':
    # main function for execute flask app
    #change IP and port if needed
    app.run(host='localhost', port=5000, debug=True)