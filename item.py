from flask_restful import Resource, reqparse
from flask_jwt import jwt_required


class ItemList(Resource):
    def get(self):
        return {"items": items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="Price field can not be left blank")

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return ({'item': item}, 200) if item else ({"message": "item '{}' not found".format(name)}, 404)

    def post(self, name):
        if next(iter([item for item in items if item['name'] == name]), None):
            return {'message': "An item with name '{}' already exists".format(name)}, 400
        data = Item.parser.parse_args()
        item = {
            "name": name,
            "price": data['price']
        }
        items.append(item)
        return item, 201

    def put(self, name):
        data = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': data['price']}
            items.append(item)
        else:
            item.update(data)
        return item, 200

    def delete(self, name):
        global items
        items = [x for x in items if x['name'] != name]
        return {'message': "Item '{}' deleted.".format(name)}, 202
