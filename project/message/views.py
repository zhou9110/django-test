from django.shortcuts import render
from django.core import serializers
from rest_framework.decorators import api_view
from django.http import HttpResponse, JsonResponse
import json
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q

# /message/streams/
@api_view(['GET'])
def streams(request):
    if (not request.user.is_authenticated):
        return JsonResponse({
                "command"   :   "NOT_AUTHENTICATED",
                "info"      :   "user is not authenticated"
            }, status=400)
    try:
        user_id = request.user.id
        '''
        Find all Messages with the user as either the author or recipient,
        and add the other user attached to the Message to a set--'friends.' 
        '''
        friends = set()
        for m in Message.objects.filter(author=user_id).select_related('recipient'):
            friends.add(m.recipient)
        for m in Message.objects.filter(recipient=user_id).select_related('author'):
            friends.add(m.author)

        data = {'streams': []}
        for friend_id in friends:
            messages_from = Q(author=user_id, recipient=friend_id)
            messages_to = Q(author=friend_id, recipient=user_id)
            query_1 = Message.objects.filter(messages_to)
            '''
            To determine whether the user has 'read' the stream,
            first assume they they have, and then check all messages
            where the user is the recipient--if even one is unread,
            mark the whole stream as such for ease of computation on
            the frontend.
            '''
            messages_read = True
            for v in query_1.values():
                if v['read'] == False:
                    messages_read = False
                    break
            '''
            To assemble the messages for the stream, query all messages
            that are attached to the user or the current friend. Don't worry
            about sorting by date sent, as this is done dynamically
            on the frontend.
            '''
            query_2 = Message.objects.filter(messages_from | messages_to)
            message_list = serializers.serialize('json', query_2)
            data['streams'].append({
                'friend': friend_id.pk,
                'messages': message_list,
                'read': messages_read
            })
        return JsonResponse(json.dumps(data))
    except Exception as e:
        JsonResponse({
                "command"   :   "GET_STREAMS_FAILED",
                "info"      :   str(e)
            }, status=400)
    