# encoding: utf-8
import time
from behave import given, when, then
from django.contrib.auth.hashers import make_password


@given('I am an existing non logged professor')
def step_impl(context):
    from test.factories.user import ProfessorFactory
    pass


@given('I am a logged in professor')
def step_impl(context):
    context.execute_steps(u"""
        Given I am an existing non logged professor
        Given I am on the login page
        Then I enter my username
        When I submit my username
        Then I am on the password page
        Then I enter my password
        When I submit my password
        Then I am redirected to the professor home page
    """)


@then('I create the class "{classname}", with students "{firstname1}" "{lastname1}" and "{firstname2}" "{lastname2}"')
def step_impl(context, classname, firstname1, lastname1, firstname2, lastname2):
    context.execute_steps(u"""
        Then I go on class creation page
        Then I create a class "{classname}"
        Then I create two students, "{firstname1}" "{lastname1}" and "{firstname2}" "{lastname2}" for my class
        Then I am on the class homepage
        """.format(classname=classname, firstname1=firstname1, firstname2=firstname2, lastname2=lastname2, lastname1=lastname1))


@then('I create the test "{test_name}" for skill "{skill}"')
def step_impl(context, test_name, skill):
    context.class_page.add_new_test()
    assert context.class_page.currently_on_test_type_choice()
    context.class_page.add_online_test()
    context.add_online_test_page.currently_on_this_page()
    context.add_online_test_page.select_skill(skill)
    time.sleep(0.1)
    context.add_online_test_page.add_skill()
    time.sleep(0.1)
    context.add_online_test_page.add_test_name(test_name)
    context.add_online_test_page.create_test()


@then('I create the test "{test_name}" for skill "{skill}" and access question generator')
def step_impl(context, test_name, skill):
    context.execute_steps(u"""
        Then I create the test "{test_name}" for skill "{skill}"
        Then I click on generate the question
        Given I am on the generator page
    """.format(test_name=test_name, skill=skill))


@given('I am logged with a fresh class, created a test and accessed question generator')
def step_impl(context):
    context.execute_steps(u"""
        Given I am a logged in professor
        Then I go on my existing class
        Then I access the class tests page
        Then I create the test "{test_name}" for skill "{skill}"
        Then I click on generate the question
        Given I am on the generator page
    """.format(test_name="test", skill="T4-U5-A1b"))
