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
        print "Error: le premier niveau d'indentation (zero) 'exercice/%s' doit être une série de chaînes de caractères se terminant par des ':'" % (name)
        return False

    return True


if __name__ == '__main__':
    main()
