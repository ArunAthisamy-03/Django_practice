from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from .models import Answers
from .serializers import AnswersSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from microsoftservices import LuisGetIntent

class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)

class CategoriesList(APIView):
    def get(self, request, format=None):
        data = {'categories': {
            'displayName': 'About Me',
            'id': 'about_me',
            'subCategories': {
                'displayName': 'Personal',
                'id': 'personal',
                'questions': [{
                    'id': 'about_me_name',
                    'question': 'What is your name?'
                }, {
                    'id': 'about_me_address',
                    'question': 'What is your address?'
                }, {
                    'id': 'about_me_dob',
                    'question': 'What is your date of birth?'
                }, {
                    'id': 'about_me_place',
                    'question': 'Where are you living?'
                }
                ]
            }
        }}
        return Response(data)

    def post(self, request, format=None):
        serializer = AnswersSerializer(data=request.data)
        #To Do Database logic

        if serializer.is_valid():
            #serializer.save()
            data = LuisGetIntent(serializer.data['question'])
            #topintent = data['topScoringIntent']
            #print(serializer.data['question'])
            return Response(data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def product_list(request):
#     if request.method == 'GET':
#         data = {'categories': {
#             'displayName':'About Me',
#             'id': 'about_me',
#             'subCategories':{
#                 'displayName': 'personal',
#                 'id':'personal',
#                 'questions': [{
#                     'id': 'about_me_name',
#                     'question': 'What is your name?'
#                 },{
#                     'id': 'about_me_address',
#                     'question': 'What is your address?'
#                 },{
#                     'id': 'about_me_dob',
#                     'question': 'What is your date of birth?'
#                 },{
#                     'id': 'about_me_place',
#                     'question': 'Where are you living?'
#                 }
#                 ]
#
#             }
#         }}
#         return JSONResponse(data)
#     elif request.method == 'POST':

