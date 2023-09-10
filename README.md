# GES calendar


Ges calendar est une application python permettant de récupérer son planning [myGES](https://myges.fr) et de créer un fichier .ics, permettant ainsi de l'importer sur sur n'importe quel agenda.


## Installation


Pré-requis:
- [python 3.10](https://www.python.org/downloads/) ou version ultérieure
- vos identifiant myGES


Lancer la commande `pip install -r ./requirements.txt` pour installer les paquets.


Créer un fichier .env à la racine du projet en se basant sur le fichier .env.templates


## Utilisation


Pour lancer le script:


```
python ./main.py
```


Par défaut un fichier .ics est créé à la racine du projet avec tous les événements du mois en cours, il est possible de spécifier les dates de début et de fin.


```
python ./main.py --start-date=2023-09-11 --end-date=2023-09-17
```


Vous pouvez ensuite importer ce fichier sur l'agenda de votre choix


- pour importer sur [Google Calendar](https://support.google.com/calendar/answer/37118?hl=en&co=GENIE.Platform%3DDesktop#)
- pour importer sur [Outlook](https://support.microsoft.com/en-us/office/import-calendars-into-outlook-8e8364e1-400e-4c0f-a573-fe76b5a2d379)
- pour importer sur [iCloud calendar](https://support.apple.com/fr-fr/guide/calendar/icl1023/mac)


## Commentaires
Voici quelques liens de projets similaires réalisés dans d'autres languages et qui m'ont inspiré.
- [MyCal](https://github.com/obito/mycal)
- [MyGES CLI](https://github.com/quantumsheep/myges-cli)
- [Agenda-GES](https://github.com/kidelag/agenda-ges)
- [MyGes API Client Library for PHP](https://github.com/tchenu/myges/tree/master)
- [How to get an .ics and online calendar file instead using MyGES Extranet?](https://tomjorge.me/how-to-get-an-ics-and-online-calendar-file-instead-using-myges-extranet/amp/)

