import unittest
from HogwartsREST import GenderEnum,House,Person,BloodPurityEnum,Subject

class TestCaseUnitHouse(unittest.TestCase):
    #Houses Tests
    def test_new_house(self):
        """
        GIVEN a House model
        WHEN a new House is created
        THEN Check the attributes
        """
        house = House(0,"DSHouse","Rocco","Lion","Science","Brugg")
        assert house.name == 'DSHouse'
        assert house.founder == 'Rocco'
        assert house.animal == 'Lion'
        assert house.ghost == 'Science'
        assert house.location == 'Brugg'

class TestCaseUnitPerson(unittest.TestCase):
    # Person Tests
    def test_new_person(self):
        """
        GIVEN a person model
        WHEN a new person is created
        THEN Check the attributes
        """
        person = Person(0,"Seamus","Finnigan",1980,GenderEnum.MALE,BloodPurityEnum.HALFBLOOD,1,Subject(0,"subjectname"))
        assert person.first_name == 'Seamus'
        assert person.name == 'Finnigan'
        assert person.birthyear == 1980
        assert person.gender == GenderEnum.MALE
        assert person.blood_purity == BloodPurityEnum.HALFBLOOD
        assert person.house_id == 1


