from django.db import models
from userApp.models import MyUser


class Frame(models.Model):
    frame_name = models.CharField(max_length=255)
    frame_url =  models.ImageField(upload_to='user/frame', blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2,default=10)


    def __str__(self):
        return self.frame_name



class UserFrame(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.frame.frame_name}'
