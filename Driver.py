# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 00:56:10 2022

@author: rohan
"""

from flask import Flask, render_template,redirect,url_for,request,jsonify
from flask_sqlalchemy import SQLAlchemy

from Models import User,Project,ProjLang

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CSinder.db'
db = SQLAlchemy(app)

@app.route("/Home")
def home():
   return render_template("Home.html")

@app.route("/About")
def about():
   return render_template("About.html")

@app.route("/Manage")
def manage():
   return render_template("ManagePr.html")

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
@app.route("/Account/ro")
def profile():
    profile=User.query.filter_by(username="ro")
    
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
        usertemp=User(name="default1",username=us,password=pwd,userID="U99999",email="test@gmail.com",experience=4)
        db.session.add(usertemp)
        db.session.commit()
        
        return redirect(url_for('login'))

@app.route("/createProject")
def createProject():
   return render_template("CreateProject.html")

@app.route("/ProjectsLoggedIn",methods=['GET',"POST"])
def projectsLoggedIn():
    if request.method=='GET':
        #Query DB and send in list of all projects into the html file:
        projs=Project.query.order_by(Project.name).all() #Alphabetical ordering rn... will add some ranking later
        result=[]
        for p in projs:
            temp=[p.name,p.description,p.difficulty,p.github]#name,desc,difficulty, github, languages, creatorID
            languages=ProjLang.query.filter_by(projID=p.projID).all()
            temp.append(','.join(languages)) #make it a single string
            
            creator=User.query.filter_by(userID=p.creatorID).one()
            temp.append(creator.name)
            result.append(temp)
        
        return render_template("ProjectsLoggedIn.html",allprojs=result)
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
        
        return render_template("ProjectsLoggedIn.html",allprojs=result)

if __name__ == '__main__':
    
    app.run(debug=True,port=5000)