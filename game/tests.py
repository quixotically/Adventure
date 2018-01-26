from django.db.models import Count
from django.test import TestCase
from django.urls import reverse

from .models import Situation, Choice


def create_situation(situation_text):
    """
    Create a situation with the given `situation_text` and any
    associated choices. Choices is a list of tuples of (choice_text, situation_id)
    """
    return Situation.objects.create(situation_text=situation_text)


def create_choice(choice_text, siutation_id, next_situation_id):
    """
    Create a choice with the given `choice_text`, the situation_id it
    is associated with, and its next_situation_id.
    """
    return Choice.objects.create(
        choice_text=choice_text,
        situation_id=siutation_id,
        next_situation_id=next_situation_id
    )


class SituationDetailViewTests(TestCase):
    def test_index_situation(self):
        """
        The detail view of the situation with id=1 should be the same as
        the index view. Check by looking for the situation's situation_text in each view.
        """
        situation = create_situation('First situation')
        other_situation = create_situation('Other situation')

        detail_url = reverse('game:detail', args=(situation.id,))
        detail_response = self.client.get(detail_url)
        index_url = reverse('game:index')
        index_response = self.client.get(index_url)

        self.assertContains(detail_response, situation.situation_text)
        self.assertContains(index_response, situation.situation_text)

    def test_restart_situation(self):
        """
        The detail view of a situation with no choices
        displays the Restart button.
        """
        situation = create_situation('First situation')
        other_situation = create_situation('Other situation')
        choice = create_choice('Choice', situation.id, other_situation.id)

        situation = Situation.objects.annotate(num_choices=Count('choice')).filter(num_choices=0)[0]
        detail_url = reverse('game:detail', args=(situation.id,))
        detail_response = self.client.get(detail_url)

        self.assertContains(detail_response, 'Restart')

    def test_situation(self):
        """
        The detail view of a situation with choices
        displays the choices.
        """
        situation = create_situation('First situation')
        other_situation = create_situation('Other situation')
        choice = create_choice('Choice1', situation.id, other_situation.id)
        choice = create_choice('Choice2', situation.id, other_situation.id)

        situation = Situation.objects.get(id=situation.id)
        detail_url = reverse('game:detail', args=(situation.id,))
        detail_response = self.client.get(detail_url)

        self.assertContains(detail_response, 'First situation')
        self.assertContains(detail_response, 'Choice1')
        self.assertContains(detail_response, 'Choice2')
