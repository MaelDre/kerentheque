from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from items.views import get_available_item, render_detail

from . import services
from .forms import ContactRequestForm
from .models import ContactRequest


@login_required
@require_POST
def send(request, item_pk):
    item = get_available_item(item_pk)
    form = ContactRequestForm(request.POST)
    if not form.is_valid():
        return render_detail(request, item, request_form=form)
    try:
        services.send_request(request.user, item, form.cleaned_data["message"])
    except services.RequestError as error:
        messages.error(request, str(error))
        return redirect(item)
    messages.success(request, f"Votre demande a été envoyée à {item.owner.pseudo}.")
    return redirect("contacts:sent")


@login_required
def sent(request):
    requests = request.user.sent_requests.select_related("item__owner")
    return render(request, "contacts/sent.html", {"requests": requests})


@login_required
def received(request):
    requests = (
        ContactRequest.objects.filter(item__owner=request.user)
        .select_related("item", "requester__neighborhood")
        .annotate(
            pending_first=Case(
                When(status=ContactRequest.Status.PENDING, then=Value(0)), default=Value(1), output_field=IntegerField()
            )
        )
        .order_by("pending_first", "-created_at", "-pk")
    )
    return render(request, "contacts/received.html", {"requests": requests})


def _decide(request, pk, action, success_message):
    contact_request = get_object_or_404(ContactRequest, pk=pk, item__owner=request.user)
    try:
        action(contact_request, request.user)
    except services.RequestError as error:
        messages.error(request, str(error))
    else:
        messages.success(request, success_message.format(pseudo=contact_request.requester.display_name))
    return redirect("contacts:received")


@login_required
@require_POST
def accept(request, pk):
    return _decide(request, pk, services.accept, "Demande acceptée : {pseudo} a reçu vos coordonnées par email.")


@login_required
@require_POST
def refuse(request, pk):
    return _decide(request, pk, services.refuse, "Demande refusée.")
