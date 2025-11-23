from django import forms

from .models import DefectReport, MaintenanceRecord, Vehicle


class EvidenceMultiFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class VehicleForm(forms.ModelForm):
    class Meta:
        model = Vehicle
        fields = [
            "unit_number",
            "registration",
            "category",
            "make",
            "model",
            "year",
            "department",
            "notes",
        ]


class DefectReportForm(forms.ModelForm):
    class Meta:
        model = DefectReport
        fields = ["vehicle", "description", "severity"]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4}),
        }


class MaintenanceRecordForm(forms.ModelForm):
    evidence_files = forms.FileField(
        required=False,
        widget=EvidenceMultiFileInput(attrs={"multiple": True}),
        help_text="Upload supporting documents or images.",
    )

    def __init__(self, *args, **kwargs):
        vehicle = kwargs.pop("vehicle", None)
        super().__init__(*args, **kwargs)
        defect_field = self.fields["defect_report"]
        defect_field.required = False
        if vehicle is not None:
            self.fields["vehicle"].initial = vehicle
            defect_field.queryset = vehicle.defects.all()
        else:
            defect_field.queryset = DefectReport.objects.all()

    class Meta:
        model = MaintenanceRecord
        fields = [
            "vehicle",
            "defect_report",
            "date",
            "description",
            "odometer_km",
            "cost",
            "next_due_date",
        ]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "next_due_date": forms.DateInput(attrs={"type": "date"}),
            "description": forms.Textarea(attrs={"rows": 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        defect = cleaned_data.get("defect_report")
        vehicle = cleaned_data.get("vehicle")
        if defect and vehicle and defect.vehicle_id != vehicle.id:
            raise forms.ValidationError(
                "Selected defect report does not belong to the chosen vehicle."
            )
        return cleaned_data
