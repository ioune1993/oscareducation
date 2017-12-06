import time
from behave import then


@then('I select the object rhombus')
def step_impl(context):
    context.generator_page.select_perim_area_object_rhombus()


@then('I select the object rectangle')
def step_impl(context):
    context.generator_page.select_perim_area_object_rectangle()


@then('I select the object square')
def step_impl(context):
    context.generator_page.select_perim_area_object_square()


@then('I select the object triangle')
def step_impl(context):
    context.generator_page.select_perim_area_object_triangle()


@then('I select the object trapezium')
def step_impl(context):
    context.generator_page.select_perim_area_object_trapezium()


@then('I select the object quadrilateral')
def step_impl(context):
    context.generator_page.select_perim_area_object_quadrilateral()


@then('I select the object circle')
def step_impl(context):
    context.generator_page.select_perim_area_object_circle()


@then('I select the object parallelogram')
def step_impl(context):
    context.generator_page.select_perim_area_object_parallelogram()


@then('I select the object regular polygon')
def step_impl(context):
    context.generator_page.select_perim_area_object_regular_polygon()

