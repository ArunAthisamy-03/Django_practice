import json

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Questions
from .serializers import QuestionSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from microsoftservices import LuisGetIntent
from pymongo import MongoClient
from bson import json_util
from bson.json_util import dumps

question = "Question"
answer = "Answer"
def get_mongo_db():
    client = MongoClient("mongodb://127.0.0.1:27017")

    return client

class JSONResponse(HttpResponse):
    """
        An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class Retrieve(APIView):

    def post(self, request, format=None):
        serializer = QuestionSerializer(data=request.data)
        #To Do Database logic

        if serializer.is_valid():
            data = json.loads(LuisGetIntent(serializer.data['question']))
            intent_id = data["topScoringIntent"]["intent"]
            try:
                client = get_mongo_db()
                mymemDb = client['mymem_database']
                resultdata = {}
                response = []
                resultdata[question] = intent_id
                #json_data = json.dumps(resultdata)
                response = dumps(mymemDb.intents.find(resultdata))
                print response
                if response is None:
                    return Response("Service unavailable", status=status.HTTP_503_SERVICE_UNAVAILABLE)
                else:
                    return Response(response, status=status.HTTP_200_OK)
            except Exception as exc:
                print exc
                return Response("connection not established", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)