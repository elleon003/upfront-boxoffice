from django.shortcuts import render, get_object_or_404
from .models import Event

def event_list(request):
    events = Event.published.all()
    return render(
        request,
        'events/event/list.html',
        {'events': events}
    )

def event_detail(request, id):
    event = get_object_or_404(
        Event,
        id=id,
        status=Event.Status.PUBLISHED
    )
    return render(
        request,
        'events/event/detail.html',
        {'event': event}
    )
