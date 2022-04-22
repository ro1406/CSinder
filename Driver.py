# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 00:56:10 2022

@author: rohan
"""

from flask import Flask, render_template,redirect,url_for,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import random
from random import randrange


from Models import User,Project,ProjLang

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CSinder.db'
db = SQLAlchemy(app)

@app.route("/Home")
def home():
   return render_template("Home.html")

@app.route("/")
def homedefault():
   return redirect(url_for('home'))


@app.route("/error")
def error():
   return render_template("Error.html")

@app.route("/Projects",methods=['GET','POST'])
def projects():
    if request.method=='GET':
        #Query DB and send in list of all projects into the html file:
        projs=Project.query.order_by(Project.name).all() #Alphabetical ordering rn... will add some ranking later
        result=[]
        for p in projs:
            temp=[p.name,p.description,p.difficulty,p.github]#name,desc,difficulty,github, languages, creatorID
            languages=ProjLang.query.filter_by(projID=p.projID).all()
            temp.append(','.join(languages)) #make it a single string
            
            creator=User.query.filter_by(userID=p.creatorID).one()
            temp.append(creator.name)
            result.append(temp)
        
        return render_template("Projects.html",allprojs=result)
    else:
        searchterm=request.form['searchbar']
        #Search by area for demo.. later search by name, description, and language
        
        projs=Project.query.filter_by(name=searchterm).all()
        result=[]
        for p in projs:
            temp=[p.name,p.description,p.difficulty]#name,desc,difficulty, languages, creatorID
            languages=ProjLang.query.filter_by(projID=p.projID).all()
            temp.append(','.join(languages)) #make it a single string
            
            creator=User.query.filter_by(userID=p.creatorID).one()
            temp.append(creator.name)
            result.append(temp)
        
        return render_template("Projects.html",allprojs=result)
        


@app.route("/Login", methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template("Login.html")
    else:
        us,pwd=request.form['username'],request.form['password']
        
        dbUser=User.query.filter_by(username=us).one()
        
        if dbUser is not None:
            if dbUser.username==us and dbUser.password==pwd:
                return render_template("Account-Page.html")
        return redirect(url_for('error'))
        
@app.route("/checkLogin", methods=['GET','POST'])
def checkLogin():
   if request.method=='GET':
       return redirect(url_for('login'))
   else:
       us,pwd=request.form['username'],request.form['password']
       dbUser=User.query.filter_by(username=us).one()
       if dbUser is not None:
           if dbUser.username==us and dbUser.password==pwd:
               return redirect(url_for('profile',us=us))
       return redirect(url_for('error'))

#Account page needs to be customizable
@app.route("/Account/<us>")
def profile(us):
    profile=User.query.filter_by(username=us)
    
    return render_template("Logged.html",profile=profile)

@app.route("/register")
def register():
    return render_template("Register.html")
    
@app.route("/checkregistration", methods=['GET','POST'])
def checkregistration():
    if request.method=="GET":
        return render_template("Register.html")
    else:
        us,pwd=request.form['username'],request.form['password'] #Add additional fields after
        #Generate User ID:
        UserID = "U" + str(randrange(10000, 99999))
        UserIDs=User.query.order_by(User.userID).all()
        while UserID in UserIDs:
            UserID = "U" + str(randrange(10000, 99999))
        usertemp=User(name="default1",username=us,password=pwd,userID=UserID,email="test@gmail.com",experience=4)
        db.session.add(usertemp)
        db.session.commit()
        
        return redirect(url_for('login'))

@app.route("/createProject",methods=['GET',"POST"])
def createProject(us):
    if request.method=="GET":
        return render_template("CreateProject.html")
    else:
        name=request.form['title']
        #creatorName=request.form['creator'] #Find their ID and update all tables
        github=request.form['Github']
        choice=request.form['meal_preference']
        email=request.form['email']
        desc=request.form['big_texty']
        lang=request.form['lang']
        
        #Get difficulty
        #Generate projID
        ## Project ID generation: 
        ProjID = "P" + str(randrange(10000, 99999))
        ProjIDs=Project.query.order_by(Project.projID).all()
        while ProjID in ProjIDs:
            ProjID = "P" + str(randrange(10000, 99999))
                
        #Get record of creator
        user1=User.query.filter_by(username=us).one()
        
        newProj=Project(name=name,projID=ProjID,description=desc,difficulty=3,user=user1) 
        
        db.session.add(newProj)
        db.session.commit()
        return redirect(url_for('projectsLoggedIn'),username=us)
        

@app.route("/Projects",methods=['GET',"POST"])
def projectsLoggedIn(us):
    if request.method=='GET':
        #Query DB and send in list of all projects into the html file:
        projs=Project.query.order_by(Project.name).all() #Add some ranking later
        result=[]
        for p in projs:
            temp=[p.name,p.description,p.difficulty,p.github]#name,desc,difficulty, github, languages, creatorID
            languages=ProjLang.query.filter_by(projID=p.projID).all()
            temp.append(','.join(languages)) #make it a single string
            
            creator=User.query.filter_by(userID=p.creatorID).one()
            temp.append(creator.name)
            result.append(temp)
        
        return render_template("ProjectsLoggedIn.html",allprojs=result,username=us)
    else:    
        searchterm=request.form['searchbar']
        #Search by area for demo.. later search by name, description, and language
        projs=Project.query.filter_by(name=searchterm).all()
        result=[]
        for p in projs:
            temp=[p.name,p.description,p.difficulty]#name,desc,difficulty, languages, creatorID
            languages=ProjLang.query.filter_by(projID=p.projID).all()
            temp.append(','.join(languages)) #make it a single string
            
            creator=User.query.filter_by(userID=p.creatorID).one()
            temp.append(creator.name)
            result.append(temp)
        
        return render_template("ProjectsLoggedIn.html",allprojs=result,username=us)

if __name__ == '__main__':
    
    app.run(debug=True,port=80)