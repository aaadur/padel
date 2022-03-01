import pytest
import time
from datetime import date
from datetime import datetime
from datetime import timedelta
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.service import Service
from xml.dom.minidom import Element, parse
import xml.dom.minidom
import sys
from threading import Thread, RLock
from pyvirtualdisplay import Display


verrou = RLock ()

class tache (Thread):
    
    def __init__ (self, fichier , fct , mail, mdp , court, dateRes, heure, hAttente):
        super(tache, self).__init__()
        self.actif = False
        self.execute = True
        self.fichier = fichier
        self.fct = fct
#        s = Service("C:\Données\Projets\Python\geckodriver\geckodriver.exe")
        self.driver = webdriver.Firefox()
        self.vars = {}
#        self.driver.get("http://www.tennis94.fr/?_si=trem")
#        self.driver.get("http://www.tennis94.fr/page/dispo")
        self.driver.get("https://sport94.fr/")
        self.driver.set_window_size(1400, 600)
        self.mail = mail
        self.mdp = mdp
        self.court = court
        self.heure = heure
#        self.dateRes = dateRes
        self.dateRes = dateRes[8:10]+"/"+dateRes[5:7]+"/"+dateRes[0:4]

        self.attente = True
        self.datetime = ((date.today() + timedelta(days=1)).isoformat())+" "+hAttente
        self.iteration = 1
        self.termine = False
        cdtTremblayLog (self.fichier, self.driver, self.court, self.dateRes, self.heure, self.mail, self.mdp)
        print ("Activation robot "+self.mail)

    def __del__ (self):
        self.desactive ()
        self.stop ()
#        self.join()
        self.driver.quit()

    def minuit (self, flag):
        self.attente=flag
    
    def active(self):
        self.actif = True

    def desactive(self):
        self.actif = False

    def stop(self):
        self.execute= False

    def run(self):
        i=0
        while (self.execute):
            dt = str(datetime.today())
            time.sleep(0.05)
            while (self.actif and self.execute and i<self.iteration and (dt > self.datetime or self.attente == False)  ):
                print ("dt "+dt+" cible "+self.datetime)
                while (self.actif and self.execute and i<self.iteration):
                    i = i + 1
#                    with verrou:               
                    self.fichier.write (str(datetime.today())+": réservation "+self.mail+" court "+self.court+" horaire "+self.heure+"\n")
                    self.fct (self.fichier, self.driver, self.court, self.dateRes, self.heure, self.mail, self.mdp)
                self.termine = True


def cdtTremblayLog (fichier , driver, court, dateRes, heure, mail, mdp):
#    driver.find_element(By.NAME, "login").click()
#    driver.find_element(By.NAME, "login").send_keys(mail)
#    driver.find_element(By.NAME, "password").send_keys(mdp)
#    driver.find_element(By.NAME, "btnlogin").click()
#    driver.find_element(By.LINK_TEXT, "Calendrier réservations").click()
#    driver.get("http://www.tennis94.fr/page/dispo/date"+dateRes)

    driver.find_element(By.LINK_TEXT, "Me connecter").click()
    # 4 | click | id=input_login | 
    #driver.find_element(By.ID, "input_login").click()
    # 5 | type | id=input_login | sduroi@laposte.net
    driver.find_element(By.ID, "input_login").send_keys(mail)
    # 6 | click | id=input_passwd | 
    #driver.find_element(By.ID, "input_passwd").click()
    # 7 | type | id=input_passwd | newsc@fÃ©
    driver.find_element(By.ID, "input_passwd").send_keys(mdp)
    # 8 | click | id=btnlogin | 
    driver.find_element(By.ID, "btnlogin").click()
    driver.find_element(By.LINK_TEXT, "Choix du site").click()
    # 10 | click | css=.sitebox:nth-child(1) div | 
    driver.find_element(By.CSS_SELECTOR, ".sitebox:nth-child(1) div").click()
    #element = driver.find_element(By.ID, "d")
    #actions = ActionChains(driver)
    #actions.double_click(element).perform()
    # 14 | click | id=d | 
    #driver.find_element(By.ID, "d").click()






def cdtTremblayRes (fichier , driver, court, dateRes, heure, mail, mdp):
#    driver.get("http://www.tennis94.fr/page/dispo/date"+dateRes)
    driver.find_element(By.ID, "d").clear()
    driver.find_element(By.ID, "d").send_keys(dateRes)
#    driver.find_element(By.ID, "d").send_keys("17/02/2022")
    fichier.write (str(datetime.today())+": LOG date "+ dateRes+ " court "+ court + " heure " + heure+" verif 1\n")
    driver.save_screenshot("capture"+court+heure+"v1.png")
    driver.find_element(By.CSS_SELECTOR, ".btn").click()
    elements = driver.find_elements(By.NAME, "btnreza_"+court+"_"+heure)
    fichier.write (str(elements)+" verif 1.1\n")
    
    dtd = datetime.today()
    while len(elements)==0 and (datetime.today()-dtd).seconds < 3:
        print("1")
