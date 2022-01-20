from django.http import JsonResponse
from utils import get_db, parse_json
from bson import datetime, ObjectId

# Connect to database
try:
    db, _ = get_db("votingapp")
    print("Connection to database enstablished!")
except Exception:
    print("Could not connect to database")


# Return all votes
def getVotes(request):
    response = db['votes'].find({})
    return JsonResponse(parse_json(response), safe=False)


# Return vote by primary key
def getVote(request, pk):
    response = db['votes'].find_one({"_id": ObjectId(pk)})
    return JsonResponse(parse_json(response), safe=False)


# Insert new vote
def insertVote(request):

    post = {
        "macanache": "genial",
        "varsta": 13,
        "date":datetime.datetime.utcnow()
    }

    response = db['votes'].insert_one(post).inserted_id
    return JsonResponse(parse_json(response), safe=False)