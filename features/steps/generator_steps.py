import time
from behave import given, when, then


@given('I am on the generator page')
def step_impl(context):
    assert context.generator_page.currently_on_this_page()


@then('I enter "{low:d}" as lower range and "{up:d}" as upper range')
def step_impl(context, low, up):
    context.generator_page.fill_range_from(low)
    context.generator_page.fill_range_to(up)


@then('I enter "{elements:d}" elements asked')
def step_impl(context, elements):
    context.generator_page.fill_statistic_elements(elements)


@when('I click on the create button')
def step_impl(context):
    time.sleep(2)
    context.generator_page.generate_questions()


@then('I see a list of generated problems')
def step_impl(context):
    assert context.generated_questions_page.currently_on_this_page()


@then('I see an error panel')
def step_impl(context):
    assert context.generator_page.error_displayed()


@then('I choose a generated problem')
def step_impl(context):
    context.generated_questions_page.select_generated_problem()


@then('I click on going back to the test')
def step_impl(context):
    context.generated_questions_page.go_back_to_test()


@then('I select the rational domain')
def step_impl(context):
    context.generator_page.select_rational_domain()


@then('I set the time placed to "{time_unit}"')
def step_impl(context, time_unit):
    context.generator_page.set_time_placed_to(time_unit)


@then('I set the type of rate to "{time_unit}"')
def step_impl(context, time_unit):
    context.generator_page.set_type_rate_to(time_unit)

# Select Generator Type


@then("I select the simple interest problem generator")
def step_impl(context):
    context.generator_page.select_simple_interest_problem_generator()


@then("I select the arithmetic problem generator")
def step_impl(context):
    context.generator_page.select_arithmetic_problem_generator()


@then("I select the statistic problem generator")
def step_impl(context):
    context.generator_page.select_statistic_problem_generator()


@then("I select the volume problem generator")
def step_impl(context):
    context.generator_page.select_volume_problem_generator()


@then("I select the perimeter problem generator")
def step_impl(context):
    context.generator_page.select_perimeter_problem_generator()


@then("I select the area problem generator")
def step_impl(context):
    context.generator_page.select_area_problem_generator()


@then("I select the pythagoras problem generator")
def step_impl(context):
    context.generator_page.select_pythagoras_problem_generator()


@then('I chose to generate "{number:d}" questions')
def step_impl(context, number):
    context.generator_page.select_number_of_questions(number)


@then('I chose "{number:d}" decimals')
def step_impl(context, number):
    context.generator_page.select_number_of_decimals(number)