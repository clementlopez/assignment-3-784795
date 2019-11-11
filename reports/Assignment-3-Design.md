# Part 1 : Design for streaming analytics
## Question 1

### Dataset
timestamp = placement temporel, c'est des records generes par des capteurs
c'est une base de donnee simple et propre (juste derniere colonne vide) --> contrairement a BD google
sensor = hyper bien pour analytic = tres doc sur 
	= near real time ingestion (se prete tres bien)

The dataset I will use for this assignment will be the one of bts.
This is a collection of sensors data from base stations. The data structure is as follow:

* station_id: the id of the stations
* datapoint_id: the id of the sensor (data point)
* alarm_id: the id of the alarm
* event_time: the time at which the event occurs
* value: the value of the measurement of the datapoint
* valueThreshold: the threshold set for the alarm. Note that some threshold values are set to a default value of 999999.
* isActive: the alarm is active (true ) or not (false)
* storedtime: no store


### Stream
For a given station we can keep track of minimum, maximum and mean values for each sensor. 
In addition, streaming analysis will be used mainly for predictive maintenance and reliability analysis in the case of a sensor dataset (in an IoT environment)
As it allows an near-real time analysis, it allows to have a very short reaction time to a possible problem that could occur

* frequency analysis : check that it is coherent and stable
** example: anomaly detection diagnosis : automatically remove noise/incoherent data (peak of a value whereas before and after the data are stable and the measurements are very close in time)
* reliability analytic: predict future alarms
** example: if the temperature starts to rise slowly and approaches the maximum threshold --> launch an imminent overheating alert
* detect that the alarm is currently on (isActive is true) (and detect where that alarm is)
* send back in the pipe (another one) to the user the data of the real-time analysis


stream :
analyse de frequence = verifier que ce soit coherent et stable
predictive maintenance et reability analysis
analyser temperature max sur les dernieres 24h pour une station
reliability analytic = quand ca va foirer ou quand ca foire
exemple = si temperature commence a augmenter doucement --> lancer alerte surchauffe imminente
anomaly detection diagnosis = enlever automatiquement le bruit/ donnees incoherente = (pic d'une valeur alors que avant et apres pas de probleme)
moyenne sur les dernieres 24h
dire alarme est a true/alarme est actuellement enclenchee
renvoyer dans le tuyau (un autre ?) a l'utilisateur les donnees de l'analyse en temps reel


### Batch

For batch analytics we can compute metrics like :
* rate distribution data by station (which station issued the most data)
* for a station, make a histogram of the temperature over a day (over a month, over a year...)
* look at the number of alarms triggered per day/month/... per station
* look at the type of alarm that occurs most often (the alarm that exceeds the threshold the most)
* for an alarm type: at which time of the day it is most triggered





historigramme = batch
taux de repartition des donnees (quelle station a emis le plus de donnees, sur une station faire histogramme de la temperature sur une journee, regarder le nombre d'alarme declenchee par jour/heure par station, le type d'alarme qui arrive le plus souvent = l'alarme qui depasse le plus le threshold (seuil), , ..., en gros un summary)
tx repartition donnees par station
nbr alarmes declenchees par heure par station
alarmes les plus declenchees
type alarme qui se declenche le plus souvent
pour un type alarme : a quel moment de la journee elle est le plus declenchee




## Question 2

Pour faciliter les choses je vais partir sur un schema basique avec 1 utilisateur = 1 station, il y aura donc deja une repartition par station et handle keyed n'est donc pas obligatoire.
Cependant, pour faire analytics se serait pratique de pouvoir trier par alarme par exemple et la on peut voir apparaitre le handle keyed, je vais donc m'orienter vers du handle keyed.

Pour faire analytics se serait plus pratique de pouvoir trier 
keyed = repartitionner avec machin gerant analytic


Garanties fournies aux utilisateurs sur la perte de donnees 
order of file arrival (pour le declenchement d'alerte l'ordre est important = si non alerte a 19h55 puis si alerte a 19h50 --> pas necessaire de declencher une alerte puisque l'alarme est finie), availability (serveur full dispo en fonction du taux de duplication), 

https://admhelp.microfocus.com/lr/en/12.60-12.63/help/WebHelp/Content/Controller/mon_mqtt.htm

IoT = recherche de peu de connexion, rapide execution
At most once : by default pour MQTT --> IoT, sensors = souvent beaucoup de donnees et pas forcement une bonne borne passante, il est peut etre preferable de perdre une donnee de temps en temps au profit de la rapidite

Exactly-once processing
Exactly-once delivery
https://docs.microsoft.com/en-us/stream-analytics-query/event-delivery-guarantees-azure-stream-analytics

## Question 3

on a des timestamp dans le dataset --> on les garde pour les associer a la stream source

on pourrait avoir/ne pas avoir de fenetre
si stream analysis ou on declenche des triggers pas besoin
Pour analyse/a quel point les donnees sont fiables -- pour tout ce qui est filtering
Window en nbre de row = toujours le meme nombre de donnees pour analyse, toujours meme taux de fiabilite mais la coherence temporelle peut etre nulle (si gap entre deux rows)
en time window : si grand gap entre chaque row, le taux de fiabilite peut etre moins fiable mais ca semble plus proche de la realite
Ca peut etre au cas par cas en fonction des datas envoyes par les capteurs et des envies du client

avec keyed on peut regler la window !!!!!!!!!

## Question 4

