from django.shortcuts import render, redirect
from .models import *
from ..login.models import User
from django.contrib.messages import error

def home(request):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    users_trips = user.trips.all()
    joined_trips = Trip.objects.filter(joiners=user)
    context = {
        'user': user,
        'users_trips': users_trips,
        'joined_trips': joined_trips,
        'trips': Trip.objects.exclude(joiners=request.session['user_id']).exclude(planner=request.session['user_id'])
    }
    return render(request, 'plans/index.html', context)

def add(request):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    return render(request, 'plans/add.html')

def create(request):
    result = Trip.objects.validate_trip(request.POST, request.session['user_id'])
    if type(result) == dict:
        for tag, message in result.iteritems():
            error(request, message, extra_tags=tag)
        return redirect('/travels/add')
    else:
        return redirect('/travels')

def trip(request, trip_id):
    if 'user_id' not in request.session.keys():
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    joiners = trip.joiners.all()
    context = {
        'trip': Trip.objects.get(id=trip_id),
        'joiners': joiners
    }
    return render(request, 'plans/trip.html', context)

def join(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    user = request.session['user_id']
    trip.joiners.add(user)
    trip.save()
    return redirect('/travels')
