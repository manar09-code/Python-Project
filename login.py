# login.py
# Import necessary modules for GUI creation and functionality
from tkinter import *  # Import all Tkinter widgets for building the GUI
import customtkinter as ctk  # Import customtkinter for modern-looking widgets
from tkinter import messagebox  # Import messagebox for displaying messages
from PIL import Image, ImageTk  # Import PIL for image handling and Tkinter image support
import os  # Import os for file path operations
import home  # Import the home module for navigation

# ------------------ Window -----------------

fenetre = Tk()  # Create the main Tkinter window
fenetre.title("Connexion - Réservation sportive")  # Set the window title
fenetre.state("zoomed")  # Maximize the window to full screen
fenetre.update_idletasks()  # Update the window to get correct dimensions

# --- Background Image ---

# --- Background Image ---
try:
    base_dir = os.path.dirname(__file__)
    image_path = os.path.join(base_dir, "pictures", "background.jpg")
    image = Image.open(image_path)
    screen_width = fenetre.winfo_screenwidth()
    screen_height = fenetre.winfo_screenheight()
    image = image.resize((screen_width, screen_height))
    bg_photo = ImageTk.PhotoImage(image)

    bg_canvas = Canvas(fenetre, highlightthickness=0)
    bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
    bg_canvas.create_image(0, 0, image=bg_photo, anchor="nw")
    bg_canvas.image = bg_photo
except Exception as e:
    print("Erreur image:", e)
    fenetre.configure(bg="white")


# --- Main Frame ---

frame = ctk.CTkFrame(fenetre, width=300, height=350,  # Create a frame for the login/register forms
fg_color="white", border_width=1, border_color="lightgray")
frame.place(relx=0.5, rely=0.5, anchor="center")  # Place the frame in the center of the window

# ------------------ Clear Frame ------------------

def clear_frame():  # Define a function to clear all widgets from the frame
    for widget in frame.winfo_children():  # Iterate over all child widgets
        widget.destroy()  # Destroy each widget

# ------------------ Password Toggle ------------------

def add_eye(entry):  # Define a function to add an eye button for toggling password visibility
    def toggle():  # Nested function to toggle the show/hide state of the password
        entry.configure(show="" if entry.cget("show") == "*" else "*")  # Toggle between showing and hiding the password
    eye_btn = ctk.CTkButton(entry.master, text="👁", width=30, height=38,  # Create an eye button next to the entry
    fg_color="transparent", hover_color="#e0e0e0",
    command=toggle)  # Set the command to toggle visibility
    eye_btn.pack(side=LEFT)  # Pack the button to the left of the entry
    return eye_btn  # Return the button for potential further use

# ------------------ LOGIN ACTION ------------------

def login_action():  # Define the function to handle login attempts
    try:
        user = entry_user.get().strip()  # Get the username and strip whitespace
        pwd = entry_pass.get().strip()  # Get the password and strip whitespace
        if not user or not pwd:  # Check if fields are empty
            messagebox.showerror("Erreur", "Veuillez remplir tous les champs.")  # Show error message
            return  # Exit the function
        messagebox.showinfo("Connexion réussie", f"Bienvenue {user} !")  # Show success message
        fenetre.after(500, lambda: (fenetre.destroy(), home.main(user)))  # After 500ms, destroy window and open home page
    except:  # Catch any exceptions
        # If entry widgets don't exist, do nothing
        pass  # Pass silently

# ------------------ REGISTER ACTION ------------------

def register_action():  # Define the function to handle user registration
    if not reg_name.get() or not reg_email.get() or not reg_user.get() or not reg_pass.get() or not reg_confirm.get():  # Check if all fields are filled
        messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")  # Show error message
        return  # Exit the function
    if reg_pass.get() != reg_confirm.get():  # Check if passwords match
        messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")  # Show error message
        return  # Exit the function
    user = reg_user.get().strip()  # Get the username and strip whitespace
    messagebox.showinfo("Succès", f"Compte créé pour {user} !")  # Show success message
    fenetre.after(500, lambda: (fenetre.destroy(), home.main(user)))  # After 500ms, destroy window and open home page

# ------------------ FORGOT ACTION ------------------

def forgot_action():  # Define the function to handle forgot password steps
    global fp_step  # Access the global step variable
    if fp_step == 1:  # Step 1: Enter email
        if fp_email.get() == "":  # Check if email is empty
            messagebox.showerror("Erreur", "Veuillez saisir votre email.")  # Show error message
            return  # Exit the function
        messagebox.showinfo("Code envoyé", "Un code vous a été envoyé (test=1234).")  # Show info message (test code)
        fp_email.place_forget()  # Hide email entry
        fp_code.place(relx=0.5, y=65, anchor="center")  # Show code entry
        fp_step = 2  # Move to step 2
    elif fp_step == 2:  # Step 2: Enter code
        if fp_code.get() != "1234":  # Check if code is correct (test code)
            messagebox.showerror("Erreur", "Code incorrect.")  # Show error message
            return  # Exit the function
        fp_code.place_forget()  # Hide code entry
        fp_new.place(relx=0.5, y=65, anchor="center")  # Show new password entry
        fp_confirm.place(relx=0.5, y=105, anchor="center")  # Show confirm password entry
        fp_step = 3  # Move to step 3
    elif fp_step == 3:  # Step 3: Enter new password
        if fp_new.get() == "" or fp_confirm.get() == "":  # Check if fields are empty
            messagebox.showerror("Erreur", "Tous les champs sont obligatoires.")  # Show error message
            return  # Exit the function
        if fp_new.get() != fp_confirm.get():  # Check if passwords match
            messagebox.showerror("Erreur", "Les mots de passe ne correspondent pas.")  # Show error message
            return  # Exit the function
        messagebox.showinfo("Succès", "Mot de passe réinitialisé (UI seulement).")  # Show success message (UI only)
        show_login()  # Return to login screen

