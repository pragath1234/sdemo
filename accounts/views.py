from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from tablib import Dataset
from .models import Person
from django.contrib import messages
from .resources import PersonResource
from subprocess import run,PIPE
from django.core.files.storage import FileSystemStorage
import sys
#from .import script


def home(request):
    return render(request, 'index.html')

@login_required
def upload(request):
    if request.method == 'POST':
        person_resource = PersonResource()
        dataset = Dataset()
        new_person = request.FILES['myfile']
        print(new_person.size)

        if not new_person.name.endswith('xlsx'):
            messages.info(request,'worng format')
        else:
            messages.info(request,'File upload successful')
        imported_data = dataset.load(new_person.read(), format='xlsx')

        for data in imported_data:
            print(data[1])
            value = Person(
                data[0],
                data[1],
                data[2],
                data[3],
                data[4],
                data[5]
            )
            value.save()
    return render(request, 'mainframe.html')

def export(request):
    person_resource = PersonResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.xls, content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename="persons.xls"'
    return response

def export_csv(request):
    person_resource = PersonResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.csv, content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="persons.csv"'
    return response

def export_json(request):
    person_resource = PersonResource()
    dataset = person_resource.export()
    response = HttpResponse(dataset.json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="persons.json"'
    return response


def external(request):
    out = run([sys.executable,'D://Django_project//mainframe//script.py'],shell=False,stdout=PIPE)
    if not out:
        messages.info(request, 'unsuccessfull')
    else:
        messages.info(request, 'json to excel Executed successfully')
    return render(request, 'mainframe.html')
   # response = HttpResponse(content_type='application/excel')# response['Content-Disposition'] = 'attachment; filename="output.xlsx"'#   response = HttpResponse(request,{'data1':out.stdout})

def external_excel(request):
    outs = run([sys.executable,'D://Django_project//backup(mainframe)//mainframe//media//code.py'],shell=False,stdout=PIPE)
    ot = outs.stdout.decode()
    fs = FileSystemStorage()
    fs.save=ot
    if not ot:
        messages.info(request, 'unsuccessfull')
    else:
        messages.info(request, 'Excel to Nested json Executed successfully')
        print("data2")
    return render(request, 'mainframe.html',{'data2':ot})

def multiple_excel(request):
    outs = run([sys.executable,'D://Django_project//backup(mainframe)//mainframe//media//Multiple//single_shot.py'],shell=False,stdout=PIPE)
    ot = outs.stdout.decode()
    fs = FileSystemStorage()
    fs.save=ot
    if not ot:
        messages.info(request, 'unsuccessfull')
    else:
        messages.info(request, 'Multiple Nested json Executed successfully')
        print("data2")
    return render(request, 'mainframe.html',{'data2':ot})


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form':form})
