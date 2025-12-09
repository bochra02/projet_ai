"""
=========================================================
  Application Diagnostic Médical CLINICONE
  
  Description :
      - Diagnostic grippe / rhume
      - Diagnostic maladie cardiaque
      - Calculateurs médicaux (IMC, Surface Corporelle)
      - Certificats médicaux (PDF avec logo)
      - Multi-langues (FR/AR/EN)
      - Historique patients (protégé par MDP)
      - Génération de rapports PDF avec alertes et détails
      - Interface graphique CustomTkinter (Dark + Vert)
=========================================================
"""

import customtkinter as ctk
from tkinter import messagebox
from sklearn.tree import DecisionTreeClassifier
import numpy as np
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from datetime import datetime
import warnings
import math

# Supprimer les warnings de type UserWarning
warnings.filterwarnings("ignore", category=UserWarning)

# =========================
# CONFIG UI NOIR + VERT
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

# =========================
# SYSTÈME MULTI-LANGUES
# =========================
LANGUES = {
    "fr": {
        "titre_principal": "Système de Diagnostic Médical",
        "diagnostic_grippe": "Diagnostic Grippe / Rhume",
        "diagnostic_coeur": "Diagnostic Maladie Cardiaque",
        "calculateurs": "Calculateurs Médicaux",
        "certificats": "Certificats Médicaux",
        "historique": "Historique Patients",
        "symptomes": "Sélectionnez vos symptômes :",
        "fievre": "Fièvre",
        "fatigue": "Fatigue",
        "toux": "Toux",
        "courbatures": "Courbatures",
        "diagnostiquer": "Diagnostiquer",
        "reinitialiser": "Réinitialiser",
        "imprimer": "Imprimer le Rapport",
        "nom": "Nom",
        "prenom": "Prénom",
        "date_naissance": "Date de naissance",
        "adresse": "Adresse",
        "age": "Âge",
        "generer_pdf": "Générer PDF",
        "attention": "Attention",
        "remplir_champs": "Veuillez remplir tous les champs !",
        "cocher_symptome": "Veuillez cocher au moins un symptôme !",
        "succes": "Succès",
        "pdf_genere": "PDF généré avec succès !",
        "grippe_detecte": "✅ Grippe",
        "rhume_detecte": "✅ Rhume",
        "conseil_grippe": "Il est conseillé de consulter un médecin si les symptômes persistent.",
        "conseil_rhume": "Repos et hydratation recommandés.",
        "parametres_cardiaques": "Entrez les paramètres cardiaques :",
        "maladie_cardiaque": "❤️ Maladie Cardiaque",
        "coeur_sain": "✅ Cœur sain",
        "msg_maladie": "Maladie cardiaque détectée.",
        "msg_sain": "Continuez un mode de vie sain.",
        "nombres_valides": "Veuillez remplir tous les champs avec des nombres valides !",
        # Calculateurs
        "titre_calculateurs": "Calculateurs Médicaux",
        "imc": "IMC (Indice de Masse Corporelle)",
        "surface_corporelle": "Surface Corporelle",
        "poids": "Poids (kg)",
        "taille": "Taille (cm)",
        "taille_m": "Taille (m)",
        "calculer": "Calculer",
        "resultat": "Résultat",
        # Certificats
        "titre_certificats": "Certificats Médicaux",
        "type_certificat": "Type de certificat",
        "arret_travail": "Arrêt de Travail",
        "aptitude_sport": "Aptitude au Sport",
        "certificat_general": "Certificat Médical Général",
        "certificat_non_contagion": "Certificat de Non-Contagion",
        "date_debut": "Date début",
        "date_fin": "Date fin",
        "type_sport": "Type de sport",
        "motif": "Motif",
        "pathologie": "Pathologie",
        # Historique
        "titre_historique": "Historique des Patients",
        "acces_securise": "🔒 Accès Sécurisé",
        "info_mdp": "ℹ️ Mot de passe : admin",
        "entrer_mdp": "Entrez le mot de passe :",
        "valider": "Valider",
        "annuler": "Annuler",
        "mdp_incorrect": "⚠️ Mot de passe incorrect !",
        "liste_patients": "Liste des patients de la session :",
        "aucun_patient": "Aucun patient enregistré dans cette session.",
        "imprimer_historique": "Imprimer Historique (PDF)",
        "fermer": "Fermer",
    },
    "ar": {
        "titre_principal": "نظام التشخيص الطبي",
        "diagnostic_grippe": "تشخيص الأنفلونزا / الزكام",
        "diagnostic_coeur": "تشخيص أمراض القلب",
        "calculateurs": "الحاسبات الطبية",
        "certificats": "الشهادات الطبية",
        "historique": "سجل المرضى",
        "symptomes": "اختر الأعراض:",
        "fievre": "حمى",
        "fatigue": "تعب",
        "toux": "سعال",
        "courbatures": "آلام العضلات",
        "diagnostiquer": "تشخيص",
        "reinitialiser": "إعادة تعيين",
        "imprimer": "طباعة التقرير",
        "nom": "الاسم",
        "prenom": "اللقب",
        "date_naissance": "تاريخ الميلاد",
        "adresse": "العنوان",
        "age": "العمر",
        "generer_pdf": "إنشاء PDF",
        "attention": "تنبيه",
        "remplir_champs": "يرجى ملء جميع الحقول!",
        "cocher_symptome": "يرجى اختيار عرض واحد على الأقل!",
        "succes": "نجح",
        "pdf_genere": "تم إنشاء PDF بنجاح!",
        "grippe_detecte": "✅ أنفلونزا",
        "rhume_detecte": "✅ زكام",
        "conseil_grippe": "يُنصح باستشارة الطبيب إذا استمرت الأعراض.",
        "conseil_rhume": "يوصى بالراحة والترطيب.",
        "parametres_cardiaques": "أدخل المعايير القلبية:",
        "maladie_cardiaque": "❤️ مرض قلبي",
        "coeur_sain": "✅ قلب سليم",
        "msg_maladie": "تم اكتشاف مرض قلبي.",
        "msg_sain": "استمر في نمط حياة صحي.",
        "nombres_valides": "يرجى ملء جميع الحقول بأرقام صحيحة!",
        # Calculateurs
        "titre_calculateurs": "الحاسبات الطبية",
        "imc": "مؤشر كتلة الجسم",
        "surface_corporelle": "مساحة سطح الجسم",
        "poids": "الوزن (كغ)",
        "taille": "الطول (سم)",
        "taille_m": "الطول (م)",
        "calculer": "حساب",
        "resultat": "النتيجة",
        # Certificats
        "titre_certificats": "الشهادات الطبية",
        "type_certificat": "نوع الشهادة",
        "arret_travail": "شهادة توقف عن العمل",
        "aptitude_sport": "شهادة لياقة رياضية",
        "certificat_general": "شهادة طبية عامة",
        "certificat_non_contagion": "شهادة عدم عدوى",
        "date_debut": "تاريخ البداية",
        "date_fin": "تاريخ النهاية",
        "type_sport": "نوع الرياضة",
        "motif": "السبب",
        "pathologie": "المرض",
        # Historique
        "titre_historique": "سجل المرضى",
        "acces_securise": "🔒 دخول آمن",
        "info_mdp": "ℹ️ كلمة المرور : admin",
        "entrer_mdp": "أدخل كلمة المرور:",
        "valider": "تأكيد",
        "annuler": "إلغاء",
        "mdp_incorrect": "⚠️ كلمة مرور خاطئة!",
        "liste_patients": "قائمة مرضى الجلسة:",
        "aucun_patient": "لا يوجد مرضى مسجلون في هذه الجلسة.",
        "imprimer_historique": "طباعة السجل (PDF)",
        "fermer": "إغلاق",
    },
    "en": {
        "titre_principal": "Medical Diagnostic System",
        "diagnostic_grippe": "Flu / Cold Diagnosis",
        "diagnostic_coeur": "Heart Disease Diagnosis",
        "calculateurs": "Medical Calculators",
        "certificats": "Medical Certificates",
        "historique": "Patient History",
        "symptomes": "Select your symptoms:",
        "fievre": "Fever",
        "fatigue": "Fatigue",
        "toux": "Cough",
        "courbatures": "Body aches",
        "diagnostiquer": "Diagnose",
        "reinitialiser": "Reset",
        "imprimer": "Print Report",
        "nom": "Last Name",
        "prenom": "First Name",
        "date_naissance": "Date of Birth",
        "adresse": "Address",
        "age": "Age",
        "generer_pdf": "Generate PDF",
        "attention": "Warning",
        "remplir_champs": "Please fill in all fields!",
        "cocher_symptome": "Please check at least one symptom!",
        "succes": "Success",
        "pdf_genere": "PDF generated successfully!",
        "grippe_detecte": "✅ Flu",
        "rhume_detecte": "✅ Cold",
        "conseil_grippe": "It is advisable to consult a doctor if symptoms persist.",
        "conseil_rhume": "Rest and hydration recommended.",
        "parametres_cardiaques": "Enter cardiac parameters:",
        "maladie_cardiaque": "❤️ Heart Disease",
        "coeur_sain": "✅ Healthy Heart",
        "msg_maladie": "Heart disease detected.",
        "msg_sain": "Continue a healthy lifestyle.",
        "nombres_valides": "Please fill in all fields with valid numbers!",
        # Calculateurs
        "titre_calculateurs": "Medical Calculators",
        "imc": "BMI (Body Mass Index)",
        "surface_corporelle": "Body Surface Area",
        "poids": "Weight (kg)",
        "taille": "Height (cm)",
        "taille_m": "Height (m)",
        "calculer": "Calculate",
        "resultat": "Result",
        # Certificats
        "titre_certificats": "Medical Certificates",
        "type_certificat": "Certificate type",
        "arret_travail": "Work Leave Certificate",
        "aptitude_sport": "Sports Fitness Certificate",
        "certificat_general": "General Medical Certificate",
        "certificat_non_contagion": "Non-Contagion Certificate",
        "date_debut": "Start date",
        "date_fin": "End date",
        "type_sport": "Sport type",
        "motif": "Reason",
        "pathologie": "Pathology",
        # Historique
        "titre_historique": "Patient History",
        "acces_securise": "🔒 Secure Access",
        "info_mdp": "ℹ️ Password: admin",
        "entrer_mdp": "Enter password:",
        "valider": "Validate",
        "annuler": "Cancel",
        "mdp_incorrect": "⚠️ Incorrect password!",
        "liste_patients": "Session patient list:",
        "aucun_patient": "No patients registered in this session.",
        "imprimer_historique": "Print History (PDF)",
        "fermer": "Close",
    }
}

