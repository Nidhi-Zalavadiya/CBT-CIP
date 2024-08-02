from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.ttk import *
from PIL import Image, ImageTk
from random import randint



def setup_styles():
    style = ttk.Style()
    # Define a new style for the reset button
    style.configure('TButton',
                    background='lightblue',  
                    foreground='black',      
                    font=('Arial', 20, 'bold'),
                    borderwidth=2,
                    relief='raised')
    style.map('TButton',
              background=[('active', '#ffcccb')],  
              foreground=[('active', 'black')])

player_point = int(0)
computer_point = int(0)
round_count = int(0)

options = {
    1 : "Rock",
    2 : "Paper",
    3 : "Scissor"
}

def reset_game():
    global computer_point , player_point , round_count
    player_point = 0
    computer_point = 0
    round_count = 0
    update_selection("Game Reset!\nReady to Play!")

#Get Computer choice
def get_computer_choice():
    return options[randint(1, 3)]

#handle the results
def handle_result(user_choice):

    global player_point, computer_point, round_count

    computer_choice = get_computer_choice()

    if user_choice == computer_choice:
        result = "It's Tie!"

    elif (user_choice == "Rock" and computer_choice == "Scissor") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissor" and computer_choice == "Paper"):
        player_point += 1
        result = "You Win!"
    else:
        computer_point += 1
        result = "You Lose!"
    
    round_count = round_count + 1

  
    if round_count >= 3:
        if computer_point == player_point:
            final_result = "The game is a Tie!"
        elif computer_point > player_point:
            final_result = "Computer wins the game!"
        else:
            final_result = "You win the game!"
        messagebox.showinfo("Game Over", f"Final Score:\nComputer: {computer_point}\nYou: {player_point}\n{final_result}")

        reset_game()
    else:
        update_selection(f"Player: {user_choice.capitalize()}\nComputer: {computer_choice.capitalize()}\n{result}\n\nPlayer Points: {player_point} \nComputer Points: {computer_point}")

# update result label text
def update_selection(selection):
    selection_label.config(text=selection)


root = Tk()
root.title("Rock ... Paper .... Sessior ")
root.geometry("600x500+100+100")
root.configure(bg="#FAFAD2")

header_font = ("Arial", 20, "bold")
label_font = ("Arial", 16, "italic")


w = Label(root, text="Let's Play Tpgether",font=header_font, foreground="darkblue", background="lightyellow")
w.place(x=200,y=25)

l1 = Label(root, text="You",font=label_font, foreground="green", background="lightgrey", borderwidth=2, relief="raised")
l1.place(x=70,y=60)


l2 = Label(root, text="Computer",font=label_font, foreground="red", background="lightgrey", borderwidth=2, relief="raised")
l2.place(x=480,y=60)



# For PLayer
def load_image(i,angle, size=(50,50)):
    image = Image.open(i)
    resized_image = image.resize(size)
    rotated_image = resized_image.rotate(angle, expand=True)  
    return ImageTk.PhotoImage(rotated_image)
    
photo1 = load_image("rock.webp",90)
photo2 = load_image("paper.jpg",90)
photo3 = load_image("scissor.webp",90)

rock = Button(root, image = photo1, compound=LEFT, command=lambda: handle_result("Rock"))
paper = Button(root, image = photo2, compound=LEFT,command=lambda: handle_result("Paper"))
scissor = Button(root, image = photo3, compound=LEFT,command=lambda: handle_result("Scissor"))

rock.place(x=30,y=100)
paper.place(x=30,y=200)
scissor.place(x=30,y=300)


# For Computer

def rotate_image(image_path, angle,size=(50,90)):
    """Rotate an image by the given angle and return the rotated image."""
    image = Image.open(image_path)
    resized_image = image.resize(size)
    rotated_image = resized_image.rotate(angle, expand=True)  
    return ImageTk.PhotoImage(rotated_image)


p1 = rotate_image("rock.webp", 270) 
p2 = rotate_image("paper.jpg", 270) 
p3 = rotate_image("scissor.webp", 270) 

rock2 = Button(root, image=p1)
paper2 = Button(root, image=p2)
scissor2 = Button(root, image=p3)

rock2.place(x=480,y=100)
paper2.place(x=480,y=200)
scissor2.place(x=480,y=300)



# Result Label
selection_label = Label(root, text=None, font=("Arial", 16),background="#FAFAD2")
selection_label.place(x = 240,y = 170)


# Reset Button
reset = Button(
    root, 
    text = "Reset Game",
    command = reset_game,
    style='TButton',
    width=20,
    
)

reset.place(x=270,y=350)

# Mainloop to diplay GUI
root.mainloop() 