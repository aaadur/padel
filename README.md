# padel
Robot padel

Création instance container à partir de modèle

Sur le portail utiliser le service : Déployer un modèle personnalisé

![image](https://user-images.githubusercontent.com/56845103/233350099-a6b48abc-9ddb-4554-8efe-2516f210d9c6.png)


https://labs.play-with-docker.com/

Cnx Putty

Utiliser Putty gen
Charger la clé générée par Azure (*.pem) et sauvegarder la en clé private (save private key)
configurer putty en utilisant le fichier généré (*.ppk) en le paramétrant dans ssh/auth


touch a
-> copier dans a : git clone https//.....(prendre l'adresse dans github)
$(cat a)
cd padel
docker image build -t aaadur/padel .
docker login -u a...
docker image push aaadur/padel


Heure été fr - 2h : FR 00h00 = utc 22h00
Heure hivers FR - 1h: FR 00h00 = utc 23h00
