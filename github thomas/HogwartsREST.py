"""

#TODO:
    - prepare statements in sql
    - Students Methoden P und A (person_id aktivieren, 0 mitgeben) -> Testing + Dok
    - Unittesting Prototyp alle
        - Python Funktionen (Eingabe/Ausgabe)
            - Datentypen (int, Bigint, float, xml, json, html, ...)
            - jede Methode mit einem unit-test
        - Integrationstests
            - sql-injection (drop...)
            - Serververbindung, SQL
    - immer CleanCode
    - Code kommentieren
    - Github Repository Beteiligungen
    - Report 1-3 Seiten
"""
# %%
from dataclasses import dataclass
from enum import Enum
from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
import json
import pandas as pd

# %%
global server
server = '127.0.0.1'
global database
database = 'hogwarts'
global mysqlUser
mysqlUser = 'restapi'
global mysqlUserPassword
mysqlUserPassword = 'sN24*tqNP7bzBSe4@yw&'

# %%
class GenderEnum(Enum):
    MALE = "male"
    FEMALE = "female"

class BloodPurityEnum(Enum):
    PUREBLOOD = "pure-blood"
    MUGGLEBORN = "muggle-born"
    HALFBLOOD = "half-blood"
    SQUIB = "squib"

@dataclass(init=True)
class Subject():
    subject_id: int
    name: str

    def as_dict(self):
        return {
            'id': self.subject_id,
            'Name': self.name,
        }

@dataclass(init=True, unsafe_hash=True)
class Person():
    person_id: int
    first_name: str
    name: str
    birthyear: int
    gender: GenderEnum
    blood_purity: BloodPurityEnum
    house_id: int
    favorite_subject: Subject

    def as_dict(self):
        return {
            'id': self.person_id,
            'First Name': self.first_name,
            'Last Name': self.name,
            'Year of Birth': self.birthyear,
            'Gender': self.gender.value,
            'Blood Purity': self.blood_purity.value,
            'House': self.house_id,
            'Favorite Subject': self.favorite_subject,
        }

@dataclass(init=True, unsafe_hash=True)
class House():
    house_id: int
    name: str
    founder: str
    animal: str
    ghost: str
    location: str

    def as_dict(self):
        return {
            'id': self.house_id,
            'Name': self.name,
            'Founder': self.founder,
            'Animal': self.animal,
            'Ghost': self.ghost,
            'Location': self.location
        }

@dataclass(init=True)
class Student(Person):
    person_id: int
    house_id: int
    favorite_subject: Subject

    def as_dict(self):
        return {
            'Favorite Subject': self.favorite_subject,
        }

# %%
# SQL Functions Students

def SelectAllStudents(cursor):
    '''This function selects all students from the hogwarts mysql Database and returns them as a list'''
    Students = []
    try:
        # Create and execute the SQL Query for all Fields and without a selection
        query = f"SELECT Person_idPerson,House_idHouse,favorite_subject,first_name, name, birthyear, gender, blood_purity FROM student LEFT JOIN person on person.idPerson=student.Person_idPerson ORDER BY Person_idPerson"
        cursor.execute(query)
        # Create House instances from the cursor fields
        for (idPerson, houseId, favorite_subject, first_name, name, birthyear, gender, blood_purity) in cursor:
            student = Student(person_id=idPerson, house_id=houseId, favorite_subject=favorite_subject, name=name, first_name=first_name,
                              birthyear=birthyear, gender=gender, blood_purity=blood_purity)
            # Add House instance to list
            Students.append(student)
    except Exception:
        # raise exceptions to the upper methods
        raise
    return Students

def SelectAllStudentsfromHouse(cursor, house_id):
    Students = []
    try:
        query = f"SELECT Person_idPerson,House_idHouse,favorite_subject,first_name, name, birthyear, gender, blood_purity FROM student LEFT JOIN person on person.idPerson=student.Person_idPerson WHERE House_idHouse = {house_id}"
        cursor.execute(query)
        for (idPerson, houseId, favorite_subject, first_name, name, birthyear, gender, blood_purity) in cursor:
            student = Student(person_id=idPerson, house_id=houseId, favorite_subject=favorite_subject, name=name, first_name=first_name,
                              birthyear=birthyear, gender=gender, blood_purity=blood_purity)
            Students.append(student)
    except Exception:
        raise
    return Students

