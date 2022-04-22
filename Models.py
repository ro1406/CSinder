# -*- coding: utf-8 -*-
"""
Created on Thu Apr 21 11:15:31 2022

@author: rohan
"""
from flask import Flask, render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.oracle import BLOB


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///CSinder.db'
db = SQLAlchemy(app)

# LOGIN TO DATABASE WITH: Username: ro  Password: ropass

workedOn=db.Table('workedOn',
                  db.Column('userID',db.String(6), db.ForeignKey('user.userID')),
                  db.Column('projID',db.String(6), db.ForeignKey('project.projID')))

worksIn=db.Table('worksIn',
                  db.Column('userID',db.String(6), db.ForeignKey('user.userID')),
                  db.Column('projID',db.String(6), db.ForeignKey('project.projID')))

#########################################################################################################
 
class User(db.Model):
    name = db.Column(db.String(100), unique=False, nullable=False)
    username = db.Column(db.String(80), unique=True,nullable=False)
    userID = db.Column(db.String(6), primary_key=True)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    experience = db.Column(db.Integer, unique=False, nullable=False,default=0)
    github = db.Column(db.String(500), default="www.github.com")
    picture = db.Column(BLOB)
    # POST function: image = request.files['image'].read()
    # user=User(...., picture=image)
    
    workedOn = db.relationship('Project',secondary=workedOn)#Projects the user has worked on
    
    projectsCreated=db.relationship('Project',backref='user')
    
    interestedIn = db.relationship('InterestedIn',backref="user") #Fields user is interested in
    
    codesIn = db.relationship('CodesIn',backref="user") #Languages user prefers to code in
    
    worksIn = db.relationship('Project',secondary=worksIn)#Projects the user has worked on
    
    appliedTo = db.relationship('AppliedTo',backref="user") #Projects user has applied to be part of
    
    def __repr__(self):
        return f'User: {self.name} {self.username}'

#########################################################################################################
    
class Project(db.Model):
    name = db.Column(db.String(100), unique=False, nullable=False)
    projID = db.Column(db.String(6), primary_key=True)
    description = db.Column(db.String(500), unique=False, nullable=False,default="")
    difficulty = db.Column(db.Integer, unique=False, nullable=False,default=0)
    github = db.Column(db.String(500), default="www.github.com")
    
    creatorID = db.Column(db.String(6),db.ForeignKey('user.userID'))
    
    projLang = db.relationship('ProjLang',backref="project") #Languages user prefers to code in
    
    projAreas = db.relationship('ProjectAreas',backref="project") #Fields user is interested in
    
    applicants = db.relationship('AppliedTo',backref="project") #Users who have applied to be part of this project
    
    def __repr__(self):
        return f"Project: {self.name} {self.projID}" 
 
#########################################################################################################
 
class InterestedIn(db.Model):
    userID = db.Column('userID',db.String(6), db.ForeignKey('user.userID'),primary_key=True)
    areaOfInterest = db.Column('areaOfInterest',db.String(80),primary_key=True)
    
    def __repr__(self):
        return f'Interested Relation: {self.userID} {self.areaOfInterest}'
 
#########################################################################################################
    
class CodesIn(db.Model):
    userID = db.Column('userID',db.String(6), db.ForeignKey('user.userID'),primary_key=True)
    language = db.Column('Language',db.String(80),primary_key=True)
    
    def __repr__(self):
        return f'Interested Relation: {self.userID} {self.language}'

#########################################################################################################
     
class ProjLang(db.Model):
    projID = db.Column('projID',db.String(6), db.ForeignKey('project.projID'),primary_key=True)
    language = db.Column('Language',db.String(80),primary_key=True)
    
    def __repr__(self):
        return f'Interested Relation: {self.projID} {self.language}'

#########################################################################################################
      
class ProjectAreas(db.Model):
    projID = db.Column('projID',db.String(6), db.ForeignKey('project.projID'),primary_key=True)
    areaOfInterest = db.Column('areaOfInterest',db.String(80),primary_key=True)
    
    def __repr__(self):
        return f'Interested Relation: {self.projID} {self.areaOfInterest}'
 
