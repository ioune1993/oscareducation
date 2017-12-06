from questions_factory.models.problem_models.arithmetic_problem import *
from questions_factory.models.problem_models.simple_interest_problem import *
from questions_factory.models.problem_models.statistics_problem import *
from questions_factory.models.problem_models.volume_problem import *
from questions_factory.models.problem_models.perimeter_problem import *
from questions_factory.models.problem_models.area_problem import *
from questions_factory.models.problem_models.pythagoras_problem import *


class ProblemGenerator:

    def __init__(self):
        pass

    def factory(input_dict):
        problem = input_dict["generator_name"]
        nb_decimal = input_dict["nb_decimal"]
        if problem == ArithmeticPolynomialSecondDegree.NAME:
            domain, range, image = input_dict["domain"], (input_dict["range_from"], input_dict["range_to"]), input_dict[
                "image"]
            values = input_dict.get("val", None)
            return ArithmeticPolynomialSecondDegree(domain, image, range, values, nb_decimal=nb_decimal)

        elif problem == SimpleInterestProblem.NAME:
            time_placed, type_rate = input_dict["time_placed"], input_dict["type_rate"]
            return SimpleInterestProblem(time_placed, type_rate, nb_decimal=nb_decimal)

        elif problem == StatisticsProblem.NAME:
            range, nb = (input_dict["range_from"], input_dict["range_to"]), input_dict["nb"]
            return StatisticsProblem(nb, range, nb_decimal=nb_decimal)

        elif problem == VolumeProblem.NAME:
            object_type, range_from, range_to = input_dict["object_type"], input_dict["range_from"], input_dict[
                "range_to"]
            return VolumeProblem(object_type, range_from, range_to, nb_decimal=nb_decimal)

        elif problem == PerimeterProblem.NAME:
            object_type, range_from, range_to = input_dict["object_type"], input_dict["range_from"], input_dict[
                "range_to"]
            return PerimeterProblem(object_type, range_from, range_to, nb_decimal=nb_decimal)

        elif problem == AreaProblem.NAME:
            object_type, range_from, range_to = input_dict["object_type"], input_dict["range_from"], input_dict[
                "range_to"]
            return AreaProblem(object_type, range_from, range_to, nb_decimal=nb_decimal)

        elif problem == PythagorasProblem.NAME:
            range_from, range_to = input_dict["range_from"], input_dict["range_to"]
            return PythagorasProblem(range_from, range_to, nb_decimal=nb_decimal)
        else:
            raise ValueError('Wrong problem type')

    factory = staticmethod(factory)