def SelectaStudentbyId(cursor, person_id):
    Students = []
    try:
        query = f"SELECT Person_idPerson,House_idHouse,favorite_subject,first_name, name, birthyear, gender, blood_purity FROM student LEFT JOIN person on person.idPerson=student.Person_idPerson WHERE Person_idPerson = {person_id}"
        cursor.execute(query)
        for (idPerson, houseId, favorite_subject, first_name, name, birthyear, gender, blood_purity) in cursor:
            student = Student(person_id=idPerson, house_id=houseId, favorite_subject=favorite_subject, name=name, first_name=first_name,
                              birthyear=birthyear, gender=gender, blood_purity=blood_purity)
            Students.append(student)
    except Exception:
        raise
    return Students
        
def InsertNewStudentPrepared(cursor, Person):
    try:
        query_person = """INSERT INTO Person (first_name, name, birthyear, gender, blood_purity) VALUES (%s, %s, %s, %s, %s)"""
        tuple = (f'{Person.first_name}', f'{Person.name}', f'{Person.birthyear}', f'{Person.gender}', f'{Person.blood_purity}')
        cursor.execute(query_person, tuple)
    except Exception as e:
        raise  
    try:
        last_id = cursor.lastrowid
        query_student = """INSERT INTO Student (Person_idPerson, House_idHouse, favorite_subject) VALUES (%s, %s, %s)"""
        tuple = (f'{last_id}', f'{Person.house_id}', f'{Person.favorite_subject}')
        cursor.execute(query_student, tuple)
        return True
    except Exception:
        raise 

def UpdateAStudent(cursor, Person):
    try:
        query_student = """UPDATE person SET first_name = %s, name= %s, birthyear= %s, gender= %s, blood_purity = %s WHERE idPerson = %s"""
        tuple = (f'{Person.first_name}', f'{Person.name}', f'{Person.birthyear}', f'{Person.gender}', f'{Person.blood_purity}', f'{Person.person_id}')
        cursor.execute(query_student, tuple)
        return True
    except Exception:
        raise


def DeleteStudent(cursor, person_id):
    try:
        # query = f"DELETE FROM Person WHERE idPerson = {person_id}"
        query_student = """DELETE FROM Person WHERE idPerson = %s"""
        tuple = (f'{person_id}')
        cursor.execute(query_student, tuple)
        return True
    except Exception:
        raise


# %%
# SQL Functions Houses

def SelectAllHouses(cursor):
    '''This function selects all houses from the hogwarts mysql Database and returns them as a list'''
    Houses = []
    try:
        # Create and execute the SQL Query for all Fields and without a selection
        query = f"SELECT idHouse, name, founder, animal, ghost, location FROM house"
        cursor.execute(query)
        # Create House instances from the cursor fields
        for (idHouse, name, founder, animal, ghost, location) in cursor:
            house = House(house_id=idHouse, name=name, founder=founder, animal=animal, ghost=ghost,
                          location=location)
            # Add House instance to list
            Houses.append(house)
    except Exception:
        # raise exceptions to the upper methods
        raise
    return Houses


def SelectAllHousesQuery(cursor, wherequery:str):
    '''This function selects all houses with a selection by a where query from the hogwarts mysql Database and returns them as a list'''
    Houses = []
    try:
        # Create and execute the SQL Query for all Fields and with a selection from the passed where query
        query = f"SELECT idHouse, name, founder, animal, ghost, location FROM house WHERE {wherequery}"
        cursor.execute(query)
        # Create House instances from the cursor fields
        for (idHouse, name, founder, animal, ghost, location) in cursor:
            house = House(house_id=idHouse, name=name, founder=founder, animal=animal, ghost=ghost,
                          location=location)
            # Add House instance to list
            Houses.append(house)
    except Exception:
        # raise exceptions to the upper methods
        raise
    return Houses

def SelectaHousebyId(cursor, house_id):
    Houses = []
    try:
        query = f"SELECT idHouse, name, founder, animal, ghost, location FROM house WHERE idHouse = {house_id}"
        cursor.execute(query)
        for (idHouse, name, founder, animal, ghost, location) in cursor:
            house = House(house_id=idHouse, name=name, founder=founder, animal=animal, ghost=ghost,
                          location=location)
            Houses.append(house)
    except Exception:
        raise
    return Houses

