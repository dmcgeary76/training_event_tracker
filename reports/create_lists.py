from .models import Content_Area, District, Event_Profile, Attendance_Entry
import csv
import datetime

def content_area_list():
    cas = [
            'Division Wide',
            'Digital Education',
            'ELA',
            'ECWC',
            'Leadership Speaker Series',
            'Math',
            'Scholastic',
            'Science',
            'Social Studies',
            'Special Pops'
            ]
    for content_area in cas:
        entry = Content_Area(content_name=content_area)
        entry.save()


def district_list():
    with open('districts.csv', 'r') as f:
        reader = csv.reader(f)
        your_list = list(reader)
    for row in your_list:
        for district in row:
            entry = District(district_name=district)
            entry.save()


def add1718():
    with open('1718SDS.csv', 'r') as f:
        reader = csv.reader(f)
        list1718 = list(reader)
        for entry in list1718[1:]:
            content_area = entry[0]
            event_date = datetime.datetime.strptime(entry[1], '%m/%d/%Y')
            workshop_number = entry[2]
            workshop_title = entry[3]
            cost_per_person = float(entry[8].replace(',',''))
            if workshop_number == 'Contract':
                event_location = '2'
            else:
                event_location = '1'
            new_event = Event_Profile(
                        content_area = content_area,
                        event_date = event_date,
                        workshop_number = workshop_number,
                        workshop_title = workshop_title,
                        cost_per_person = cost_per_person,
                        event_location = event_location
                    )
            for district in entry[10:]:
                if district != '':
                    event = new_event.save()
                    district_name = list1718[0][entry.index(district)]
                    number_registered = int(district)
                    print(str(number_registered) + ' at index ' + str(entry.index(district)))
                    attendance = Attendance_Entry(
                        event = event,
                        district_name = district_name,
                        number_registered = number_registered,
                        number_of_noshows = 0
                    )
                    print(attendance)
                    a_record = attendance.save()


def check1718():
    with open('1718SDS.csv', 'r') as f:
        reader = csv.reader(f)
        list1718 = list(reader)
        districts = District.objects.all()
        district_list = []
        for district in districts:
            district_list.append(district.district_name)
        for entry in list1718[0][10:]:
            if entry in district_list:
                print(entry + ' is in the list at position ' + str(district_list.index(entry) + 1) + '.')
            else:
                print(entry + ' is not in the list.')
                break


def main():
    content_area_list()
    district_list()
