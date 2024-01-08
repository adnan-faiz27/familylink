from django.shortcuts import render, redirect , HttpResponse
from .forms import MemberForm , MemberForm1
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate , login , logout
from .forms import MemberForm
from .models import member , game , score , room , message
from datetime import datetime , date
import requests
import folium
from django.db.models import Q
from folium import plugins
import geopy.distance
from django.template.loader import get_template 
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
import pdfkit

from django import db

def reset(request):
    db.connections.close_all()
    return render(request, 'home/home.html')


def home(request):
   return render(request, 'home/home.html')


def faq(request):
   return render(request, 'home/faq.html')



def loginPage(request):

    if request.user.is_authenticated:
        return redirect('viewMember')

    if request.method =="POST":
        user_name = request.POST.get('user_name')
        password = request.POST.get('password')

        try:
            user = member.objects.get(user_name = user_name)
            print(user.user_name)
        except:
            messages.error(request, 'User doesnt exist')
        user = authenticate(request , user_name = user_name, password = password)

        if user != None:
            login(request , user)
            return redirect('viewMember')

        else:
  
            messages.error(request  ,"Username or Password incorrect" )


    context = {'page':"LOGIN"}
    return render (request , 'home/memberForm.html' , context)


def check(username):
    if member.objects.filter(user_name=username).exists():
        return True
    return False


def registerPage(request):
    form = MemberForm
    message = ""
    if request.method =="POST":
        form = MemberForm(request.POST ,request.FILES)
        if form.is_valid():
            user = form.save(commit = False)
            user.firstName = user.firstName.capitalize()
            user.lastName = user.lastName.capitalize()
            city = request.POST["city"].capitalize()
            pinCode = request.POST["pinCode"]
            location = maplocation(pinCode , city)
            if (len(location))!=0:
                lat = location[0]
                lng = location[1]
                user.lat = lat
                user.lng = lng
            user.birthDay = request.POST["date"]
            password = request.POST["password1"]
            user.set_password(password)
            user.save()
            login(request , user)
            return redirect('viewMember')
        else:
            username = request.POST["user_name"]
            if(check(username)):
                message = "UserName already exists"
                return render(request , 'home/memberForm.html' , {'form':form , 'page':"REGISTER" , 'message':message} )
            message = "Password not valid"

    return render(request , 'home/memberForm.html' , {'form':form , 'page':"REGISTER" , 'message':message} )
 

@login_required(login_url= 'login')
def logoutPage(request):
    logout(request)
    return redirect('home')



@login_required(login_url= 'login')
def edit_profile(request , pk):
    mem = member.objects.get(id = pk)
    form = MemberForm1(instance=mem)
    if(mem.gender == 'Male'):
        gen = 'Female'
    else:
        gen = 'Male'
    form.fields["mother"].queryset =member.objects.filter(FID=request.user.FID , birthDay__year__lte=request.user.birthDay.year - 15 , gender = "Female")
    form.fields["father"].queryset =member.objects.filter(FID=request.user.FID , birthDay__year__lte=request.user.birthDay.year - 18 , gender = "Male")
    form.fields["spouse"].queryset =member.objects.filter(FID=request.user.FID , gender = gen)
    if request.method=='POST':
        mem.email = request.POST.get('email')
        if(request.POST.get('middleName')):
            if(request.POST.get('middleName')!=None):
                if(request.POST.get('middleName')!=''):
                    mem.middleName = request.POST.get('middleName')
        mem.movie = request.POST.get('movie')
        mem.sport = request.POST.get('sport')
        mem.book = request.POST.get('book')
        mem.present = request.POST.get('present')
        if(request.POST.get('mobileNo')):
            mem.mobileNo = request.POST.get('mobileNo')
        else:
            mem.mobileNo =None
        mem.address1 = request.POST.get('address1').capitalize()
        mem.city = request.POST.get('city').capitalize()
        if(len(request.POST.get('pinCode'))!=0):
            mem.pinCode = int(request.POST.get('pinCode'))
            location = maplocation(mem.pinCode , mem.city)
            if (len(location))!=0:
                lat = location[0]
                lng = location[1]
                mem.lat = lat
                mem.lng = lng
        mem.maritalStatus = request.POST.get('maritalStatus')
        mem.jobOrg = request.POST.get('jobOrg').capitalize()
        m = request.POST.get('mother')
        f = request.POST.get('father')
        s = request.POST.get('spouse')
        
        if(m!=''):
            mother = member.objects.get(id = m )
            mem.mother = mother
        else:
            mem.mother =None
        if(f!=''):
            father = member.objects.get(id = f )
            mem.father = father
        else:
            mem.father = None
        if(s!=''):
            spouse = member.objects.get(id = s )
            mem.spouse = spouse
        else:
            mem.spouse = None
        mem.save()
        return redirect('viewProfile' , pk = request.user.id) 
    context = {'member' : mem , 'form':form}
    return render(request , 'home/edit.html' , context) 



