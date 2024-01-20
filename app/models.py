from django.db import models

class CafeResturant(models.Model):
    cafe_resturant_type = [
        ('cafe' , 'cafe'),
        ('resturant' , 'resturant'),
    ]
    cafe_name = models.CharField(max_length=255, unique=True)
    image = models.ImageField(upload_to='cafes')
    type_of = models.CharField(max_length=100, choices=cafe_resturant_type)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.cafe_name

class Dish(models.Model):
    meal_choices = [
        ('breakfast', 'breakfast'),
        ('lunch', 'lunch'),
        ('dinner', 'dinner'),
    ]
    cafe = models.ForeignKey(CafeResturant, on_delete=models.CASCADE)
    dish_name = models.CharField(max_length=100)
    ingredients = models.TextField()
    meal_name = models.CharField(max_length=50, choices=meal_choices)
    image = models.ImageField(upload_to='dishes')
    price = models.DecimalField(max_digits=6, decimal_places=2)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Team(models.Model):
    cafe = models.ForeignKey(CafeResturant, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='team')
    post = models.CharField(max_length=150)
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Reviews(models.Model):
    cafe = models.ForeignKey(CafeResturant, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    comment = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)