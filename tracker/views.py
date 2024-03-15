from django.shortcuts import render, HttpResponse
from yahoo_fin.stock_info import *
from django.views.decorators.csrf import csrf_exempt
from threading import Thread
import queue
from asgiref.sync import sync_to_async
import datetime
@sync_to_async
def checkAuth(request):
    if not request.user.is_authenticated:
        return False 
    else:
        return True

def pick_stocks(request):
    
    stocks = tickers_nifty50()
    print(stocks)
    context = {"stocks":stocks}
    return render(request, "track.html", context)

@csrf_exempt
async def selected_stocks_to_track(request):
    # if request.method == "POST":
        is_logged_in = checkAuth(request)
        if not is_logged_in:
            return HttpResponse("Log in first")
        selected_list = []
        stocks_selected = request.GET.getlist("stockpicker")
        que = queue.Queue()
        stocks_available = tickers_nifty50()
        data = {}
        nothreads = len(stocks_selected)
        list_threads = []
        print("views", stocks_selected)
        for i in range(nothreads):
            thread = Thread(target=lambda q, arg1:q.put({stocks_selected[i]:get_quote_table(arg1)}), args = (que, stocks_selected[i]))
            list_threads.append(thread)
            list_threads[i].start()
        for thread in list_threads:
            thread.join()
            
        while not que.empty():
            result = que.get()
            data.update(result)
        
        print("context", data)
        # return HttpResponse(data)
        context = {"data":data, "room_name":"track"}
        return render(request, "selected.html", context)
    
    
    
     # for i in stocks_selected:
        #     if i in stocks_available:
        #         details = get_quote_table(i)
        #         context[i] = details
        #     else:
        #         return HttpResponse({f"Stock {i} is unavailable"})
        
        # details = get_quote_table('RELIANCE.NS')