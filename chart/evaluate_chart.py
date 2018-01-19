# encoding: utf-8

from __future__ import unicode_literals
from django.db import models
from django.contrib.postgres.fields import JSONField
from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
import yaml
import yamlordereddictloader
import json
import re


def standardizedTxt(str):
    return str.lower().strip().replace(" ", "")


def sameArray(a1, a2):
    '''
    :return: True if they are the same, False otherwise
    '''
    if len(a1) != len(a2): return False

    for (e1,e2) in zip(a1,a2):
        if e1 != e2:
            return False
    return True


def sameTupleArray(a1, a2):
    '''
    :return: True if they are the same, False otherwise
    '''
    if len(a1) != len(a2): return False

    for (e1,e2) in zip(a1,a2):
        if e1[0] != e2[0]:
            return False
        elif e1[1] != e2[1]:
            return False
    return True


def evaluate_chart(question, response):
    '''
    :param question: a Question object
    :param response: The response to assess
    :return: 1 if the response is correct, 0 if incorrect, -1 if automatic evaluation is impossible
    '''
    try:
        raw_correct_answers = question.get_answer()
        evaluation_type = raw_correct_answers["type"]
        list_raw_correct_answers = raw_correct_answers['answers']
        # raise Exception('response len =' + str(len(response)) + '  ' + str(response))
        if evaluation_type == "chart-barchart":
            student_answers = []
            for x in response[0].decode('utf-8').split(','):
                try:
                    student_answers.append(int(x))
                except ValueError:
                    pass
                    # print('Value error, student has send nothing or has send non int parameters')
            # raise Exception('response len ='+str(len(response))+'  '+str(response))
            for answer_str in list_raw_correct_answers:
                answer_json = json.loads(str(answer_str['chart']))
                correct_answer = answer_json['point']
                if sameArray(correct_answer, student_answers):
                    return 1
            return 0
        elif evaluation_type == "chart-piechart":
            #Assuming answer are in a dic key are sectorname and value are sector size
            student_answers = []
            try:
                student_answers_json = json.loads(str(response[0].decode('utf-8')))
            except:
                return 0
            for (l,x) in zip(student_answers_json['labels'],student_answers_json['data']):
                student_answers.append((standardizedTxt(l), int(x)))
            student_answers = sorted(student_answers,reverse=True)
            for answer_str in list_raw_correct_answers:
                try:
                    answer_json = json.loads(str(answer_str['chart']))
                except Exception as e:
                    print(str(answer_str['chart']))
                    print(e)
                point = answer_json['point']
                labels = answer_json['labels']
                correct_answer = []
                for (l,x) in zip(labels,point):
                    try:
                        correct_answer.append((standardizedTxt(l), int(x)))
                    except ValueError:
                        pass
                correct_answer = sorted(correct_answer,reverse=True)
                if sameTupleArray(correct_answer, student_answers):
                    return 1
            return 0
        else:
            return -1
    except ValueError as e:
        return -1
