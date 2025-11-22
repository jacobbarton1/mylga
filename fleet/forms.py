from django import forms

from .models import DefectReport, MaintenanceRecord, Vehicle


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
    class Meta:
        model = MaintenanceRecord
        fields = [
            "vehicle",
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


