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
