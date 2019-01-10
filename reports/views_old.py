from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .forms import New_Event_Form, New_District_Form
from .models import Event_Profile, Attendance_Entry


def entry_create_view(request):
    form = New_Event_Form(request.POST or None)
    if form.is_valid():
        entry = form.save()
        # if the form data passes validation, save the form and add id to request session
        request.session['event_id'] = entry.id
        # reverse to a new view - add a district view
        return HttpResponseRedirect(reverse('new_district_view'))
    else:
        # used as a signal to indicate an invalid form submission attempt
        print('Invalid')
        context = {
                'form': form,
        }
        return render(request, "entry_create.html", context)


def new_district_view(request):
    # Need to get the event details from the associated event entry
    event = Event_Profile.objects.get(id = request.session['event_id'])
    try:
        districts = Attendance_Entry.objects.all().filter(event_id = request.session['event_id'])
    except:
        districts = []
    new_district = New_District_Form(request.POST or None)
    if new_district.is_valid():
        new_district.save()
        new_district = New_District_Form()
        context = {
            "new_district": new_district,
            "event": event,
            "event_id": request.session['event_id'], # Assign the event_id value from the request.session id
            "districts": districts
        }
        return render(request, "new_district.html", context)
    else:
        print('Invalid')
        context = {
            "new_district": new_district,
            "event": event,
            "event_id": request.session['event_id'],
            "districts": districts
        }
        return render(request, "new_district.html", context)

# Junk view assignment until I can replace it with a proper menu
def home_view(request):
    return render(request, "home.html", {})
