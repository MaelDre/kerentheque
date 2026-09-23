from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_http_methods

from contacts.forms import ContactRequestForm
from contacts.services import existing_request

from .forms import CatalogFilterForm, ItemForm
from .models import Item
from .search import normalize
from .services import delete_item


def catalog(request):
    items = Item.objects.available().select_related("owner__neighborhood", "category")
    form = CatalogFilterForm(request.GET or None)
    if form.is_valid():
        if query := normalize(form.cleaned_data["q"]).strip():
            for word in query.split():
                items = items.filter(search_text__contains=word)
        if category := form.cleaned_data["category"]:
            items = items.filter(category=category)
        if neighborhood := form.cleaned_data["neighborhood"]:
            items = items.filter(owner__neighborhood=neighborhood)

    page = Paginator(items, settings.CATALOG_PAGE_SIZE).get_page(request.GET.get("page"))
    # Conserve les filtres dans les liens de pagination.
    params = request.GET.copy()
    params.pop("page", None)
    return render(
        request,
        "items/catalog.html",
        {"form": form, "page": page, "filter_query": params.urlencode()},
    )


def get_available_item(pk):
    return get_object_or_404(Item.objects.available().select_related("owner__neighborhood", "category"), pk=pk)


def render_detail(request, item, request_form=None):
    """Fiche objet ; aussi utilisée pour réafficher le formulaire de demande en erreur."""
    context = {"item": item, "is_owner": item.owner_id == request.user.pk}
    if request.user.is_authenticated and not context["is_owner"]:
        context["existing_request"] = existing_request(request.user, item)
        if context["existing_request"] is None:
            context["request_form"] = request_form or ContactRequestForm()
            context["shared_contact"] = request.user.shared_contact()
    return render(request, "items/detail.html", context)


def detail(request, pk):
    return render_detail(request, get_available_item(pk))


@login_required
def mine(request):
    items = request.user.items.not_deleted().select_related("category")
    return render(request, "items/mine.html", {"items": items})


@login_required
@require_http_methods(["GET", "POST"])
def create(request):
    form = ItemForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        item = form.save(commit=False)
        item.owner = request.user
        item.save()
        messages.success(request, f"« {item.name} » est maintenant visible dans le catalogue.")
        return redirect(item)
    return render(request, "items/form.html", {"form": form})


def _get_own_item(request, pk):
    return get_object_or_404(Item.objects.not_deleted(), pk=pk, owner=request.user)


@login_required
@require_http_methods(["GET", "POST"])
def edit(request, pk):
    item = _get_own_item(request, pk)
    form = ItemForm(request.POST or None, instance=item)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Objet mis à jour.")
        return redirect(item)
    return render(request, "items/form.html", {"form": form, "item": item})


@login_required
@require_http_methods(["GET", "POST"])
def delete(request, pk):
    item = _get_own_item(request, pk)
    if request.method == "POST":
        delete_item(item)
        messages.success(request, f"« {item.name} » a été retiré du catalogue.")
        return redirect("items:mine")
    pending = item.requests.filter(status="pending").count()
    return render(request, "items/delete.html", {"item": item, "pending": pending})
