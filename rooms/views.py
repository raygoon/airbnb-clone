from django.utils import timezone
from django.urls import reverse
from django.views.generic import ListView, View
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from . import models, forms
import re


class HomeView(ListView):

    """HomeView Definition"""

    model = models.Room
    paginate_by = 12
    paginate_orphans = 5
    ordering = "created"
    context_object_name = "rooms"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        context["now"] = now
        paginator = context["paginator"]
        page = self.request.GET.get("page")
        page_range = set_pagenumber_range(10, page, paginator)
        context["page_range"] = page_range
        return context


def room_detail(request, pk):
    try:
        room = models.Room.objects.get(pk=pk)
        return render(request, "rooms/detail.html", {"room": room})
    except models.Room.DoesNotExist:
        return redirect(reverse("core:home"))
        # raise Http404()


class SearchView(View):

    """SearchView Definition"""

    def get(self, request):

        country = request.GET.get("country")
        if country:  # bounded form
            form = forms.SearchForm(request.GET)
            if form.is_valid():
                city = form.cleaned_data.get("city")
                country = form.cleaned_data.get("country")
                room_type = form.cleaned_data.get("room_type")
                price = form.cleaned_data.get("price")
                guests = form.cleaned_data.get("guests")
                bedrooms = form.cleaned_data.get("bedrooms")
                beds = form.cleaned_data.get("beds")
                baths = form.cleaned_data.get("baths")
                instant_book = form.cleaned_data.get("instant_book")
                superhost = form.cleaned_data.get("superhost")
                amenities = form.cleaned_data.get("amenities")
                facilities = form.cleaned_data.get("facilities")

                filter_args = {}

                if city != "Anywhere":
                    # 도시이름표시 정규화
                    city = city.strip()
                    city = re.sub(r"\s+", " ", city)
                    city = city.title()
                    # request.GET은 수정이 안되므로 copy해서 update
                    get_data = request.GET.copy()
                    get_data.update({"city": city})
                    form = forms.SearchForm(get_data)
                    filter_args["city__startswith"] = city

                filter_args["country"] = country

                if room_type is not None:
                    filter_args["room_type"] = room_type

                if price is not None:
                    filter_args["price__lte"] = price

                if guests is not None:
                    filter_args["guests__gte"] = guests

                if bedrooms is not None:
                    filter_args["bedrooms__gte"] = bedrooms

                if beds is not None:
                    filter_args["beds__gte"] = beds

                if baths is not None:
                    filter_args["baths__gte"] = baths

                if instant_book is True:
                    filter_args["instant_book"] = True

                if superhost is True:
                    filter_args["host__superhost"] = True

                rooms = models.Room.objects.filter(**filter_args)

                for amenity in amenities:
                    rooms = rooms.filter(amenities=amenity)

                for facility in facilities:
                    rooms = rooms.filter(facilities=facility)

                qs = rooms.order_by("-created")
                paginator = Paginator(qs, 5, orphans=3)
                page = request.GET.get("page", 1)
                rooms = paginator.get_page(page)
                page_range = set_pagenumber_range(10, page, paginator)

                # paginator에서 중복된 page argument 제거
                current_url = request.get_full_path()
                current_url = current_url.replace(f"&page={page}", "")

                return render(
                    request,
                    "rooms/search.html",
                    {
                        "form": form,
                        "rooms": rooms,
                        "current_url": current_url,
                        "page_range": page_range,
                    },
                )

        else:  # unbounded form
            form = forms.SearchForm()

        return render(request, "rooms/search.html", {"form": form})


def set_pagenumber_range(page_numbers_range, page, paginator):
    page_num = int(page) if page else 1
    start_index = int((page_num - 1) / page_numbers_range) * page_numbers_range
    end_index = start_index + page_numbers_range
    page_range = paginator.page_range[start_index:end_index]
    return page_range
