#!/usr/bin/env python3
# coding: utf-8

# Add your tests in this file
# pyhamcrest has to be installed
# doc: http://pyhamcrest.readthedocs.io/en/release-1.8/tutorial/

import unittest
# from selenium import webdriver
# from selenium.webdriver.comm.keys import Keys
# from selenium.webdriver.support.ui import Select
# from selenium.webdriver.support import WebDriverWait
from chart.evaluate_chart import evaluate_chart
from examinations.models import Question
from django.test import TestCase
import types

# class TeacherSide(unittest.TestCase):
#
# 	def setUp(self):
# 		self.driver = webdriver.Firefox()
# 		driver = self.driver
# 		driver.get("http://127.0.01:8000")
# 		wait = WebDriverWait(driver, 10)
# 		#assert "No results found." not in driver.page_source
#
# 	def tearDown(self):
# 		self.driver.close()
#"[u'{&quot;point&quot;:[25,25,8.333333333333332,16.666666666666664,25],&quot;labels&quot;:[&quot;secteur&quot;,&quot;secteur&quot;,&quot;secteur&quot;,&quot;secteur&quot;,&quot;secteur&quot;]}']

class CorrectionChartExercices(TestCase):
    #[u'{"data":[13.88888888888889],"labels":["uigg"]}']
    def setUp(self):
        commonQparts = ["type: ","""\nanswers:""","""\n- chart: '{"point":""",""","labels":""",
						""","AxisX":"abscisses","AxisY":"ordonnees","zeroX":-1,"zeroY":-1,"maxX":10,"maxY":10}'"""]
        setOfTest = [['chart-barchart',('[1,1,1,2]','[]'), [u'1,1,2'], 0,'response of different lenght shouldnt be considere as a True answer'],
					 ['chart-barchart',('[1,1,1,2]','[]'), [u'1,1,1,2'], 1,'same answer should be True'],
                     ['chart-barchart',('[2,2,2,2,2]','[]'),[u'1,1,2,2,2'],0,'answer different but of same length'],
                     ['chart-barchart',('','[]'),[u'1,2,1'],-1,'without true answer, it is impossible to correct'],
                     ['chart-barchart',[('[1,2,1,1]','[]'),('[1,2,2,1]','[]'),('[1,2,2,2]','[]')],[u'1,1,1,1'],0,'answer different but of same length, multiple possible answer'],
                     ['chart-barchart',[('[1,2,1,1]','[]'),('[1,2,2]','[]'),('[1,2,2,2,2]','[]')], [u'1,1,1,1'], 0,'answer different but of same length, multiple possible answer with different length'],
                     ['chart-barchart',[('[1,2,1,1]','[]'),('[1,2,2]','[]'),('[1,2,2,2,2]','[]')], [u'1,2,2'], 1,'answer correct but of same length, multiple possible answer'],
                     ['chart-barchart',[('[1,2,1,1]','[]'),('[1,2,2]','[]'),('[1,2,2,2]','[]')], [u'1,1,1,1,1'], 0,'answer different but of different length, multiple possible answer'],
                     ['chart-barchart',[('[1,2,1,1]','[]'),('[1,2,2]','[]'),('[1,2,2,2]','[]')], [u'1,2,2,2'], 1,'answer correct but of same length, multiple possible answer, last is the one'],
                     ['chart-barchart',('[]','[]'), [u''], 1,'empty answer with empty correct answer - fundamentaly correct'],
                     ['chart-barchart',('[1,1]','[]'), [u''], 0,'empty answer with non empty correct answer - fundamentaly incorrect'],
                     ['chart-piechart',('[25,25,50]','["secteur","secteur","secteur"]'),[u'{"data":[25,25,50],"labels":["secteur","secteur","secteur"]}'],1,'simple correct answer'],
                     ['chart-piechart',('[25,25,50]','["secteur","secteur","secteur"]'),[u'{"data":[13.88,25,50],"labels":["secteur","secteur","secteur"]}'],0, 'the first sector is different'],
                     ['chart-piechart',('[25,25,50]','["secteur","secteur","secteur"]'),[u'{"data":[25,25,52.77],"labels":["secteur","secteur","secteur"]}'],0, 'the last sector is different and over 360 degrees'],
                     ['chart-piechart',('[25,25,50]','["secteur","secteur","secteur"]'),[u''],0, 'no answer'],
                     ['chart-piechart',('[13.88,50,25,11.11]','["secteur","secteur","secteur","secteur"]'),[u'{"data":[25,13.88,11.11,50],"labels":["secteur","secteur","secteur","secteur"]}'],1, 'correct answer with shuffle the sectors'],
                     ['chart-piechart',('[13.88,50,25,11.11]','["secteur","s1","s2","s3"]'),[u'{"data":[25,13.88,11.11,50],"labels":["s2","secteur","s3","s1"]}'], 1, 'correct answer with shuffle the sectors and different sectors name'],
                     ['chart-piechart',('[25,25,50]','["secteur","secteur","secteur"]'), [u'{"data":[25,25,50],"labels":["secteur","s","secteur"]}'],0, 'only names does not match'],
                     ['chart-piechart',[('[25,25,50]','["secteur","secteur","secteur"]'),('[13.88,36.11,50]','["secteur","s","secteur"]')],[u'{"data":[13.88,36.11,50],"labels":["secteur","s","secteur"]}'], 1,'multiple answer are possible - the propose answer match second'],
                     ['chart-piechart',[('[25,25,50]','["secteur","secteur","secteur"]'),('[13.88,36.11,50]','["secteur","s","secteur"]')],[u'{"data":[13.88,36.11,50],"labels":["secteur","secteur","secteur"]}'], 0, 'multiple answer are possible - the propose answer does not match'],
                     ['chart-piechart',[('[25,25,50]','["secteur","secteur","secteur"]'),('[13.88,36.11,50,22.22]','["secteur","s","secteur","sec"]')],[u'{"data":[13.88,36.11,22.22,50],"labels":["secteur","s","sec","secteur"]}'], 1, 'multiple answer are possible - the propose answer match']]
        self.studentAnswer = []
        self.output = []
        self.message = []
        for (test,i) in zip(setOfTest,range(len(setOfTest))):
            if isinstance(test[1][0],types.StringTypes):
                ans = commonQparts[0]+test[0]+commonQparts[1]+commonQparts[2]+test[1][0]+commonQparts[3]+test[1][1]+commonQparts[4]
            else:
                ans = commonQparts[0]+test[0]+commonQparts[1]
                for (x,y) in test[1]:
                    ans += commonQparts[2]+x+commonQparts[3]+y + commonQparts[4]
            Question.objects.create(description=('Q' + str(i)), answer=ans, source="None", indication=test[0])
            self.studentAnswer.append(test[2])
            self.output.append(test[3])
            self.message.append(test[4])
            print(ans)
            print(test[2])

    def testBarchart(self):
        for i in range(len(self.studentAnswer)):
            Q = Question.objects.get(description='Q'+str(i))
            if Q.indication == "chart-barchart":
                self.assertEqual(evaluate_chart(Q,self.studentAnswer[i]),self.output[i],self.message[i])


    def testPiechart(self):
        for i in range(len(self.studentAnswer)):
            Q = Question.objects.get(description='Q'+str(i))
            if Q.indication == "chart-piechart":
                self.assertEqual(evaluate_chart(Q,self.studentAnswer[i]),self.output[i],self.message[i])

if __name__ == '__main__':
	unittest.main()

