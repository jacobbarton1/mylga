from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, ListView, TemplateView, UpdateView
from django.urls import reverse_lazy

from .forms import (
    CorrectiveActionForm,
    FieldSampleForm,
    IncidentForm,
    LaboratoryForm,
    NonConformanceForm,
    SampleCollectionForm,
    SampleResultForm,
    SchemeForm,
    ServiceProviderForm,
    TestPointForm,
    TestTypeForm,
)
from .models import (
    CorrectiveAction,
    FieldSample,
    Incident,
    Laboratory,
    NonConformance,
    SampleCollection,
    SampleResult,
    Scheme,
    ServiceProvider,
    TestPoint,
    TestType,
)


@method_decorator(login_required, name="dispatch")
class HomeView(TemplateView):
    template_name = "dwqmp/home.html"


@method_decorator(login_required, name="dispatch")
class ServiceProviderListView(ListView):
    model = ServiceProvider
    template_name = "dwqmp/serviceprovider_list.html"


@method_decorator(login_required, name="dispatch")
class ServiceProviderCreateView(CreateView):
    model = ServiceProvider
    form_class = ServiceProviderForm
    success_url = reverse_lazy("dwqmp:serviceprovider_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class ServiceProviderUpdateView(UpdateView):
    model = ServiceProvider
    form_class = ServiceProviderForm
    success_url = reverse_lazy("dwqmp:serviceprovider_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class SchemeListView(ListView):
    model = Scheme
    template_name = "dwqmp/scheme_list.html"


@method_decorator(login_required, name="dispatch")
class SchemeCreateView(CreateView):
    model = Scheme
    form_class = SchemeForm
    success_url = reverse_lazy("dwqmp:scheme_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class SchemeUpdateView(UpdateView):
    model = Scheme
    form_class = SchemeForm
    success_url = reverse_lazy("dwqmp:scheme_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class TestPointListView(ListView):
    model = TestPoint
    template_name = "dwqmp/testpoint_list.html"


@method_decorator(login_required, name="dispatch")
class TestPointCreateView(CreateView):
    model = TestPoint
    form_class = TestPointForm
    success_url = reverse_lazy("dwqmp:testpoint_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class TestPointUpdateView(UpdateView):
    model = TestPoint
    form_class = TestPointForm
    success_url = reverse_lazy("dwqmp:testpoint_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class FieldSampleListView(ListView):
    model = FieldSample
    template_name = "dwqmp/fieldsample_list.html"


@method_decorator(login_required, name="dispatch")
class FieldSampleCreateView(CreateView):
    model = FieldSample
    form_class = FieldSampleForm
    success_url = reverse_lazy("dwqmp:fieldsample_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class FieldSampleUpdateView(UpdateView):
    model = FieldSample
    form_class = FieldSampleForm
    success_url = reverse_lazy("dwqmp:fieldsample_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class SampleCollectionListView(ListView):
    model = SampleCollection
    template_name = "dwqmp/samplecollection_list.html"


@method_decorator(login_required, name="dispatch")
class SampleCollectionCreateView(CreateView):
    model = SampleCollection
    form_class = SampleCollectionForm
    success_url = reverse_lazy("dwqmp:samplecollection_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class SampleCollectionUpdateView(UpdateView):
    model = SampleCollection
    form_class = SampleCollectionForm
    success_url = reverse_lazy("dwqmp:samplecollection_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class SampleResultListView(ListView):
    model = SampleResult
    template_name = "dwqmp/sampleresult_list.html"


@method_decorator(login_required, name="dispatch")
class SampleResultCreateView(CreateView):
    model = SampleResult
    form_class = SampleResultForm
    success_url = reverse_lazy("dwqmp:sampleresult_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class NonConformanceListView(ListView):
    model = NonConformance
    template_name = "dwqmp/nonconformance_list.html"


@method_decorator(login_required, name="dispatch")
class NonConformanceCreateView(CreateView):
    model = NonConformance
    form_class = NonConformanceForm
    success_url = reverse_lazy("dwqmp:nonconformance_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class IncidentListView(ListView):
    model = Incident
    template_name = "dwqmp/incident_list.html"


@method_decorator(login_required, name="dispatch")
class IncidentCreateView(CreateView):
    model = Incident
    form_class = IncidentForm
    success_url = reverse_lazy("dwqmp:incident_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class CorrectiveActionListView(ListView):
    model = CorrectiveAction
    template_name = "dwqmp/correctiveaction_list.html"


@method_decorator(login_required, name="dispatch")
class CorrectiveActionCreateView(CreateView):
    model = CorrectiveAction
    form_class = CorrectiveActionForm
    success_url = reverse_lazy("dwqmp:correctiveaction_list")
    template_name = "dwqmp/form.html"

