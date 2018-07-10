from iqvia.application import create_app
from flask_script import Manager
from flask_apidoc.commands import GenerateApiDoc
from flask_script import Server


manager = Manager(create_app('testing'), False)
manager.add_command('runserver', Server('0.0.0.0', 7000))
manager.add_command('apidoc', GenerateApiDoc('iqvia/', 'iqvia/static/docs/'))


if __name__ == "__main__":
    manager.run()

