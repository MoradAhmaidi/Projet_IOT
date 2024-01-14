import telepot
from django.db.models import Max, Min
from twilio.rest import Client
from django.contrib import messages
from django.shortcuts import render,redirect
from .models import Dht,TemplateMessage,Norms
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User,Group,auth
from django.contrib.auth.decorators import login_required

# Authentification
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request,username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.error(request,'invalid credentials')
            return redirect('login')
    else:
        return render(request,'auth/login.html')

#logout
def logout(request):
    auth.logout(request)
    return redirect('login')

#index
@login_required()
def home(request):
    data = Dht.objects.all()
    max_temp = Dht.objects.aggregate(Max('temp'))
    min_temp = Dht.objects.aggregate(Min('temp'))
    max_hum = Dht.objects.aggregate(Max('hum'))
    min_hum = Dht.objects.aggregate(Min('hum'))
    lastData = Dht.objects.all().last()
    template = {'Température maximale': Norms.MAX_TEMP, 'Température miminale': Norms.MIN_TEMP,
                'Humidité maximale': Norms.MAX_HUM, 'Humidité miminale': Norms.MIN_HUM}
    context = {'data': data, 'lastData': lastData,'template': template,"maxTemp":max_temp['temp__max'],"minTemp":min_temp['temp__min'],"maxHum":max_hum['hum__max'],"minHum":min_hum['hum__min']}
    return render(request, 'index.html', context)

@login_required()
def userlist(request):
    users = User.objects.all()
    context = {'users': users}
    return render(request,"user/user_list.html", context)
@login_required()
def useradd(request):
    if request.method == 'POST':

        email = request.POST['email']
        password = request.POST['password']
        username = request.POST['username']
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        passwordConfirm = request.POST['passwordConfirm']
        groupname = request.POST['group']

        if User.objects.filter(email=email).exists():
            messages.info(request, 'email taken')
            return redirect('useradd')
        elif User.objects.filter(username=username, password=password).exists():
            messages.info(request, 'invalid username or password')
            return redirect('useradd')
        elif passwordConfirm != password:
            messages.info(request, 'invalid password')
            return redirect('useradd')

        user = User.objects.create_user(first_name=firstname, last_name=lastname, username=username, email=email,
                                        password=password)
        user.save();

        user = User.objects.get(username=username)
        group = Group.objects.get(name=groupname)

        user.groups.add(group)

        return redirect('userlist')
    else:
        groupes = Group.objects.all()
        context = {'groupes': groupes}
        return render(request, 'user/user_add.html', context)

@login_required()
def userupdate(request,id):

    user = get_object_or_404(User,id=id)

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        lastname = request.POST['lastname']
        firstname = request.POST['firstname']
        groupname = request.POST['group']

        if User.objects.filter(email=email).exclude(id=user.id).exists():
            messages.info(request, 'Email already taken')
            return redirect('userupdate',id=id)
        elif User.objects.filter(username=username).exclude(pk=user.pk).exists():
            messages.info(request, 'Username already taken')
            return redirect('userupdate', id=id)

        user.email = email
        user.username = username
        user.first_name = firstname
        user.last_name = lastname
        user.save()

        group = Group.objects.get(name=groupname)
        user.groups.set([group])

        return redirect('userlist')
    else:
        groupes = Group.objects.all()
        context = {'user': user, 'groupes': groupes}
        return render(request, 'user/user_update.html', context)
@login_required()
def userdetele(request,id):
    user = User.objects.filter(id=id)
    user.delete()
    messages.success(request, 'User deleted successfully')
    return redirect('userlist')
@login_required()
def messagelist(request):
    template = {'EMAIL':TemplateMessage.EMAIL, 'TELEGRAM':TemplateMessage.TELEGRAM, 'WHATSAPP':TemplateMessage.WHATSAPP}
    context ={'template': template}
    return render(request,"parametre/message_list.html", context)
@login_required()
def messageupdate(request, name):
    if name == "EMAIL":
        context = {'key':name,'template': TemplateMessage.EMAIL}
    if name == "TELEGRAM":
        context = {'key':name,'template': TemplateMessage.TELEGRAM}
    if name == "WHATSAPP":
        context = {'key':name,'template': TemplateMessage.WHATSAPP}

    if request.method == 'POST':

        message = request.POST['message']

        if name == "EMAIL":
            TemplateMessage.EMAIL = message
        if name == "TELEGRAM":
            TemplateMessage.TELEGRAM = message
        if name == "WHATSAPP":
            TemplateMessage.WHATSAPP = message

        return redirect('messagelist')

    return render(request,"parametre/message_update.html", context)
@login_required()
def normsupdate(request,name):
    if name == "Température maximale":
        context = {'key': name, 'template': Norms.MAX_TEMP}
    if name == "Température miminale":
        context = {'key': name, 'template': Norms.MIN_TEMP}
    if name == "Humidité maximale":
        context = {'key': name, 'template': Norms.MAX_HUM}
    if name == "Humidité miminale":
            context = {'key': name, 'template': Norms.MIN_HUM}

    if request.method == 'POST':

        newvalue = request.POST['value']

        if name == "Température maximale":
            Norms.MAX_TEMP = newvalue
        if name == "Température miminale":
            Norms.MIN_TEMP = newvalue
        if name == "Humidité maximale":
            Norms.MAX_HUM = newvalue
        if name == "Humidité miminale":
            Norms.MIN_HUM = newvalue

        return redirect('home')

    return render(request, "parametre/norms_update.html", context)

def sendtele(message):
    token = '6436101701:AAHdYFMJXV4uFdDYoTqq1jsEhgSV1AogDMI'
    rece_id = 1092321991
    bot = telepot.Bot(token)
    bot.sendMessage(rece_id, message)

def sendwhatsap(body):
    account_sid = 'AC3da34e6234a1cbd00d6faaa4aa97bbd7'
    auth_token = '9146f244fc4c4c9fab4286a2a404037a'
    client = Client(account_sid, auth_token)
    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=body,
        to='whatsapp:+212615503124'
    )