from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from items.views import get_available_item

from .forms import ReportForm
from .models import Report


@login_required
@require_http_methods(["GET", "POST"])
def report(request, item_pk):
    item = get_available_item(item_pk)
    if item.owner_id == request.user.pk:
        raise Http404  # on ne peut signaler ni soi-même ni ses propres objets
    form = ReportForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        target = {"item": item} if form.cleaned_data["target"] == "item" else {"user": item.owner}
        Report.objects.create(author=request.user, reason=form.cleaned_data["reason"], **target)
        messages.success(request, "Merci, votre signalement a été transmis à l'équipe de modération.")
        return redirect(item)
    return render(request, "moderation/report.html", {"form": form, "item": item})
