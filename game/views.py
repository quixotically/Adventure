from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse

from .models import Situation, Choice

def index(request):
    return detail(request, 1)

def detail(request, situation_id):
    situation = get_object_or_404(Situation, id=situation_id)
    return render(request, 'game/detail.html', { 'situation': situation, })

def choose(request, situation_id):
    situation = get_object_or_404(Situation, id=situation_id)
    try:
        selected_choice = situation.choice_set.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'game/detail.html', {
            'situation': situation,
            'error_message': "You didn't select a choice.",
        })
    else:
        return HttpResponseRedirect(reverse('game:detail', args=(selected_choice.next_situation.id,)))
