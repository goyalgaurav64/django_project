from django.db import models

# Create your models here.
class Blogpost(models.Model):   #see documentation
    post_id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    heado=models.CharField(max_length=500,default="")
    cheado=models.CharField(max_length=20000,default="")  # cheado --> content of heading 0
    head1=models.CharField(max_length=500,default="")
    chead1=models.CharField(max_length=20000,default="")
    head2=models.CharField(max_length=500,default="")
    chead2=models.CharField(max_length=20000,default="")
    pub_name=models.CharField(max_length=100,default="")
    pub_date=models.DateField()
    thumbnail=models.ImageField(upload_to="shop/images",default="")

    def __str__(self):
        return self.title