@login_required(login_url= 'login')
def map(request):
    members = member.objects.all()
    members = members.filter(FID=request.user.FID)
    user_lat = request.user.lat
    user_lng = request.user.lng
    m = folium.Map(location=[request.user.lat , request.user.lng] , zoom_start=5)

    if request.method=='POST':
        user = request.POST.get('user')
        mem = member.objects.get(id = user)
        kw = {"color": "green"}
        icon = folium.Icon(**kw)
        coordinates = (request.user.lat , request.user.lng)
        folium.Marker(coordinates,icon=icon , tooltip="You").add_to(m)
        coordinates1 = (mem.lat , mem.lng)
        folium.Marker(coordinates1 , tooltip=mem.user_name).add_to(m)
        distance = geopy.distance.geodesic(coordinates, coordinates1).km
        distance  = round(distance, 2)
        line = folium.PolyLine([coordinates1 , coordinates],color='grey',dash_array='7')
        attr = {'fill': 'black', 'font-weight': 'bold', 'font-size': '20'}
        distance_textpath = plugins.PolyLineTextPath(line, str(distance)+"  Km", center=True, offset=-2,attributes=attr)
        line.add_to(m)
        distance_textpath.add_to(m)
        context = {'map':m._repr_html_() , 'members':members , 'distance':distance , "selected":mem , "count":2}
        return render(request , 'home/map.html' , context)
    
    count = 0
    for mem in members:
        count = count+1
        coordinates = (mem.lat , mem.lng)
        if(coordinates[0]==user_lat and coordinates[1]==user_lng):
            kw = {"color": "green"}
            icon = folium.Icon(**kw)
            folium.Marker(coordinates,icon=icon,tooltip="You").add_to(m)
        else:
            folium.Marker(coordinates , tooltip=mem.user_name).add_to(m)

    context = {'map':m._repr_html_() , 'members':members ,"selected":None , "count":count}
    return render(request , 'home/map.html' , context)




@login_required(login_url= 'login')
def viewProfile(request , pk):
    mem = member.objects.get(id = pk)
    if(mem.mother==None and mem.father==None):
        siblings=None
    elif(mem.father!=None and mem.mother==None):
        siblings = member.objects.all().filter(mother = mem.mother)
        if(len(siblings)==0):
            siblings=None
    else:
        siblings = member.objects.all().filter(father = mem.father)
        if(len(siblings)==0):
            siblings=None
        
            
    if(mem.gender == 'Female'):
        kids = member.objects.all().filter(mother = mem)
    else:
        kids = member.objects.all().filter(father = mem)
    if(len(kids)==0):
        kids = None
    return render(request, 'home/profile.html' , {'member': mem , 'kids':kids , 'siblings':siblings})
    

