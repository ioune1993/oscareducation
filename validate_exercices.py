import os
import sys
import yaml

def main():
    failed = False

    for yaml_file in filter(lambda x: x.endswith(".yaml"), os.listdir("exercices")):
        try:
            yaml.safe_load(open(os.path.join("exercices", yaml_file)))
        except Exception as e:
            print "Error: failed to load yaml exercice file 'exercice/%s' because the yaml is invalide: %s" % (yaml_file, e)
            failed = True

    if not failed:
        print "All checks passed."
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
