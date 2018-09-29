a = 0
mois = str(input('entrer le mois : '))
jour=0

def med_annee(a):                                                                # création de la fonction med_annee qui permet à l'utilisateur d'entrer l'année souhaitée
    while a < 1582:                                                              # Condition qui oblige l'utilisateur a entrer une annee supérieur à 1582
        a = int(input('Entrer l annee'))                                         # on demande à l'utilisateur d'entrer une année
    return a

f = med_annee(a)                                                                 # on affecte la fonction med_annee a la variable f

def modulo(f):                                                                   # création de la fonction modulo qui permet de garder les deux derniers chiffres de l'année
    d = f % 100                                                                  # utilisation du modulo pour permettre de récuperer les 2 derniers chiffres
    return d

y = modulo(f)                                                                    # on affecte la fonction modulo a la variable y

def med_annee2(y):                                                               # création de la fonction med_anne2 qui permet de diviser par 1/4 en ignorant les restes
    b = y // 4                                                                   # calcul pour permettre de diviser par 1/4 en ignorant les restes
    return b

z = med_annee2(y)                                                               # on affecte la fonction med_annee2 a la variable z

def med_jour(jour):                                                             # création de la fonction med_jour qui permet à l'utilisateur d'entrer le jour souhaité
    jour = int(input('entrer le jour'))                                         # on demande à l'utilisateur d'entrer un jour
    return jour

r = med_jour(jour)                                                              # on affecte la fonction med_jour a la variable r

def med_mois(mois):                                                             # création de la fonction med_mois qui va nous permettre de récupérer le mois et de l'associer a une valeur
    if mois == "janvier" or mois == "octobre":                                                  # chaque mois est assoxiées a une valeur
        return 0
    elif mois == 'mai':
        return 1
    elif mois == 'aout':
        return 2
    elif mois == 'fevrier' or mois == 'mars' or mois == 'novembre':
        return 3
    elif mois == 'juin':
        return 4
    elif mois == 'septembre' or mois == 'decembre':
        return 5
    else:
        return 6

p = med_mois(mois)                                                      # on affecte la fonction med_mois a la variable p

def med_bissextile(f):                                                   # création de la fonction med_bisextile pour déterminer si l'année est bisextile ou non
    biss = 0                                                            # biss est la variable boleennne
    if f % 4 == 0 and f % 100 !=0:                                      # l'année est bisextile si elle est divisible par 4 et non par 100, et si elle est divisible par 400
        biss = 1
    elif f % 400 == 0:
        biss = 1
    else:
        biss = 0
    if biss == 1 and mois == 'janvier' or mois == 'fevrier':                # si l'année est bissextile et si le mois et janvier ou février on ote 1
        return -1
    else:
        return 0

h = med_bissextile(f)                                                    # on affecte la fonction med_bissextile a la variable h

def med_o(f, y):                                                    # création de la fonction med_o permet selon l'année d 'associer une valeur moins les deux dernirs chiffres
    c = f - y
    if c == 1900:
        return 0                                                      # Selon l'année on affecte une valeur spécifique
    elif c == 1800:
        return 2
    elif c == 1700 or c == 2100:
        return 4
    elif c == 1600 or c == 2000:
        return 6


u = med_o(f, y)                                                 #on affecte la fonction med_o a la variable u

def result():                                                   #Création de la fonction result permet de calculer l'ensemple des variables corespondantes
    resultat = y + z + r + p + h + u
    resultat = resultat % 7
    return (resultat)

k = result()                                                        # on affecte la fonction result a la variable k

def final(k):                                                       # création de la fonction final permet d'associer une valeur a un jour de la semaine
    if k ==0:
        print ("C'est un dimanche")
    elif k == 1 :
        print ("C'est un lundi")
    elif k == 2 :
        print ("C'est un mardi")
    elif k == 3 :
        print ("C'est un mercredi")
    elif k == 4 :
        print ("C'est un jeudi")
    elif k == 5 :
        print ("C'est un vendredi")
    elif k == 6 :
        print ("C'est un  samedi")

final(k)