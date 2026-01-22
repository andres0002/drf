# py
# django
from django.shortcuts import get_object_or_404
# drf
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
# third
# own
from apps.core.utils.utils import validar_pk_numerico
from apps.features.user.models import Users
from apps.features.user.api.serializers.serializers import UsersViewSerializer

# Create your views here.

@api_view(['GET','POST']) # methods allowed.
def users_api_view(request, *args, **kwargs):
    model = Users
    serializer = UsersViewSerializer
    # list.
    if request.method == 'GET':
        # query.
        users = model.objects.filter(is_active=True)
        users_serializer = serializer(users, many = True)
        return Response(users_serializer.data,status=status.HTTP_200_OK)
    # create.
    elif request.method == 'POST':
        user_serializer = serializer(data=request.data)
        # validation.
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data,status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','PUT','DELETE']) # methods allowed.
def users_actions_by_pk_api_view(request, pk, *args, **kwargs):
    model = Users
    serializer = UsersViewSerializer
    # validation.
    pk, error_response = validar_pk_numerico(pk)
    if error_response:
        return error_response
    # query.
    # user = model.objects.filter(pk=pk).first()
    user = get_object_or_404(model, is_active=True, pk=pk)
    # validation.
    if user:
        # retrieve.
        if request.method == 'GET':
            user_serializer = serializer(user)
            return Response(user_serializer.data,status.HTTP_200_OK)
        # update
        if request.method == 'PUT':
            user_serializer = serializer(user, data=request.data)
            # validation.
            if user_serializer.is_valid():
                user_serializer.save()
                return Response(user_serializer.data,status.HTTP_200_OK)
            return Response(user_serializer.errors,status.HTTP_400_BAD_REQUEST)
        # delete
        if request.method == 'DELETE':
            # elimination logical.
            user.is_active = False
            user.save()
            user_serializer = serializer(user)
            return Response(user_serializer.data,status.HTTP_200_OK)
            # elimination direct.
            # user.delete()
            # return Response({'message':'Successfully User elimination.'},status=status.HTTP_204_NO_CONTENT)