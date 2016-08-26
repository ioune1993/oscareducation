# encoding: utf-8

import os
import sys
import yaml

def main():
    failed = False

    for yaml_file in filter(lambda x: x.endswith(".yaml"), os.listdir("exercices")):
        try:
            exercice = yaml.safe_load(open(os.path.join("exercices", yaml_file)))
        except Exception as e:
            print "Erreur: impossible de charger 'exercice/%s' car la syntaxe yaml n'est pas respectée: %s" % (yaml_file, e)
            failed = True
            continue

        if not validate_exercice_yaml_structure(yaml_file, exercice):
            failed = True

    if not failed:
        print "All checks passed."
        sys.exit(0)
    else:
        sys.exit(1)


def validate_exercice_yaml_structure(name, exercice):
    if not isinstance(exercice, dict):
        print (u"Erreur: le premier niveau d'indentation (zero) 'exercice/%s' doit être une série de chaînes de caractères se terminant par des ':' (un dictionnaire)" % (name)).encode("Utf-8")
        return False

    for i in exercice.keys():
        if not isinstance(i, basestring):
            print (u"Erreur: le premier niveau d'indentation (zero) de 'exercice/%s' doit être une série de chaînes de caractères se terminant par des ':' or '%s' n'est pas une chaîne de caractères" % (name, i)).encode("Utf-8")
            return False

    for question, data in exercice.items():
        if not isinstance(data, dict):
            print (u"Erreur: le contenu de chaque question doit avoir un doit être une série de chaînes de caractères se terminant par des ':' (un dictionnaire), or dans 'exercice/%s' la question '%s' n'est pas un dictionnaire" % (name, question)).encode("Utf-8")
            return False

        if "type" not in data:
            print (u"Erreur: chaque question doit avoir un type, or dans 'exercice/%s' la question '%s' n'a pas de type" % (name, question)).encode("Utf-8")
            return False

        if data["type"] not in ("radio", "text", "checkbox"):
            print (u"Erreur: dans 'exercice/%s' la question '%s' possède un type invalide: '%s'\nLes types valides sont : 'text', 'checkbox' et 'radio' " % (name, question, data["type"])).encode("Utf-8")
            return False

        if "answers" not in data:
            print (u"Erreur: chaque question doit avoir une section 'answer' contenant les réponses, or la question '%s' dans 'exercices/%s' ne contient pas cette section" % (question, name)).encode("Utf-8")
            return False

        if data["type"] == "radio":
            if not isinstance(data["answers"], dict):
                print (u"Erreur: le contenu des réponses d'une question de type radio doit être une série de chaînes de caractères se terminant par des ':' (un dictionnaire), or dans 'exercice/%s' les réponses de la question '%s' n'est pas sous forme d'un dictionnaire" % (name, question)).encode("Utf-8")
                return False

            number_of_true = 0
            for i in data["answers"].values():
                if i is True:
                    number_of_true += 1

            if number_of_true == 0:
                print(u"Erreur: une question de type radio doit avoir au moins une réponse de correcte, or la question '%s' dans 'exercice/%s' n'a pas de réponse correcte possible" % (question, name)).encode("Utf-8")
                return False

            if number_of_true != 1:
                print(u"Erreur: une question de type radio ne doit avoir qu'une seul réponse de correcte, or la question '%s' dans 'exercice/%s' a %s réponses correcte possible. Passez au type 'checkbox' ou retirer une réponse correcte." % (question, name, number_of_true)).encode("Utf-8")
                return False

    return True


if __name__ == '__main__':
    main()
