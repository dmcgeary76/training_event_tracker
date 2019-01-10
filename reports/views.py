from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
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


def new_district_view(request, event_id=0):
    # Need to get the event details from the associated event entry
    if event_id == 0:
        event_id = request.session['event_id']
    else:
        request.session['event_id'] = event_id

    profile = get_object_or_404(Event_Profile, id = event_id)
    attend_target = int(profile.number_registered) - int(profile.number_of_noshows)

    total_registered = 0
    try:
        districts = Attendance_Entry.objects.all().filter(event_id = event_id)
        for district in districts:
            total_registered += int(district.number_attended)
    except:
        districts = []
    new_district = New_District_Form(request.POST or None)
    if new_district.is_valid():
        instance = new_district.save(commit=False)
        instance.event = profile
        instance.save()
        new_district = New_District_Form()
        return HttpResponseRedirect(reverse('new_district_view'))
    else:
        print('Invalid')
        target = attend_target - total_registered
        context = {
            "new_district": new_district,
            "profile": profile,
            "districts": districts,
            "target": target
        }
        return render(request, "new_district.html", context)


def delete_district_view (request, district_id):
    instance = get_object_or_404(Attendance_Entry, id = district_id)
    instance.delete()
    return HttpResponseRedirect(reverse('new_district_view'))


def entry_list_view(request):
    events = Event_Profile.objects.all()
    context = {
        'events': events
    }
    return render(request, "entry_list.html", context)


def entry_edit_view(request, entry_id):
    entry = Event_Profile.objects.get(id = entry_id)
    form = New_Event_Form(instance = entry)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse('entry_list_view'))
    else:
        print('invalid')
        context = {
            'form': form
        }
        return render(request, "entry_edit.html", context)

# Junk view assignment until I can replace it with a proper menu
def home_view(request):
    return render(request, "home.html", {})
