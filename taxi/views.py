from django.shortcuts import render

from django.views.generic import ListView, DetailView

from taxi.models import Driver, Car, Manufacturer


def index(request):
    """View function for the home page of the site."""

    context = {
        "num_drivers": Driver.objects.count(),
        "num_cars": Car.objects.count(),
        "num_manufacturers": Manufacturer.objects.count(),
    }

    return render(request, "taxi/index.html", context=context)


class ManufacturerListView(ListView):
    model = Manufacturer
    queryset = Manufacturer.objects.all().order_by("name")
    paginate_by = 5
    template_name = "taxi/manufacturer_list.html"
    context_object_name = "manufacturer_list"


class CarListView(ListView):
    model = Car
    paginate_by = 5
    queryset = Car.objects.select_related("manufacturer").all()
    context_object_name = "car_list"
    template_name = "taxi/car_list.html"


class CarDetailView(DetailView):
    model = Car


class DriverListView(ListView):
    model = Driver
    paginate_by = 5


class DriverDetailView(DetailView):
    model = Driver
    template_name = "taxi/driver_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["driver_id"] = Car.objects.filter(
            drivers__id=self.kwargs.get("pk")
        )
        return context