# Langue par défaut
LANGUE_ACTUELLE = "fr"

def t(cle):
    """Fonction de traduction"""
    return LANGUES[LANGUE_ACTUELLE].get(cle, cle)

# =========================
# HISTORIQUE PATIENTS (EN MÉMOIRE)
# =========================
historique_patients = []

def ajouter_patient_historique(nom, prenom, date_naissance, type_diagnostic):
    """Ajoute un patient à l'historique de la session"""
    date_enregistrement = datetime.now().strftime("%d/%m/%Y %H:%M")
    historique_patients.append({
        "nom": nom,
        "prenom": prenom,
        "date_naissance": date_naissance,
        "type": type_diagnostic,
        "date": date_enregistrement
    })

# =========================
# FONCTION PDF AMÉLIORÉE
# =========================
def generer_pdf(nom, prenom, date_naissance, adresse, age, diagnostic, details):
    fichier = f"rapport_{nom}_{prenom}.pdf"
    date = datetime.now().strftime("%d/%m/%Y %H:%M")
    c = canvas.Canvas(fichier, pagesize=A4)
    largeur, hauteur = A4

    try:
        c.drawImage("logo.png", 50, hauteur - 120, width=80, height=60)
    except:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, hauteur - 100, "LOGO")
    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, hauteur - 70, "RAPPORT DE DIAGNOSTIC")

    c.setFont("Helvetica", 12)
    c.drawString(50, hauteur - 160, f"Nom : {nom}    Prénom : {prenom}")
    c.drawString(50, hauteur - 185, f"Date de naissance : {date_naissance}    Adresse : {adresse}")
    c.drawString(50, hauteur - 210, f"Âge : {age}")
    c.drawString(50, hauteur - 235, f"Date du rapport : {date}")

    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, hauteur - 265, "Détails :")
    y = hauteur - 290
    c.setFont("Helvetica", 11)
    for d in details:
        c.drawString(70, y, f"- {d}")
        y -= 18

    c.setFont("Helvetica-Bold", 13)
    c.drawString(50, y - 15, f"RESULTAT : {diagnostic}")

    c.drawString(350, 120, "Signature Médecin")
    c.rect(330, 80, 200, 60)

    c.save()

