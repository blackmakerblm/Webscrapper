from django.http.response import HttpResponse
from produits.models import Provenance,Produit,HistAjout,Categorie
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
import re
from djangocourse import utilitaires
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from calc.tache import save_last_scrapped_element_info

def scrape(url,from_last=False,last_info_dic=None):
    options = webdriver.ChromeOptions
    scrolled = False
    scrolledcount=1
    #navigateur = webdriver.Chrome('/usr/bin/chromedriver')
    navigateur=webdriver.Firefox(executable_path=GeckoDriverManager().install())
    navigateur.maximize_window()
    navigateur.get(url)
    wait = WebDriverWait(navigateur,30)
    wait2 = WebDriverWait(navigateur,10)
    wait.until(EC.element_to_be_clickable((By.XPATH,"//*[@id='root']/nav/ul/li[1]")))
    menu=navigateur.find_element_by_xpath("//*[@id='root']/nav/ul/li[1]")
    menu.click()
    wait.until(EC.presence_of_element_located((By.CLASS_NAME,"jsx-711432432"))) 
    nombre_elements=len(navigateur.find_elements_by_xpath("//*[@id='filters-block']/div/ul/li"))
    print(nombre_elements)
    for i in range(1 if not from_last else last_info_dic['i'],nombre_elements+1,1):
        navigateur.find_element_by_xpath("//*[@id='filters-block']/div/ul/li[{}]".format(i)).click()
        #element.click()
        time.sleep(3)
        WebDriverWait(driver=navigateur,timeout=10).until(EC.presence_of_element_located((By.CLASS_NAME,"jsx-3858928620")))
        nombre_element_niveau2= len(navigateur.find_elements_by_xpath("//*[@id='filters-block']/div/ul/li"))
        for j in range(1 if not from_last else last_info_dic['j'],nombre_element_niveau2+1,1):
            categorie_element = navigateur.find_element_by_xpath("//*[@id='filters-block']/div[1]/ul/li[{}]".format(j))
            label_categorie = categorie_element.text
            categorie_element.click()
            if(i==1):
                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='filters-block']/div/ul/li[{}]/ul/li".format(j))))
            else:
                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='filters-block']/div[1]/ul/li[{}]/ul/li".format(j))))
            nombre_elements_niveau3= len(navigateur.find_elements_by_xpath("//*[@id='filters-block']/div/ul/li[{}]/ul/li".format(j)))
            #utilitaires.save_marjane_elements_number(nombre_elements,nombre_element_niveau2,nombre_elements_niveau3)
            print(nombre_elements_niveau3)
            for k in range(1 if not from_last else last_info_dic['k'],nombre_elements_niveau3+1,1):
                if from_last:
                    try:
                        navigateur.find_element_by_xpath("//*[@id='filters-block']/div/ul/li[{}]/ul/li[{}]".format(j,k)).click()
                    except NoSuchElementException:
                        try:
                            navigateur.find_element_by_xpath("//*[@id='filters-block']/div[1]/ul/li[{}]/ul/li".format(j)).click()
                        except NoSuchElementException:
                            try:
                                 navigateur.find_element_by_xpath("//*[@id='filters-block']/div[1]/ul/li[{}]".format(k)).click()
                            except NoSuchElementException:
                                print("scrapping from last aucun element trouver")
                else:
                #Cette condition existe parce que le path de l'element k change en fonction de certains paramètres
                    if(j==1):
                        if(k==1):
                            if(i==1):
                                navigateur.find_element_by_xpath("//*[@id='filters-block']/div/ul/li[{}]/ul/li[{}]".format(j,k)).click()
                            else:
                                if(nombre_elements_niveau3==1):
                                    navigateur.find_element_by_xpath("//*[@id='filters-block']/div[1]/ul/li[{}]/ul/li".format(j)).click()
                                else:
                                    navigateur.find_element_by_xpath("//*[@id='filters-block']/div[1]/ul/li[{}]".format(k)).click()
                        else:
                            wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='filters-block']/div[1]/ul/li[{}]".format(k)))) 
                            navigateur.find_element_by_xpath("//*[@id='filters-block']/div[1]/ul/li[{}]".format(k)).click()
                            time.sleep(5)
                    else:
                        if(k==1):
                            if(nombre_elements_niveau3==1):
                                navigateur.find_element_by_xpath("//*[@id='filters-block']/div[1]/ul/li[{}]/ul/li".format(j)).click()
                            else:
                                navigateur.find_element_by_xpath("//*[@id='filters-block']/div[1]/ul/li[{}]/ul/li[{}]".format(j,k)).click() 
                        else:
                            navigateur.find_element_by_xpath("//*[@id='filters-block']/div[1]/ul/li[{}]".format(k)).click()   
                
                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/ul/li[1]"))) 
                nombre_articles = len(navigateur.find_elements_by_xpath("//*[@id='content']/div/div/div[2]/ul/li"))
                print("nombre article"+str(nombre_articles))
                for l in range(1 if not from_last else last_info_dic['l'],nombre_articles+1,1):
                    try:
                        wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/ul/li[{}]/div/a/img".format(l))))
                        #bouton article à cliquer
                        time.sleep(2)
                        try:
                            btnarticlexpath="//*[@id='content']/div/div/div[2]/ul/li[{}]/div/a/img".format(l)
                            btnarticle = navigateur.find_element_by_xpath(btnarticlexpath)
                            #waiting for element before checking presence in portview
                            wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/ul/li[{}]".format(l))))
                            if(not utilitaires.is_element_visible_in_viewpoint(navigateur,btnarticle)):
                                utilitaires.scrollpagebyelementheigh(navigateur,navigateur.find_element_by_xpath("//*[@id='content']/div/div/div[2]/ul/li[{}]".format(l)),
                                btnarticlexpath)
                                time.sleep(2)
                            attempt=0
                            while(attempt<3):
                                try:
                                    action = ActionChains(navigateur)
                                    action.move_to_element(btnarticle).perform()
                                    time.sleep(2)
                                    btnarticle.click()
                                    wait2.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div[2]/aside/div[1]/h2")))
                                    break
                                except TimeoutException:
                                    attempt+=1
                            if(not attempt==3):
                                try:
                                    try:
                                        produit_description = ""
                                        wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div[2]/section/div/p")))
                                        parent = navigateur.find_element_by_xpath("//*[@id='content']/div/div[2]/section/div/p")
                                        parents = parent.find_elements_by_xpath(".//*")
                                        if(parents is not None):
                                            for p in parents:
                                                produit_description+=p.text
                                            print(produit_description)
                                    except TimeoutException:
                                        pass
                                    provenance = Provenance()
                                    provenance.url = navigateur.current_url
                                    provenance.save()
                                    categorie = Categorie()
                                    categorie.label = label_categorie
                                    categorie.save()
                                    marque_label = navigateur.find_element_by_xpath("//*[@id='content']/div/div[2]/aside/div[1]/h3").text
                                    articlenom=navigateur.find_element_by_xpath("//*[@id='content']/div/div[2]/aside/div[1]/h2")
                                    produit = Produit()
                                    produit.label = articlenom.text
                                    if(produit_description is not ""):
                                        produit.description = produit_description
                                    if(marque_label is not None):
                                        produit.marque= marque_label
                                    produit.provenance = provenance
                                    produit.categorie = categorie
                                    poids = re.search(r"\d+(g|kg|Kg|G|KG)",articlenom.text)
                                    if(poids is not None):
                                        unit = re.search(r"(g|kg|Kg|G|KG)",poids.group()).group()
                                        qt =  re.search(r"\d+",poids.group()).group()
                                        produit.quantite=int(qt)
                                        produit.unite=unit
                                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,".jsx-3381872774.price")))
                                    prix_text = navigateur.find_element_by_css_selector(".jsx-3381872774.price").text
                                    prix = re.search(r"\d+,*\d*",prix_text).group()
                                    converted_prix_to_float = utilitaires.convert_price_in_float(prix)
                                    produit.prix = converted_prix_to_float
                                    produit.save()
                                    #cette tache est asynchrone
                                    save_last_scrapped_element_info.delay(i,j,k,l)
                                except:
                                    pass
                                #utilitaires.save_last_scrapped_info(i,j,k)
                                btnretour=navigateur.find_element_by_xpath("//*[@id='content']/div/a/i")
                                btnretour.click()
                                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div/div[2]/ul/li[1]")))
                        except NoSuchElementException:
                            pass
                    except TimeoutException:
                            #print("L'article à cliquer n'a pas été retrouvé dans le delai")
                            #navigateur.quit()
                            pass
                time.sleep(5)
            wait.until(EC.presence_of_element_located((By.CLASS_NAME,"jsx-3255672915")))
            navigateur.find_element_by_class_name("jsx-3255672915").click() #bouton retourner 
            time.sleep(5)
        navigateur.find_element_by_class_name("jsx-3255672915").click() # Bouton retourner
        wait.until(EC.presence_of_element_located((By.CLASS_NAME,"jsx-711432432")))
    navigateur.quit()



