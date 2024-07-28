from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from .models import Event

class EventListView(ListView):
    queryset = Event.published.all()
    context_object_name = 'events'
    paginate_by = 3
    template_name = 'events/event/list.html'



# def event_list(request):
#     event_list = Event.published.all()
#     # Pagination with 3 events per page
#     paginator = Paginator(event_list, 3)
#     page_number = request.GET.get('page', 1)
#     try:
#         events = paginator.page(page_number)
#     except PageNotAnInteger:
#         events = paginator.page(1)
#     except EmptyPage:
#         # If the page number is out of range, get the last page of results
#         events = paginator.page(paginator.num_pages)
#     return render(
#         request,
#         'events/event/list.html',
#         {'events': events}
#     )

def event_detail(request, year, month, day, event):
    event = get_object_or_404(
        Event,
        status=Event.Status.PUBLISHED,
        slug=event,
        event_date__year=year,
        event_date__month=month,
        event_date__day=day
    )
    return render(
        request,
        'events/event/detail.html',
        {'event': event}
    )
