from model.database import mongo_client


def fetch_posts(match: dict):
    pipeline = [
        {
            "$match": match
        },
        {
            "$lookup": {'from': 'users', 'localField': 'file_owner', 'foreignField': '_id', 'as': 'user'}
        },
        {
            "$unwind": '$user'
        },
        {
            "$lookup": {'from': 'liked', 'localField': 'image_hash', 'foreignField': 'image_hash', 'as': 'likes_objects'},
        },
        {
            "$set": {
                "likes": {
                    "$size": "$likes_objects"
                }
            }
        }
    ]

    data = list(mongo_client.get_collection('images').aggregate(pipeline))

    return data
