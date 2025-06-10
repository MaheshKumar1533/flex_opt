import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Quiz, Subject


class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.quiz_id = self.scope['url_route']['kwargs']['quiz_id']
        self.quiz_group_name = f'quiz_{self.quiz_id}'

        # Join quiz group
        await self.channel_layer.group_add(
            self.quiz_group_name,
            self.channel_name
        )

        await self.accept()

        # Send current subject counts when user connects
        subject_counts = await self.get_subject_counts()
        await self.send(text_data=json.dumps({
            'type': 'subject_counts',
            'data': subject_counts
        }))

    async def disconnect(self, close_code):
        # Leave quiz group
        await self.channel_layer.group_discard(
            self.quiz_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        # Handle incoming WebSocket messages if needed
        pass

    # Receive message from quiz group
    async def subject_update(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'type': 'subject_update',
            'data': event['data']
        }))

    @database_sync_to_async
    def get_subject_counts(self):
        try:
            quiz = Quiz.objects.get(id=self.quiz_id)
            subjects = quiz.subjects.all()
            return [
                {
                    'id': subject.id,
                    'name': subject.name,
                    'code': subject.code,
                    'current_count': subject.current_count,
                    'max_limit': subject.max_limit,
                    'is_full': subject.is_full()
                }
                for subject in subjects
            ]
        except Quiz.DoesNotExist:
            return []
