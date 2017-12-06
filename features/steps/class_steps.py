import time
from behave import then


@then('I go on my existing class')
def step_impl(context):
    context.professor_dashboard_page.access_first_class()


@then('I click on modify an existing test')
def step_impl(context):
    context.class_page.modify_existing_test()


@then('I go on class creation page')
def step_impl(context):
    context.professor_dashboard_page.click_add_class()
    assert context.create_class_page.currently_on_this_page()


@then('I access the class tests page')
def step_impl(context):
    context.class_page.access_class_tests()


@then('I create a class "{classname}"')
def step_impl(context, classname):
    context.create_class_page.enter_class_name(classname)
    context.create_class_page.select_id_stage("13")
    context.create_class_page.submit()
    assert context.add_student_class_page.currently_on_this_page()


@then('I create two students, "{firstname1}" "{lastname1}" and "{firstname2}" "{lastname2}" for my class')
def step_impl(context, firstname1, lastname1, firstname2, lastname2):
    context.add_student_class_page.fill_student_1_first_name(firstname1)
    context.add_student_class_page.fill_student_1_last_name(lastname1)
    context.add_student_class_page.fill_student_2_first_name(firstname2)
    context.add_student_class_page.fill_student_2_last_name(lastname2)
    context.add_student_class_page.submit()


@then('I am on the class homepage')
def step_impl(context):
    assert context.class_page.currently_on_this_page()
