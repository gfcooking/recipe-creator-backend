from argparse import ArgumentParser
from flask import Flask
from flask_cors import CORS
from flask_ruko import RukoDB
from raille import Api
from uuid import uuid4

app = Flask(__name__)
CORS(app)
api = Api(app)
db = RukoDB(app, host='localhost', port=12422)
recipes = db['recipes']


class Recipe:
    def create(self):
        recipes.append({
            'uuid': str(uuid4()),
            'title': api.json['title'],
            'description': api.json['description'],
            'ingredientCategories': api.json['ingredientCategories'],
            'directions': api.json['directions'],
            'notes': api.json['notes'],
            'tags': api.json['tags']
        })
        return {}

    def replace(self, recipe_uuid):
        recipes.by('uuid')[recipe_uuid] = {
            'uuid': recipe_uuid,
            'title': api.json['title'],
            'description': api.json['description'],
            'ingredientCategories': api.json['ingredientCategories'],
            'directions': api.json['directions'],
            'notes': api.json['notes'],
            'tags': api.json['tags']
        }
        return {}

    def get(self, recipe_uuid):
        return recipes.by('uuid')[recipe_uuid]()

    def get_all(self):
        return recipes.get() or []

    def delete(self, recipe_uuid):
        del recipes.by('uuid')[recipe_uuid]
        return {}


api.resources = {
    '/recipes': {
        'POST': Recipe.create,
        'GET': Recipe.get_all,

        '/<recipe_uuid>': {
            'GET': Recipe.get,
            'PUT': Recipe.replace,
            'DELETE': Recipe.delete
        }
    }
}


def main():
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=8080)
    parser.add_argument('-o', '--host', default='localhost')
    args = parser.parse_args()
    app.add_url_rule('/options', 'options', lambda x: '{}')
    app.run(port=args.port, host=args.host)


if __name__ == '__main__':
    main()
