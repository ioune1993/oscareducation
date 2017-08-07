# encoding: utf-8


def validate_exercice_yaml_structure(exercice):
    """Defines if an exercice is valid, with correct
        answers types.

        :param exercice: The exercice to validate
        :type exercice: dict
        :returns: True if the exercice is valid, False otherwise
        :rtype: bool
        """

    if not isinstance(exercice, dict):
        return (u"le premier niveau d'indentation (zero) doit être une série de chaînes de caractères se terminant par des ':' (un dictionnaire)").encode("Utf-8")

    for i in exercice.keys():
        if not isinstance(i, basestring):
            return (u"le premier niveau d'indentation (zero) doit être une série de chaînes de caractères se terminant par des ':' or '%s' n'est pas une chaîne de caractères" % (i)).encode("Utf-8")

    for question, data in exercice.items():
        if not isinstance(data, dict):
            return (u"le contenu de chaque question doit avoir un doit être une série de chaînes de caractères se terminant par des ':' (un dictionnaire), or le contenu '%s' de la question '%s' n'est pas un dictionnaire" % (data, question)).encode("Utf-8")

        if "type" not in data:
            return (u"chaque question doit avoir un type, or la question '%s' n'a pas de type" % (question)).encode("Utf-8")

        if data["type"] not in ("radio", "text", "checkbox", "math", "math-simple", "math-advanced", "graph", "professor"):
            return (u"la question '%s' possède un type invalide: '%s'\nLes types valides sont : 'text', 'checkbox', 'math', 'math-simple', 'math-advanced', 'graph' et 'radio' " % (question, data["type"])).encode("Utf-8")

        if "answers" not in data:
            return (u"chaque question doit avoir une section 'answers' contenant les réponses, or la question '%s' ne contient pas cette section" % (question)).encode("Utf-8")

        if data["type"] == "radio":
            if not isinstance(data["answers"], dict):
                return (u"le contenu des réponses d'une question de type radio doit être une série de chaînes de caractères se terminant par des ':' (un dictionnaire), or les réponses de la question '%s' n'est pas sous forme d'un dictionnaire" % (question)).encode("Utf-8")

            for i in data["answers"].values():
                if i not in (True, False):
                    return (u"le contenu des réponses d'une question de type radio ne peuvent être que 'true' ou 'false' or la question '%s' possède une réponse qui est '%s' qui n'est pas 'true' ou 'false'" % (question, i)).encode("Utf-8")

            number_of_true = 0
            for i in data["answers"].values():
                if i is True:
                    number_of_true += 1

            if number_of_true == 0:
                return(u"une question de type radio doit avoir au moins une réponse de correcte, or la question '%s' n'a pas de réponse correcte possible" % (question)).encode("Utf-8")

            if number_of_true != 1:
                return(u"une question de type radio ne doit avoir qu'une seul réponse de correcte, or la question '%s' a %s réponses correcte possible. Passez au type 'checkbox' ou retirer une réponse correcte." % (question, number_of_true)).encode("Utf-8")

        elif data["type"] == "checkbox":
            if not isinstance(data["answers"], dict):
                return (u"le contenu des réponses d'une question de type checkbox doit être une série de chaînes de caractères se terminant par des ':' (un dictionnaire), or les réponses de la question '%s' n'est pas sous forme d'un dictionnaire" % (question)).encode("Utf-8")

            for i in data["answers"].values():
                if i not in (True, False):
                    return (u"le contenu des réponses d'une question de type checkbox ne peuvent être que 'true' ou 'false' or la question '%s' possède une réponse qui est '%s' qui n'est pas 'true' ou 'false'" % (question, i)).encode("Utf-8")

            number_of_true = 0
            for i in data["answers"].values():
                if i is True:
                    number_of_true += 1

            if number_of_true == 0:
                return(u"une question de type checkbox doit avoir au moins une réponse de correcte, or la question '%s' n'a pas de réponse correcte possible" % (question)).encode("Utf-8")

        elif data["type"] in ("text", "math", "math-simple", "math-advanced"):
            if not isinstance(data["answers"], list):
                return (u"le contenu des réponses d'une question de type text doit être une série de chaînes de caractères précédé par '- ' (une liste), or les réponses de la question '%s' ne sont pas sous forme d'une liste" % (question)).encode("Utf-8")

            if len(data["answers"]) < 1:
                return (u"la question '%s' ne possède pas de réponses possibles" % (question)).encode("Utf-8")

        elif data["type"] == "graph":
            for answer in data["answers"]:
                graph = answer["graph"]
                if "type" not in graph or not graph["type"]:
                    return (u"Une réponse de type graph doit avoir un sous type ('point par exemple').")

                elif graph["type"] == "point":
                    assert "coordinates" in graph
                    assert isinstance(graph["coordinates"], dict)
                    assert isinstance(graph["coordinates"].get("X"), int)
                    assert isinstance(graph["coordinates"].get("Y"), int)

                    # XXX put warning if X/Y is our of graph

        elif data["type"] == "professor":
            # No verification to perform, no automatic grade if the Professor grades the Question
            pass

        else:
            raise Exception("This case shouldn't happen as all possible questions type have been checked before")

    return True
