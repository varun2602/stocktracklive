# chat/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs
from asgiref.sync import sync_to_async, async_to_sync
from django_celery_beat.models import PeriodicTask, IntervalSchedule
import simplejson
import copy
from . import models
class StockConsumer(AsyncWebsocketConsumer):
    @sync_to_async
    def addToCeleryBeat(self, stockpicker):
        task = PeriodicTask.objects.filter(name = "every-second")
        if len(task) > 0:
            task = task.first()
            print("task", task)
            args = json.loads(task.args)
            print("args", args)
            args = args[0]
            print("args2", args)
            for x in stockpicker:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            print("task args", task.args)
            task.save()
        else:
            print("consumer", stockpicker)
            schedule, created = IntervalSchedule.objects.get_or_create(every = 1, period = IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval = schedule, name = "every-second", task = "tracker.tasks.update_stock_2", args = json.dumps([stockpicker]))
            task.save()
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'stock_%s' % self.room_name
        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        # Parse query string 
        query_params= parse_qs(self.scope["query_string"].decode())
        print("scope", self.scope)
        print("query params", query_params)
        
        # Add to celery beat  
        stockpicker = query_params["stockpicker"]
        
        await self.addToCeleryBeat(stockpicker)
        
        # Add user to stock details 
        await self.addToStockDetails(stockpicker)
        
        
        await self.accept()
    @sync_to_async  
    def addToStockDetails(self, stockpicker):
        user = self.scope["user"]
        for i in stockpicker:
            stock, created = models.StockDetails.objects.get_or_create(stock = i)
            stock.user.add(user.id)
        
    @sync_to_async
    def helper_function(self):
        user = self.scope["user"]
        stocks = models.StockDetails.objects.filter(user= user.id)
        task = PeriodicTask.objects.get(name = "every-second")
        args = json.loads(task.args)
        args = args[0]
        for i in stocks:
            i.user.remove(user)
            if i.user.count == 0:
                args.remove(i.stock)
                i.delete()
            if args == None:
                args = []
            if len(args) == 0:
                task.delete()
            else:
                task.args = json.dumps([args])
                task.save()
            
            

    async def disconnect(self, close_code):
        await self.helper_function()
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_update',
                'message': message
            }
        )
    @sync_to_async
    def select_user_stocks(self):
        user = self.scope["user"]
        user_stocks = user.stockdetails_set.values_list('stock', flat = True)
        return list(user_stocks)
    # Receive message from room group
    async def send_stock_update(self, event):
        message = event['message']
        user_stocks = await self.select_user_stocks()
        message = copy.copy(message)
        keys = message.keys()
        for key in list(keys):
            if key in user_stocks:
                pass 
            else:
                del message[key]
        # Send message to WebSocket
        await self.send(text_data=json.dumps(message))