import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from . models import Room
from django.shortcuts import redirect
from random import randint
from .utils import check_winner

class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.room_code = self.scope['url_route']['kwargs']['code']
        self.id_user = self.scope['session']['id_user']
        self.session_id = self.scope['cookies']['sessionid']
        
        room = Room.objects.get(code=self.room_code)
        
        room.jogadores.append({'user_id': self.id_user, 'session_id': self.session_id})
        
        room.save()
        
        self.accept()
        
        async_to_sync(self.channel_layer.group_add)(
            self.room_code,
            self.channel_name
        )
        
        if len(room.jogadores) == 1:            
            async_to_sync(self.channel_layer.group_send)(
            self.room_code,
            {
                'type': 'waiting'
            }
            )
        elif len(room.jogadores) == 2:
            x = randint(0, 1)
            
            room.turno = x
            
            room.save()
            
            async_to_sync(self.channel_layer.group_send)(             
            self.room_code,
            {
                'type': 'start'
            }
            )
        else:
            async_to_sync(self.channel_layer.group_discard)(
                self.room_code,
                self.channel_name
            )
            return redirect('home')
         

    def disconnect(self, close_code):
        room = Room.objects.get(code=self.room_code)
        
        room.tabuleiro = [[" " for col in range(3)] for row in range(3)]
        room.jogadores.remove({'user_id': self.id_user, 'session_id': self.session_id})
        
        async_to_sync(self.channel_layer.group_discard)(
            self.room_code,
            self.channel_name
        )

        if len(room.jogadores) == 0:
            room.delete()
        elif len(room.jogadores) == 1:    
            async_to_sync(self.channel_layer.group_send)(
            self.room_code,
            {
                'type': 'waiting'
            }
            )
            room.save()
        else:
            self.disconnect()
            

    # Receive message from WebSocket
    def receive(self, text_data):
        
        room = Room.objects.get(code=self.room_code)
        
        if self.session_id == room.jogadores[room.turno]['session_id'] and not room.vencedor:
            
            text_data_json = json.loads(text_data)
            position = {'row': int(text_data_json['position'][0]), 'col': int(text_data_json['position'][1])}
            
            async_to_sync(self.channel_layer.group_send)(           
                self.room_code,
                {
                    'type': 'play',
                    'position': position
                }
            )
            
            room.troca_turno()
            room.save()


    
    def waiting(self, event):
        self.send(text_data=json.dumps({
            'type': event['type']
        }))
        
    
    def start(self, event):
        self.send(text_data=json.dumps({
            'type': event['type']
        }))
        
        
    def play(self, event):
        room = Room.objects.get(code=self.room_code)
        
        position = event['position']
        room.tabuleiro[position['row']][position['col']] = 'x' if room.turno == 1 else 'o'   

        self.send(text_data=json.dumps({
            'type': 'play',
            'tabuleiro': room.tabuleiro
        }))
        
        
        room.vencedor = check_winner(room.tabuleiro)
        if room.vencedor != 'tie' and room.vencedor:
            room.vencedor = 0 if room.vencedor == 'x' else 1
        if room.vencedor == 'tie':
            room.vencedor = 2
        
        
        
        if room.vencedor:
            
            if room.vencedor == 2:
                self.send(text_data=json.dumps({
                    'type': 'tie',
                }))
                
            elif self.id_user == room.jogadores[room.vencedor]['user_id']:
                self.send(text_data=json.dumps({
                    'type': 'venceu',
                }))
                
            elif self.id_user != room.jogadores[room.vencedor]['user_id']:
                self.send(text_data=json.dumps({
                    'type': 'perdeu',
                }))
                
        room.save()
            
                
        
    