#########################################################################################################
      
class AppliedTo(db.Model):
    userID = db.Column('userID',db.String(6), db.ForeignKey('user.userID'),primary_key=True)
    projID = db.Column('projID',db.String(6), db.ForeignKey('project.projID'),primary_key=True)
    pendingConfirmation = db.Column(db.Boolean, nullable=False, default=True)
    accepted = db.Column(db.Boolean, nullable=False, default=False)
    
    def __repr__(self):
        if self.pendingConfirmation:
            return f'Interested Relation: {self.projID} {self.areaOfInterest} is pending confirmation'
        elif self.accepted:
            return f'Interested Relation: {self.projID} {self.areaOfInterest} has been accepted'
        else:
            return f'Interested Relation: {self.projID} {self.areaOfInterest} has been rejected'
 
#########################################################################################################

if __name__ == '__main__':
        
    db.create_all()
    user1 = User(name="Rohan",username="ro",password="ropass",userID="U12345",email="rohanmitra8@gmail.com",experience=4)
    user2 = User(name="Ali Soufi",username="AliWali",password="alipass",userID="U11223",email="alisoufi7@gmail.com",experience=2)
    user3 = User(name = "Dara", username = "DRaw", password = "Dpass", userID = "U11111" , email = "dara7varam@gmail.com", experience = 1 )
    
    # db.session.add_all([user,proj1,proj2])
    
    user4 = User(name="Issa",username="isss",password="issapass",userID="U82222",email="IssaNajjar@gmail.com",experience=0)
    # user5 = User(name="John Smith",username="JohnWon",password="12345",userID="U81313",email="WangDang@gmail.com",experience=5)
    # user6 = user4 = User(name="Jennifer",username="Jennifer123",password="12333",userID="U78789",email="Jenni@gmail.com",experience=3)
    
    db.session.add_all([user1,user2,user3,user4 ])
    
    user5 = User(name="John Smith",username="JohnWon",password="12345",userID="U81313",email="WangDang@gmail.com",experience=5)
    user6 = User(name="Jennifer",username="Jennifer123",password="12333",userID="U78789",email="Jenni@gmail.com",experience=3)
    user7 = User(name="Jack Harlow",username="jjhlow",password="12345",userID="U88233",email="jackwack@gmail.com",experience=5)
    user8 = User(name="Lil Nas X",username="lilnax",password="1234",userID="U77722",email="lilnas@gmail.com",experience=5)
    user9 = User(name="Sam Smith",username="singerwinger",password="1234",userID="U22223",email="samsmith@gmail.com",experience=5)
    user10 = User(name="Drake Bake",username="aubreydrake",password="1234",userID="U88882",email="drake@gmail.com",experience=5)
    
    db.session.add_all([user5, user6, user7, user8, user9, user10 ])
    
    ''' MANY TO MANY RELATIONSHIPS '''
    # user.workedOn.append(proj1)
    
    #db.session.commit()
    
    #To add new entry in that table:
    #userToAdd=User.query.filter_by(userID='U12345').first()
    #projTheyWorkedOn=Project.query.filter_by(projID='P12345').first()
    #userToAdd.workedOn.append(projTheyWorkedOn)
    #db.session.commit()
    
    #Removing objects:
    #userToAdd.workedOn.remove(projToRemove)
    #db.session.commit()
    
    ''' ONE TO MANY RELATIONSHIPS '''    
    
    proj1 = Project(name="ML Sample Project",projID="P84282",description="Quisque eget vehicula tortor. Pellentesque iaculis turpis magna, at rutrum felis scelerisque id. Sed pharetra enim eros, sit amet cursus metus laoreet vitae. Praesent nec mollis nulla, et pulvinar mi. Mauris porttitor, ligula ac blandit molestie, diam dui tempor augue, mollis condimentum nisi mauris eu mauris.",difficulty=3,user=user1)
    proj2 = Project(name="Programming in Games Project",projID="P93882",description="Morbi mollis magna sit amet mauris rutrum malesuada. Integer tortor nisi, mollis sed vestibulum sit amet, consequat eu erat. ",difficulty=1,user=user2)
    proj3 = Project(name="WoWo Game Design Graphics",projID="P98387",description="Maecenas diam augue, bibendum et commodo ac, convallis sed dui. Fusce fermentum enim non urna accumsan dictum. Proin tempor pharetra leo eu tincidunt.",difficulty=5,user=user3)
    proj4 = Project(name="Anime Neural Networks",projID="P88772",description="Cras a enim vitae turpis finibus cursus sit amet non risus. Quisque nulla eros, luctus sed lorem eget, fringilla facilisis lectus. Mauris quis commodo mauris, eu tempor turpis.",difficulty=2,user=user3)
    proj5 = Project(name="Wonky Networking LMAOO",projID="P56352",description="Curabitur ornare metus ut mauris bibendum vulputate. Maecenas ac condimentum libero. Nam magna nulla, scelerisque eu maximus euismod, imperdiet sit amet tortor.",difficulty=2,user=user2)
    proj6 = Project(name="UML Design for AI",projID="P88372",description="Phasellus dictum maximus nisi, vitae interdum mi volutpat et. Vivamus placerat pretium metus vel tincidunt. Donec vestibulum tortor non porttitor ultrices.",difficulty=4,user=user1)
    proj7 = Project(name="Homework Help?!",projID="P55442",description="enean convallis risus in massa imperdiet mattis. Sed sem nunc, consectetur id ipsum eu, sagittis scelerisque mi. Maecenas non imperdiet felis.",difficulty=4,user=user4)
    db.session.add_all([proj1,proj2,proj3, proj4, proj5, proj6, proj7])
    db.session.commit()
    
    
    '''Interested In'''
    interest1 = InterestedIn(userID='U82222',areaOfInterest="Machine Learning")
    interest2 = InterestedIn(userID='U11111',areaOfInterest="Artificial Intelligence")
    interest3 = InterestedIn(userID='U11223',areaOfInterest="Back-End Development")
    interest4 = InterestedIn(userID='U82222',areaOfInterest="Computer Networks")
    interest5 = InterestedIn(userID='U12345',areaOfInterest="Computer Graphics")
    interest6 = InterestedIn(userID='U11223',areaOfInterest="Computer Systems")
    interest7 = InterestedIn(userID='U82222',areaOfInterest="Cybersecurity")
    interest8 = InterestedIn(userID='U12345',areaOfInterest="Cryptography")
    interest9 = InterestedIn(userID='U11111',areaOfInterest="Cloud Computing")
    interest10 = InterestedIn(userID='U82222',areaOfInterest="Computer Human Interface")
    interest11 = InterestedIn(userID='U11223',areaOfInterest="Data Science")
    interest12 = InterestedIn(userID='U11111',areaOfInterest="Full-Stack Development")
    interest13 = InterestedIn(userID='U82222',areaOfInterest="Front-End Development")
    interest14 = InterestedIn(userID='U12345',areaOfInterest="Game Design")
    interest15 = InterestedIn(userID='U11223',areaOfInterest="Information Security")
    interest16 = InterestedIn(userID='U82222',areaOfInterest="Programming Languages")
    interest17  = InterestedIn(userID='U12345',areaOfInterest="Mobile Application Design")
    interest18 = InterestedIn(userID='U11223',areaOfInterest="Neural Networks")
    interest19 = InterestedIn(userID='U82222',areaOfInterest="Software Engineering")
    interest20 = InterestedIn(userID='U11111',areaOfInterest="Theory")
     
    db.session.add_all([interest1, interest2, interest3, interest4, interest5, interest6, interest7, interest8, interest9, interest10, interest11, interest12,interest13,interest14,interest15,interest16,interest17,interest18,interest19,interest20])


    '''Codes In'''
    programsin1 = CodesIn(userID='U82222',language="ASP")
    programsin2 = CodesIn(userID='U11111',language="C")
    programsin3 = CodesIn(userID='U11223',language="C#")
    programsin4 = CodesIn(userID='U82222',language="C++")
    programsin5 = CodesIn(userID='U12345',language="Objective C")
    programsin6 = CodesIn(userID='U11223',language="Erlang")
    programsin7 = CodesIn(userID='U82222',language="Git")
    programsin8 = CodesIn(userID='U12345',language="Go")
    programsin9 = CodesIn(userID='U11111',language="Haskell")
    programsin10 = CodesIn(userID='U82222',language="HTML")
    programsin11 = CodesIn(userID='U11223',language="Java")
    programsin12 = CodesIn(userID='U11111',language="Javascript")
    programsin13 = CodesIn(userID='U82222',language="LaTeX")
    programsin14 = CodesIn(userID='U12345',language="Lisp")
    programsin15 = CodesIn(userID='U11223',language="MATLAB")
    programsin16 = CodesIn(userID='U82222',language="Perl")
    programsin17 = CodesIn(userID='U12345',language="PHP")
    programsin18 = CodesIn(userID='U11223',language="Python")
    programsin19 = CodesIn(userID='U82222',language="R")
    programsin20 = CodesIn(userID='U11111',language="SQL")

    db.session.add_all([programsin2, programsin3, programsin4, programsin5, programsin6, programsin7, programsin8, programsin9, programsin10, programsin11, programsin12, programsin13,programsin14,programsin1,programsin15,programsin16,programsin17,programsin18,programsin19,programsin20])
    
    
    user1.workedOn.append(proj1)
    user1.worksIn.append(proj2)
    user1.worksIn.append(proj3)
    user2.workedOn.append(proj2)
    user3.workedOn.append(proj1)
    user3.workedOn.append(proj3)
    user4.workedOn.append(proj5)
    user4.workedOn.append(proj6)
    user4.workedOn.append(proj7)

    user1.worksIn.append(proj6)
    user1.worksIn.append(proj7)
    user1.worksIn.append(proj5)
    
    projecthasarea1 = ProjectAreas(projID='P84282',areaOfInterest="Machine Learning")
    projecthasarea2 = ProjectAreas(projID='P93882',areaOfInterest="Artificial Intelligence")
    projecthasarea3 = ProjectAreas(projID='P98387',areaOfInterest="Back-End Development")
    projecthasarea4 = ProjectAreas(projID='P84282',areaOfInterest="Computer Networks")
    projecthasarea5 = ProjectAreas(projID='P93882',areaOfInterest="Computer Graphics")
    projecthasarea6 = ProjectAreas(projID='P88772',areaOfInterest="Computer Systems")
    projecthasarea7 = ProjectAreas(projID='P84282',areaOfInterest="Cybersecurity")
    projecthasarea8 = ProjectAreas(projID='P98387',areaOfInterest="Cryptography")
    projecthasarea9 = ProjectAreas(projID='P56352',areaOfInterest="Cloud Computing")
    projecthasarea10 = ProjectAreas(projID='P88372',areaOfInterest="Computer Human Interface")
    projecthasarea11 = ProjectAreas(projID='P84282',areaOfInterest="Data Science")
    projecthasarea12 = ProjectAreas(projID='P55442',areaOfInterest="Theory")

    db.session.add_all([projecthasarea1, projecthasarea2, projecthasarea3, projecthasarea4, projecthasarea5, projecthasarea6, projecthasarea7, projecthasarea8, projecthasarea9, projecthasarea10, projecthasarea11, projecthasarea12])
    
    applied1 = AppliedTo(userID = "U81313", projID = "P93882")
    applied2 = AppliedTo(userID = "U81313", projID = "P88772")
    applied3 = AppliedTo(userID = "U88233", projID = "P55442")
    applied4 = AppliedTo(userID = "U77722", projID = "P93882")
    applied5 = AppliedTo(userID = "U22223", projID = "P84282")
    applied6 = AppliedTo(userID = "U88882", projID = "P93882")
     
    db.session.add_all([applied1, applied2, applied3, applied4, applied6, applied5 ])
    
    
    db.session.commit()
    
    '''Update record'''
    #u=User.query.filter_by(userID='U12345').first()
    #u.experience=4
    #db.session.commit()
    
    #app.run(debug=True)