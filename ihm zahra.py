'encoding: utf8'
from tkinter import *
from tkinter.messagebox import *
import os
import re
import requests
import smtplib
import csv
from bs4 import BeautifulSoup
from email.mime.text import MIMEText


def main(entry_file):
    os.chdir("C:/Users/zahra/PycharmProjects/naoyade/venv\Scripts\python")
    nom_du_fichier = entry_file.get()  # Récupere la valeur de la Saisie de la Campagne
    campagne.withdraw()  # Réduit la fenêtre (sans la détruire)

    choix = Toplevel()
    choix.title("Projet Mailling")
    choix.resizable(width=FALSE, height=False)  # On bloque la redim* de la fenre
    choix.geometry('800x400+200+100')

    def ajout_mail(entry_file, enter1):
        saisie = enter1.get()
        try: # Gestion d'erreur
            if saisie == "" or 0:
                showwarning('Erreur', "Le champ de saisie est vide ou invalide")
            else:#Sinon
                listbox1.insert(END, saisie)#On écrit la saisie dans la listebox
                nom_du_fichier = entry_file.get()#On récupère le nom du fichier csv de base
                nom_du_fichier = open(nom_du_fichier + ".csv", "a")#On ouvre le fichier en mode ajout
                nom_du_fichier.write(saisie + "\n")#On ecrit le fichier puis on saute une ligne
                nom_du_fichier.close()#On ferme le fichier
        except TypeError: # Gestion d'erreur
            showwarning('Erreur, "FATAL ERROR')

    def supprimer_mail(entry_file):
        nom_du_fichier = entry_file.get()
        index = listbox1.curselection()#Récupérattion du n° d'index de la selection
        mot = listbox1.get(index)#On récupére la chaine de charactère a supprimer grace au n° d'index
        with open(nom_du_fichier + ".csv", "r") as f:#On ouvre le fichier en lecture
            lines = f.readlines()#on stock le fichier ligne par ligne dans un tableau
            lines.remove(mot)#On supprime la chaine correspondante
            with open(nom_du_fichier + "new.csv", "w") as new_f:#On crée un nouveau fichier temporaire
                for line in lines:
                    new_f.write(line)#On récrit le contenu dans le nouveau fichier
        os.remove(nom_du_fichier + ".csv")
        os.rename(nom_du_fichier + "new.csv", nom_du_fichier + ".csv")
        listbox1.delete(listbox1.curselection()) #Suppression de la ligne sélectionenr en listbox

    def revenir_nom_du_fichier():
        choix.destroy() #Détruit la fenêtre du menu
        campagne.deiconify()  # Remet la fenêtre principale

    def import_csv(entry_file):
        def concat_csv(entry_file_csv, entry_file):#Permet de concatener deux fichier csv

            nom_du_csv = entry_file_csv.get()
            nom_du_fichier = entry_file.get()
            main_csv.destroy()
            os.chdir("C:/Users/zahra/OneDrive/Documents/python")
            with open(nom_du_csv + ".csv", "r") as f:
                lines = f.readlines()# on stock le deuxieme fichier ligne par ligne dans un tableau
                with open(nom_du_fichier + ".csv", "a") as new_f:  # On ouvre en mode ajout le fichier de base
                    for line in lines:
                        new_f.write(line)
                        listbox1.insert(END, line)
            choix.deiconify()


        choix.withdraw()
        main_csv = Toplevel()
        main_csv.title("Import CSV ")
        main_csv.resizable(width=FALSE, height=False)
        main_csv.geometry('250x100+470+250')
        label_csv = Label(main_csv, text='Selectionnez votre fichier a importer')
        label_csv.place(x=25, y=20, width=200)#La position du label
        button_csv_ok = Button(main_csv, text='Ok', command=lambda: concat_csv(entry_file_csv, entry_file))
        button_csv_ok.place(x=100, y=60, width=50)
        entry_file_csv = StringVar()
        entry_file_csv = Entry(main_csv, textvariable=entry_file_csv)
        entry_file_csv.insert(0, '')
        entry_file_csv.place(x=90, y=40, width=70)

    def supp_doublon(entry_file):
        nom_du_fichier = entry_file.get()
        reader = csv.reader(open(nom_du_fichier + ".csv", 'r'), delimiter='\n')
        writer = csv.writer(open(nom_du_fichier + "copy.csv", 'w'), delimiter='\n')

        lastnames = set()
        for row in reader:
            if row[0] not in lastnames:
                writer.writerow(row)
                lastnames.add(row[0])
        os.remove(nom_du_fichier + ".csv")
        os.rename(nom_du_fichier + "copy.csv", nom_du_fichier + ".csv")
        choix.destroy()
        campagne.deiconify()


    def crawl_une_page():

        def run_crawl(entry_file):#Fonction qui déclanche la récupération de mails
            try:#Gestion d'erreur teste
                url = entry_url.get()
                requete = requests.get(url)
                page = requete.content
                Sbio = BeautifulSoup(page, 'html.parser')
                set = Sbio.get_text()
                emails = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,3}",
                                set)
                if len(emails) == 0:
                    showwarning("Erreur !", "Il n'y a aucune adresse dans cette page")
                else:
                    nom_du_fichier = entry_file.get()
                    nom_du_fichier = open(nom_du_fichier + ".csv", "a")
                    for item in emails:
                        nom_du_fichier.write(item + "\n")
                        listbox1.insert(END, item)
                nom_du_fichier.close()
                choix.deiconify()
                fen_url.destroy()
            except requests.exceptions.MissingSchema:
                showwarning('Erreur', "L'URL saisie est invalide !")
            except requests.exceptions.InvalidURL:
                showwarning('Erreur', "L'URL saisie est invalide !")

        def retour_url():
            choix.deiconify()
            fen_url.destroy()


        choix.withdraw()
        fen_url = Toplevel()
        fen_url.title("URL")
        fen_url.resizable(width=FALSE, height=False)
        fen_url.geometry('300x110+500+300')
        label_url = Label(fen_url, text="Saisissez votre URL au format HTML")
        label_url.pack()
        entry_url = StringVar()
        entry_url = Entry(fen_url, textvariable=entry_url, justify='center')
        entry_url.pack()
        button_ok_url = Button(fen_url, text="Ok", command=lambda: run_crawl(entry_file))
        button_ok_url.pack()
        button_retour_url = Button(fen_url, text="Retour", command=lambda: retour_url())
        button_retour_url.pack()
        fen_url.mainloop()



    def fenetre_mail(entry_file):
        os.chdir("C:/Users/zahra/OneDrive/Documents/python")
        nom_du_fichier = entry_file.get()
        choix.withdraw()

        mail = Toplevel()
        mail.title("MESSAGE")
        mail.resizable(width=FALSE, height=False)
        mail.geometry('800x600+200+100')
        label_exp = Label(mail, text="EXPÉDITEUR :")



        def mail_test():

            def retour_mail_test():
                mail.deiconify()
                fenetre_mail_test.destroy()

            def run_mail_test():
                exp = entry_exp.get()
                mdp = mdp_exp.get()
                mesg = text_message.get("1.0", "end-1c")
                obj = entry_obj.get()
                em = entry_mail_test.get()
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                server.login(exp,mdp)
                msg = MIMEText(mesg)
                msg['Subject'] = obj
                msg['From'] = exp
                msg['To'] = em
                server.send_message(msg)
                server.quit()


            mail.withdraw()
            fenetre_mail_test = Toplevel()
            fenetre_mail_test.title("Mail TEST")
            fenetre_mail_test.resizable(width=FALSE, height=False)
            fenetre_mail_test.geometry('300x110+500+300')
            label_mail_test = Label(fenetre_mail_test, text="Saisissez l'adresse mail pour le test")
            label_mail_test.pack()
            entry_mail_test = StringVar()
            entry_mail_test = Entry(fenetre_mail_test, textvariable=entry_mail_test, justify='center')
            entry_mail_test.pack()
            button_ok_mail_test = Button(fenetre_mail_test, text="Ok", command=lambda: run_mail_test())
            button_ok_mail_test.pack()
            button_retour_url = Button(fenetre_mail_test, text="Retour", command=lambda: retour_mail_test())
            button_retour_url.pack()
            fenetre_mail_test.mainloop()


        def envoyer():
            try:
                exp = entry_exp.get()
                mdp = mdp_exp.get()
                mesg = text_message.get("1.0", "end-1c") #On récuypére dans mesg l'entrée du text du début à la fin
                obj = entry_obj.get()
                lignes = open(nom_du_fichier + ".csv", "r")
                server = smtplib.SMTP('smtp.gmail.com',587)
                server.starttls()
                try:
                    server.login(exp,mdp)
                except smtplib.SMTPAuthenticationError :
                    showwarning("Erreur d'authentification", "L'identifiant ou le mot de passe saisie est incorrect")
                try:
                    for ligne in lignes:
                        msg = MIMEText(mesg)
                        msg['Subject'] = obj
                        msg['From'] = exp
                        msg['To'] = ligne

                    try:
                        server.send_message(msg)
                    except smtplib.SMTPSenderRefused:
                            showwarning("Erreur", "L'email n'a pas été envoyé")

                except smtplib.SMTPRecipientsRefused:
                    showwarning('Error', "L'adresse " + ligne + "est invalide, l'envoi est annulé")

            except TypeError:
                showwarning('Erreur', "Mot de passe incorrect ou champs non remplis")

            server.quit()
            lignes.close()
            showinfo("Information", "Les mails ont été corréctement envoyés")


        def retour_mail():
            choix.deiconify()
            mail.destroy()


        label_exp.place(x=50, y=50, width=100)
        entry_exp = StringVar()
        entry_exp = Entry(mail, textvariable=entry_exp)
        entry_exp.place(x=150, y=50, width=250)
        mdp_label = Label(mail, text="MDP :")
        mdp_label.place(x=400, y=50, width=50)
        mdp_exp = StringVar()
        mdp_exp = Entry(mail, textvariable=mdp_exp, show="*")
        mdp_exp.place(x=450, y=50, width=200)
        label_objet = Label(mail, text="OBJET :")
        label_objet.place(x=72, y=100, width=100)
        entry_obj = StringVar()
        entry_obj = Entry(mail, textvariable=entry_obj)
        entry_obj.place(x=150, y=100, width=500)
        label_message = Label(mail, text="MESSAGE :")
        label_message.place(x=50, y=300, width=100)
        text_message = Text(mail)
        text_message.place(x=150, y=140, width=500)
        yscroll = Scrollbar(mail, command=text_message.yview, orient=VERTICAL)
        yscroll.grid(row=300, column=135)
        text_message.configure(yscrollcommand=yscroll.set)
        bouton_retour = Button(mail, text="Retour", command=lambda: retour_mail())
        bouton_retour.place(x=30, y=560, width=90)
        bouton_test = Button(mail, text="Envoyer un test", command=lambda: mail_test())
        bouton_test.place(x=350, y=560, width=130)
        bouton_run = Button(mail, text="Envoyer", command=lambda: envoyer())
        bouton_run.place(x=685, y=560, width=90)
        mail.mainloop()


    listbox1 = Listbox(choix, width=30, height=10)
    listbox1.place(x=200, y=90, width=400)
    nom_du_fichier = entry_file.get()
    try:
        f = open(nom_du_fichier + ".csv", "x")
    except IOError:
        print
        'file already exists'
        nom_du_fichier = open(nom_du_fichier + ".csv", "r")
        lignes = nom_du_fichier.readlines()
        for ligne in lignes:
            listbox1.insert(END, ligne)
        nom_du_fichier.close()

    yscroll = Scrollbar(command=listbox1.yview, orient=VERTICAL)
    yscroll.grid(row=0, column=1, sticky=N + S)
    listbox1.configure(yscrollcommand=yscroll.set)

    enter1 = Entry(choix, width=20)
    enter1.insert(0, '')
    enter1.place(x=200, y=255, width=400)

    button = Button(choix, text='Ajouter', command=lambda: ajout_mail(entry_file, enter1))
    button.place(x=200, y=275, width=400)

    button1 = Button(choix, text='Supprimer', command=lambda: supprimer_mail(entry_file))
    button1.place(x=200, y=300, width=400)

    button3 = Button(choix, text='Retour', command=lambda: revenir_nom_du_fichier())
    button3.place(x=30, y=350, width=50)

    button4 = Button(choix, text='Import CSV', command=lambda: import_csv(entry_file))
    button4.place(x=200, y=50, width=80)

    button5 = Button(choix, text='Suppression des doublons', command=lambda: supp_doublon(entry_file))
    button5.place(x=325, y=50, width=150)

    button6 = Button(choix, text='Suivant', command=lambda: fenetre_mail(entry_file))
    button6.place(x=690, y=350, width=80)

    button7 = Button(choix, text='Import URL', command=lambda: crawl_une_page())
    button7.place(x=520, y=50, width=80)
    choix.mainloop()

campagne = Tk()
campagne.title("Application de mailing")
campagne.resizable(width=FALSE, height=False)
campagne.geometry('400x200+450+200')

entry_file = StringVar()
entry_file = Entry(campagne, textvariable=entry_file, justify='center')
entry_file.place(x=148, y=50, width=110)

label_de_campagne = StringVar()
label_de_campagne = Label(campagne, text="Nom de la Campagne", justify='center')
label_de_campagne.place(x=142, y=30)

bouton_lancer = Button(campagne, text="Run", command=lambda: main(entry_file))
bouton_lancer.pack(side=BOTTOM, pady=10, padx=10)
bouton_lancer.place(x='185', y='75')

os.chdir("C:/Users/zahra/PycharmProjects/naoyade/venv\Scripts\python")
campagne.deiconify()
campagne.mainloop()