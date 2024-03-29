# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 00:56:10 2022

@author: rohan
"""

from flask import Flask, render_template,redirect,url_for,request,jsonify
from flask_sqlalchemy import SQLAlchemy
import random
from random import randrange


from Models import User,Project,ProjLang,ProjectAreas,InterestedIn,CodesIn,worksIn,AppliedTo

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CSinder.db'
db = SQLAlchemy(app)

@app.route("/Home")
def home():
   return render_template("Home.html")

@app.route("/About")
def about():
   return render_template("About.html")

@app.route("/Manage/<us>",methods=["GET","POST"])
def manage(us): #Put us in here
    #us='U11223'
    appsTo=AppliedTo.query.filter_by(userID=us).all() #Object of AppliedTo
    appTo=[] #[[projName,PendingConfirmation?]]
    for a in appsTo:
        if a.pendingConfirmation:
            appTo.append([Project.query.filter_by(projID=a.projID).one().name,'Pending'])
        elif a.accepted:
            appTo.append([Project.query.filter_by(projID=a.projID).one().name,'Accepted'])
        else:
            appTo.append([Project.query.filter_by(projID=a.projID).one().name,'Rejected'])
            
        
    userWorksIn= Project.query.filter_by(creatorID=us).all() #worksIn.query.filter_by(userID=us).all()
    appFrom=[] #[[projName,personName]]
    for row in userWorksIn:
        temp=AppliedTo.query.filter_by(projID=row.projID).all()#Who all have applied to that project
        for r2 in temp:
            if r2.pendingConfirmation:
                #Get project and person name
                appFrom.append([Project.query.filter_by(projID=r2.projID).first().name,User.query.filter_by(userID=r2.userID).first().name])
    
    myprojs=[]
    for row in userWorksIn:
        myprojs.append(Project.query.filter_by(projID=row.projID).one().name)
        
    if request.method=="GET":
        return render_template("ManagePr.html",applicationsTo=appTo, applicationsFrom=appFrom,myProj=myprojs,userID=us)
    
    else:
        for app in appFrom:
            if 'accept-btn '+str(app[1]) not in request.form.keys() and 'reject-btn '+str(app[1]) not in request.form.keys():
                continue
            if 'accept-btn '+str(app[1]) in request.form.keys() and request.form['accept-btn '+str(app[1])]:
                appFrom.remove(app)
                #Adjust DB
                #ProjID and UserID:
                applicantUserID=User.query.filter_by(name=app[1]).first().userID
                applicantProjID=Project.query.filter_by(name=app[0]).first().projID
                row=AppliedTo.query.filter_by(userID=applicantUserID, projID=applicantProjID).first()
                row.pendingConfirmation=False
                row.accepted=True
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                #break
            elif 'reject-btn '+str(app[1]) in request.form.keys() and request.form['reject-btn '+str(app[1])]:
                appFrom.remove(app)
                #Adjust DB
                #ProjID and UserID:
                applicantUserID=User.query.filter_by(name=app[1]).first().userID
                applicantProjID=Project.query.filter_by(name=app[0]).first().projID
                row=AppliedTo.query.filter_by(userID=applicantUserID, projID=applicantProjID).first()
                row.pendingConfirmation=False
                row.accepted=False
                db.session.merge(row)
                db.session.flush()
                db.session.commit()
                #break
        db.session.commit()
        return render_template("ManagePr.html",applicationsTo=appTo, applicationsFrom=appFrom,myProj=myprojs,userID=us)
        
        

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
            temp.append(','.join([x.language for x in languages])) #make it a single string
            
            creator=User.query.filter_by(userID=p.creatorID).one()
            temp.append(creator.name)
            result.append(temp)
        
        return render_template("Projects.html",allprojs=result)
    else:
        searchterm=request.form['searchbar']
        #Search by area, search by name, description, and language
        
        projs=Project.query.filter_by(name=searchterm).all()
        result=[]
        for p in projs:
            temp=[p.name,p.description,p.difficulty,p.github]#name,desc,difficulty, languages, creatorID
            languages=ProjLang.query.filter_by(projID=p.projID).all()
            temp.append(','.join([x.language for x in languages])) #make it a single string
            
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
               return redirect(url_for('profile',us=User.query.filter_by(username=us).first().userID))
       return redirect(url_for('error'))


@app.route("/Account/<us>")
def profile(us):
    profile=User.query.filter_by(userID=us).first()
    
    return render_template("Logged.html",profile=profile,userID=us)

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

@app.route("/createProject/<us>",methods=['GET',"POST"])
def createProject(us):
    if request.method=="GET":
        return render_template("CreateProject.html",userID=us)
    else:
        name=request.form['title']
        #creatorName=request.form['creator'] #Find their ID and update all tables
        github=request.form['Github']
        choice=request.form.get('meal_preference')#request.form['meal_preference']
        choice='Data Science'
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
        user1=User.query.filter_by(userID=us).one()
        
        newProj=Project(name=name,projID=ProjID,description=desc,difficulty=3,user=user1,github=github) 
        area=ProjectAreas(projID=ProjID,areaOfInterest=choice)
        lang=ProjLang(projID=ProjID,language=lang)
        
        db.session.add(lang)
        db.session.add(area)
        db.session.commit()
        
        db.session.add(newProj)
        db.session.flush()
        db.session.commit()
        return redirect(url_for('projectsLoggedIn'),userID=us)
        

@app.route("/Projects/<us>",methods=['GET',"POST"])
def projectsLoggedIn(us):
    if request.method=='GET':
        #Query DB and send in list of all projects into the html file:
        projs=Project.query.order_by(Project.name).all()
        
        allAOIs=InterestedIn.query.filter_by(userID=us).all()
        AOIs=[x.areaOfInterest for x in allAOIs]
        
        allLangs=CodesIn.query.filter_by(userID=us).all()
        langs=[x.language for x in allLangs]
        
        yoe=User.query.filter_by(userID=us).one().experience
                
        projRanks=[] #[Proj Object, score]
        #Adding some ranking system:
        for proj in projs:
            #Get Areas,Langs,difficulty
            paoi=ProjectAreas.query.filter_by(projID=proj.projID).all()
            projAOI=[x.areaOfInterest for x in paoi]
            
            plang=ProjLang.query.filter_by(projID=proj.projID).all()
            projLang=[x.language for x in plang]
            
            difficulty=Project.query.filter_by(projID=proj.projID).one().difficulty
            
            #Check for matches:
            score=0
            #Check AOIS:
            for aoi in AOIs:
                if aoi in projAOI:
                    score+=3
            
            #Check Langs:
            for lang in langs:
                if lang in projLang:
                    score+=1
            #Check difficulty:
            if yoe<=1 and difficulty in [1,2]:
                score+=2
            elif 1<=yoe<=2 and difficulty in [2,3]:
                score+=2
            elif 2<=yoe<=4 and difficulty in [3,4]:
                score+=2
            elif yoe>=5 and difficulty in [4,5]:
                score+=2
            
            projRanks.append([proj,score])
        
        projRanks.sort(key=lambda x:(x[1],x[0].name),reverse=True)
        
        result=[]
        for p,s in projRanks:
            temp=[p.name,p.description,p.difficulty,p.github]#name,desc,difficulty, github, languages, creatorID
            languages=ProjLang.query.filter_by(projID=p.projID).all()
            temp.append(','.join([x.language for x in languages])) #make it a single string
            
            creator=User.query.filter_by(userID=p.creatorID).one()
            temp.append(creator.name)
            result.append(temp)
        
        
        return render_template("ProjectsLoggedIn.html",allprojs=result,userID=us)
    
    else:    
        searchterm=request.form['searchbar']
        #Search by area, search by name, description, and language
        projs=Project.query.filter_by(name=searchterm).all()
        result=[]
        for p in projs:
            temp=[p.name,p.description,p.difficulty,p.github]#name,desc,difficulty, github, languages, creatorID
            languages=ProjLang.query.filter_by(projID=p.projID).all()
            temp.append(','.join([x.language for x in languages])) #make it a single string
            
            creator=User.query.filter_by(userID=p.creatorID).one()
            temp.append(creator.name)
            result.append(temp)
        
        return render_template("ProjectsLoggedIn.html",allprojs=result,userID=us)

if __name__ == '__main__':
    
    app.run(debug=True,port=5000)
