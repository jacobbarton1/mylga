from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, DetailView, ListView, TemplateView, UpdateView
from django.urls import reverse_lazy

from .forms import (
    CorrectiveActionForm,
    DWQMPReportForm,
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        counts = {
            "providers": ServiceProvider.objects.count(),
            "schemes": Scheme.objects.count(),
            "test_points": TestPoint.objects.count(),
            "field_samples": FieldSample.objects.count(),
            "collections": SampleCollection.objects.count(),
            "results": SampleResult.objects.count(),
            "non_conformances": NonConformance.objects.count(),
            "incidents": Incident.objects.count(),
            "actions": CorrectiveAction.objects.count(),
        }
        context["metrics"] = [
            {"label": "Service providers", "value": counts["providers"]},
            {"label": "Schemes", "value": counts["schemes"]},
            {"label": "Test points", "value": counts["test_points"]},
            {"label": "Field samples", "value": counts["field_samples"]},
        ]
        context["nav_cards"] = [
            {
                "title": "Service providers",
                "description": "Manage DWQMP service providers and contacts.",
                "count": counts["providers"],
                "url": reverse_lazy("dwqmp:serviceprovider_list"),
                "action": "Manage providers",
            },
            {
                "title": "Schemes & sampling points",
                "description": "Configure schemes, locations, and test points.",
                "count": counts["schemes"],
                "url": reverse_lazy("dwqmp:scheme_list"),
                "action": "View schemes",
            },
            {
                "title": "Field samples",
                "description": "Log sampling events and lab submissions.",
                "count": counts["field_samples"],
                "url": reverse_lazy("dwqmp:fieldsample_list"),
                "action": "View samples",
            },
            {
                "title": "Sample collections & results",
                "description": "Track shipments and lab reports.",
                "count": counts["results"],
                "url": reverse_lazy("dwqmp:sampleresult_list"),
                "action": "View results",
            },
            {
                "title": "Non-conformances",
                "description": "Monitor exceedances and regulatory responses.",
                "count": counts["non_conformances"],
                "url": reverse_lazy("dwqmp:nonconformance_list"),
                "action": "Review alerts",
            },
            {
                "title": "Incidents & actions",
                "description": "Record incidents and corrective actions.",
                "count": counts["incidents"],
                "url": reverse_lazy("dwqmp:incident_list"),
                "action": "Manage incidents",
            },
        ]
        return context


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
class SchemeDetailView(DetailView):
    model = Scheme
    template_name = "dwqmp/scheme_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        scheme = self.object
        context["test_points"] = scheme.test_points.select_related("scheme").all()
        context["field_sample_count"] = FieldSample.objects.filter(
            test_point__scheme=scheme
        ).count()
        return context


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

    def get_initial(self):
        initial = super().get_initial()
        scheme_id = self.request.GET.get("scheme")
        if scheme_id:
            initial["scheme"] = scheme_id
        return initial


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
class SampleResultUpdateView(UpdateView):
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
class NonConformanceUpdateView(UpdateView):
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
class IncidentUpdateView(UpdateView):
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


@method_decorator(login_required, name="dispatch")
class CorrectiveActionUpdateView(UpdateView):
    model = CorrectiveAction
    form_class = CorrectiveActionForm
    success_url = reverse_lazy("dwqmp:correctiveaction_list")
    template_name = "dwqmp/form.html"


@method_decorator(login_required, name="dispatch")
class DWQMPReportView(TemplateView):
    template_name = "dwqmp/report.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = DWQMPReportForm(self.request.GET or None)
        context["form"] = form
        context["results"] = None
        if form.is_valid():
            start = form.cleaned_data["start_date"]
            end = form.cleaned_data["end_date"]
            new_samples = FieldSample.objects.filter(
                collected_at__date__gte=start, collected_at__date__lte=end
            ).select_related("test_point", "collected_by")
            sample_collections = SampleCollection.objects.filter(
                sent_at__date__gte=start, sent_at__date__lte=end
            ).prefetch_related("field_samples")
            non_conformances = NonConformance.objects.filter(
                date_created__date__gte=start, date_created__date__lte=end
            ).select_related("sample_result", "sample_result__field_sample")
            incidents = Incident.objects.filter(
                occurred_at__date__gte=start, occurred_at__date__lte=end
            ).select_related("non_conformance")
            corrective_actions = CorrectiveAction.objects.filter(
                estimated_delivery_date__gte=start, estimated_delivery_date__lte=end
            ).select_related("incident")
            context["results"] = {
                "start": start,
                "end": end,
                "new_samples": new_samples,
                "sample_collections": sample_collections,
                "non_conformances": non_conformances,
                "incidents": incidents,
                "actions": corrective_actions,
            }
        return context
