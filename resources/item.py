from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ItemSchema, ItemUpdateSchema
from sqlalchemy.exc import SQLAlchemyError

from models import ItemModel
from db import db

blp = Blueprint("items", __name__, description="Operations on items")


@blp.route("/item/<string:item_id>")
class Store(MethodView):
    @blp.response(200, ItemSchema)
    def get(self, item_id):
        try:
            return items[item_id]
        except KeyError:
            abort(404, message="Item not found.")

    def delete(self, item_id):
        try:
            del items[item_id]
            return {"message": "Item deleted"}
        except KeyError:
            abort(404, message="Item not found.")

    @blp.arguments(ItemUpdateSchema)
    @blp.response(200, ItemUpdateSchema)
    def put(self, item_data, item_id):
        try:
            item = items[item_id]
            item |= item_data

            return item, 201
        except KeyError:
            abort(400, "Item not found.")


@blp.route("/item")
class Store(MethodView):
    @blp.response(200, ItemSchema(many=True))
    def get(self):
        return ItemModel.query.all()

    @blp.arguments(ItemSchema)
    @blp.response(201, ItemSchema)
    def post(self, item_data):
        item = ItemModel(**item_data)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(
                500,
                message="An Error occured while inserting item data into the database",
            )
        return item
