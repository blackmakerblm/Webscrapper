from calc.scrapper_marjane import scrape_from_last
from django.urls import path

from . import views

urlpatterns = [
    path("",views.index,name="home"),
    path("add",views.add,name="add"),
    path("scrape",views.scrapemarjane,name="add"),
    path("scrapefromlast",views.scrapemarjanefromlast,name="add")
     
]