from django.db import models
from datetime import date , datetime
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import  PermissionsMixin , AbstractBaseUser , BaseUserManager
# from datetime import date , datetime


class family(models.Model):
    RELIGION_CHOICES = (
    ("Islam", "Islam"),
    ("Hindu", "Hindu"),
    ("Sikh", "Sikh"),
    ("Christian", "Christian"),
    )
    familyID = models.IntegerField()
    religion = models.CharField(max_length=20,choices=RELIGION_CHOICES,default="Islam")
    def __str__(self):
        return str(self.familyID)


class CustomMember(BaseUserManager):

    def create_superuser(self , email , user_name , password , **other_fields):
        other_fields.setdefault('is_staff' , True)
        other_fields.setdefault('is_superuser' , True)
        other_fields.setdefault('is_active' , True)

        if other_fields.get('is_staff') is not True:
            raise ValueError('SuperUser must be assigned to is_staff=True')
        if other_fields.get('is_superuser') is not True:
            raise ValueError('SuperUser must be assigned to is_superuser=True')

        return self.create_user(email , user_name , password , **other_fields)


    def create_user(self , email , user_name , password , **other_fields):
        other_fields.setdefault('is_active' , True)
        if not user_name:
            raise ValueError(_("Your must provide UserName"))
        email = self.normalize_email(email)
        user = self.model(email = email, user_name = user_name , **other_fields)
        user.set_password(password)
        user.save()
        return user



class member(AbstractBaseUser , PermissionsMixin):
    GENDER_CHOICES = (
    ("Male", "Male"),
    ("Female", "Female"),)
    MARITAL_CHOICES = (
    ("Unmarried", "Unmarried"),
    ("Married", "Married"),
    )
    SPORT_CHOICES = (
    ("Football", "Football"),
    ("Basketball", "Basketball"),
    ("Badminton", "Badminton"),
    ("Cycling", "Cycling"),
    ("Swimming", "Swimming"),
    ("Cricket", "Cricket"),
    ("TT", "TT"),
    ("Tennis", "Tennis"),
    ("Volley Ball", "Volley Ball"),
    ("Baseball", "Baseball"),
    ("Carrom", "Carrom")
    )
    BOOK_CHOICES = (
    ("Thriller", "Thriller"),
    ("Fantasy", "Fantasy"),
    ("Teen", "Teen"),
    ("Fiction", "Fiction"),
    ("Autobiography", "Autobiography"),
    ("Mystery", "Mystery"),
    ("History", "History"),
    ("Romance", "Romance"),
    ("Self Help", "Self Help"),
    ("Horror", "Horror"),
    ("Crime", "Crime")
    )
    MOVIE_CHOICES = (
    ("Action", "Action"),
    ("Thriller", "Thriller"),
    ("Drama", "Drama"),
    ("Romance", "Romance"),
    ("Autobiography", "Autobiography"),
    ("Comedy", "Comedy"),
    ("History", "History"),
    ("Romance", "Romance"),
    ("Crime", "Crime"),
    ("Horror", "Horror"),
    ("Animation", "Animation"),
    ("Adventure", "Adventure")
    )
    FID = models.ForeignKey(family , on_delete=models.DO_NOTHING , null=True)
    email = models.EmailField(max_length= 35)
    user_name = models.CharField(max_length= 20 , unique=True)
    firstName = models.CharField(max_length=20 ,  blank = True)
    middleName = models.CharField(max_length=20 , blank = True , null = True)
    lastName = models.CharField(max_length= 20 , blank = True)
    mobileNo = models.IntegerField(blank=True , null = True)
    birthDay = models.DateField(default=date.today)
    gender = models.CharField(max_length=9,choices=GENDER_CHOICES,default="Male")
    maritalStatus = models.CharField(max_length = 10,null=True , blank = True , choices=MARITAL_CHOICES)
    jobOrg = models.CharField(max_length= 20 , blank = True)
    address1 = models.TextField(_("Address line 1"),max_length=50 , blank = True)
    country = models.CharField("Country",max_length=15 , blank = True)
    city = models.CharField("City" , max_length=15 , blank=True)
    pinCode = models.IntegerField(blank=True)
    lat = models.DecimalField(max_digits=9 ,decimal_places = 6, blank=True , null = True)
    lng = models.DecimalField(max_digits=9 , decimal_places = 6, blank=True , null = True)
    mother = models.ForeignKey('self', on_delete=models.PROTECT , null=True , blank=True)
    father = models.ForeignKey('self', on_delete=models.PROTECT , null=True , blank=True , related_name='+')
    spouse = models.ForeignKey('self', on_delete=models.PROTECT , null=True , blank=True , related_name='++')
    kidsCount = models.IntegerField(blank=True , null = True , default=0)
    gender = models.CharField(max_length=9,choices=GENDER_CHOICES , default='Male')
    book = models.CharField(max_length=15,choices=BOOK_CHOICES,blank=True )
    sport = models.CharField(max_length=15,choices=SPORT_CHOICES,blank=True)
    movie = models.CharField(max_length=15,choices=MOVIE_CHOICES, blank=True)
    present = models.CharField(max_length=15,blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)


    objects = CustomMember()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = ['email' , 'city' , 'country' , 'firstName' , 'lastName' , 'gender' , 'pinCode']

    class Meta:
        ordering = ['-updated' , '-created']

    def __str__(self):
        return str(self.user_name)


class game(models.Model):
    name = models.CharField(max_length= 20 , unique=True)

    def __str__(self):
        return str(self.name)
    

class score(models.Model):
    game = models.ForeignKey(game , on_delete=models.CASCADE , null=True)
    player = models.ForeignKey(member , on_delete=models.CASCADE , null=True)
    score = models.DecimalField(max_digits=4, decimal_places=1)
    def __str__(self):
        return str(self.game.name+"_"+self.player.user_name)
    

class room(models.Model):
    name = models.CharField(max_length= 20 , unique=True)
    description = models.TextField(null = True , blank = True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']

    def __str__(self):
        return str(self.name)
    
    
class message(models.Model):
    room = models.ForeignKey(room , on_delete=models.CASCADE , null=True)
    sender = models.ForeignKey(member , on_delete=models.CASCADE , null=True)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated' , '-created']

    def __str__(self):
        return self.body[0:50]
    