@login_required(login_url= 'login')
def pdf(request , pk):
    mem = member.objects.get(id = pk)
    if(date.today().day != mem.birthDay.day or date.today().month != mem.birthDay.month):
        return redirect('birthdayList')
    
    age = date.today().year - mem.birthDay.year
    context = {
        'member':mem,
        'age':age,
    }
    options = {
        'page-size': 'A6',
        'margin-top': '0.3in',
        'margin-right': '0.75in',
        'margin-bottom': '0.3in',
        'margin-left': '0.75in',
    }
    PATH = 'C:\Program Files\wkhtmltopdf\\bin\wkhtmltopdf.exe'
    config = pdfkit.configuration(wkhtmltopdf=PATH)
    template = get_template("email/emailbirthday.html")
    html = template.render(context) 
    pdfkit.from_string(html, 'birthday.pdf' , options=options)
    mail1 = EmailMultiAlternatives(
        "Happy Birthday",
        "Happy birthday",
        "settings.EMAIL_HOST_USER",
        [mem.email],
    )
    mail1.attach_file('birthday.pdf')
    mail1.send(fail_silently=False)
    return render(request, 'birthday/birthday.html',{'selectedmonth':date.today().month , 'day':date.today().day , 'month': date.today().month , 'message':"Your wish is sent to your mail"})




def feedbackmail(email , member , message):
    context = {
        'email':email,
        'user_name': member.user_name,
        'firstName': member.firstName,
        'lastName': member.lastName,
        'message':message,
    }
    html_content = render_to_string("email/email_template.html" , context) 
    message1 = strip_tags(html_content)

    mail = EmailMultiAlternatives(
        "FAMILY LINK MESSAGE",
        message1,
        "settings.EMAIL_HOST_USER",
        ['adnanfaiz57@gmail.com'],
    )
    mail.send(fail_silently=False)


@login_required(login_url= 'login')
def viewMember(request):
    if request.method == 'POST':
        m = request.POST.get('member')
        message = request.POST.get('message')
        feedbackmail(m , request.user , message)
    q = request.GET.get('search') if request.GET.get('search') != None else ''
    members = member.objects.filter(
        Q(firstName__startswith = q)|
        Q(lastName__startswith = q) |
        Q(user_name__startswith = q)
        )
    members = members.filter(FID=request.user.FID)
    members=sorted(members, key=lambda x: x.birthDay)
    return render(request, 'home/member.html',{'members': members,'obj':'leaders'})


@login_required(login_url= 'login')
def contact(request):
    members = []
    q = request.GET.get('search') if request.GET.get('search') != None else ''
    mem = member.objects.filter(
        Q(firstName__startswith = q)|
        Q(lastName__startswith = q) |
        Q(user_name__startswith = q)
        )
    mem.filter(FID = request.user.FID)
    for m in mem:
        if(m.mobileNo != None):
            members.append(m)
    return render(request, 'home/contact.html',{'members': members})


@login_required(login_url= 'login')
def leaders(request):
    members = member.objects.all()
    members = members.filter(FID = request.user.FID)
    year = str(int(datetime.now().strftime("%Y"))-60)
    members = members.filter(birthDay__year__lte=year)
    return render(request, 'home/member.html',{'members': members,'obj':'members' })


@login_required(login_url= 'login')
def seeadmins(request):
    members = member.objects.all()
    members = members.filter(is_staff = True)
    return render(request , "home/member.html" , {'members': members,'obj':'admins' })


def createTuple(members , years):
    obj = list(zip(members , years))
    return obj



