# home.py
# Import necessary modules for GUI creation
from tkinter import *  # Import all Tkinter widgets for building the GUI
from PIL import Image, ImageTk  # Import PIL for image handling and Tkinter image support
import customtkinter as ctk  # Import customtkinter for modern-looking widgets
import os  # Import os for file path operations
import reservation, payment, news, stats  # Import other modules for navigation
def main(user=None):  # Define the main function for the home page, taking an optional user parameter
    # --- Main Window ---
    fenetre = Tk()  # Create the main Tkinter window
    fenetre.title("Accueil - Système de Réservation Sportive")  # Set the window title
    fenetre.configure(bg="white")  # Set the background color to white
    fenetre.state("zoomed")  # Maximize the window to full screen

    # --- Absolute Path Setup ---
    current_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    pictures_dir = os.path.join(current_dir, "pictures")  # Join to get the pictures directory path
    bg_path = os.path.join(pictures_dir, "background1.jpg")  # Full path to the background image

    # Debug (optional)
    print("PATH:", bg_path)  # Print the background image path for debugging
    print("EXISTS:", os.path.exists(bg_path))  # Check if the background image exists and print the result

    # --- Background Image ---
    bg_image = Image.open(bg_path)  # Open the background image using PIL
    bg_image = bg_image.resize(  # Resize the image to fit the screen dimensions
        (fenetre.winfo_screenwidth(), fenetre.winfo_screenheight())
    )
    bg_photo = ImageTk.PhotoImage(bg_image)  # Convert PIL image to Tkinter-compatible photo image

    bg_label = Label(fenetre, image=bg_photo)  # Create a label to display the background image
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)  # Place the label to cover the entire window
    bg_label.image = bg_photo  # Keep a reference to prevent garbage collection

    # --- Animated Banner ---
    canvas = Canvas(  # Create a canvas for the animated banner
        fenetre,
        width=fenetre.winfo_screenwidth(),
        height=200,
        bg="#133A5C",
        highlightthickness=0
    )
    canvas.pack(fill="x")  # Pack the canvas to fill the width

    welcome_text = canvas.create_text(  # Create the welcome text on the canvas
        0, 100,
        text="Bienvenue dans votre platforme de résérvation sportive!",
        font=("Arial", 24, "bold"),
        fill="white",
        anchor="w"
    )

    def animate():  # Define the animation function to move the text
        canvas.move(welcome_text, 2, 0)  # Move the text 2 pixels to the right
        pos = canvas.coords(welcome_text)  # Get the current position of the text
        if pos[0] > fenetre.winfo_screenwidth():  # If text goes off screen, reset position
            canvas.coords(welcome_text, 0, 100)
        fenetre.after(20, animate)  # Schedule the next animation frame after 20ms

    animate()  # Start the animation

    # --- Greeting ---
    if user:  # If a user is logged in, display a greeting
        greeting_text = f"Hi, {user} !"  # Format the greeting message with the user's name
        ctk.CTkLabel(fenetre, text=greeting_text, font=("Arial", 20, "bold"), text_color="#1C9273").pack(pady=10)  # Create and pack a label with the greeting

    # --- Menu Frame ---
    frame_menu = Frame(fenetre, bg="white")  # Create a frame for the menu buttons
    frame_menu.pack(pady=30)  # Pack the frame with padding

    button_width = 150  # Define button width
    button_height = 40  # Define button height

    # --- Buttons ---
    ctk.CTkButton(  # Create a button for Reservation
        frame_menu,
        text="Réservation",
        width=button_width,
        height=button_height,
        corner_radius=20,
        fg_color="#133A5C",
        hover_color="#F77F00",
        font=("Arial", 16, "bold"),
        command=lambda: open_page("reservation")  # Command to open reservation page
    ).grid(row=0, column=0, padx=20, pady=20)  # Grid position

    ctk.CTkButton(  # Create a button for Payment
        frame_menu,
        text="Paiement",
        width=button_width,
        height=button_height,
        corner_radius=20,
        fg_color="#133A5C",
        hover_color="#F77F00",
        font=("Arial", 16, "bold"),
        command=lambda: open_page("payment")  # Command to open payment page
    ).grid(row=0, column=1, padx=20, pady=20)  # Grid position

    ctk.CTkButton(  # Create a button for News
        frame_menu,
        text="Actualités",
        width=button_width,
        height=button_height,
        corner_radius=20,
        fg_color="#133A5C",
        hover_color="#F77F00",
        font=("Arial", 16, "bold"),
        command=lambda: open_page("news")  # Command to open news page
    ).grid(row=1, column=0, padx=20, pady=20)  # Grid position

    ctk.CTkButton(  # Create a button for Statistics
        frame_menu,
        text="Statistiques",
        width=button_width,
        height=button_height,
        corner_radius=20,
        fg_color="#133A5C",
        hover_color="#F77F00",
        font=("Arial", 16, "bold"),
        command=lambda: open_page("stats")  # Command to open stats page
    ).grid(row=1, column=1, padx=20, pady=20)  # Grid position

    # --- Page Switching ---
    def open_page(module_name):  # Define the function to switch to different pages
        fenetre.destroy()  # Destroy the current window
        modules = {  # Dictionary mapping module names to module objects
            "reservation": reservation,
            "payment": payment,
            "news": news,
            "stats": stats
        }
        module = modules.get(module_name)  # Get the module object
        if module:  # If the module exists
            if module_name == "reservation":  # If it's the reservation module, pass the user
                module.main(user)
            else:  # Otherwise, call main without user
                module.main()

    fenetre.mainloop()  # Start the Tkinter event loop


if __name__ == "__main__":  # If this script is run directly
    main()  # Call the main function
