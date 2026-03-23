from bson import ObjectId


class ListService:

    def __init__(self, db):
        self.db = db

    def create_list(self, list_data):

        if self.db.metadata_collection.find_one({"listName": list_data.listName}):
            return None

        result = self.db.grocery_collection.insert_one({
            "listName": list_data.listName,
            "items": []
        })

        self.db.metadata_collection.insert_one({
            "_id": result.inserted_id,
            "listName": list_data.listName
        })

        return str(result.inserted_id)

    def get_lists(self, name=None, sort_order="asc", group=False):

        if group:
            pipeline = [
                {"$unwind": "$items"},
                {
                    "$group": {
                        "_id": "$items.name",
                        "total_quantity": {"$sum": "$items.quantity"}
                    }
                }
            ]
            return list(self.db.grocery_collection.aggregate(pipeline))

        query = {}
        if name:
            query["listName"] = name

        order = 1 if sort_order == "asc" else -1

        data = list(
            self.db.metadata_collection.find(query).sort("listName", order)
        )

        # Convert ObjectId → string
        for d in data:
            d["_id"] = str(d["_id"])

        return data

    def get_list_by_id(self, list_id):

        try:
            obj_id = ObjectId(list_id)
        except:
            return None

        lst = self.db.grocery_collection.find_one({"_id": obj_id})

        if lst:
            lst["_id"] = str(lst["_id"])

        return lst

    def delete_list(self, list_id):

        try:
            obj_id = ObjectId(list_id)
        except:
            return 0

        result = self.db.grocery_collection.delete_one({"_id": obj_id})
        self.db.metadata_collection.delete_one({"_id": obj_id})

        return result.deleted_count