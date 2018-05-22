from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import User, Trip
import bcrypt
import datetime

def main(request):
    return render(request, "belt/index.html")


def register(request):
    errors = User.objects.validate_register(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        # bcrypt
        hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(name=request.POST['name'], username=request.POST['username'], password=hash)
        user.save()
        messages.success(request, "Account successfully registered")
        return redirect('/main')


def signin(request):
    errors = User.objects.validate_signin(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/main')
    else:
        user = User.objects.get(username=request.POST['username'])
        request.session['username_signed_in'] = request.POST['username']
        return redirect('/travels')

def travels(request):
    user = User.objects.get(username=request.session['username_signed_in'])
    trips = Trip.objects.filter(planned_by=user)|Trip.objects.filter(attended_by=user)
    context = {
        'user': user,
        'trips': trips.order_by("date_from"),
        'other_trips': Trip.objects.exclude(planned_by=user).exclude(attended_by=user).order_by("date_from"),
    }
    return render(request, 'belt/travels.html', context)

def addTravel(request):
    return render(request, 'belt/addTravel.html')

def addTravel_process(request):
    if not request.POST['destination'] or not request.POST['description'] or not request.POST['date_from'] or not request.POST['date_to']:
        messages.error(request, "All fields are required.")
        return redirect('/travels/add')
    today = datetime.datetime.now()
    date_from = datetime.datetime.strptime(request.POST['date_from'], '%Y-%m-%d')
    date_to = datetime.datetime.strptime(request.POST['date_to'], '%Y-%m-%d')
    if date_to < date_from:
        messages.error(request, "Travel Date To must be on or after Travel Date From. Time machine hasn't been invented. We apologize for the inconvenience.")
        return redirect('/travels/add')
    if date_from < today:
        messages.error(request, "Travel date must be today or in the future. Time machine hasn't been invented. We apologize for the inconvenience.")
        return redirect('/travels/add')

    user = User.objects.get(username=request.session['username_signed_in'])
    Trip.objects.create(destination=request.POST['destination'], description=request.POST['description'], date_from=request.POST['date_from'], date_to=request.POST['date_to'], planned_by=user).save()
    return redirect('/travels')


def destination(request, id):
    context = {
        'trip': Trip.objects.get(id=id),
        'attended_by': User.objects.filter(trips_attending=Trip.objects.get(id=id)),
    }
    return render(request, 'belt/destination.html', context)

def join(request, id):
    user = User.objects.get(username=request.session['username_signed_in'])
    trip = Trip.objects.get(id=id)
    trip.attended_by.add(user)
    trip.save()
    return redirect('/travels')

def delete(request, id):
    Trip.objects.get(id=id).delete()
    messages.error(request, 'Trip deleted')
    return redirect('/travels')

def logout(request):
    request.session.clear()
    messages.error(request, "You have successfully logged out.")
    return redirect('/main')
