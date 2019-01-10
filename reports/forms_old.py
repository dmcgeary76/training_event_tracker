from django import forms
from django.core.validators import MinValueValidator
from .models import Event_Profile, Attendance_Entry, Content_Area, District
import csv
import datetime

# Set a simple two-option choice list to use with RadioSelect option
location_list = [
    (1, 'Irvington',),
    (2, 'Off-Site / Contract',)
]

# Create a new event with the below fields
class New_Event_Form(forms.ModelForm):
    content_area         = forms.ModelChoiceField(
                                    queryset=Content_Area.objects.all(),
                                    required=True)
    event_date           = forms.DateField(
                                    label = 'Event Date',
                                    required=True,
                                    initial=datetime.datetime.today().strftime('%Y-%m-%d'))
    event_location       = forms.ChoiceField(
                                    choices = location_list,
                                    required=True,
                                    widget = forms.RadioSelect())
    workshop_number      = forms.CharField(
                                    required=False)
    cost_per_person      = forms.DecimalField(
                                    required=True,
                                    decimal_places=2,
                                    label='Cost/Person',
                                    initial="0.00")
    class Meta:
        model = Event_Profile
        fields = [
            'content_area',
            'event_date',
            'event_location',
            'workshop_number',
            'cost_per_person'
        ]

# Add a district to a corresponding event and carry over the id from the event listing to event_id
class New_District_Form(forms.ModelForm):
    district_name       = forms.ModelChoiceField(
                                    queryset = District.objects.all(),
                                    required=True)
    number_registered   = forms.IntegerField(
                                    help_text = 'Input the total number registered for this workshop / event.',
                                    required = True,
                                    label = "Number Registered",
                                    validators=[MinValueValidator(0)])
    number_of_noshows   = forms.IntegerField(
                                    help_text = 'Input the total number of no-shows from this district.',
                                    label = "Number No-Shows")
    event_id            = forms.IntegerField(
                                    widget=forms.HiddenInput(),
                                    required = False)
    class Meta:
        model = Attendance_Entry
        fields = [
            'district_name',
            'number_registered',
            'number_of_noshows',
            'event_id'
        ]
    # Validation to make certain that the reg value is not greater than no-shows
    def clean(self):
        cleaned_data = super().clean()
        registered = cleaned_data.get("number_registered")
        noshows = cleaned_data.get("number_of_noshows")

        if registered and noshows:
            # Only do something if both fields are valid so far.
            if noshows > registered:
                # If the number of no-shows is greater than registrants, then raise a non_field_error
                raise forms.ValidationError(
                    "The number of registered participants cannot exceed "
                    "the number of no-shows for the event."
                )
