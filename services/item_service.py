from bson import ObjectId


class ItemService:

    def __init__(self, db):
        self.db = db

    def get_items(self, list_id):

        try:
            obj_id = ObjectId(list_id)
        except:
            return None

        lst = self.db.grocery_collection.find_one({"_id": obj_id})

        if not lst:
            return None

        return lst["items"]

    def add_item(self, list_id, item):

        try:
            obj_id = ObjectId(list_id)
        except:
            return "INVALID_ID"

        lst = self.db.grocery_collection.find_one({"_id": obj_id})

        if not lst:
            return "LIST_NOT_FOUND"

        for i in lst["items"]:
            if i["id"] == item.id:
                return "DUPLICATE"

        self.db.grocery_collection.update_one(
            {"_id": obj_id},
            {"$push": {"items": item.dict()}}
        )

        return "SUCCESS"

    def delete_item(self, list_id, item_id):

        try:
            obj_id = ObjectId(list_id)
        except:
            return 0

        result = self.db.grocery_collection.update_one(
            {"_id": obj_id},
            {"$pull": {"items": {"id": item_id}}}
        )

        return result.modified_count

    def update_item(self, list_id, item):

        try:
            obj_id = ObjectId(list_id)
        except:
            return 0

        result = self.db.grocery_collection.update_one(
            {"_id": obj_id, "items.id": item.id},
            {
                "$set": {
                    "items.$.name": item.name,
                    "items.$.quantity": item.quantity
                }
            }
        )

        return result.modified_count

    def patch_item(self, list_id, item_id, data):

        try:
            obj_id = ObjectId(list_id)
        except:
            return "INVALID_ID"

        update_fields = {}

        if data.name is not None:
            update_fields["items.$.name"] = data.name

        if data.quantity is not None:
            update_fields["items.$.quantity"] = data.quantity

        if not update_fields:
            return "NO_DATA"

        result = self.db.grocery_collection.update_one(
            {"_id": obj_id, "items.id": item_id},
            {"$set": update_fields}
        )

        return result.modified_count