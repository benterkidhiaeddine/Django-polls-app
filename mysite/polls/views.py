from typing import Any
from django.db import models
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import Question, Choice


# Create your views here.


# Use generic views here
class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_questions"

    def get_queryset(self):
        """
        Return the latest 5 question by publication date and sotre into the context_object
        """
        return Question.objects.order_by("-pub_date")[:5]


class DetailView(generic.DetailView):
    # specify the model so the generic view know which item to query
    model = Question
    template_name = "polls/detail.html"


class ResultView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        choice = question.choice_set.get(pk=request.POST["choice"])
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "This choice does not exist",
            },
        )
    else:
        # To avoid race condition we use F expressions
        choice.votes = F("votes") + 1
        choice.save()
        return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