@login_required(login_url= 'login')
def birthdayList(request):
    months = [
        ("January",1),
        ("February",2),
        ("March",3),
        ("April",4), 
        ("May",5),
        ("June",6),
        ("July",7),
        ("August",8),
        ("September",9),
        ("October",10),
        ("November",11),
        ("December",12)
    ]
    if request.method=='POST':
        selectedmonth = request.POST.get('month')
        for x in months:
            if x[0] == selectedmonth:
                selectedmonth = x[1]
        
        members = member.objects.filter(birthDay__month = selectedmonth , FID = request.user.FID)
        members=sorted(members, key=lambda x: x.birthDay)
        
        years = []
        dates = []
        month = []
            
        for mem in members:
            years.append(mem.birthDay.year)
            dates.append(mem.birthDay.day)
            month.append(mem.birthDay.month)
        
        size = len(years)


        for x in range(size):
            years[x] = date.today().year - years[x]
            if years[x] == 0:
                years[x] = 0
            elif month[x]>date.today().month:
                years[x]=years[x]-1
            elif month[x]==date.today().month and dates[x]>date.today().day:
                years[x]=years[x]-1
        obj = createTuple(members , years)
        return render(request, 'birthday/birthday.html',{'members': members ,"months":months,'obj':obj , 'selectedmonth':selectedmonth , 'day':date.today().day , 'month': date.today().month , 'message':""})
    
    selectedmonth = date.today().month
    members = member.objects.filter(birthDay__month = selectedmonth , FID = request.user.FID)
    members=sorted(members, key=lambda x: x.birthDay)

    years = []
    dates = []
    month = []
        
    for mem in members:
        years.append(mem.birthDay.year)
        dates.append(mem.birthDay.day)
        month.append(mem.birthDay.month)
    
    size = len(years)


    for x in range(size):
        years[x] = date.today().year - years[x]
        if years[x] == 0:
            years[x] = 0
        elif month[x]>date.today().month:
            years[x]=years[x]-1
        elif month[x]==date.today().month and dates[x]>date.today().day:
            years[x]=years[x]-1
    obj = createTuple(members , years)


    return render(request, 'birthday/birthday.html',{'members': members, "months":months,'obj':obj , 'selectedmonth':selectedmonth , 'day':date.today().day , 'month': date.today().month , 'message':""})



