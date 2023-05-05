from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from helper.authentication import CustomUserAuth, IsAuthenticatedModular, is_authenticated
from .models import Hackathon, HackathonRegistration, HackathonSubmission
from .serializers import HackathonSerializer, SubmissionSerializer
from rest_framework import status, viewsets, pagination
from rest_framework.decorators import api_view
from cerberus import Validator


# This viewset will be used to get all hackathons, registered hackathons and also used to create hackathon
class HackathonCreateAPIView(viewsets.ModelViewSet):
    serializer_class = HackathonSerializer
    permission_classes = [IsAuthenticatedModular]
    authentication_classes = [CustomUserAuth]
    allowed_methods = ['get', 'post']
    
    # this function will be called when we use get method
    def get_queryset(self):
        try:
            # if we pass registered_only true in query params it result will be the user registered hackathons
            if self.request.query_params.get("registered_only", False):
                registered_hackathons = HackathonRegistration.objects.filter(user = self.request.user).values_list("hackathon",flat= True).distinct()
                queryset = Hackathon.objects.filter(id__in = registered_hackathons ).order_by("start_datetime")
            else:
                queryset = Hackathon.objects.all().order_by("start_datetime")
            return queryset
        except Exception as e:
            return None
        
    # this function will be called when we use post method
    def create(self, request, *args, **kwargs):
        try:
            request.data['created_by'] = request.user.pk
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        except Exception as e:
            print("Error for log purpose", e)
            return Response({"error" : "Error in creating hackathon"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


# This api view will be used to register user to hackathon
@api_view(['POST'])
@is_authenticated
def register_hackathon(request):
    try:
        schema = {
                'hackathon_id': {
                    'type': 'integer',
                    'required': True,
                    'empty': False
                }
            }
        v= Validator()
        if not v.validate(request.data, schema):
            return Response({'error': v.errors}, status=status.HTTP_400_BAD_REQUEST)
        
        hackathon_id = request.data.get('hackathon_id', None)
        hackathon = get_object_or_404(Hackathon, id=hackathon_id)
        
        user = request.user

        if HackathonRegistration.objects.filter(user=user, hackathon=hackathon).exists():
            return Response({"error" : "User is already registered to hackathon"}, status= status.HTTP_400_BAD_REQUEST)

        registration = HackathonRegistration.objects.create(user=user, hackathon=hackathon)
        
        return Response({"message" : "Registration Successful"}, status=status.HTTP_201_CREATED)
    
    except Exception as e:
            print("Error for log purpose", e)
            return Response({"error" : "Error in hackathon registration"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


# This viewset will be used to make submission to hackathon
class HackathonSubmissionAPIView(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticatedModular]
    authentication_classes = [CustomUserAuth]
    allowed_methods = ['get', 'post']

    def get_queryset(self):
        try:
            queryset = HackathonSubmission.objects.filter(registration__user = self.request.user).order_by("created_at")
            return queryset
        except Exception as e:
            print("Error for log purpose", e)
            return None

    def create(self, request, *args, **kwargs):
        try:
            context = self.get_serializer_context()
            hackathon_id = request.data.get("hackathon_id", None)
            if hackathon_id is None or not Hackathon.objects.filter(id = hackathon_id).exists():
                return Response({"error" : "Hackathon does not exists"}, status= status.HTTP_400_BAD_REQUEST)
            context["hackathon_id"] = hackathon_id
            serializer = SubmissionSerializer(data= request.data, context = context )
            if not serializer.is_valid():
                return Response(serializer.errors)
            if HackathonSubmission.objects.filter(registration__user = request.user, registration__hackathon__id = hackathon_id).exists() :
                return Response({"error" : "User is already made submission to hackathon"}, status= status.HTTP_400_BAD_REQUEST)

            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print("Error for log purpose", e)
            return Response({"error" : "Error in hackathon submissio"}, status= status.HTTP_500_INTERNAL_SERVER_ERROR)


    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context = {"user" : self.request.user}
        return context
    
