# reservation.py
from tkinter import *
from tkinter import ttk, messagebox
from datetime import date
from PIL import Image, ImageTk, ImageOps
import customtkinter as ctk
import os
import csv
import pandas as pd

import home
import payment
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
def main(user=None):
    fenetre = Tk()
    fenetre.title("Système de Réservation Sportive")
    fenetre.configure(bg="white")
    fenetre.state("zoomed")
    fenetre.bind("<Escape>", lambda e: fenetre.attributes("-fullscreen", False))

    reservations_list = []

    # ------------------------------
    # BOUTON RETOUR
    # ------------------------------
    def go_back():
        fenetre.destroy()
        home.main(user)

    btn_retour = ctk.CTkButton(
        fenetre,
        text="⟵ Retour",
        fg_color="#1C9273",
        text_color="white",
        corner_radius=15,
        width=120,
        height=40,
        font=("Arial", 14, "bold"),
        command=go_back
    )
    btn_retour.pack(anchor="nw", padx=20, pady=20)

    # ------------------------------
    # FRAME 1 – Choix du terrain
    # ------------------------------
    frame1_outer = LabelFrame(
        fenetre, text="Choisissez un terrain/salle",
        font=("Arial", 12, "bold"), bg="white"
    )
    frame1_outer.pack(pady=10, padx=10, fill="x")

    canvas = Canvas(frame1_outer, height=260, bg="white", highlightthickness=0)
    canvas.pack(side=LEFT, fill=X, expand=True)

    scrollbar = Scrollbar(frame1_outer, orient=HORIZONTAL, command=canvas.xview)
    scrollbar.pack(side=BOTTOM, fill=X)
    canvas.configure(xscrollcommand=scrollbar.set)

    frame1 = Frame(canvas, bg="white")
    canvas.create_window((0, 0), window=frame1, anchor="nw")

    terrain = StringVar(value="")
    terrains = [
        ("Terrain de Football", "foot.jpg"),
        ("Terrain de Basketball", "basketball.jpg"),
        ("Terrain de Tennis", "tennis.jpg"),
        ("Salle de Handball", "handball.jpg"),
        ("Terrain de Padel", "padel.jpg")
    ]

    photo_refs = []  # garder les images en mémoire

    # fonction de sélection avec surbrillance
    selected_frame = [None]  # variable mutable pour référence

    def select_terrain(name, frame_img):
        terrain.set(name)
        # retirer contour des anciens
        if selected_frame[0]:
            selected_frame[0].config(highlightthickness=0)
        # mettre contour vert
        frame_img.config(highlightbackground="green", highlightthickness=4)
        selected_frame[0] = frame_img

    # création des frames terrains
    for i, (name, filename) in enumerate(terrains):
        try:
            img_path = os.path.join(os.path.dirname(__file__), "Pictures", filename)
            img = Image.open(img_path).convert("RGBA").resize((220, 160), Image.LANCZOS)
            photo = ImageTk.PhotoImage(img)
        except:
            photo = None
        photo_refs.append(photo)

        frame_img = Frame(frame1, bg="#F77F00", padx=8, pady=8)
        frame_img.grid(row=0, column=i, padx=20, pady=10)

        if photo:
            lbl_img = Label(frame_img, image=photo, bg="#F77F00", cursor="hand2")
            lbl_img.image = photo
            lbl_img.pack()
        else:
            lbl_img = Label(frame_img, text="Image\nnon trouvée", bg="#F77F00", width=28, height=10)
            lbl_img.pack()

        rb = Radiobutton(
            frame_img, text="", variable=terrain, value=name,
            bg="#F77F00", fg="white", activebackground="#F77F00",
            selectcolor="#ffffff", indicatoron=1
        )
        rb.pack(pady=(8, 2))

        Label(frame_img, text=name, font=("Arial", 12, "bold"),
              bg="#F77F00", wraplength=220, justify="center").pack(pady=(2, 6))

        # clic sur image ou frame sélectionne le terrain
        def make_on_click(n=name, f=frame_img):
            return lambda e: select_terrain(n, f)

        lbl_img.bind("<Button-1>", make_on_click())
        frame_img.bind("<Button-1>", make_on_click())

    frame1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox("all"))

    # ------------------------------
    # FRAME 2 – Formulaire
    # ------------------------------
    frame2 = LabelFrame(
        fenetre, text="Formulaire de Réservation",
        font=("Arial", 12, "bold"), bg="white"
    )
    frame2.pack(pady=10, padx=10, fill="x")

    frame2.grid_columnconfigure(1, weight=1)

    Label(frame2, text="Nom complet :", font=("Arial", 11),
          bg="white").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    nom_entry = ctk.CTkEntry(
        frame2, width=300, height=35, corner_radius=10,
        fg_color="#f2f2f2", text_color="black",
        placeholder_text="Nom complet", font=("Arial", 12)
    )
    nom_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")

    Label(frame2, text="Date de réservation :", font=("Arial", 11),
          bg="white").grid(row=1, column=0, padx=10, pady=5, sticky="w")
    date_entry = ctk.CTkEntry(
        frame2, width=300, height=35, corner_radius=10,
        fg_color="#f2f2f2", text_color="black",
        placeholder_text="JJ/MM/AAAA", font=("Arial", 12)
    )
    date_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
    date_entry.insert(0, date.today().strftime("%d/%m/%Y"))

    Label(frame2, text="Heure :", font=("Arial", 11),
          bg="white").grid(row=2, column=0, padx=10, pady=5, sticky="w")
    hours = ["08:00-10:00", "10:00-12:00", "14:00-16:00",
             "16:00-18:00", "18:00-20:00", "20:00-22:00", "23:00-01:00"]
    heure_combo = ctk.CTkComboBox(frame2, values=hours, width=300, height=35,
                                  corner_radius=10, font=("Arial", 12))
    heure_combo.grid(row=2, column=1, padx=10, pady=5, sticky="w")

    Label(frame2, text="Forfait :", font=("Arial", 11), bg="white").grid(row=3, column=0, padx=10, pady=5, sticky="w")
    forfait_var = StringVar(value="Standard")
    forfait_combo = ctk.CTkComboBox(frame2, values=["Standard", "Premium", "VIP"],
                                     width=300, height=35, corner_radius=10, variable=forfait_var)
    forfait_combo.grid(row=3, column=1, padx=10, pady=5, sticky="w")

    # Additional Options
    Label(frame2, text="Options supplémentaires :", font=("Arial", 11), bg="white").grid(row=4, column=0, padx=10, pady=5, sticky="w")
    options_frame = Frame(frame2, bg="white")
    options_frame.grid(row=4, column=1, padx=10, pady=5, sticky="w")

    equipment_var = IntVar()
    coaching_var = IntVar()

    ctk.CTkCheckBox(options_frame, text="Location d'équipement (+5 TND)", variable=equipment_var, text_color="black").pack(anchor="w")
    ctk.CTkCheckBox(options_frame, text="Coaching personnel (+10 TND)", variable=coaching_var, text_color="black").pack(anchor="w")

    csv_file = os.path.join(os.path.dirname(__file__), "reservations.csv")

    # ------------------------------
    # FONCTIONS CRUD
    # ------------------------------
    def find_alternatives(date_r, heure, terr):
        alternatives = []
        # Suggest next available time for same terrain
        current_index = hours.index(heure) if heure in hours else 0
        for i in range(current_index + 1, len(hours)):
            next_heure = hours[i]
            conflict = any(res["date"] == date_r and res["heure"] == next_heure and res["terrain"] == terr for res in reservations_list)
            if not conflict:
                alternatives.append(f"{terr} à {next_heure}")
                break

        # Suggest alternative terrains at same time
        terrains_list = [t[0] for t in terrains]
        for alt_terr in terrains_list:
            if alt_terr != terr:
                conflict = any(res["date"] == date_r and res["heure"] == heure and res["terrain"] == alt_terr for res in reservations_list)
                if not conflict:
                    alternatives.append(f"{alt_terr} à {heure}")
                    break
        return alternatives

    def modifier_reservation():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une réservation à modifier.")
            return
        # For simplicity, just show a message
        messagebox.showinfo("Modifier", "Fonction de modification à implémenter.")

    def supprimer_reservation():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Sélection", "Veuillez sélectionner une réservation à supprimer.")
            return
        if messagebox.askyesno("Confirmer", "Êtes-vous sûr de vouloir supprimer cette réservation ?"):
            item = tree.item(selected[0])
            values = item['values']
            # Remove from list
            for res in reservations_list[:]:
                if (res["nom"] == values[0] and res["date"] == values[1] and
                    res["heure"] == values[2] and res["terrain"] == values[3]):
                    reservations_list.remove(res)
                    break
            update_reservations_table()
            messagebox.showinfo("Supprimé", "Réservation supprimée.")

    def get_selected_reservation():
        selected = tree.selection()
        if not selected:
            return None
        item = tree.item(selected[0])
        values = item['values']
        return {
            "nom": values[0], "date": values[1], "heure": values[2],
            "terrain": values[3], "forfait": values[4]
        }

    # Frame boutons à droite
    frame_btn = Frame(frame2, bg="white")
    frame_btn.grid(row=0, column=2, rowspan=7, padx=20, sticky="n")

    btn_ajouter = ctk.CTkButton(frame_btn, text="Ajouter", command=lambda: ajouter_reservation(),
                                fg_color="#1C9273", text_color="white", corner_radius=20, height=40,
                                font=("Arial", 12, "bold"))
    btn_ajouter.grid(row=0, column=0, padx=5, pady=5)

    btn_modifier = ctk.CTkButton(frame_btn, text="Modifier", command=lambda: modifier_reservation(),
                                 fg_color="#F7A400", text_color="white", corner_radius=20, height=40,
                                 font=("Arial", 12, "bold"), state="disabled")
    btn_modifier.grid(row=0, column=1, padx=5, pady=5)

    btn_supprimer = ctk.CTkButton(frame_btn, text="Supprimer", command=lambda: supprimer_reservation(),
                                  fg_color="#D90429", text_color="white", corner_radius=20, height=40,
                                  font=("Arial", 12, "bold"), state="disabled")
    btn_supprimer.grid(row=0, column=2, padx=5, pady=5)

    btn_paiement = ctk.CTkButton(frame_btn, text="Passer au Paiement", command=lambda: payment.main(get_selected_reservation()),
                                 fg_color="#1C9273", text_color="white", corner_radius=20, height=40,
                                 font=("Arial", 12, "bold"), state="disabled")
    btn_paiement.grid(row=0, column=3, padx=5, pady=5)

    abonnement_var = IntVar(value=0)

    # ------------------------------
    # FRAME 3 – Liste des réservations
    # ------------------------------
    frame3 = LabelFrame(
        fenetre, text="Vos Réservations",
        font=("Arial", 12, "bold"), bg="white"
    )
    frame3.pack(pady=10, padx=10, fill="both", expand=True)

    # Treeview pour afficher les réservations
    columns = ("Nom", "Date", "Heure", "Terrain", "Forfait", "Abonnement", "Équipement", "Coaching")
    tree = ttk.Treeview(frame3, columns=columns, show="headings", height=10)
    tree.pack(fill="both", expand=True, padx=10, pady=10)

    # Définir les en-têtes
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")

    # Scrollbar verticale
    scrollbar = ttk.Scrollbar(frame3, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")

    # Enable buttons on selection
    def on_tree_select(event):
        selected = tree.selection()
        if selected:
            btn_modifier.configure(state="normal")
            btn_supprimer.configure(state="normal")
            btn_paiement.configure(state="normal")
        else:
            btn_modifier.configure(state="disabled")
            btn_supprimer.configure(state="disabled")
            btn_paiement.configure(state="disabled")

    tree.bind("<<TreeviewSelect>>", on_tree_select)

    # Fonction pour mettre à jour la liste des réservations
    def update_reservations_table():
        # Vider la table
        for item in tree.get_children():
            tree.delete(item)
        # Ajouter les réservations
        for res in reservations_list:
            tree.insert("", "end", values=(
                res["nom"], res["date"], res["heure"], res["terrain"],
                res["forfait"], "Oui" if res.get("abonnement", 0) else "Non",
                "Oui" if res.get("equipment", 0) else "Non",
                "Oui" if res.get("coaching", 0) else "Non"
            ))

    # ------------------------------
    # CHARGEMENT CSV
    # ------------------------------
    if os.path.isfile(csv_file):
        with open(csv_file, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                res = {
                    "nom": row["nom"],
                    "date": row["date"],
                    "heure": row["heure"],
                    "terrain": row["terrain"],
                    "forfait": row["forfait"],
                    "abonnement": int(row["abonnement"]),
                    "equipment": int(row.get("equipment") or 0),
                    "coaching": int(row.get("coaching") or 0),
                    "user": row.get("user", "")
                }
                if user is None or res["user"] == user:
                    reservations_list.append(res)

    # Mettre à jour la table après chargement
    update_reservations_table()

    # Mettre à jour la table après ajout d'une réservation
    def ajouter_reservation():
        nom = nom_entry.get().strip()
        date_r = date_entry.get().strip()
        heure = heure_combo.get().strip()
        terr = terrain.get().strip()
        forfait = forfait_var.get().strip()
        abonnement = abonnement_var.get()
        equipment = equipment_var.get()
        coaching = coaching_var.get()

        if not nom or not date_r or not heure or not terr:
            messagebox.showwarning("Champs manquants", "Veuillez remplir tous les champs.")
            return

        conflict = False
        for res in reservations_list:
            if res["date"] == date_r and res["heure"] == heure and res["terrain"] == terr:
                conflict = True
                break

        if conflict:
            alternatives = find_alternatives(date_r, heure, terr)
            msg = f"Le terrain {terr} est déjà réservé à {heure}.\n\nSuggestions AI :\n"
            if alternatives:
                msg += "\n".join(f"- {alt}" for alt in alternatives)
                msg += "\n\nVoulez-vous réessayer avec une alternative ?"
                retry = messagebox.askyesno("Conflit détecté", msg)
                if retry:
                    return  # Allow user to change selection
            else:
                msg += "Aucune alternative disponible pour cette date."
                messagebox.showerror("Indisponible", msg)
            return

        new_res = {
            "nom": nom, "date": date_r, "heure": heure,
            "terrain": terr, "forfait": forfait, "abonnement": abonnement,
            "equipment": equipment, "coaching": coaching, "user": user
        }
        reservations_list.append(new_res)

        nom_entry.delete(0, END)
        heure_combo.set("")
        terrain.set("")
        equipment_var.set(0)
        coaching_var.set(0)
        messagebox.showinfo("Succès", "Réservation ajoutée !")

        # Mettre à jour la table
        update_reservations_table()

        # Ask to proceed to payment
        proceed = messagebox.askyesno("Paiement", "Voulez-vous procéder au paiement maintenant ?")
        if proceed:
            fenetre.destroy()
            payment.main(new_res)

        file_exists = os.path.isfile(csv_file)
        with open(csv_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["nom", "date", "heure", "terrain", "forfait", "abonnement", "equipment", "coaching", "user"])
            if not file_exists:
                writer.writeheader()
            writer.writerow({"nom": nom, "date": date_r, "heure": heure,
                             "terrain": terr, "forfait": forfait, "abonnement": abonnement,
                             "equipment": equipment, "coaching": coaching, "user": user})

    fenetre.mainloop()


if __name__ == "__main__":
    main()