# ------------------ SHOW LOGIN ------------------

def show_login():  # Define the function to display the login form
    clear_frame()  # Clear the frame of any existing widgets
    global entry_user, entry_pass  # Declare global variables for username and password entries
    ctk.CTkLabel(frame, text="Connexion", text_color="black",  # Create a label for the login title
    font=("Arial", 16, "bold")).place(relx=0.5, y=25, anchor="center")  # Place the label in the center

    entry_user = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Nom d'utilisateur")  # Create username entry
    entry_user.place(relx=0.5, y=65, anchor="center")  # Place the entry in the center

    pass_frame = Frame(frame, bg="white")  # Create a frame for the password entry and eye button
    pass_frame.place(relx=0.5, y=115, anchor="center")  # Place the frame in the center
    entry_pass = ctk.CTkEntry(pass_frame, width=180, height=38, placeholder_text="Mot de passe", show="*")  # Create password entry
    entry_pass.pack(side=LEFT)  # Pack the entry to the left
    add_eye(entry_pass)  # Add the eye button for password visibility toggle

    ctk.CTkButton(frame, text="Se connecter", width=160, height=38, corner_radius=18,  # Create login button
                  fg_color="#F77F00", hover_color="#E57100",
                  command=login_action).place(relx=0.5, y=170, anchor="center")  # Place the button in the center

    ctk.CTkButton(frame, text="Mot de passe oublié ?", fg_color="transparent",  # Create forgot password button
                  text_color="#CC0000", hover_color="#e0e0e0",
                  command=show_forgot).place(relx=0.5, y=210, anchor="center")  # Place the button in the center

    ctk.CTkButton(frame, text="Créer un compte", fg_color="transparent",  # Create register button
                  text_color="#0077CC", hover_color="#e0e0e0",
                  command=show_register).place(relx=0.5, y=250, anchor="center")  # Place the button in the center

# ------------------ SHOW REGISTER ------------------

def show_register():  # Define the function to display the registration form
    clear_frame()  # Clear the frame of any existing widgets
    global reg_name, reg_email, reg_user, reg_pass, reg_confirm  # Declare global variables for registration entries
    ctk.CTkButton(frame, text="←", width=30, height=30, fg_color="transparent",  # Create back button to return to login
    text_color="#0077CC", hover_color="#e0e0e0",
    command=show_login).place(x=10, y=10)  # Place the button at the top left

    ctk.CTkLabel(frame, text="Créer un compte", text_color="black",  # Create a label for the registration title
                 font=("Arial", 16, "bold")).place(relx=0.5, y=25, anchor="center")  # Place the label in the center

    reg_name = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Nom complet")  # Create full name entry
    reg_name.place(relx=0.5, y=65, anchor="center")  # Place the entry in the center

    reg_email = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Email")  # Create email entry
    reg_email.place(relx=0.5, y=105, anchor="center")  # Place the entry in the center

    reg_user = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Nom d'utilisateur")  # Create username entry
    reg_user.place(relx=0.5, y=145, anchor="center")  # Place the entry in the center

    pass_frame = Frame(frame, bg="white")  # Create a frame for the password entry and eye button
    pass_frame.place(relx=0.5, y=185, anchor="center")  # Place the frame in the center
    reg_pass = ctk.CTkEntry(pass_frame, width=180, height=38, placeholder_text="Mot de passe", show="*")  # Create password entry
    reg_pass.pack(side=LEFT)  # Pack the entry to the left
    add_eye(reg_pass)  # Add the eye button for password visibility toggle

    confirm_frame = Frame(frame, bg="white")  # Create a frame for the confirm password entry and eye button
    confirm_frame.place(relx=0.5, y=225, anchor="center")  # Place the frame in the center
    reg_confirm = ctk.CTkEntry(confirm_frame, width=180, height=38, placeholder_text="Confirmer mot de passe", show="*")  # Create confirm password entry
    reg_confirm.pack(side=LEFT)  # Pack the entry to the left
    add_eye(reg_confirm)  # Add the eye button for password visibility toggle

    ctk.CTkButton(frame, text="Créer le compte", width=160, height=38, corner_radius=18,  # Create register button
                  fg_color="#F77F00", hover_color="#E57100",
                  command=register_action).place(relx=0.5, y=270, anchor="center")  # Place the button in the center

# ------------------ SHOW FORGOT ------------------

def show_forgot():
    clear_frame()
    global fp_step, fp_email, fp_code, fp_new, fp_confirm
    fp_step = 1

    ctk.CTkButton(frame, text="←", width=30, height=30, fg_color="transparent",
                  text_color="#0077CC", hover_color="#e0e0e0",
                  command=show_login).place(x=10, y=10)

    ctk.CTkLabel(frame, text="Mot de passe oublié", text_color="black",
                 font=("Arial", 16, "bold")).place(relx=0.5, y=25, anchor="center")

    fp_email = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Votre email")
    fp_email.place(relx=0.5, y=65, anchor="center")
    fp_code = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Code reçu")
    fp_new = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Nouveau mot de passe", show="*")
    fp_confirm = ctk.CTkEntry(frame, width=220, height=38, placeholder_text="Confirmer mot de passe", show="*")

    ctk.CTkButton(frame, text="Continuer", width=160, height=38,
                  corner_radius=18, fg_color="#F77F00", hover_color="#E57100",
                  command=forgot_action).place(relx=0.5, y=115, anchor="center")

# ------------------ Start ------------------

show_login()
fenetre.bind("<Return>", lambda e: login_action())
fenetre.mainloop()
