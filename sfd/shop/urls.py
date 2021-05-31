from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="ShopHome"),
    path("about/",views.about,name="AboutUs"),
    path("contactus/",views.contact,name="ContactUs"),
    path("tracker/",views.track,name="TrackingStatus"),
    path("search/",views.search,name="Search"),
    path("products/<int:myid>",views.prodView,name="ProductView"),
    path("checkout/",views.checkout,name="Checkout"),
    path("meetthedeveloper/",views.devop,name="MeetTheDeveloper"),
    path("handlerequest/",views.handlerequest,name="HandleRequest"),
    path("test/",views.testing,name="Testing"),     # for testing purpose temporary
]