def UpdateAHouse(cursor, House):
    try:
        # query = f"UPDATE house SET name = '{House.name}', founder= '{House.founder}', animal= '{House.animal}', ghost= '{House.ghost}', location = '{House.location}' WHERE idHouse = '{House.house_id}'"
        # query_student = """UPDATE person SET first_name = %s, name= %s, birthyear= %s, gender= %s, blood_purity = %s WHERE idPerson = %s"""
        query = """UPDATE house SET name = %s, founder= %s, animal= %s, ghost= %s, location = %s WHERE idHouse = %s"""
        tuple = (f'{House.name}', f'{House.founder}', f'{House.animal}', f'{House.ghost}', f'{House.location}', f'{House.house_id}')
        cursor.execute(query, tuple)
        return True
    except Exception:
        raise



def InitFlaskApp():
    app = Flask(__name__)

    app.config['MYSQL_HOST'] = server
    app.config['MYSQL_USER'] = mysqlUser
    app.config['MYSQL_PASSWORD'] = mysqlUserPassword
    app.config['MYSQL_DB'] = database

    mysqlconnectorflask = MySQL(app)
    return app, mysqlconnectorflask
# %%
# Flask
app,mysqlconnectorflask = InitFlaskApp()

@app.route("/")
def hello():
    return "Hello World! I feel good"

# %%
# Flask Student Routes

@app.route("/StudentList")
def studentsall():
    try:

        x = jsonify(SelectAllStudents(mysqlconnectorflask.connection.cursor()))
        return jsonify(SelectAllStudents(mysqlconnectorflask.connection.cursor()))
    except Exception as e:
        return jsonify(f"Error while getting list of students: {e})")
    
@app.route("/AllStudentsfromHouse/<house_id>")
def studentshouse(house_id):
    try:
        return jsonify(SelectAllStudentsfromHouse(mysqlconnectorflask.connection.cursor(), house_id))
    except Exception as e:
        return jsonify(f"Error while getting list of students: {e})")

@app.route("/StudentInfo/<person_id>")
def studentbyid(person_id):
    try:
        return jsonify(SelectaStudentbyId(mysqlconnectorflask.connection.cursor(), person_id))
    except Exception as e:
        return jsonify(f"Error while getting student ({person_id}) : {e})")

@app.route("/NewStudent",   methods=['POST'])
def newstudent():
    try:
        # InsertNewStudent(mysqlconnectorflask.connection.cursor(),
        InsertNewStudentPrepared(mysqlconnectorflask.connection.cursor(),
                     Person(**json.loads(request.get_data())))
        mysqlconnectorflask.connection.commit()
        return "Welcome to Hogwarts"
    except Exception as e:
        return jsonify(f"Error while patching person: {e})")


@app.route("/UpdateStudent/<person_id>", methods=['PUT'])
def UpdateStudent(person_id):
    try:
        UpdateAStudent(mysqlconnectorflask.connection.cursor(),
                     Person(**json.loads(request.get_data())))
        mysqlconnectorflask.connection.commit()
        return f"student ({person_id}) successfully updated"
    except Exception as e:
        return jsonify(f"Error while updating student ({person_id}) : {e})")

@app.route("/LeavingStudent/<person_id>",   methods=['DELETE'])
def leavingstudent(person_id):
    try:
        DeleteStudent(mysqlconnectorflask.connection.cursor(), person_id)
        mysqlconnectorflask.connection.commit()
        return "Goodbye from Hogwarts"
    except Exception as e:
        return jsonify(f"Error while deleting person: {e})")

# %%
# Flask House Routes

@app.route("/House")
def housesall():
    if len(request.args) == 0:
        try:
            return jsonify(SelectAllHouses(mysqlconnectorflask.connection.cursor()))
        except Exception as e:
            return jsonify(f"Error while getting houses: {e})")
    else:
        houselocation = request.args.get('location')
        try:
            return jsonify(SelectAllHousesQuery(mysqlconnectorflask.connection.cursor(), f"location = '{houselocation}'"))
        except Exception as e:
            return jsonify(f"Error while getting houses with location: {houselocation}) : {e})")

@app.route("/House/<house_id>")
def housebyid(house_id):
    try:
        return jsonify(SelectaHousebyId(mysqlconnectorflask.connection.cursor(), house_id))
    except Exception as e:
        return jsonify(f"Error while getting house ({house_id}) : {e})")

@app.route("/UpdateHouse/<house_id>", methods=['PUT'])
def PatchHouse(house_id):
    try:
        UpdateAHouse(mysqlconnectorflask.connection.cursor(),
                     House(**json.loads(request.get_data())))
        mysqlconnectorflask.connection.commit()
        return f"house ({house_id}) successfully updated"
    except Exception as e:
        return jsonify(f"Error while updating house ({house_id}) : {e})")

if __name__ == '__main__':
    app.run(debug=False)
