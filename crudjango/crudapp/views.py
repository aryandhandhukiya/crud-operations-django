from django.shortcuts import render, redirect, get_object_or_404
from .models import Persons
from .forms import PersonForm

# Create
def create_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm()
    return render(request, 'persons/person_form.html', {'form': form})

# Read
def person_list(request):
    persons = Persons.objects.all()
    return render(request, 'persons/person_list.html', {'persons': persons})

# Update
def update_person(request, pk):
    person = get_object_or_404(Persons, pk=pk)
    if request.method == 'POST':
        form = PersonForm(request.POST, instance=person)
        if form.is_valid():
            form.save()
            return redirect('person_list')
    else:
        form = PersonForm(instance=person)
    return render(request, 'persons/person_form.html', {'form': form})

# Delete
def delete_person(request, pk):
    person = get_object_or_404(Persons, pk=pk)
    if request.method == 'POST':
        person.delete()
        return redirect('person_list')
    return render(request, 'persons/person_confirm_delete.html', {'person': person})
