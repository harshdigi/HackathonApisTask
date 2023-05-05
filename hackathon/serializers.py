from rest_framework import serializers
from .models import Hackathon, HackathonSubmission, HackathonRegistration


class HackathonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Hackathon
        fields = ('id', 'title', 'description', 'background_image', 'hackathon_image', 'submission_type',
                  'start_datetime', 'end_datetime', 'reward_prize', 'created_by')
        
class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = HackathonSubmission
        fields = ('name', 'summary', 'submission_file', 'submission_link', 'submission_image', )

    

    def validate(self, data):
        submission_file = data.get('submission_file', None)
        submission_link = data.get('submission_link', None)
        submission_image = data.get('submission_image',None)
        hackathon_id = self.context.get('hackathon_id', None)
        registration = HackathonRegistration.objects.filter(user= self.context.get("user",None), hackathon__id = hackathon_id).first()
        if registration is None:
            raise serializers.ValidationError("User is not registered to hackathon, register user to make submission")
        data["registration"] =registration
        submission_type = None
        if submission_file is not None:
            submission_type = 'file'
        elif submission_link is not None:
            submission_type  = 'link'
        elif submission_image is not None:
            submission_type  = 'image'
        else:
            raise serializers.ValidationError("At least one of submission_file, submission_link, or submission_image must be present.")
        hackathon = Hackathon.objects.get(id = hackathon_id)
        if not submission_type == hackathon.submission_type :
            raise serializers.ValidationError("Submission type should be " + hackathon.submission_type)
        
        return data
    
    def create(self,validated_data):
        print(self.context)
        instance = super().create(validated_data)
        return instance

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        
        return instance
    
    def to_representation(self, instance):
        response = super().to_representation(instance)
        response["hackathon_id"] = instance.registration.hackathon.id
        return response
        