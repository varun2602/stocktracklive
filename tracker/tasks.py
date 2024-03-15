from celery import shared_task 
from yahoo_fin.stock_info import *
from threading import Thread
import queue
from channels.layers import get_channel_layer
import asyncio
import simplejson as json
@shared_task(bind = True)
def update_stock_2(self, stocks_selected):
    selected_list = []
    stocks_available = tickers_nifty50()
    for i in stocks_selected:
        if i in stocks_available:
            pass 
        else:
            stocks_selected.remove(i)
    que = queue.Queue()
    print("task test", stocks_selected)
    data = {}
    nothreads = len(stocks_selected)
    list_threads = []
    for i in range(nothreads):
        thread = Thread(target=lambda q, arg1:q.put({stocks_selected[i]:json.loads(json.dumps(get_quote_table(arg1), ignore_nan = True))}), args = (que, stocks_selected[i]))
        list_threads.append(thread)
        list_threads[i].start()
    for thread in list_threads:
        thread.join()
        
    while not que.empty():
        result = que.get()
        data.update(result)
        
    # Send data to group 
    print("data test", data)
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(channel_layer.group_send("stock_track", {
    "type": "send_stock_update",
    "message": data
    }))

        
    return "Done"
    