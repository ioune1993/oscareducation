import time
from behave import then


@then('I select the object cone')
def step_impl(context):
    context.generator_page.select_volume_object_cone()


@then('I select the object prism')
def step_impl(context):
    context.generator_page.select_volume_object_prism()


@then('I select the object pyramid')
def step_impl(context):
    context.generator_page.select_volume_object_pyramid()


@then('I select the object cube')
def step_impl(context):
    context.generator_page.select_volume_object_cube()


@then('I select the object cylinder')
def step_impl(context):
    context.generator_page.select_volume_object_cylinder()