def scrape_from_last(URL):
    last_scrapped_info = utilitaires.read_last_scrapped_info()
    if last_scrapped_info is None:
        scrape(URL)
    else:
        scrape(URL,from_last=True,last_info_dic=last_scrapped_info)

def scrape_product_name(URL,prodname):
    options = webdriver.ChromeOptions
    #navigateur = webdriver.Chrome('/usr/bin/chromedriver')
    navigateur=webdriver.Firefox(executable_path=GeckoDriverManager().install())
    navigateur.maximize_window()
    navigateur.get(URL)
    searchboxxpath = "//*[@id='root']/header/div/section/form/input"
    wait = WebDriverWait(navigateur,30)
    wait2 = WebDriverWait(navigateur,5)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH,searchboxxpath)))
        searchbox = navigateur.find_element_by_xpath(searchboxxpath)
        searchbox.send_keys(prodname)
        searchbtn = navigateur.find_element_by_xpath("//*[@id='root']/header/div/section/form/button")
        searchbtn.click()
        try:
            wait2.until(EC.presence_of_element_located((By.XPATH,"/html/body/div[2]/div/main/div/div[2]/p")))
            navigateur.quit()
            raise ValueError('0 resultat trouvé pour {}'.format(prodname))
        except TimeoutException:
            try:
                 wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div[2]/ul/li[1]")))
                 nombre_article = len(navigateur.find_elements_by_xpath("//*[@id='content']/div/div[2]/ul/li"))
                 print(nombre_article)
                 for i in range(1,nombre_article+1,1):
                        try:
                            btn_articlexpath = "//*[@id='content']/div/div[2]/ul/li[{}]/div/a/img".format(i)
                            btn_artcile = navigateur.find_element_by_xpath(btn_articlexpath)
                            if(not utilitaires.is_element_visible_in_viewpoint(navigateur,btn_artcile)):
                                utilitaires.scrollpagebyelementheigh(navigateur,navigateur.find_element_by_xpath("//*[@id='content']/div/div[2]/ul/li[{}]".format(i)),
                                btn_articlexpath)
                                time.sleep(2)
                            attempt=0
                            while(attempt<3):
                                try:
                                    action = ActionChains(navigateur)
                                    action.move_to_element(btn_artcile).perform()
                                    time.sleep(2)
                                    btn_artcile.click()
                                    wait2.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div[2]/aside/div[1]/h2")))
                                    break
                                except TimeoutException:
                                    attempt+=1
                            time.sleep(3)
                            navigateur.find_element_by_xpath("/html/body/div[2]/div/main/div/a").click()#bouton retourner
                            try:
                                wait.until(EC.presence_of_element_located((By.XPATH,"//*[@id='content']/div/div[2]/ul/li[{}]".format(i))))
                            except TimeoutException:
                                raise ValueError("Erreur de chargement des articles")
                        except NoSuchElementException:
                            print("article {} n'a pas pu être accedé".format(i))
                 navigateur.quit()    
            except TimeoutException:
                raise ValueError('Temps écoulé avant d\'acceder à l\'article')
    except TimeoutException:
        pass

