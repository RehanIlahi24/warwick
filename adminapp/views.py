from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import User
from django.contrib.auth.hashers import make_password
import uuid 
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Reviews, Team, CafeResturant, Dish

def login_page(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    
    if request.method == 'POST':
        data = request.POST
        email = data['email']
        password = data['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            auth_login(request, user)
            messages.success(request,"Successfully Login!")
            return redirect("dashboard")
        else:
            messages.warning(request,"Incorrect email or password!")
        
    return render(request,'adminapp/login.html')

@login_required
def change_password(request):
    try:
        if request.method == "POST":
            p1 = request.POST.get('password1')
            p2 = request.POST.get('password2')
            user = User.objects.get(username=request.user.username)
            if p1 == p2:
                user.set_password(p1) 
                user.save()   
                messages.success(request,"Successfully Change Password!")
                return redirect('dashboard')
            else:
                messages.warning(request,"Password does not match!")
        return render(request, 'adminapp/change_password.html')
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def logout_page(request):
    try:
        logout(request)
        messages.success(request, 'Logout Successfully!')
        return redirect('login')
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def dashboard(request):
    try:
        return render(request, 'adminapp/dashboard.html', {'active' : 'active'})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def user_view(request):
    try:
        if not request.user.is_superuser:
            return redirect('dashboard')
        users = User.objects.all()
        users = pagination_custom(request,users)
        if request.method == "POST":
            data = request.POST
            type = data.get('type')
            if type == 'delete':
                uid = data.get('user_id')
                user = User.objects.get(uid=uid)
                user.delete()
                messages.success(request, 'Successfully Delete User!')
                return redirect('user_view')
            if type == 'new-user':
                email = data.get('email')
                username = data.get('username')
                first_name = data.get('first_name')
                last_name = data.get('last_name')
                password = data.get('password')
                password2 = data.get('password2')
                if password == password2:
                    uid = uuid.uuid1()
                    hashed_password = make_password(password)
                    User.objects.create(email=email, username=username, first_name=first_name, last_name=last_name, password=hashed_password, uid=uid)
                    messages.success(request,"Successfully Created User!")
                    return redirect('user_view')
                else:
                    messages.warning(request,"Password does not match, Please try again!")
                    return redirect('user_view')
        return render(request, 'adminapp/user.html', {'users' : users, 'active1' : 'active'})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def user_detail(request, uid):
    try:
        if not request.user.is_superuser:
            return redirect('dashboard')
        users = User.objects.all()
        usr = User.objects.get(uid=uid)
        if request.method == "POST":
            data = request.POST
            email = data.get('email')
            username = data.get('username')
            first_name = data.get('first_name')
            last_name = data.get('last_name')
            is_active = data.get('is_active') == 'on'
            password1 = data.get('password')
            password2 = data.get('password2')
            if password1 and password2:
                if password1 == password2:
                    usr.email = email
                    usr.username = username
                    usr.first_name = first_name
                    usr.last_name = last_name
                    usr.is_active = is_active
                    usr.set_password(password1)
                    usr.save()
                    messages.success(request,f'Successfully Updated {usr.username}!')
                    return redirect('user_view')
                else:
                    messages.warning(request,"Password does not match, Please try again!")
                    return redirect('user_view')
            elif password1=="" and password2=="":
                usr.email = email
                usr.username = username
                usr.first_name = first_name
                usr.last_name = last_name
                usr.is_active = is_active
                usr.save()
                messages.success(request,f'Successfully Updated {usr.username}!')
                return redirect('user_view')
            else:
                messages.warning(request,"Password does not match, Please try again!")
                return redirect('user_view')
        return render(request, 'adminapp/user_detail.html', {'users' : users, 'usr' : usr})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('user_view')

@login_required()
def cafe(request):
    try:
        cafes = CafeResturant.objects.filter(type_of='cafe')
        cafes = pagination_custom(request,cafes)

        if request.method == "POST":
            data = request.POST
            type = data.get('type')
            if type == 'delete':
                id = data.get('cafe_id')
                caf = CafeResturant.objects.get(id=id)
                caf.delete()
                messages.success(request, 'Successfully Delete Cafe!')
                return redirect('cafe')
            if type == 'new-cafe':
                cafe_name = data.get('cafe')
                open_time = data.get('open_time')
                closing_time = data.get('closing_time')
                contact = data.get('contact')
                location = data.get('location')
                description = data.get('description')
                image = request.FILES.get('image')
                type_of = 'cafe'

                caf_name = CafeResturant.objects.filter(cafe_name=cafe_name)
                if caf_name:
                    messages.warning(request,"Cafe name is already taken, Please choose another!")
                    return redirect('cafe')
                else:
                    CafeResturant.objects.create(cafe_name=cafe_name, image=image, type_of=type_of, location=location, description=description, contact_number=contact, opening_time=open_time, closing_time=closing_time)
                    messages.success(request,"Successfully Register Cafe!")
                    return redirect('cafe')
            
        return render(request, 'adminapp/cafe.html', {'active2' : 'active', 'cafes' : cafes})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def cafe_detail(request, id):
    try:
        caf = CafeResturant.objects.get(id=id)

        if request.method == "POST":
            data = request.POST
            cafe_name = data.get('cafe')
            open_time = data.get('open_time')
            closing_time = data.get('closing_time')
            contact = data.get('contact')
            location = data.get('location')
            description = data.get('description')
            image = request.FILES.get('image')

            caf.cafe_name = cafe_name
            caf.opening_time = open_time
            caf.closing_time = closing_time
            caf.contact_number = contact
            caf.location = location
            caf.description = description
            if image:
                caf.image = image
                caf.save()
                messages.success(request,f'Successfully Updated {caf.cafe_name}!')
                return redirect('cafe')
            caf.save()
            messages.success(request,f'Successfully Updated {caf.cafe_name}!')
            return redirect('cafe')
                
        return render(request, 'adminapp/cafe_detail.html', {'caf' : caf})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def restaurant(request):
    try:
        restaurants = CafeResturant.objects.filter(type_of='resturant')
        restaurants = pagination_custom(request,restaurants)

        if request.method == "POST":
            data = request.POST
            type = data.get('type')
            if type == 'delete':
                id = data.get('restaurant_id')
                caf = CafeResturant.objects.get(id=id)
                caf.delete()
                messages.success(request, 'Successfully Delete Restaurant!')
                return redirect('restaurant')
            if type == 'new-restaurant':
                cafe_name = data.get('restaurant')
                open_time = data.get('open_time')
                closing_time = data.get('closing_time')
                contact = data.get('contact')
                location = data.get('location')
                description = data.get('description')
                img = request.FILES.get('image')
                type_of = 'resturant'

                caf_name = CafeResturant.objects.filter(cafe_name=cafe_name)
                if caf_name:
                    messages.warning(request,"Restaurant name is already taken, Please choose another!")
                    return redirect('restaurant')
                else:
                    CafeResturant.objects.create(cafe_name=cafe_name, image=img, type_of=type_of, location=location, description=description, contact_number=contact, opening_time=open_time, closing_time=closing_time)
                    messages.success(request,"Successfully Register Restaurant!")
                    return redirect('restaurant')
            
        return render(request, 'adminapp/restaurant.html', {'active3' : 'active', 'restaurants' : restaurants})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def restaurant_detail(request, id):
    try:
        caf = CafeResturant.objects.get(id=id)

        if request.method == "POST":
            data = request.POST
            cafe_name = data.get('cafe')
            open_time = data.get('open_time')
            closing_time = data.get('closing_time')
            contact = data.get('contact')
            location = data.get('location')
            description = data.get('description')
            image = request.FILES.get('image')

            caf.cafe_name = cafe_name
            caf.opening_time = open_time
            caf.closing_time = closing_time
            caf.contact_number = contact
            caf.location = location
            caf.description = description
            if image:
                caf.image = image
                caf.save()
                messages.success(request,f'Successfully Updated {caf.cafe_name}!')
                return redirect('restaurant')
            caf.save()
            messages.success(request,f'Successfully Updated {caf.cafe_name}!')
            return redirect('restaurant')
        return render(request, 'adminapp/restaurant_detail.html', {'caf' : caf})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def dish(request):
    try:
        cafes = CafeResturant.objects.all()
        dishes = Dish.objects.all()
        dishes = pagination_custom(request,dishes)

        if request.method == "POST":
            data = request.POST
            type = data.get('type')
            if type == 'delete':
                id = data.get('dish_id')
                caf = Dish.objects.get(id=id)
                caf.delete()
                messages.success(request, 'Successfully Delete Dish!')
                return redirect('dish')
            if type == 'new-dish':
                cafe_name = data.get('cafe')
                dish_name = data.get('dish_name')
                meal_type = data.get('meal_type')
                price = data.get('price')
                ingredients = data.get('ingredients')
                img = request.FILES.get('image')
                cafee_id = CafeResturant.objects.get(id=cafe_name)

                Dish.objects.create(cafe=cafee_id, image=img, dish_name=dish_name, meal_name=meal_type, price=price, ingredients=ingredients)
                messages.success(request,"Successfully add dish!")
                return redirect('dish')
            
        return render(request, 'adminapp/dish.html', {'active4' : 'active', 'dishes' : dishes, 'cafes' : cafes})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def dish_detail(request, id):
    try:
        cafes = CafeResturant.objects.all()
        dis = Dish.objects.get(id=id)

        if request.method == "POST":
            data = request.POST
            cafe_name = data.get('cafe')
            meal_type = data.get('meal_type')
            ingredients = data.get('ingredients')
            dish_name = data.get('dish_name')
            price = data.get('price')
            image = request.FILES.get('image')
            cafee_id = CafeResturant.objects.get(id=cafe_name)

            dis.cafe = cafee_id
            dis.meal_name = meal_type
            dis.dish_name = dish_name
            dis.ingredients = ingredients
            dis.price = price
            if image:
                dis.image = image
                dis.save()
                messages.success(request,f'Successfully Updated {dis.dish_name}!')
                return redirect('dish')
            dis.save()
            messages.success(request,f'Successfully Updated {dis.dish_name}!')
            return redirect('dish')
        
        return render(request, 'adminapp/dish_detail.html', {'cafes' : cafes, 'dis' : dis})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def team(request):
    try:
        cafes = CafeResturant.objects.all()
        teams = Team.objects.all()
        teams = pagination_custom(request,teams)

        if request.method == "POST":
            data = request.POST
            type = data.get('type')
            if type == 'delete':
                id = data.get('team_id')
                caf = Team.objects.get(id=id)
                caf.delete()
                messages.success(request, 'Successfully Delete Team Member!')
                return redirect('team')
            if type == 'new-team':
                cafe_name = data.get('cafe')
                name = data.get('name')
                post = data.get('post')
                description = data.get('description')
                img = request.FILES.get('image')
                cafee_id = CafeResturant.objects.get(id=cafe_name)

                Team.objects.create(cafe=cafee_id, image=img, name=name, post=post, description=description)
                messages.success(request,"Successfully add team member!")
                return redirect('team')
            
        return render(request, 'adminapp/team.html', {'active5' : 'active', 'teams' : teams, 'cafes' : cafes})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def team_detail(request, id):
    try:
        cafes = CafeResturant.objects.all()
        mem = Team.objects.get(id=id)

        if request.method == "POST":
            data = request.POST
            cafe_name = data.get('cafe')
            post = data.get('post')
            name = data.get('name')
            description = data.get('description')
            price = data.get('price')
            image = request.FILES.get('image')
            cafee_id = CafeResturant.objects.get(id=cafe_name)

            mem.cafe = cafee_id
            mem.post = post
            mem.name = name
            mem.description = description
            if image:
                mem.image = image
                mem.save()
                messages.success(request,f'Successfully Updated {mem.name}!')
                return redirect('team')
            mem.save()
            messages.success(request,f'Successfully Updated {mem.name}!')
            return redirect('team')
        
        return render(request, 'adminapp/team_detail.html', {'cafes' : cafes, 'mem' : mem})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

@login_required()
def reviews(request):
    try:
        review = Reviews.objects.all()
        review = pagination_custom(request,review)

        if request.method == "POST":
            data = request.POST
            type = data.get('type')
            if type == 'delete':
                id = data.get('review_id')
                caf = Reviews.objects.get(id=id)
                caf.delete()
                messages.success(request, 'Successfully Delete Review!')
                return redirect('reviews')
            
        return render(request, 'adminapp/reviews.html', {'active6' : 'active', 'review' : review})
    except:
            messages.warning(request, 'Request is not responed please check your internet connection and try again!')
            return redirect('dashboard')

def pagination_custom(request,table):
    paginator = Paginator(table, 10)
    page = request.GET.get('page')
    try:
        table = paginator.page(page)
    except PageNotAnInteger:
        table = paginator.page(1)
    except EmptyPage:
        table = paginator.page(paginator.num_pages)
    return table