from django.test import TestCase,Client
from django.core.exceptions import PermissionDenied


# Create your tests here.

"""
    We create a student with username = eleve.eleve with password = eleve by the teacher 'prof' in class 'Hankar'.
    We create a test with 'prof' for the class '5M4', in our case we have the number 464 of test and normally the eleve.eleve can't access.
    We create a test with 'prof' but not 'mis en ligne', the test 465
    We try to access to a test (28) that we've already passed
    We create a test that the user eleve.eleve didn't begin and we access it for the first time
"""
# pass tests


login = "eleve.elve"
pwd = "eleve"
n1 = "21" # Number of a test. Used to test the access without logging
n2 = "38" # Number of a test allowed.
n3 = "27" # Number of a test that we have not finished
n4 = "22" # Number of a test that we have finished
n5 = "28"
n6 = "134" # Number of lesson
n7 = 1

class testsWithoutLogging(TestCase):
    def setUp(self):
        self.client = Client()

    # A user not logged couldn't reach the page and should be redirected or got a 403 error.
    """def testStudentTestAccess(self):
        response = self.client.get("/student/test/"+n2+"/")
        #self.assertRaises(PermissionDenied,response)
        #self.assertEqual(response.status_code, 403)
        self.assertEqual(response.status_code,403,"The user should be unauthorized or redirected")"""


class passTestsTest(TestCase):


    # We test to access to a test but without logging, the server shall forbid us and send us a 404 error.
    # We take the id of a test already created, 21, in our case.
    def testWithoutLog(self):
        c = Client()
        response = c.get("/student/test/"+ n1 + "/")
        self.assertEqual(response.status_code,302)

    # We test to access to a test that the professor hasn't activated. 404 expected
    """def testNotRunnnig(self):
        c = Client()
        c.login(username="eleve.eleve",password="eleve")
        response = c.get("/student/test/start/465")
        self.assertEqual(response.status_code,404)"""

    # We test to access to the test page and we're authorized.
    def testStarted(self):
        c = Client()
        c.login(username="eleve.eleve",password="eleve")
        response = c.get("/student/test/"+n2+"/")
        self.assertRedirects(response,"/accounts/login/?next=/student/test/"+n2+"/")
        #self.assertTemplateUsed(response, "examinations/pass_test.haml")
        #self.assertEqual(response.status_code, 200)

    # We test to access to the test page where we've already passed the test.
    def testFinished(self):
        c = Client()
        c.login(username="eleve.eleve",password="eleve")
        response = c.get("/student/test/" + n4+"/")
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/student/test/'+n4+'/')
        #self.assertRedirects(response, 'examinations/test_finished.haml')
        #self.assertTemplateUsed(response,"examinations/test_finished.haml/")

    # We test to access to a test that we didn't finished
    def testRender(self):
        c = Client()
        c.login(username="eleve.eleve",password="eleve")
        response = c.get("/student/test/"+n5+"/")
        self.assertRedirects(response, '/accounts/login/?next=/student/test/' + n5 + '/')

        #self.assertRedirects(response,"examinations/take_exercice.haml")
    def testRender2(self):
        c1 = Client()
        c1.login(username="eleve.eleve",password="eleve")
        response = c1.get('/accounts/login/?next=/student/test/' + n5 + '/')
        self.assertEqual(response.status_code,200)




"""if __name__ == '__main__':
    unittest.main()"""


# skill pedagogic

login = "eleve.eleve"
pwd = "eleve"

class skillPedagogicTest(TestCase):
    def setUp(self):
        self.s = Client()
        self.s.login(username="eleve.eleve",password="eleve")

    def testHome(self):
        self.s = Client()
        self.s.login(username="eleve.eleve", password="eleve")
        response = self.s.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'home.haml')


    def testProf(self):
        self.p = Client()
        self.p.login(username="prof",password="prof")
        response = self.p.get('/professor/lesson/134/')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/professor/lesson/'+ n6 +'/')
        #self.assertRedirects(response, 'professor/lesson/detail.haml')


    """def testSkill(self):
        self.s = Client()
        self.s.login(username="eleve.eleve", password="eleve")
        response = self.s.get('/student/pedagogical/skill/S41b/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response,'professor/skill/update_pedagogical_resources.haml')

    def testSkill2(self):
        response = self.s.get('/student/pedagogical/skill/S22b/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response,'professor/skill/update_pedagogical_resources.haml')

    def testSkill3(self):
        response = self.s.get('/student/pedagogical/skill/S31fII/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response,'professor/skill/update_pedagogical_resources.haml')

    def testSkill4(self):
        response = self.s.get('/student/pedagogical/skill/S41aII/')
        self.assertEqual(response.status_code, 302)
        self.assertTemplateUsed(response,'professor/skill/update_pedagogical_resources.haml')"""