def maplocation(pinCode , city):
    location = []
    url = "https://trueway-geocoding.p.rapidapi.com/Geocode"
    querystring = {"address":str(pinCode),"language":"en"}
    headers = {
        "X-RapidAPI-Key": "a1bceba3b9msh3accda498be30adp1867fejsn9fc9632ba986",
        "X-RapidAPI-Host": "trueway-geocoding.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    obj = response.json()
    if len(obj['results'])==0:
        url = "https://trueway-geocoding.p.rapidapi.com/Geocode"
        querystring = {"address":city,"language":"en"}
        headers = {
            "X-RapidAPI-Key": "a1bceba3b9msh3accda498be30adp1867fejsn9fc9632ba986",
            "X-RapidAPI-Host": "trueway-geocoding.p.rapidapi.com"
        }
        response = requests.get(url, headers=headers, params=querystring)
        obj1 = response.json()
        if len(obj1['results'])==0:
            return location
        else:
            location.append(obj1['results'][0]['location']['lat'])
            location.append(obj1['results'][0]['location']['lng'])
            return location
    else:
        location.append(obj['results'][0]['location']['lat'])
        location.append(obj['results'][0]['location']['lng'])
        return location
    


@login_required(login_url= 'login')
def interest(request):

    book_choice = [
        '---',
        'Thriller',
        'Fantasy',
        'Teen',
        'Fiction',
        'Autobiography',
        'Mystery',
        'History',
        'Romance',
        'Self Help',
        'Horror',
        'Crime'
    ]

    movie_choice = [
        '---',
        'Thriller',
        'Action',
        'Drama',
        'Fiction',
        'Autobiography',
        'Mystery',
        'History',
        'Romance',
        'Comedy',
        'Horror',
        'Crime',
        'Animation',
        'Adventure'
    ]

    sport_choice = [
        '---',
        'Football',
        'Basketball',
        'Badminton',
        'Cycling',
        'Swimming',
        'Cricket',
        'TT',
        'Tennis',
        'Romance',
        'Volley Ball',
        'Baseball',
        'Carrom'
    ]
    
    if request.method=='POST':
        movie_selected = request.POST.get('movie')
        sport_selected = request.POST.get('sport')
        book_selected = request.POST.get('book')
        if(movie_selected == '---' and book_selected == '---' and sport_selected =='---'):
            return render(request , 'interest/interest.html' , {'movie_selected':movie_selected , 'sport_selected':sport_selected ,'book_selected':book_selected , 'movie_choice':movie_choice , 'sport_choice':sport_choice  , 'book_choice':book_choice })
        
        if((movie_selected == '---' and book_selected == '---' and sport_selected !='---') | (movie_selected != '---' and book_selected == '---' and sport_selected =='---')| (movie_selected == '---' and book_selected != '---' and sport_selected =='---')):
            members = member.objects.filter(
                Q(movie = movie_selected) |
                Q(sport = sport_selected) |
                Q(book = book_selected)
                )
            if(movie_selected!='---'):
                obj = 'm'
            if(sport_selected!='---'):
                obj = 's'
            if(book_selected!='---'):
                obj = 'b'

        
        if((movie_selected != '---' and book_selected == '---' and sport_selected !='---') | (movie_selected != '---' and book_selected != '---' and sport_selected =='---')| (movie_selected == '---' and book_selected != '---' and sport_selected !='---')):
            
            if(movie_selected=='---'):
                obj = 'sb'
                members = member.objects.filter(
                Q(sport = sport_selected) &
                Q(book = book_selected)
                )
            if(sport_selected=='---'):
                obj = 'bm'
                members = member.objects.filter(
                Q(movie = movie_selected) &
                Q(book = book_selected)
                )
            if(book_selected=='---'):
                obj = 'sm'
                members = member.objects.filter(
                Q(movie = movie_selected) &
                Q(sport = sport_selected)
                )
               
        if(movie_selected != '---' and book_selected != '---' and sport_selected != '---'):
            obj = 'smb'

            members = member.objects.filter(
                Q(movie = movie_selected) &
                Q(sport = sport_selected) &
                Q(book = book_selected) 
            )
        members = members.filter(FID = request.user.FID)
        return render(request , 'interest/interest.html' , {'obj':obj , 'members':members , 'movie_selected':movie_selected , 'sport_selected':sport_selected ,'book_selected':book_selected , 'movie_choice':movie_choice , 'sport_choice':sport_choice  , 'book_choice':book_choice })
    
    return render(request , 'interest/interest.html' , {'movie_choice':movie_choice , 'sport_choice':sport_choice  , 'book_choice':book_choice })
    

@login_required(login_url= 'login')
def islam(request , pk):
    if(pk=='99names'):
        return render(request , "interest/islam/islam.html")
    if(pk=='para'):
        return render(request , "interest/islam/para.html")
    if(pk=='stories'):
        return render(request , "interest/islam/stories.html")
    if(pk=='hadiths'):
        return render(request , "interest/islam/hadiths.html")


@login_required(login_url= 'login')
def para(request , pk):
    
    if (pk == '1_7'):
        print("hello")
        return render(request , 'interest/islam/para/para1_7.html' , {'obj':'Para 1-7'})
    if pk == '7_10':
        return render(request , "interest/islam/para/para7_10.html", {'obj':'Para 7-10'})
    if pk == '10_13':
        return render(request , "interest/islam/para/para10_13.html", {'obj':'Para 10-13'})
    if pk == '14_16':
        return render(request , "interest/islam/para/para14_16.html", {'obj':'Para 14-16'})
    if pk == '17_18':
        return render(request , "interest/islam/para/para17_18.html", {'obj':'Para 17-18'})
    if pk == '19_21':
        return render(request , "interest/islam/para/para19_21.html", {'obj':'Para 19-21'})
    if pk == '21_23':
        return render(request , "interest/islam/para/para21_23.html", {'obj':'Para 21-23'})
    if pk == '24_25':
        return render(request , "interest/islam/para/para24_25.html", {'obj':'Para 24-25'})
    if pk == '26':
        return render(request , "interest/islam/para/para26.html", {'obj':'Para 26'})
    if pk == '27':
        return render(request , "interest/islam/para/para27.html", {'obj':'Para 27'})
    if pk == '28':
        return render(request , "interest/islam/para/para28.html", {'obj':'Para 28'})
    if pk == '29':
        return render(request , "interest/islam/para/para29.html", {'obj':'Para 29'})
    if pk == '30':
        return render(request , "interest/islam/para/para30.html", {'obj':'Para 30'})



@login_required(login_url= 'login')
def story(request , pk):
    obj = ""
    if(pk=='adam'):   
        obj = "Adam (AS)"
    if(pk=='nuh'):
        obj = "Nuh (AS)"
    if(pk=='ibrahim'):
        obj = "Ibrahim (AS)"
    if(pk=='yasa'):
        obj = "Yasa (AS)"
    if(pk=='idris'):
        obj = "Idris (AS)"
    if(pk=='musa'):
        obj = "Musa (AS)" 
    if(pk=='lut'):
        obj = "Lut (AS)"
    if(pk=='dhul'):
        obj = "Dhul (AS)"
    if(pk=='isa'):
        obj = "Isa (AS)"
    if(pk=='ismael'):
        obj = "Ismail (AS)"
    if(pk=='ayyub'):
        obj = "Ayyub (AS)"
    if(pk=='yusuf'):
        obj = "Yusuf (AS)"
    if(pk=='yunus'):
        obj = "Yunus (AS)"
    if(pk=='saleh'):
        obj = "Saleh (AS)"
    if(pk=='suleman'):
        obj = "Sulaiman (AS)"
    if(pk=='muhammad'):
        obj = "Muhammad SAW"
    
    return render(request , "interest/islam/story.html" , {'obj':obj})


@login_required(login_url= 'login')
def gamehouse(request):
    games = game.objects.all()
    winner = []
    for g in games:
        p = score.objects.all()
        p = p.filter(game  = g)
        p = sorted(p , key=lambda x: x.score , reverse=True)
        if(p):
            winner.append([g , p[0].player])
        else:
            winner.append([g ,""])
   
    return render(request , 'gamehouse/gamehouse.html' , {'winner':winner})


@login_required(login_url= 'login')
def leaderboard(request , pk):
    scores = []
    g = game.objects.get(name = pk)
    allscores = score.objects.all()
    allscores = allscores.filter(game = g)
    for s in allscores:
        if(s.player.FID == request.user.FID):
            scores.append(s)
    scores = sorted(scores, key=lambda x: x.score , reverse=True)
    return render(request , 'gamehouse/leaderboard.html' , {'pk':pk , 'scores':scores})


@login_required(login_url= 'login')
def playgame(request , pk):
    if request.method == 'GET':
        if(request.GET.get('count')!=None):
            result = request.GET.get('count')
            g = game.objects.get(name = pk)
            m = member.objects.get(id = request.user.id)
            try:
                score.objects.get(game = g , player = m)
                s = score.objects.get(game = g , player = m)
                if s.score<float(result):
                    s.score = result
                    s.save()
            except:
                score.objects.create(
                    player = request.user,
                    game = g,
                    score = result
                )
    if(pk=='memory'):
        return render(request ,'gamehouse/memory.html' , {'name':pk})
    if(pk=='hangman'):
        return render(request ,'gamehouse/hangman.html' , {'name':pk})
    if(pk=='guess'):
        return render(request ,'gamehouse/guess.html' , {'name':pk})
    if(pk=='typing'):
        return render(request ,'gamehouse/typing.html' , {'name':pk})



@login_required(login_url= 'login')
def Room(request , pk):
    Room = room.objects.get(id = pk)
    room_messages = message.objects.all()
    room_messages = room_messages.filter(room = Room.id)
    request.session['forward'] = True
    if request.method == 'POST':
        print("hello")
        m = message.objects.create(
            sender = request.user,
            room = Room,
            body = request.POST.get('body')
        )
        return redirect('room' , pk = Room.id)
    context = {'room' : Room , 'room_messages': room_messages}
    return render(request , 'interest/room/room.html' , context)


@login_required(login_url= 'login')
def delete_message(request , pk):
    
    m = message.objects.get(id = pk)
    if request.method =="POST":
        m.delete()
        return redirect('room' , pk = m.room.id)
    return render(request , 'interest/room/delete_message.html' , {'message':m})