# =========================
# FONCTION PDF CERTIFICAT
# =========================
def generer_certificat_pdf(nom, prenom, date_naissance, type_cert, donnees_supp):
    fichier = f"certificat_{nom}_{prenom}.pdf"
    date = datetime.now().strftime("%d/%m/%Y")
    c = canvas.Canvas(fichier, pagesize=A4)
    largeur, hauteur = A4

    # Logo
    try:
        c.drawImage("logo.png", 50, hauteur - 120, width=80, height=60)
    except:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, hauteur - 100, "LOGO CLINIQUE")

    # Titre
    c.setFont("Helvetica-Bold", 18)
    c.drawString(180, hauteur - 70, type_cert.upper())

    # Ligne de séparation
    c.line(50, hauteur - 85, largeur - 50, hauteur - 85)

    # Corps du certificat
    c.setFont("Helvetica", 12)
    y = hauteur - 140

    c.drawString(50, y, f"Je soussigné(e), Docteur [Nom du médecin],")
    y -= 25
    c.drawString(50, y, f"certifie avoir examiné ce jour :")
    y -= 30

    c.setFont("Helvetica-Bold", 12)
    c.drawString(70, y, f"Nom : {nom}    Prénom : {prenom}")
    y -= 20
    c.drawString(70, y, f"Date de naissance : {date_naissance}")
    y -= 35

    c.setFont("Helvetica", 12)

    # Contenu spécifique selon le type
    if "Arrêt" in type_cert:
        c.drawString(50, y, f"Nécessite un arrêt de travail du {donnees_supp['date_debut']}")
        y -= 20
        c.drawString(50, y, f"au {donnees_supp['date_fin']} inclus.")
        y -= 25
        c.drawString(50, y, f"Motif : {donnees_supp.get('motif', 'Raison médicale')}")

    elif "Aptitude" in type_cert:
        c.drawString(50, y, f"Est apte à la pratique du sport suivant :")
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, y, donnees_supp.get('sport', 'Sport général'))
        y -= 25
        c.setFont("Helvetica", 12)
        c.drawString(50, y, "Sans contre-indication à ce jour.")

    elif "Non-Contagion" in type_cert:
        c.drawString(50, y, f"Certifie que l'intéressé(e) ne présente aucun signe de")
        y -= 20
        c.drawString(50, y, "contagion lié à la pathologie suivante :")
        y -= 20
        c.setFont("Helvetica-Bold", 12)
        c.drawString(70, y, donnees_supp.get('pathologie', 'Maladie infectieuse'))
        y -= 25
        c.setFont("Helvetica", 12)
        c.drawString(50, y, "Et peut reprendre une activité normale.")

    else:  # Certificat Général
        c.drawString(50, y, "Certifie que l'état de santé de l'intéressé(e) ne présente")
        y -= 20
        c.drawString(50, y, "aucune contre-indication à ce jour.")
        y -= 20
        if donnees_supp.get('motif'):
            c.drawString(50, y, f"Motif : {donnees_supp['motif']}")

    # Date et signature
    c.setFont("Helvetica", 11)
    c.drawString(50, 150, f"Fait à [Ville], le {date}")
    c.drawString(350, 120, "Signature et cachet du médecin")
    c.rect(330, 80, 200, 60)

    c.save()

