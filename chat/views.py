from django.shortcuts import render

# Create your views here.
def room(request):
    room_name = "TEST"
    return render(request, 'room.html', {
        'room_name': room_name
    })
