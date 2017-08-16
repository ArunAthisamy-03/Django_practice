import json

from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Answers
from .serializers import AnswersSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from microsoftservices import LuisGetIntent
from pymongo import MongoClient
from bson import json_util


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

class Feed(APIView):

    def post(self, request, format=None):
        serializer = AnswersSerializer(data=request.data)
        #To Do Database logic

        if serializer.is_valid():
            data = json.loads(LuisGetIntent(serializer.data['question']))
            intent_id = data["topScoringIntent"]["intent"]
            try:
                client = get_mongo_db()
                mymemDb = client['mymem_database']
                resultdata = {}
                resultdata[question] = intent_id
                resultdata[answer] = serializer.data['answer']
                json_data = json.dumps(resultdata)
                temp = json_util.loads(json_data)
                collection = mymemDb['intents']
                response = mymemDb.intents.insert(temp)
                if response is None:
                    return Response("Memory not added", status=status.HTTP_503_SERVICE_UNAVAILABLE)
                else:
                    return Response("Memory added successfully", status=status.HTTP_201_CREATED)
            except Exception as exc:
                print exc
                return Response("connection not established", status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    #def get(self, request, format=None):
    #    serializer = AnswersSerializer(data=request.data)
    #   #To Do Database logic

    #   if serializer.is_valid():
    #        data = json.loads(LuisGetIntent(serializer.data['question']))
    #        intent_id = data["topScoringIntent"]["intent"]

    #       try:
    #            client = get_mongo_db()
    #            mymemDb = client['mymem_database']
    #            resultdata = {}
    #            resultdata[question] = intent_id
    #            resultdata[answer] = serializer.data['answer']
    #            json_data = json.dumps(resultdata)
    #            temp = json_util.loads(json_data)
    #            collection = mymemDb['intents']
    #            response = mymemDb.intents.insert(temp)
    #            if response is None:
    #                return Response("Memory not added", status=status.HTTP_503_SERVICE_UNAVAILABLE)
    #            else:
    #                return Response("Memory added successfully", status=status.HTTP_201_CREATED)
    #        except Exception as exc:
    #            print exc
    #            return Response("connection not established", status=status.HTTP_400_BAD_REQUEST)
    #    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)