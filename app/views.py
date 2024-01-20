from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import CafeResturant, Dish, Team, Reviews
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.
def index(request):
    try:
        cafe_reviews = Reviews.objects.filter(rating__gt=3)[:6]
        return render(request, 'index.html', {'active' : 'active', 'cafe_reviews' : cafe_reviews})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('index')

def cafe(request):
    try:
        time_str = datetime.now().strftime('%H:%M:%S')  
        time_format = '%H:%M:%S'
        time_datetime = datetime.strptime(time_str, time_format)
        time_now = time_datetime.time()

        cafes = CafeResturant.objects.filter(type_of='cafe')
        famous_cafes = CafeResturant.objects.all()[:3]
        return render(request, 'cafe.html', {'active2' : 'active', 'cafes' : cafes, 'famous_cafes' : famous_cafes, 'time_now' : time_now})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('index')

def cafe_detail(request, id):
    try:
        time_str = datetime.now().strftime('%H:%M:%S')  
        time_format = '%H:%M:%S'
        time_datetime = datetime.strptime(time_str, time_format)
        time_now = time_datetime.time()

        cafes = CafeResturant.objects.filter(type_of='cafe')
        caf = CafeResturant.objects.get(id=id)
        bf_dishes = Dish.objects.filter(cafe=caf, meal_name="breakfast")
        lunch_dishes = Dish.objects.filter(cafe=caf, meal_name="lunch")
        dinner_dishes = Dish.objects.filter(cafe=caf, meal_name="dinner")
        cafe_reviews = Reviews.objects.filter(cafe=caf).order_by('-rating')[:6]

        if request.method == "POST" : 
            data = request.POST
            cafe_id = data.get('feedback-cafe')
            rating = data.get('rating')
            comment = data.get('comment')
            review_cafe = CafeResturant.objects.get(id=cafe_id)
            if rating:
                Reviews.objects.create(cafe=review_cafe, rating=rating, comment=comment)
                messages.success(request,"Thank you for your feedback!")
                return redirect(f'/cafe_detail/{review_cafe.id}')
            else:
                messages.warning(request,"Please Rate Us!")
                return redirect(f'/cafe_detail/{review_cafe.id}')

        return render(request, 'cafe_detail.html', {'active2' : 'active', 'cafes' : cafes, 'caf' : caf, 'bf_dishes' : bf_dishes, 'lunch_dishes' : lunch_dishes, 'dinner_dishes' : dinner_dishes, 'time_now' : time_now, 'cafe_reviews' : cafe_reviews})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('/cafe/')

def restaurant(request):
    try:
        time_str = datetime.now().strftime('%H:%M:%S')  
        time_format = '%H:%M:%S'
        time_datetime = datetime.strptime(time_str, time_format)
        time_now = time_datetime.time()

        rest_ob = CafeResturant.objects.filter(type_of='resturant').order_by('-id')
        rest_famous = CafeResturant.objects.filter(type_of='resturant')[:3]
        return render(request, 'restaurant.html', {'active3' : 'active', 'rest_ob' : rest_ob, 'rest_famous' : rest_famous, 'time_now' : time_now})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('index')

def restaurant_detail(request,id):
    try:
        time_str = datetime.now().strftime('%H:%M:%S')  
        time_format = '%H:%M:%S'
        time_datetime = datetime.strptime(time_str, time_format)
        time_now = time_datetime.time()

        rests = CafeResturant.objects.filter(type_of='resturant')
        rest = CafeResturant.objects.get(id=id)
        bf_dishes = Dish.objects.filter(cafe=rest, meal_name="breakfast")
        lunch_dishes = Dish.objects.filter(cafe=rest, meal_name="lunch")
        dinner_dishes = Dish.objects.filter(cafe=rest, meal_name="dinner")
        cafe_reviews = Reviews.objects.filter(cafe=rest).order_by('-rating')[:6]

        if request.method == "POST" : 
            data = request.POST
            cafe_id = data.get('feedback-cafe')
            rating = data.get('rating')
            comment = data.get('comment')
            review_cafe = CafeResturant.objects.get(id=cafe_id)
            if rating:
                Reviews.objects.create(cafe=review_cafe, rating=rating, comment=comment)
                messages.success(request,"Thank you for your feedback!")
                return redirect(f'/restaurant_detail/{review_cafe.id}')
            else:
                messages.warning(request,"Please Rate Us!")
                return redirect(f'/restaurant_detail/{review_cafe.id}')
            
        return render(request, 'restaurant_detail.html', {'active3' : 'active', 'bf_dishes' : bf_dishes, 'lunch_dishes' : lunch_dishes, 'dinner_dishes' : dinner_dishes, 'rests' : rests, 'rest' : rest, 'time_now' : time_now, 'cafe_reviews' : cafe_reviews})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('/restaurant/')

def team(request):
    try:
        members = Team.objects.all()
        return render(request, 'team.html', {'active4' : 'active', 'members' : members})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('index')

def about(request):
    try:
        return render(request, 'about.html')
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('index')

def search_bar(request):
    try:
        if request.method == 'POST':
            search = request.POST.get('search')
            caf = CafeResturant.objects.filter(cafe_name=search).first()
            if caf:
                if caf.type_of == 'cafe':
                    return redirect(f'/cafe_detail/{caf.id}')
                elif caf.type_of == 'resturant':
                    return redirect(f'/restaurant_detail/{caf.id}')
            else:
                messages.error(request, 'Not found, please enter correct name!')
                return redirect('index')
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('index')


    