from django.db import models
from accounts.models import User
from movies.models import movies

# Create your models here.

class theatre(models.Model):

    name=models.CharField(max_length=255)
    city=models.CharField(max_length=255)
    address=models.CharField(max_length=255)
    manager=models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name



    
    def generate_seats(self, screen_number, rows=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'], seats_per_row=10):
        from .models import seats

        for row in rows:
            if row in ['A', 'B', 'C']:
                seat_type = 'VIP'
            elif row in ['D', 'E', 'F']:
                seat_type = 'Gold'
            else:
                seat_type = 'Regular'

            for number in range(1, seats_per_row + 1):
                seats.objects.get_or_create(
                    theatre=self,
                    screen_number=screen_number,
                    row_label=row,
                    seat_number=number,
                    defaults={'seat_type': seat_type}
                )



class showtimes(models.Model):
    movie=models.ForeignKey(movies, on_delete=models.SET_NULL, null=True, blank=True)
    theatre=models.ForeignKey(theatre, on_delete=models.CASCADE)
    show_time=models.DateTimeField()
    screen_number=models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            self.theatre.generate_seats(screen_number=self.screen_number)


class seats(models.Model):
    theatre=models.ForeignKey(theatre, on_delete=models.CASCADE)
    screen_number = models.IntegerField(null=True, blank=True)
    row_label = models.CharField(max_length=255)
    seat_number = models.IntegerField()
    seat_type = models.CharField(max_length=255,choices=[['VIP', 'VIP'], ['Gold', 'Gold'], ['Regular', 'Regular']])    


# models.py




   