'''//*[@id="filters-block"]/div/ul/li[1]/ul/li[1] first before click //*[@id="filters-block"]/div/ul/li[2]/ul/li[1] //*[@id="filters-block"]/div/ul/li[1]/ul/li
//*[@id="filters-block"]/div[1]/ul/li[1] after first click
//*[@id="filters-block"]/div[1]/ul/li[1]
//*[@id="filters-block"]/div[1]/ul/li[1]/ul/li[1] after retourne button before click
//*[@id="filters-block"]/div[1]/ul/li[1]/ul/li
//*[@id="filters-block"]/div[1]/ul/li[2]/ul/li[1]
//*[@id="filters-block"]/div[1]/ul/li[1]/ul/li
//*[@id="filters-block"]/div[1]/ul/li[1] after retourne button after click
//*[@id="filters-block"]/div[1]/ul/li[1]
//*[@id="filters-block"]/div[1]/ul/li[2] 


//*[@id="content"]/div/div/div[2]/ul/li[1]
//*[@id="content"]/div page article
//*[@id="content"]/div/div/div[2]/ul/li[1]/div
//*[@id="content"]/div/div/div[2]/ul/li[1]/div/a image à cliquer pour se rendre sur la page de l'article
//*[@id="content"]/div/a bouton retour pour revenir à la liste des articles
//*[@id="content"]/div/div[1]/button/img image de l'article
//*[@id="content"]/div/div[2]/aside/div[1]/h3 marque de l'article
//*[@id="content"]/div/div[2]/aside/div[1]/h2 nom article
//*[@id="content"]/div/div[2]/aside/section/span prix de l'article
//*[@id="content"]/div/div[2]/section/div/p/div[1]
//*[@id="content"]/div/div[2]/section/div/p/div[2]
//*[@id="content"]/div/div[2]/section/div/p/div[3]
//*[@id="content"]/div/div[2]/section/div/p/div[4]
//*[@id="content"]/div/div[2]/section/div/p/div[5]
//*[@id="content"]/div/div[2]/section/div/p/div[6]
//*[@id="content"]/div/div[2]/section/div/p/div[7]
//*[@id="content"]/div/div[2]/section/div/p
'''
