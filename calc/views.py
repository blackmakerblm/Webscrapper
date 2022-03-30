import time
from calc.scrapper_marjane import scrape,scrape_from_last,scrape_product_name
from django.shortcuts import render
from django.http import HttpResponse
from produits import models
from calc.tache import addi

# Create your tests here.


# Create your views here.
def index(request):
    return render(request,"index.html")

def add(request):
    a=addi.delay(40,5)
    time.sleep(5)
    return HttpResponse(a.get())

def scrapemarjane(request):
    scrape_product_name("https://www.marjane.ma/","lait")
    return HttpResponse("Operation achevée")

def scrapemarjanefromlast(resquest):
    scrape_from_last("https://www.marjane.ma/")
    