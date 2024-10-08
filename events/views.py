from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.postgres.search import (
    SearchVector,
    SearchQuery,
    SearchRank
)
from django.db.models import Count
from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from .forms import EmailEventForm, SearchForm
from .models import Event

# class EventListView(ListView):
#     queryset = Event.published.all()
#     context_object_name = 'events'
#     paginate_by = 3
#     template_name = 'events/event/list.html'

def event_list(request, tag_slug=None):
    event_list = Event.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        event_list = event_list.filter(tags__in=[tag])
    # Pagination with 3 events per page
    paginator = Paginator(event_list, 3)
    page_number = request.GET.get('page', 1)
    try:
        events = paginator.page(page_number)
    except PageNotAnInteger:
        events = paginator.page(1)
    except EmptyPage:
        # If the page number is out of range, get the last page of results
        events = paginator.page(paginator.num_pages)
    return render(
        request,
        'events/event/list.html',
        {
            'events': events,
            'tag': tag
        }
    )

def event_detail(request, year, month, day, event):
    event = get_object_or_404(
        Event,
        status=Event.Status.PUBLISHED,
        slug=event,
        event_date__year=year,
        event_date__month=month,
        event_date__day=day
    )
    # List of similar events
    event_tags_ids = event.tags.values_list('id', flat=True)
    similar_events = Event.published.filter(
        tags__in=event_tags_ids
    ).exclude(id=event.id)
    similar_events = similar_events.annotate(
        same_tags=Count('tags')
    ).order_by('-same_tags', 'event_date')[:4]
    return render(
        request,
        'events/event/detail.html',
        {
            'event': event,
            'similar_events': similar_events
        }
    )


# Allows users to share events via email
def event_share(request, event_id):
    event = get_object_or_404(
        Event,
        id=event_id,
        status=Event.Status.PUBLISHED
    )
    sent = False
    if request.method == 'POST':
        # Form was submitted
        form = EmailEventForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data 
            event_url = request.build_absolute_uri(
                event.get_absolute_url()
            )
            subject = (
                f"{cd['name']} ({cd['email']}) "
                f"recommends you check out {event.title}"
            )
            message = (
                f"View {event.title} at {event_url}\n\n"
                f"{cd['name']}\'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=None,
                recipient_list=[cd['to']]
            )
            sent = True
    else:
        form = EmailEventForm()
    return render(
        request,
        'events/event/share.html',
        {
            'event': event,
            'form': form,
            'sent': sent
        }
    )


def event_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            search_vector = SearchVector(
                'title', weight='A'
            )
            search_query = SearchQuery(query)
            results = (
                Event.published.annotate(
                    search=search_vector,
                    rank=SearchRank(search_vector, search_query)
                ) + SearchVector('description', weight='B')
                .filter(rank__gte=0.3
                )
                .order_by('-rank')
            )
    return render(
        request,
        'events/event/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        }
    )