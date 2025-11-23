from django import forms

from .models import (
    CorrectiveAction,
    FieldSample,
    Incident,
    IncidentCorrespondence,
    Laboratory,
    NonConformance,
    SampleCollection,
    SampleResult,
    Scheme,
    ServiceProvider,
    TestPoint,
    TestType,
)


class ServiceProviderForm(forms.ModelForm):
    class Meta:
        model = ServiceProvider
        fields = ["name", "spid", "primary_contact"]


class SchemeForm(forms.ModelForm):
    class Meta:
        model = Scheme
        fields = [
            "service_provider",
            "type",
            "description",
            "latitude",
            "longitude",
            "address",
        ]


class TestTypeForm(forms.ModelForm):
    class Meta:
        model = TestType
        fields = ["description", "units", "limit", "estimated_cost", "test_method"]


class TestPointForm(forms.ModelForm):
    class Meta:
        model = TestPoint
        fields = [
            "reference",
            "scheme",
            "test_types",
            "description",
            "frequency",
            "frequency_units",
        ]
        widgets = {
            "test_types": forms.CheckboxSelectMultiple,
        }


class FieldSampleForm(forms.ModelForm):
    class Meta:
        model = FieldSample
        fields = ["test_point", "collected_at", "collected_by"]
        widgets = {
            "collected_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class LaboratoryForm(forms.ModelForm):
    class Meta:
        model = Laboratory
        fields = ["name", "address", "email", "phone"]


class SampleCollectionForm(forms.ModelForm):
    class Meta:
        model = SampleCollection
        fields = ["field_samples", "sent_at", "received_at", "attachments"]
        widgets = {
            "field_samples": forms.CheckboxSelectMultiple,
            "sent_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "received_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class SampleResultForm(forms.ModelForm):
    class Meta:
        model = SampleResult
        fields = ["field_sample", "test_type", "value", "comments"]


class NonConformanceForm(forms.ModelForm):
    class Meta:
        model = NonConformance
        fields = ["sample_result", "status"]


class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        fields = ["non_conformance", "incident_id", "occurred_at", "status"]
        widgets = {
            "occurred_at": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class IncidentCorrespondenceForm(forms.ModelForm):
    class Meta:
        model = IncidentCorrespondence
        fields = ["incident", "attachments", "date_time", "comments"]
        widgets = {
            "date_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


class CorrectiveActionForm(forms.ModelForm):
    class Meta:
        model = CorrectiveAction
        fields = [
            "incident",
            "short_description",
            "long_description",
            "status",
            "estimated_delivery_date",
            "actual_delivery_date",
            "estimated_cost",
        ]
        widgets = {
            "estimated_delivery_date": forms.DateInput(attrs={"type": "date"}),
            "actual_delivery_date": forms.DateInput(attrs={"type": "date"}),
        }


class DWQMPReportForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="Start date"
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), label="End date"
    )

    def clean(self):
        cleaned_data = super().clean()
        start = cleaned_data.get("start_date")
        end = cleaned_data.get("end_date")
        if start and end and start > end:
            raise forms.ValidationError("Start date must be before end date.")
        return cleaned_data

