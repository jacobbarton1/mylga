from django import forms

from .models import Checkpoint, Journey


class JourneyForm(forms.ModelForm):
    class Meta:
        model = Journey
        fields = [
            "driver",
            "buddy",
            "vehicle",
            "origin",
            "destination",
            "start_time",
            "expected_end_time",
            "mode",
            "notes",
        ]
        widgets = {
            "start_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "expected_end_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }


class CheckpointForm(forms.ModelForm):
    class Meta:
        model = Checkpoint
        fields = [
            "name",
            "sequence",
            "expected_time",
            "latitude",
            "longitude",
        ]
        widgets = {
            "expected_time": forms.DateTimeInput(attrs={"type": "datetime-local"}),
        }


