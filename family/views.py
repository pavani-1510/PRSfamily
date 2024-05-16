from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from .models import User
from .forms import LoginForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from django.core.exceptions import ValidationError

def index(request):
    if request.user.is_authenticated:
        return redirect('user')
    else:
        return redirect('login')

def login(request):
    message = ''
    if request.method == 'POST' and 'username' in request.POST and 'password' in request.POST:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            request.session['loggedin'] = True
            request.session['userid'] = user.id
            request.session['name'] = user.username
            message = 'Logged in successfully!'
            return redirect('user')
        else:
            message = 'Please enter correct username/password!'
    return render(request, 'login.html', {'message': message})

def logout(request):
    request.session.flush()
    return redirect('login')

@login_required
def user(request):
    if 'name' in request.session:
        name = request.session['name']
        message = 'Welcome back!'
    else:
        name = None
        message = 'Welcome!'

    return render(request, 'user.html', {'name': name, 'message': message})

# views.py

from django.shortcuts import render
from .models import FamilyMember

def familytree(request):
    # Retrieve all family members
    all_members = FamilyMember.objects.all()

    return render(request, 'family-tree.html', {'family_members': all_members})

def events(request):
    return render(request, 'events.html')

from django.shortcuts import render, redirect
from .models import Event
from .forms import EventForm

def event_list(request):
    events = Event.objects.all()
    return render(request, 'event_list.html', {'events': events})



from django.shortcuts import render, get_object_or_404
from .models import Event

def event_detail(request, event_id):
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})


from twilio.rest import Client
from django.conf import settings

def send_whatsapp_message(body, to):
    # Your Twilio Account SID and Auth Token
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    # Send the WhatsApp message
    message = client.messages.create(
        from_='whatsapp:+14155238886',  # Twilio's WhatsApp Sandbox number
        body=body,
        to='whatsapp:' + to
    )

    return message.sid

def add_event(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save()

            # Get the list of contacts
            contacts = ['contact1', 'contact2', ...]  # Replace with your contact list

            # Send WhatsApp message to each contact
            for contact in contacts:
                send_whatsapp_message(f'New event added: {event.title}', contact)

            return redirect('event_list')
    else:
        form = EventForm()
    return render(request, 'add_event.html', {'form': form})

