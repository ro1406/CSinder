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
    
    #user4 = User(name="Issa",username="isss",password="issapass",userID="U82222",email="IssaNajjar@gmail.com",experience=0)
    # user5 = User(name="John Smith",username="JohnWon",password="12345",userID="U81313",email="WangDang@gmail.com",experience=5)
    # user6 = user4 = User(name="Jennifer",username="Jennifer123",password="12333",userID="U78789",email="Jenni@gmail.com",experience=3)
    
    #db.session.add_all([user4 ])
    
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
    proj1 = Project(name="Proj1",projID="P12345",description="test project",difficulty=3,user=user1)
    proj2 = Project(name="Proj2",projID="P12346",description="test project number 2",difficulty=1,user=user2)
    proj3 = Project(name="Proj3",projID="P12347",description="test project number 3",difficulty=5,user=user3)
    db.session.add_all([user1,user2,user3,proj1,proj2,proj3])
    db.session.commit()
    
    
    '''Interested In'''
    # interest=InterestedIn(userID='U12345',areaOfInterest="Machine Learning")
    # db.session.add(interest)
    # db.session.commit()
    
    
    '''Update record'''
    #u=User.query.filter_by(userID='U12345').first()
    #u.experience=4
    #db.session.commit()
    
    #app.run(debug=True)