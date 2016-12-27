from django.shortcuts import render
from django.http import HttpResponse
from .models import User, Guide, Country, City
import elasticsearch
import json
import requests
from requests_aws4auth import AWS4Auth
from googleplaces import GooglePlaces, types, lang
import boto3
from .forms import LoginForm, CreateForm
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.shortcuts import redirect



#from .forms import UserForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

def adduser(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)

            #print (new_user.password)
            login( request, new_user)
            username = new_user.username
            country = Country.objects.all()
            context = {'country': country, "username": username}
            return render(request, 'places/home.html', context)
    else:
        form = CreateForm()

    return render(request, 'places/adduser.html', {'form': form})

def logins(request):
    #
    #print ("in the view")

    if request.session.has_key('username'):
        username = request.session['username']
        country = Country.objects.all()
        context = {'country': country, "username": username}
        #return redirect('home', {"username": username})
        return render(request, 'places/home.html', context)
    else:
        username = "not logged in"
        if request.method == "POST":
            # Get the posted form
            MyLoginForm = LoginForm(request.POST)
            #print ("post is working")
            #form = UserForm(request.POST)

            if MyLoginForm.is_valid():
                #print "form is valid"
                username = MyLoginForm.cleaned_data['username']
                password = MyLoginForm.cleaned_data['password']
                user = authenticate(username=username, password=password)

                if user is not None:
                    #print "trying to login"
                    login(request, user)
                    request.session['username'] = username
                    #return redirect('home', {"username": username})
                    country = Country.objects.all()
                    context = {'country':country,"username": username}
                    return render(request, 'places/home.html', context)
                else:
                    #raise MyLoginForm.ValidationError("Sorry, that login was invalid. Please try again.")
                    MyLoginForm = LoginForm()
                    return HttpResponse("Invalid, please go back..")

        return render(request, 'places/login.html', {"username": username})


def formView(request):
   if request.session.has_key('username'):
      username = request.session['username']
      country = Country.objects.all()
      context = {'country': country, "username": username}
      #return redirect('home', {"username": username})
      return render(request, 'places/home.html', context)
   else:
      return render(request, 'places/login.html', {})

def logout(request):
   try:
      del request.session['username']
   except:
      pass
   return render(request, 'places/logout.html')

#
# def home(request):
#     country = Country.objects.all()
#     context = {'country':country}#,"username": username }
#     return render(request,'places/home.html',context)

def city(request, country_id):
    city = City.objects.filter(country_id = country_id)
#    country = Country.objects.all()

    context = {'cities':city,'country_id':country_id}# 'country': country}
    return render(request,'places/citi.html',context)

def place(request, city_id):
    city = City.objects.get(id = city_id)
    awslink = 'ENTER AWS ELASTIC SEARCH LINK ALONG WITH QUERY HERE'
    full = awslink + city.city_name
    tweet = requests.get(full)
    results = json.loads(tweet.text)
    round1 = results["hits"]["hits"]
    list1 = round1[0]['_source']['attractionslist']
    #attract = list1.split(',')
    context = {'list1':list1}
    return render(request,'places/attractions.html',context)

def attraction(request):
    sel = request.POST.getlist('attr[]')
    rank = []
    dest = Guide.objects.all()
    for i in dest:
    #    print (i,i.guide_places.split(','))
        list2=[]
    #print (dest)
    # spot = dest.guide_places.split(',')
    # for i in dest:
        spot = i.guide_places.split(',')
        count = 0
        for j in sel:
            for k in spot:
                if (k == j):
                    list2.append(k)
                    count += 1
        temp = {'Name': i.guide_name, 'matches': count, 'places':list2}
        rank.append(temp)
    newlist = sorted(rank, key=lambda k: k['matches'], reverse=True)
    context = {'newlist':newlist}
    return render(request,'places/select.html',context)

def book(request):
    # con = request.POST.get('book')
    # tet = request.POST.get('phone_number', False)
    # sns = boto3.client(service_name="sns",
    #                    aws_access_key_id='',
    #                    aws_secret_access_key='',
    #                    region_name='us-west-2')  # , use_ssl=True)
    # ph = Guide.objects.get(guide_name=con)
    # phone = ph.guide_number
    # number = tet
    # # days = request.POST.get('days')
    # # print(days)
    # Message_guide = "This is message to confirm that you have been booked and the user number is " + str(
    #     number) + " Please contact the number soon for furthur information"
    # Message_user = "This is a message to confirm that you have booked " + con + " as your guide and you will be contacted by the guide soon."
    # sns.publish(PhoneNumber=number, Message=Message_user)
    # sns.publish(PhoneNumber=phone, Message=Message_guide)
    # return render(request, 'places/book.html', {})


    con = request.POST.get('book')
    tet = request.POST.get('phone_number',False)
    ph = Guide.objects.get(guide_name=con)
    phone = ph.guide_number
    guideinfo = Guide.objects.all()
    #rds = boto3.setup_default_session(region_name='us-east-2')

    session = boto3.Session(
        aws_access_key_id='',
        aws_secret_access_key='',
        region_name='us-east-2',
    )
    # sqs = boto3.client(service_name="sqs",
    #                    aws_access_key_id='',
    #                    aws_secret_access_key='',
    #                    region_name='us-east-2')
    sqs = boto3.resource('sqs')
    #sqs = boto3.resource('sqs', region_name='us-east-2')
    queue = sqs.get_queue_by_name(QueueName='sms_test')
    #queue = sqs.create_queue(QueueName='sms_test')
    numbersqs = []
    numbersqs.append(tet)
    for i in numbersqs:
        queue.send_message(MessageBody=i)

    sns = boto3.client(service_name="sns",
                       aws_access_key_id='',
                       aws_secret_access_key='',
                       region_name='us-west-2')  # , use_ssl=True)

    queuesns = sqs.get_queue_by_name(QueueName='sms_test')
    for x in queuesns.receive_messages(VisibilityTimeout=1, MaxNumberOfMessages=10, WaitTimeSeconds=5):
        number = x.body
        print number
        for guide_n in guideinfo:

            print guide_n.guide_name
            if con == guide_n.guide_name:
                message_guide = "This is message to confirm that you have been booked and the user number is " + str(number) + " Please contact the number soon for furthur information"
                message_user = "This is a message to confirm that you have booked " + con + " as your guide and you will be contacted by the guide soon."
                sns.publish(PhoneNumber=phone, Message=message_guide)
                sns.publish(PhoneNumber=number, Message=message_user)
                print "done"
            else:
                print "Guide not found"
        return render(request, 'places/book.html', {})




    # ph = Guide.objects.get(guide_name = con)
    # phone = ph.guide_number
    # number = tet
    # Message_guide = "This is message to confirm that you have been booked and the user number is " + str(number) + " Please contact the number soon for furthur information"
    # Message_user = "This is a message to confirm that you have booked " + con + " as your guide and you will be contacted by the guide soon."
    # sns.publish(PhoneNumber=number, Message=Message_user)
    # sns.publish(PhoneNumber=phone, Message=Message_guide)
    # return render(request,'places/book.html',{})