# =========================
# FONCTION PDF HISTORIQUE
# =========================
def generer_historique_pdf():
    fichier = f"historique_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(fichier, pagesize=A4)
    largeur, hauteur = A4

    try:
        c.drawImage("logo.png", 50, hauteur - 120, width=80, height=60)
    except:
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, hauteur - 100, "LOGO")

    c.setFont("Helvetica-Bold", 16)
    c.drawString(180, hauteur - 70, "HISTORIQUE DES PATIENTS")

    c.setFont("Helvetica", 10)
    c.drawString(50, hauteur - 130, f"Date d'édition : {datetime.now().strftime('%d/%m/%Y %H:%M')}")

    y = hauteur - 170
    c.setFont("Helvetica-Bold", 11)
    c.drawString(50, y, "Nom")
    c.drawString(150, y, "Prénom")
    c.drawString(250, y, "Date Naissance")
    c.drawString(350, y, "Type")
    c.drawString(450, y, "Date Enreg.")
    y -= 5
    c.line(50, y, largeur - 50, y)
    y -= 20

    c.setFont("Helvetica", 10)
    for patient in historique_patients:
        if y < 100:
            c.showPage()
            y = hauteur - 100
        c.drawString(50, y, patient['nom'][:15])
        c.drawString(150, y, patient['prenom'][:15])
        c.drawString(250, y, patient['date_naissance'][:15])
        c.drawString(350, y, patient['type'][:15])
        c.drawString(450, y, patient['date'][:15])
        y -= 18

    c.save()

# =========================
# IA GRIPPE / RHUME
# =========================
Xg = [[1,1,1,1],[1,0,1,0],[0,1,0,1],[1,1,0,1],[0,0,1,0],[0,1,1,1],[1,0,0,0]]
Yg = [1,0,1,1,0,1,0]
model_g = DecisionTreeClassifier()
model_g.fit(Xg, Yg)

def diag_grippe(vals):
    r = model_g.predict(np.array([vals]))
    if r[0] == 1:
        return t("grippe_detecte"), t("conseil_grippe")
    else:
        return t("rhume_detecte"), t("conseil_rhume")

# =========================
# IA COEUR
# =========================
data = pd.read_csv("processed.cleveland.csv")
data = data.replace('?', pd.NA).dropna()

for c in data.columns:
    data[c] = data[c].astype(float)

X = data.drop("target", axis=1)
Y = data["target"].apply(lambda x: 1 if x > 0 else 0)

model_c = DecisionTreeClassifier(max_depth=4)
model_c.fit(X, Y)

def diag_coeur(vals):
    alert = ""
    if vals[3] > 180:
        alert += "⚠ Tension artérielle très élevée\n"
    elif vals[3] > 140:
        alert += "⚠ Tension artérielle élevée\n"
    if vals[4] > 300:
        alert += "⚠ Cholestérol élevé\n"

    r = model_c.predict(np.array([vals]))
    if r[0] == 1:
        msg = t("msg_maladie")
        if alert:
            msg += " " + alert.strip()
        return t("maladie_cardiaque"), msg, alert.strip()
    else:
        return t("coeur_sain"), t("msg_sain"), alert.strip()

