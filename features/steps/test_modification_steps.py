import time
from behave import given, when, then


@then('I click on generate the question')
def step_impl(context):
    context.test_modify_page.click_on_generate_questions()
