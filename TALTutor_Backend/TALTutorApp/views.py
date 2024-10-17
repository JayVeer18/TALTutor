from django.shortcuts import render

# Create your views here.

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import TALTutorAppModel, ChatMessage

@api_view(['POST'])
def save_or_update_app_instance(request):
    data = request.data
    session_key = data.get('session_key')

    # Find or create the AppModel instance
    app_model_instance, created = TALTutorAppModel.objects.update_or_create(
        session_key=session_key,
        defaults={
            'section_name': data.get('section_name'),
            'file_path': data.get('file_path'),
            'video_url': data.get('video_url')
        }
    )

    # Clear old messages associated with the app instance
    ChatMessage.objects.filter(app=app_model_instance).delete()

    # Save the new messages (including both old and new messages)
    messages = data.get('messages', [])
    for message in messages:
        ChatMessage.objects.create(
            app=app_model_instance,
            role=message['role'],
            content=message['content']
        )

    if created:
        return Response({"status": "success", "message": "App instance created and messages saved."})
    else:
        return Response({"status": "success", "message": "App instance updated with new messages."})


# Retrieving the App instance and chat messages
@api_view(['GET'])
def load_app_instance(request, session_key):
    app_model_instance = get_object_or_404(TALTutorAppModel, session_key=session_key)
    messages = ChatMessage.objects.filter(app=app_model_instance).values('role', 'content')

    response_data = {
        "section_name": app_model_instance.section_name,
        "file_path": app_model_instance.file_path,
        "video_url": app_model_instance.video_url,
        "session_key": app_model_instance.session_key,
        "messages": list(messages),
    }

    return Response(response_data)