# =========================
# APPLICATION PRINCIPALE
# =========================
class DiagnosticApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("CLINICONE - Application Diagnostic Médical")
        self.geometry("600x700")

        # Frame supérieur pour les boutons de langue
        frame_langue = ctk.CTkFrame(self, fg_color="transparent")
        frame_langue.pack(pady=10)

        ctk.CTkLabel(frame_langue, text="🌍", font=("Arial", 18)).pack(side="left", padx=5)
        ctk.CTkButton(frame_langue, text="FR", command=lambda: self.changer_langue("fr"), width=50).pack(side="left", padx=2)
        ctk.CTkButton(frame_langue, text="AR", command=lambda: self.changer_langue("ar"), width=50).pack(side="left", padx=2)
        ctk.CTkButton(frame_langue, text="EN", command=lambda: self.changer_langue("en"), width=50).pack(side="left", padx=2)

        # Titre principal
        self.titre_label = ctk.CTkLabel(self, text=t("titre_principal"), font=("Arial", 22, "bold"))
        self.titre_label.pack(pady=30)

        # Boutons principaux
        self.btn_grippe = ctk.CTkButton(self, text=t("diagnostic_grippe"), command=self.page_grippe, width=350, height=45)
        self.btn_grippe.pack(pady=10)

        self.btn_coeur = ctk.CTkButton(self, text=t("diagnostic_coeur"), command=self.page_coeur, width=350, height=45)
        self.btn_coeur.pack(pady=10)

        self.btn_calculateurs = ctk.CTkButton(self, text=t("calculateurs"), command=self.page_calculateurs, width=350, height=45)
        self.btn_calculateurs.pack(pady=10)

        self.btn_certificats = ctk.CTkButton(self, text=t("certificats"), command=self.page_certificats, width=350, height=45)
        self.btn_certificats.pack(pady=10)

        self.btn_historique = ctk.CTkButton(self, text=t("historique"), command=self.page_historique_login, width=350, height=45)
        self.btn_historique.pack(pady=10)

    def changer_langue(self, langue):
        global LANGUE_ACTUELLE
        LANGUE_ACTUELLE = langue
        self.actualiser_textes()

    def actualiser_textes(self):
        self.titre_label.configure(text=t("titre_principal"))
        self.btn_grippe.configure(text=t("diagnostic_grippe"))
        self.btn_coeur.configure(text=t("diagnostic_coeur"))
        self.btn_calculateurs.configure(text=t("calculateurs"))
        self.btn_certificats.configure(text=t("certificats"))
        self.btn_historique.configure(text=t("historique"))

    # ---------- LOGIN HISTORIQUE ----------
    def page_historique_login(self):
        login_win = ctk.CTkToplevel(self)
        login_win.title(t("acces_securise"))
        login_win.geometry("350x250")
        login_win.lift()
        login_win.focus_force()

        ctk.CTkLabel(login_win, text=t("acces_securise"), font=("Arial", 16, "bold")).pack(pady=15)
        ctk.CTkLabel(login_win, text=t("info_mdp"), font=("Arial", 12), text_color="cyan").pack(pady=5)
        ctk.CTkLabel(login_win, text=t("entrer_mdp"), font=("Arial", 12)).pack(pady=10)

        entry_mdp = ctk.CTkEntry(login_win, show="*", width=200)
        entry_mdp.pack(pady=10)

        def valider_mdp():
            if entry_mdp.get() == "admin":
                login_win.destroy()
                self.page_historique()
            else:
                messagebox.showerror(t("attention"), t("mdp_incorrect"))

        frame_btns = ctk.CTkFrame(login_win, fg_color="transparent")
        frame_btns.pack(pady=15)
        ctk.CTkButton(frame_btns, text=t("valider"), command=valider_mdp, width=120).pack(side="left", padx=5)
        ctk.CTkButton(frame_btns, text=t("annuler"), command=login_win.destroy, width=120).pack(side="left", padx=5)

    # ---------- HISTORIQUE ----------
    def page_historique(self):
        hist_win = ctk.CTkToplevel(self)
        hist_win.title(t("titre_historique"))
        hist_win.geometry("700x500")
        hist_win.lift()
        hist_win.focus_force()

        ctk.CTkLabel(hist_win, text=t("titre_historique"), font=("Arial", 18, "bold")).pack(pady=15)

        frame_liste = ctk.CTkScrollableFrame(hist_win, width=650, height=320)
        frame_liste.pack(pady=10, padx=10)

        if not historique_patients:
            ctk.CTkLabel(frame_liste, text=t("aucun_patient"), font=("Arial", 12)).pack(pady=20)
        else:
            ctk.CTkLabel(frame_liste, text=t("liste_patients"), font=("Arial", 13, "bold")).pack(pady=10)
            for i, patient in enumerate(historique_patients, 1):
                texte = f"{i}. {patient['nom']} {patient['prenom']} - {patient['date_naissance']} - {patient['type']} - {patient['date']}"
                ctk.CTkLabel(frame_liste, text=texte, font=("Arial", 11), anchor="w").pack(pady=3, padx=10, fill="x")

        def imprimer_hist():
            if historique_patients:
                generer_historique_pdf()
                messagebox.showinfo(t("succes"), t("pdf_genere"))
            else:
                messagebox.showwarning(t("attention"), t("aucun_patient"))

        frame_btns = ctk.CTkFrame(hist_win, fg_color="transparent")
        frame_btns.pack(pady=15)
        ctk.CTkButton(frame_btns, text=t("imprimer_historique"), command=imprimer_hist, width=200).pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text=t("fermer"), command=hist_win.destroy, width=120).pack(side="left", padx=10)

    # ---------- CALCULATEURS ----------
    def page_calculateurs(self):
        calc_win = ctk.CTkToplevel(self)
        calc_win.title(t("titre_calculateurs"))
        calc_win.geometry("550x500")
        calc_win.lift()
        calc_win.focus_force()

        ctk.CTkLabel(calc_win, text=t("titre_calculateurs"), font=("Arial", 18, "bold")).pack(pady=15)

        # Sélection du type de calcul
        type_var = ctk.StringVar(value="imc")
        frame_choix = ctk.CTkFrame(calc_win)
        frame_choix.pack(pady=10)

        ctk.CTkRadioButton(frame_choix, text=t("imc"), variable=type_var, value="imc").pack(side="left", padx=10)
        ctk.CTkRadioButton(frame_choix, text=t("surface_corporelle"), variable=type_var, value="surface").pack(side="left", padx=10)

        # Frame pour les entrées
        frame_inputs = ctk.CTkFrame(calc_win)
        frame_inputs.pack(pady=20, padx=20)

        ctk.CTkLabel(frame_inputs, text=t("poids"), font=("Arial", 12)).grid(row=0, column=0, pady=5, padx=10, sticky="w")
        entry_poids = ctk.CTkEntry(frame_inputs, width=150)
        entry_poids.grid(row=0, column=1, pady=5, padx=10)

        ctk.CTkLabel(frame_inputs, text=t("taille"), font=("Arial", 12)).grid(row=1, column=0, pady=5, padx=10, sticky="w")
        entry_taille = ctk.CTkEntry(frame_inputs, width=150)
        entry_taille.grid(row=1, column=1, pady=5, padx=10)

        # Frame résultat
        result_label = ctk.CTkLabel(calc_win, text="", font=("Arial", 14, "bold"))
        result_label.pack(pady=20)

        def calculer():
            try:
                poids = float(entry_poids.get())
                taille = float(entry_taille.get())

                if type_var.get() == "imc":
                    # IMC = poids / (taille en m)²
                    taille_m = taille / 100
                    imc = poids / (taille_m ** 2)
                    
                    # Interprétation
                    if imc < 18.5:
                        interpretation = "Insuffisance pondérale"
                        couleur = "orange"
                    elif 18.5 <= imc < 25:
                        interpretation = "Poids normal"
                        couleur = "green"
                    elif 25 <= imc < 30:
                        interpretation = "Surpoids"
                        couleur = "orange"
                    else:
                        interpretation = "Obésité"
                        couleur = "red"
                    
                    result_label.configure(
                        text=f"IMC : {imc:.2f}\n{interpretation}",
                        text_color=couleur
                    )

                else:  # Surface corporelle
                    # Formule de Mosteller : √(poids × taille / 3600)
                    surface = math.sqrt((poids * taille) / 3600)
                    result_label.configure(
                        text=f"Surface corporelle :\n{surface:.2f} m²",
                        text_color="cyan"
                    )

            except ValueError:
                messagebox.showwarning(t("attention"), t("nombres_valides"))

        def reset():
            entry_poids.delete(0, ctk.END)
            entry_taille.delete(0, ctk.END)
            result_label.configure(text="")

        frame_btns = ctk.CTkFrame(calc_win, fg_color="transparent")
        frame_btns.pack(pady=15)
        ctk.CTkButton(frame_btns, text=t("calculer"), command=calculer, width=150).pack(side="left", padx=10)
        ctk.CTkButton(frame_btns, text=t("reinitialiser"), command=reset, width=150).pack(side="left", padx=10)

    # ---------- CERTIFICATS ----------
    def page_certificats(self):
        cert_win = ctk.CTkToplevel(self)
        cert_win.title(t("titre_certificats"))
        cert_win.geometry("600x650")
        cert_win.lift()
        cert_win.focus_force()

        ctk.CTkLabel(cert_win, text=t("titre_certificats"), font=("Arial", 18, "bold")).pack(pady=15)

        # Sélection du type
        ctk.CTkLabel(cert_win, text=t("type_certificat"), font=("Arial", 12)).pack(pady=5)
        type_cert = ctk.CTkComboBox(
            cert_win,
            values=[
                t("arret_travail"),
                t("aptitude_sport"),
                t("certificat_general"),
                t("certificat_non_contagion")
            ],
            width=400
        )
        type_cert.pack(pady=5)
        type_cert.set(t("certificat_general"))

        # Frame pour les champs communs
        frame_commun = ctk.CTkFrame(cert_win)
        frame_commun.pack(pady=10, padx=20)

        ctk.CTkLabel(frame_commun, text=t("nom")).grid(row=0, column=0, pady=5, padx=10, sticky="w")
        entry_nom = ctk.CTkEntry(frame_commun, width=200)
        entry_nom.grid(row=0, column=1, pady=5, padx=10)

        ctk.CTkLabel(frame_commun, text=t("prenom")).grid(row=1, column=0, pady=5, padx=10, sticky="w")
        entry_prenom = ctk.CTkEntry(frame_commun, width=200)
        entry_prenom.grid(row=1, column=1, pady=5, padx=10)

        ctk.CTkLabel(frame_commun, text=t("date_naissance")).grid(row=2, column=0, pady=5, padx=10, sticky="w")
        entry_date_naiss = ctk.CTkEntry(frame_commun, width=200)
        entry_date_naiss.grid(row=2, column=1, pady=5, padx=10)

        # Frame pour champs spécifiques
        frame_spec = ctk.CTkFrame(cert_win)
        frame_spec.pack(pady=10, padx=20)

        # Champs spécifiques (initialement cachés)
        label_date_debut = ctk.CTkLabel(frame_spec, text=t("date_debut"))
        entry_date_debut = ctk.CTkEntry(frame_spec, width=150)

        label_date_fin = ctk.CTkLabel(frame_spec, text=t("date_fin"))
        entry_date_fin = ctk.CTkEntry(frame_spec, width=150)

        label_sport = ctk.CTkLabel(frame_spec, text=t("type_sport"))
        entry_sport = ctk.CTkEntry(frame_spec, width=200)

        label_motif = ctk.CTkLabel(frame_spec, text=t("motif"))
        entry_motif = ctk.CTkEntry(frame_spec, width=200)

        label_pathologie = ctk.CTkLabel(frame_spec, text=t("pathologie"))
        entry_pathologie = ctk.CTkEntry(frame_spec, width=200)

        def afficher_champs(*args):
            # Cacher tous les champs
            for widget in frame_spec.winfo_children():
                widget.grid_forget()

            type_selectionne = type_cert.get()

            if t("arret_travail") in type_selectionne:
                label_date_debut.grid(row=0, column=0, pady=5, padx=10, sticky="w")
                entry_date_debut.grid(row=0, column=1, pady=5, padx=10)
                label_date_fin.grid(row=1, column=0, pady=5, padx=10, sticky="w")
                entry_date_fin.grid(row=1, column=1, pady=5, padx=10)
                label_motif.grid(row=2, column=0, pady=5, padx=10, sticky="w")
                entry_motif.grid(row=2, column=1, pady=5, padx=10)

            elif t("aptitude_sport") in type_selectionne:
                label_sport.grid(row=0, column=0, pady=5, padx=10, sticky="w")
                entry_sport.grid(row=0, column=1, pady=5, padx=10)

            elif t("certificat_non_contagion") in type_selectionne:
                label_pathologie.grid(row=0, column=0, pady=5, padx=10, sticky="w")
                entry_pathologie.grid(row=0, column=1, pady=5, padx=10)

            elif t("certificat_general") in type_selectionne:
                label_motif.grid(row=0, column=0, pady=5, padx=10, sticky="w")
                entry_motif.grid(row=0, column=1, pady=5, padx=10)

        type_cert.configure(command=afficher_champs)
        afficher_champs()

        def generer_cert():
            nom = entry_nom.get()
            prenom = entry_prenom.get()
            date_naiss = entry_date_naiss.get()

            if not (nom and prenom and date_naiss):
                messagebox.showwarning(t("attention"), t("remplir_champs"))
                return

            type_selectionne = type_cert.get()
            donnees_supp = {}

            if t("arret_travail") in type_selectionne:
                donnees_supp['date_debut'] = entry_date_debut.get()
                donnees_supp['date_fin'] = entry_date_fin.get()
                donnees_supp['motif'] = entry_motif.get()
                if not (donnees_supp['date_debut'] and donnees_supp['date_fin']):
                    messagebox.showwarning(t("attention"), t("remplir_champs"))
                    return

            elif t("aptitude_sport") in type_selectionne:
                donnees_supp['sport'] = entry_sport.get()
                if not donnees_supp['sport']:
                    messagebox.showwarning(t("attention"), t("remplir_champs"))
                    return

            elif t("certificat_non_contagion") in type_selectionne:
                donnees_supp['pathologie'] = entry_pathologie.get()
                if not donnees_supp['pathologie']:
                    messagebox.showwarning(t("attention"), t("remplir_champs"))
                    return

            elif t("certificat_general") in type_selectionne:
                donnees_supp['motif'] = entry_motif.get()

            generer_certificat_pdf(nom, prenom, date_naiss, type_selectionne, donnees_supp)
            ajouter_patient_historique(nom, prenom, date_naiss, f"Certificat: {type_selectionne}")
            messagebox.showinfo(t("succes"), t("pdf_genere"))

        ctk.CTkButton(cert_win, text=t("generer_pdf"), command=generer_cert, width=250, height=40).pack(pady=20)

    # ---------- Partie Grippe/Rhume ----------
    def page_grippe(self):
        fen = ctk.CTkToplevel(self)
        fen.title(t("diagnostic_grippe"))
        fen.geometry("450x400")
        fen.lift()
        fen.focus_force()

        ctk.CTkLabel(fen, text=t("symptomes"), font=("Arial", 14, "bold")).pack(pady=10)
        frame = ctk.CTkFrame(fen)
        frame.pack(pady=10, padx=10)

        self.vars_grippe = [ctk.IntVar() for _ in range(4)]
        labels = [t("fievre"), t("fatigue"), t("toux"), t("courbatures")]
        for lab, v in zip(labels, self.vars_grippe):
            ctk.CTkCheckBox(frame, text=lab, variable=v).pack(anchor="w", pady=5)

        result_label = ctk.CTkLabel(fen, text="", font=("Arial", 12, "bold"))
        result_label.pack(pady=15)

        def lancer():
            vals = [v.get() for v in self.vars_grippe]
            if sum(vals) == 0:
                messagebox.showwarning(t("attention"), t("cocher_symptome"))
            else:
                res, exp = diag_grippe(vals)
                color = "red" if t("grippe_detecte") in res else "green"
                result_label.configure(text=f"{res}\n{exp}", text_color=color)

        def reset():
            for v in self.vars_grippe:
                v.set(0)
            result_label.configure(text="")

        def imprimer():
            popup = ctk.CTkToplevel(fen)
            popup.geometry("300x300")
            n = ctk.CTkEntry(popup, placeholder_text=t("nom"))
            p = ctk.CTkEntry(popup, placeholder_text=t("prenom"))
            d_n = ctk.CTkEntry(popup, placeholder_text=t("date_naissance"))
            adr = ctk.CTkEntry(popup, placeholder_text=t("adresse"))
            age_entry = ctk.CTkEntry(popup, placeholder_text=t("age"))
            n.pack(pady=5); p.pack(pady=5); d_n.pack(pady=5); adr.pack(pady=5); age_entry.pack(pady=5)

            def valider():
                if not (n.get() and p.get() and d_n.get() and adr.get() and age_entry.get()):
                    messagebox.showwarning(t("attention"), t("remplir_champs"))
                    return
                details = [f"{labels[i]} : {'Oui' if self.vars_grippe[i].get() else 'Non'}" for i in range(4)]
                generer_pdf(n.get(), p.get(), d_n.get(), adr.get(), age_entry.get(), result_label.cget("text"), details)
                ajouter_patient_historique(n.get(), p.get(), d_n.get(), "Diagnostic Grippe/Rhume")
                messagebox.showinfo(t("succes"), t("pdf_genere"))

            ctk.CTkButton(popup, text=t("generer_pdf"), command=valider).pack(pady=10)

        ctk.CTkButton(fen, text=t("diagnostiquer"), command=lancer, width=200, height=40).pack(pady=(10,5))
        ctk.CTkButton(fen, text=t("reinitialiser"), command=reset, width=200, height=40).pack(pady=(0,5))
        ctk.CTkButton(fen, text=t("imprimer"), command=imprimer, width=200, height=40).pack(pady=(0,10))

    # ---------- Partie Cardiaque ----------
    def page_coeur(self):
        fen = ctk.CTkToplevel(self)
        fen.title(t("diagnostic_coeur"))
        fen.geometry("700x650")
        fen.lift()
        fen.focus_force()

        ctk.CTkLabel(fen, text=t("parametres_cardiaques"), font=("Arial", 14, "bold")).pack(pady=10)
        frame = ctk.CTkFrame(fen)
        frame.pack(pady=5, padx=10)

        self.entries_coeur = []
        champs = X.columns.tolist()

        for i, champ in enumerate(champs):
            row = i // 2
            col = i % 2
            ctk.CTkLabel(frame, text=champ).grid(row=row*2, column=col, sticky="w", padx=5, pady=1)
            e = ctk.CTkEntry(frame, width=150)
            e.grid(row=row*2+1, column=col, padx=5, pady=1)
            self.entries_coeur.append(e)

        result_label = ctk.CTkLabel(fen, text="", font=("Arial", 12, "bold"))
        result_label.pack(pady=(10,5))

        def lancer_coeur():
            try:
                vals = [float(e.get()) for e in self.entries_coeur]
                res, exp, alert = diag_coeur(vals)
                color = "red" if t("maladie_cardiaque") in res else "green"
                result_label.configure(text=f"{res}\n{exp}", text_color=color)
            except ValueError:
                messagebox.showwarning(t("attention"), t("nombres_valides"))

        def reset_coeur():
            for e in self.entries_coeur:
                e.delete(0, ctk.END)
            result_label.configure(text="")

        def imprimer_coeur():
            popup = ctk.CTkToplevel(fen)
            popup.geometry("350x350")
            n = ctk.CTkEntry(popup, placeholder_text=t("nom"))
            p = ctk.CTkEntry(popup, placeholder_text=t("prenom"))
            d_n = ctk.CTkEntry(popup, placeholder_text=t("date_naissance"))
            adr = ctk.CTkEntry(popup, placeholder_text=t("adresse"))
            n.pack(pady=5); p.pack(pady=5); d_n.pack(pady=5); adr.pack(pady=5)

            def valider():
                if not (n.get() and p.get() and d_n.get() and adr.get()):
                    messagebox.showwarning(t("attention"), t("remplir_champs"))
                    return
                details = [f"{champs[i]} : {self.entries_coeur[i].get()}" for i in range(len(champs))]
                _, _, alert = diag_coeur([float(e.get()) for e in self.entries_coeur])
                if alert:
                    details.append("Alertes : " + alert)
                age = self.entries_coeur[0].get()
                generer_pdf(n.get(), p.get(), d_n.get(), adr.get(), age, result_label.cget("text"), details)
                ajouter_patient_historique(n.get(), p.get(), d_n.get(), "Diagnostic Cardiaque")
                messagebox.showinfo(t("succes"), t("pdf_genere"))

            ctk.CTkButton(popup, text=t("generer_pdf"), command=valider).pack(pady=10)

        ctk.CTkButton(fen, text=t("diagnostiquer"), command=lancer_coeur, width=250, height=40).pack(pady=(5,3))
        ctk.CTkButton(fen, text=t("reinitialiser"), command=reset_coeur, width=250, height=40).pack(pady=(0,3))
        ctk.CTkButton(fen, text=t("imprimer"), command=imprimer_coeur, width=250, height=40).pack(pady=(0,10))

# =========================
# LANCEMENT DE L'APPLICATION
# =========================
if __name__ == "__main__":
    app = DiagnosticApp()
    app.mainloop()