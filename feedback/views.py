from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from . import emails
from .forms import FeedbackForm


@login_required
@require_http_methods(["GET", "POST"])
def send(request):
    form = FeedbackForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        emails.notify_feedback(request.user, form.cleaned_data["message"])
        messages.success(request, "Merci, votre message a été envoyé.")
        return redirect("items:catalog")
    return render(request, "feedback/send.html", {"form": form})
