#Ce fichier contient les fonctions utilitaires qui seront beaucoup utilisées dans les autres applications
import json
from time import sleep
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.common.exceptions import StaleElementReferenceException,NoSuchElementException

def count_elements(element):
    return len(element)

def save_last_scrapped_info(i=None,j=None,k=None,l=None):
    with open("historique.json","w+") as histor:
        dic =read_last_scrapped_info()
        if dic is not None:
            if i is not None:
                dic["i"]=i
            if j is not None:
                dic["j"]=j
            if i is not None:
                dic["k"]=k
            if l is not None:
                dic["l"]=l
        else:
            dic ={
                'i':i,
                'j':j,
                'k':k,
                'l':l
            }
        json_dic=json.dumps(dic)
        histor.write(json_dic)

def read_last_scrapped_info():
    with open("historique.json","r") as histor:
        f=histor.read()
        if f =='' or f is None:
             dic =None
        else:
            print(histor is None)
            dic = json.loads(f)
    return dic


def save_marjane_elements_number(nbre_elements1,nbre_elements2,nbre_elements3):
    with open('marjane_elts_info.json','w+') as mrjne:
        dic = read_marjane_elements_number()
        if dic is None:
            dic={
            'nbre_elts1':nbre_elements1,
            'nbre_elts2':nbre_elements2,
            'nbre_elts3':nbre_elements3
        }
        json_dic = json.dumps(dic)
        mrjne.write(json_dic)


def read_marjane_elements_number():
    with open("marjane_elts_info.json",'r') as mrjne:
        f = mrjne.read()
        if f =='':
            dic =None
        else:
            dic = json.load(mrjne)
    return dic

def last_scrapped_element():
    hist=read_last_scrapped_info()
    marjanestruct=read_marjane_elements_number()

    return hist,marjanestruct

#Cette fonction permet de verifier si un element est present dans le viewport de la page chargée
def is_element_visible_in_viewpoint(driver, element) -> bool:
    return driver.execute_script("var elem = arguments[0],                 " 
                                 "  box = elem.getBoundingClientRect(),    " 
                                 "  cx = box.left + box.width / 2,         " 
                                 "  cy = box.top + box.height / 2,         " 
                                 "  e = document.elementFromPoint(cx, cy); " 
                                 "for (; e; e = e.parentElement) {         " 
                                 "  if (e === elem)                        " 
                                 "    return true;                         " 
                                 "}                                        " 
                                 "return false;                            "
                                 , element)

#Cette fonction permet de scroller la page jusqu'à l'element  
def scrollpagebyelementheigh(driver,element,elementxpath):
    element_heigh=element.location['y']
    print("elemntheight: "+str(element_heigh)+" viewportheight= "+str(driver.execute_script("return document.body.scrollHeight")))
    if(element_heigh>1241 and element_heigh<1570):
        element_heigh=1241
    if(element_heigh>1570):
        element_heigh=1450
    
    driver.execute_script("window.scrollTo(0, {});".format(element_heigh))
    
    check_exists_by_xpath(driver,elementxpath)

        
        
#Cette après avoir scroller verifie si la page n'a pas disparue ce comportement est propre au site de marjane
def check_exists_by_xpath(driver,elementxpath):
    try:
        driver.find_element_by_xpath(elementxpath).location
    except StaleElementReferenceException:
        time.sleep(4)
        wait = WebDriverWait(driver,30)
        wait.until(EC.presence_of_element_located((By.XPATH,elementxpath)))
        scrollpagebyelementheigh(driver,driver.find_element_by_xpath(elementxpath),elementxpath)

#Cette fonction convertit un prix reccuperé sur marjane avec le format virgule ex: 10,5 et le convertit en float c-a-d 10.5
def convert_price_in_float(price):
    splittedarray = price.split(",")
    temp = ""
    x=0
    for n in splittedarray:
        if(x==1):
            temp +="."
        temp +=str(n)
        x+=1
    converted_price = float(temp)
    return converted_price
    