#!/usr/bin/env python3
import requests
import re

from argparse import ArgumentParser


def main():
    parser = ArgumentParser()
    parser.add_argument('upload_server')
    parser.add_argument('--source', default='https://github.com/gfcooking/recipes/raw/master')
    args = parser.parse_args()

    items = requests.get(args.source + '/RecipeList.txt').text.split('\n')
    items = [i.strip() for i in items if i.strip() and not i.strip().startswith('//')]
    items = [i.strip() for i in items if i.strip() and not i.strip().startswith('--')]
    items = [i.replace('.txt', '') for i in items if i.strip() and not i.strip().startswith('--')]
    recipes = [requests.get(args.source + '/{}.txt'.format(item)).text for
               item in items]
    recipes = dict(zip(items, recipes))

    for text in recipes.values():
        text = re.sub('^\s*#.*$\n?', '', text)
        parts = re.split(r'\n////*.*\n', text, re.MULTILINE)
        print(len(parts))
        title = parts[0].strip().strip('-').strip()
        description = parts[1].strip()
        sections = [''] + re.split(r'\n\*\*\**([^*\n]+)\**', parts[2])
        ingredients = {
            category.strip(): [
                re.sub(r'\s+', r' ', t.lstrip('-').lstrip())
                for t in map(str.strip, content.split('\n'))
                if t
            ]
            for category, content in zip(sections[::2], sections[1::2])
        }
        empty_keys = [k for k, v in ingredients.items() if not v]
        for empty_key in empty_keys:
            del ingredients[empty_key]
        directions = parts[3].strip()
        notes = parts[4].strip()
        data = {'title': title, 'description': description, 'ingredientCategories': ingredients,
                                  'directions': directions, 'notes': notes, 'tags': []}
        print('Uploading {}...'.format(data))
        print(requests.post(args.upload_server + '/recipes', json=data).json())


if __name__ == '__main__':
    main()
