from django.shortcuts import render

def video_call(request):
    return render(request, 'facechats/facechat.html')