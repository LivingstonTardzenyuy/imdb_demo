from rest_framework.decorators import api_view 
from rest_framework.response import Response
from user_app.api.serializers import RegistrationSerializer
from rest_framework.authtoken.models import Token 
from user_app import models
from rest_framework import status

#jwt
# from rest_framework_simplejwt.tokens import RefreshToken


@api_view(["POST"])
def logout(request):
    if request.method == "POST":
        request.user.auth_token.delete()
        return Response(status = status.HTTP_200_OK)


@api_view(["POST",])
def registration_view(request):
    if request.method == "POST":
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            account = serializer.save()
            
            #Once we Register the user we have to create an token authomatically for him.
            data['response'] = "Registration successful!"
            data['username'] = account.username             #we are using accounts b/c we stored it in our serializer
            data['email'] = account.email 
            
            #authomatic creation of tokens using Token base auth
            token = Token.objects.get(user = account).key 
            data['token'] = token 
            
            #authomatic creation of tokens using JWT base auth
            # refresh = RefreshToken.for_user(account)
            # data['token'] = {
            #     'refresh': str(refresh),
            #     'access': str(refresh.access_token)
            #     }
            
            # return Response(data, status=201)  # HTTP 201 Created for successful registration
        else:
            data = serializer.errors 
            return Response(data, status=400)  # HTTP 400 Bad Request for invalid data
        return Response(data, status = status.HTTP_201_CREATED)