#        driver.get("http://www.tennis94.fr/page/dispo/date"+dateRes)
        driver.find_element(By.ID, "dc").click()
        driver.find_element(By.ID, "dc").send_keys(Keys.ENTER)
#        driver.find_element(By.ID, "d").clear()
#        driver.find_element(By.ID, "d").send_keys(dateRes)
        fichier.write (str(datetime.today())+": LOG date "+ dateRes+ " court "+ court + " heure " + heure+" verif 2\n")
#        driver.find_element(By.CSS_SELECTOR, ".btn").click()
        elements = driver.find_elements(By.NAME, "btnreza_"+court+"_"+heure)
    driver.save_screenshot("capture"+court+heure+"v2.png")

    try:
        fichier.write (str(datetime.today())+": LOG date "+ dateRes+ " court "+ court + " heure " + heure+" A\n")
        driver.save_screenshot("capture"+court+heure+"a.png")
        driver.find_element(By.NAME, "btnreza_"+court+"_"+heure).click()
        fichier.write (str(datetime.today())+": LOG date "+ dateRes+ " court "+ court + " heure " + heure+" B\n")
        driver.save_screenshot("capture"+court+heure+"b.png")
        driver.find_element(By.NAME, "btnresa").click()
        fichier.write (str(datetime.today())+": LOG date "+ dateRes+ " court "+ court + " heure " + heure+" C\n")
        driver.save_screenshot("capture"+court+heure+"c.png")
    except Exception:
        fichier.write (str(datetime.today())+": erreur réservation date "+ dateRes+ " court "+ court + " heure " + heure+"\n")
        pass
    try:
        fichier.write (str(datetime.today())+": LOG date "+ dateRes+ " court "+ court + " heure " + heure+" D\n")
        driver.find_element(By.XPATH, ".//tagName[@attribute=’OK’]");
        fichier.write (str(datetime.today())+": LOG date "+ dateRes+ " court "+ court + " heure " + heure+" E\n")
    except Exception:
        pass
#    driver.find_element(By.NAME, "btnlogout").click()
    driver.find_element(By.LINK_TEXT, "Me déconnecter").click()

def syntaxeParametre ():
    print ("paramètre :")
    print ("    date  : date:AAAA-MM-JJ")
    print ("    attente : attente:vrai/faux")


display = Display(visible=0, size=(800, 800))
display.start()
    
dictCourt = {"A":"22" , "B":"23" , "C":"24" , "D":"25" }

fichier = open('TraceRobot.log', 'a')

print ("Lancement Robot réservation Padel")
fichier.write (str(datetime.today())+": Lancement Robot réservation Padel"+"\n")
print ("")

try:
    dictArg = dict((x.strip(), y.strip())
                         for x, y in (element.split(':')
                                  for element in sys.argv[1:]))
except :
    print ("Erreur de syntaxe dans les paramètres:")
    syntaxeParametre()
    exit()

dateRes = (date.today() + timedelta(days=7)).isoformat()
hAttente = "00:00:00"
attente = True

nbarg =0
if len(sys.argv)>1:
    if ("date" in dictArg):
        nbarg = nbarg +1
        dateRes = dictArg["date"]
    if ("attente" in dictArg):
        nbarg = nbarg +1
        attente = dictArg["attente"] == "vrai"
    if len(sys.argv)-1!=nbarg:
        print ("Erreur de paramètres ",sys.argv[1:])
        syntaxeParametre ()
        exit ()
 
def test (liste):
    vrai = True
    for elt in liste:
        vrai = vrai and elt.termine
    return vrai

# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("RéservationPadel.xml")
reservation = DOMTree.documentElement

print ("Date: ", dateRes)
if attente:
    print ("lancement du Robot "+((date.today() + timedelta(days=1)).isoformat())+" "+hAttente)
else:
    print ("lancement immédiat du Robot")

fichier.write (str(datetime.today())+": Date "+dateRes +" attente "+str(attente)+"\n")
 

# Get all créneaux
creneaux = reservation.getElementsByTagName("creneau")

# initialisation des thread pour chaque créneau à réserver
robots = []

for creneau in creneaux:
    robots.append(tache (fichier, cdtTremblayRes , creneau.getElementsByTagName("user")[0].childNodes[0].data, creneau.getElementsByTagName("mdp")[0].childNodes[0].data, dictCourt[creneau.getElementsByTagName("court")[0].childNodes[0].data],dateRes,creneau.getElementsByTagName("horaire")[0].childNodes[0].data,hAttente))

for robot in robots:
    robot.minuit (attente)
    robot.active()
    robot.start()

while not(test(robots)):
    time.sleep (1)


for robot in robots:
    robot.stop()
    
fichier.close()
display.stop()