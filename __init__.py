from cgitb import reset
import os
from flask import Flask
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
import pickle
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # a simple page that says hello
    
    @app.route('/',methods=('GET', 'POST'))
    def form():
        if request.method == 'POST':
            age = request.form['age']
            weight = request.form['weight']
            height = request.form['height']
            bodyfat = request.form['bodyfat']
            gender = request.form['gender']
            
            return redirect(url_for("predict", age=age, weight=weight, height=height, bodyfat=bodyfat, gender=gender))
        return render_template('form.html')
    
    
    @app.route('/predict/<age>/<weight>/<height>/<bodyfat>/<gender>',methods=('GET', 'POST'))
    def predict(age,weight,height,bodyfat,gender):
        pickled_model = pickle.load(open('./client/body_model.pkl', 'rb'))
        randomlist=[]
        randomlist.append(age)
        randomlist.append(gender)
        randomlist.append(height)
        randomlist.append(weight)
        randomlist.append(bodyfat)
        randomlist.append(78.796842)
        randomlist.append(130.234817)
        randomlist.append(36.963877)
        randomlist.append(15.209268)
        randomlist.append(39.771224)
        randomlist.append(190.129627)
        res=pickled_model.predict([randomlist])
        res=res[0];
        if res==1:
            str="Paleo Diet"
        elif res==2:
            str="Intermittent Fasting with high Protein intake"
        elif res==3:
            str="Keto diet"
        elif res==4:
            str="Intermittent fasting with low carbs and keep yourselves active"
            
            
        return render_template('display.html',res=res,str=str)

    return app