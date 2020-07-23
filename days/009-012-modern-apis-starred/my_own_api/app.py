import json
from typing import List

from apistar import App, Route, types, validators
from apistar.http import JSONResponse

def _load_animals_data():
    with open('MOCK_DATA.json') as f:
        animals = json.loads(f.read())
        return {animal["id"]: animal for animal in animals}

animals = _load_animals_data()
VALID_ANIMAL_NAMES = set([animal["animal"] for animal in animals.values()])
ANIMAL_NOT_FOUND = "Animal not found"


class Animal(types.Type):
    id = validators.Integer(allow_null=True)
    animal = validators.String(enum=list(VALID_ANIMAL_NAMES))
    latitude = validators.Number(minimum=-90.0, maximum=90.)
    longitude = validators.Number(minimum=-180.0, maximum=180)


# API Methods

def list_animals() -> List[Animal]:
    return [Animal(animal[1]) for animal in sorted(animals.items())]


def create_animal(animal: Animal) -> JSONResponse:
    animal_id = max(animals.keys()) + 1
    animal.id = animal_id
    animals[animal_id] = animal
    return JSONResponse(Animal(animal), status_code=201)


def get_animal(animal_id: int) -> JSONResponse:
    animal = animals.get(animal_id)
    if not animal:
        error = {'error': ANIMAL_NOT_FOUND}
        return JSONResponse(error, status_code=404)
    return JSONResponse(Animal(animal), status_code=200)


def update_animal(animal_id: int) -> JSONResponse:
    pass

def delete_animal(animal_id: int) -> JSONResponse:
    pass


routes = [
    Route('/', method='GET', handler=list_animals),
    Route('/', method='POST', handler=create_animal),
    Route('/{animal_id}/', method='GET', handler=get_animal),
    Route('/{animal_id}/', method='PUT', handler=update_animal),
    Route('/{animal_id/', method='DELETE', handler=delete_animal),
    ]

app = App(routes=routes)

if __name__ == "__main__":
    app.serve('127.0.0.1', 5000, debug=True)
