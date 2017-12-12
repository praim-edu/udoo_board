from django.shortcuts import render
from .models import SoundTrack

def index(request):
    sound_traks = SoundTrack.objects.all()
    context = {
        'sound_traks': sound_traks,
    }
    return render(request, 'server/index.html', context)
