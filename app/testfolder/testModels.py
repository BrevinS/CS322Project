from datetime import datetime, timedelta
import unittest
from app import app,db
from app.models import Professor, Student, Course

#Tests all member function for 3 essential classes
class ModelTestObject(unittest.TestCase):
    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_phash(self):
        p = Professor(username='BrevinS', firstname='Brevin', lastname='Simon')
        p.get_password('dog1234')
        self.assertFalse(p.check_password('cat4321'))
        self.assertTrue(p.check_password('dog1234'))

    def test_course_create(self):
        g = Professor(username='Mike1', firstname='Mike', lastname='Joe')
        db.session.add(g)
        db.session.commit()
        #Course now belongs to Professor!
        c = Course(coursenum='317', title='Automata', num_ta=2, min_gpa=3.2,
                    min_grade=1, professor_id=g.id)
        db.session.add(c)
        db.session.commit()
        #DISPLAYED __repr__ of the course that it associated with Professor
        #Professor will have one course created at this point!
        self.assertEqual(g.posts.all(), [c])
        self.assertEqual(c.ta_apps.all(), [])
        self.assertEqual(c.accepted_tas.all(), [])
        self.assertEqual(c.tags.all(), [])

    def test_student_allcommands(self):
        g = Professor(username='John1', firstname='John', lastname='Doe')
        db.session.add(g)
        db.session.commit()
        s = Student(username='slash', firstname='Jane', lastname='Doe')
        db.session.add(s)
        db.session.commit()
        #Course now belongs to Professor!
        c = Course(coursenum='322', title='SoftwarePrinciples', num_ta=1, min_gpa=4.0,
                    min_grade=3, professor_id=g.id)
        db.session.add(c)
        db.session.commit()
        #DISPLAYED __repr__ of the course that it associated with Professor
        #Professor will have one course created at this point!
        self.assertEqual(g.posts.all(), [c])
        self.assertEqual(c.ta_apps.all(), [])
        self.assertEqual(c.accepted_tas.all(), [])
        self.assertEqual(c.tags.all(), [])
        #TESTING STUDENT OPERATIONS
        s.apply(c)
        db.session.commit()
        self.assertTrue(s.is_applied(c))
        self.assertEqual(s.pendingapps.count(), 1)
        #Course Values
        self.assertEqual(s.pendingapps.first().coursenum, '322')
        self.assertEqual(s.pendingapps.first().title, 'SoftwarePrinciples')
        self.assertEqual(s.pendingapps.first().num_ta, 1)
        self.assertEqual(s.pendingapps.first().min_gpa, 4.0)
        self.assertEqual(s.pendingapps.first().min_grade, 3)
        self.assertEqual(s.pendingapps.first().professor_id, g.id)

        s.unapply(c)
        db.session.commit()
        self.assertFalse(s.is_applied(c))
        self.assertEqual(s.pendingapps.count(), 0)
        self.assertEqual(c.ta_apps.count(), 0)

        #Test TAship next
        #Student applies for course again
        s.apply(c)
        self.assertFalse(c.check(s))
        c.accepted(s)
        self.assertTrue(c.check(s))
        self.assertTrue(s.is_ta(c))
        #Test Professor can remove TA
        c.unaccept(s)
        self.assertFalse(s.is_ta(c))
        self.assertFalse(c.check(s))

if __name__ == '__main__':
    unittest.main(verbosity=2)
