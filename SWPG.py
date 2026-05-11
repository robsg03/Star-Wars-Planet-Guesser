#imports tkinter library for GUI creation and manipulation
import tkinter as tk
#imports pillows library and Image and ImageTk modules
from PIL import Image, ImageTk
#imports random library for random selection
import random
#imports messagebox module from tkinter for displaying dialogue boxes
from tkinter import messagebox
#imports csv library allowing save to csv file
import csv
#imports sys to give python access to system information
import sys
#imports the path class from pathlib library making file locations easier to manage
from pathlib import Path

#List named SWMovie_planets that stores all the planet data for the game (points, images, name, hint, clue)
SWMovie_planets = [
    #"name" is the correct answer user needs to input.
    #"clue" is the bit of information given to the user.
    #"hint" provides extra information that narrows down options.
    #"points" denotes the score tied to planet (harder planets = higher point score)
    #"image" is the filepath location for the displayed images in the game
    {"name": "Tatooine",
     "clue": "A harsh desert world with two suns",
     "hint": "Obi-Wan was tasked with watching over Luke on this planet after the events of Order 66",
     "points": 3,
     "image": "images/tatooine.png"},

    {"name": "Hoth",
     "clue": "An icy planet used as a rebel base",
     "hint": "This planet featured the first on-screen appearance of the iconic AT-AT imperial walker",
     "points": 2,
     "image": "images/hoth.png"},

    {"name": "Naboo",
     "clue": "A beautiful marsh world with the Queen's Palace",
     "hint": "Padme's home",
     "points": 3,
     "image": "images/naboo.png"},

    {"name": "Coruscant",
     "clue": "The capital of the Star Wars Universe",
     "hint": "The Jedi Temple is here",
     "points": 4,
     "image": "images/coruscant.png"},

    {"name": "Endor",
     "clue": "A forest moon with Ewoks",
     "hint": "Small furry creatures that live in the treetops",
     "points": 2,
     "image": "images/endor.png"},

    {"name": "Mustafar",
     "clue": "A fiery lava planet with a large mining colony",
     "hint": "'It's over Anakin! I have the high ground!'",
     "points": 4,
     "image": "images/mustafar.png"},
]

#random.shuffle randomly rearranges the list of included planets
random.shuffle(SWMovie_planets)

#score variable that starts at 0 to track user's points
score = 0
#variable used to track number of rounds the user has completed starting at 0
round_num = 0
#variable that tracks whether the user has activated a hint for the current round number
hint_used = False

#creates a function that builds a filepath to open something
def resource_path(relative_path):
    #checks to see if the program is running in a pyinstaller exe
    #if yes, creates a temporary folder named _meipass when the .exe runs
    if hasattr(sys, "_MEIPASS"):
        #builds full path to the file inside of the new temp folder
        return Path(sys._MEIPASS) / relative_path
    #runs if the program is not a .exe file so it can still save when running as .py
    return Path(__file__).resolve().parent / relative_path

#creates a function to build the correct filepath to save something
def writable_path(filename):
    #checks if app is running as .exe
    if getattr(sys, "frozen", False):
        #saves csv results in the same folder as the .exe
        return Path(sys.executable).resolve().parent / filename
    #if run as .py saves in same folder as .py file
    return Path(__file__).resolve().parent / filename

#defines a function called question
def question():
    #using global variable to make changes across the whole game
    global hint_used
    #hint_used resets the hint button to unused after every new round
    hint_used = False
    #this if/else statement ensures the game continues until the list of included planets have all been guessed
    if round_num < len(SWMovie_planets):
        #.config ensures the respective clue for the current planet being guessed from SWMovie_planets list is being displayed
        clue_label.config(text=SWMovie_planets[round_num]["clue"])
        #opens the image file in the GUI for current planet using PILLOW library
        img = Image.open(resource_path(SWMovie_planets[round_num]["image"]))
        #this line resizes each image file to 450 pixels x 450 pixels to fit GUI better
        img = img.resize((450, 450))
        #converts pillow image to version that is usable with tkinter
        planet_pic = ImageTk.PhotoImage(img)
        #sets image_label to display images
        image_label.config(image=planet_pic)
        #reference that stores the data of the images
        image_label.image = planet_pic
        #this line of code makes sure to clear the text entry box when the user enters their guess for the current planet
        entry.delete(0, tk.END)
        #this line clears the stored data from the results that say correct or incorrect and erases the clue for the current planet if one was used
        result_label.config(text="")
        #this line manages the round display showing the current round out of total max # of rounds
        #since we don't start at round 0, we have to add 1 to our round_num variable which starts at 0
        round_label.config(text=f"Round: {round_num + 1}/{len(SWMovie_planets)}")
        #updates the score label every round based on how many points the user earned from correctly guessing planets
        score_label.config(text=f"Score: {score}")
    else:
        #ends the game when the total number of rounds played reaches the number of planets in SWMovie_planets list
        end_game()

#defines function called check_answer to be used when user submits their answer for current planet
def check_answer():
    #use global variables outside of function to ensure changes made while this function is running affect the whole game
    global score, round_num
    #guess variable gets the user's typed answer using .get and uses .strip() and .lower() to remove unnecessary spaces
    #and converts their answer to lower case so answers are not case-sensitive
    guess = entry.get().strip().lower()
    #answer gets the correct planet name for the current round and converts it to lowercase to match user input
    answer = SWMovie_planets[round_num]["name"].lower()
    #this if/else statement checks to see if user's answer is exactly the same as correct answer for current round
    #and adds points accordingly based on if the user got the answer correct and whether they used a hint
    if guess == answer:
        #pts_gained starts with the total point value for the current planet
        pts_gained = SWMovie_planets[round_num]["points"]
        #if user activated a hint, it subtracts 1 from the total point value scored from current planet
        if hint_used:
            pts_gained -= 1
        #sets point value to 0 when point total falls below 0 to rid negative score results
        #makes scoring more consistent for leaderboards
        if pts_gained < 0:
            pts_gained = 0
        #adds amount of points gained in rounds to total score value
        score += pts_gained
        #displays winning message when current planet is guessed correctly and shows point value gained from current round
        result_label.config(text=f"Correct! +{pts_gained} points")
    else:
        #displays losing message and correct planet name as answer when user incorrectly guesses
        result_label.config(text=f"Incorrect! Answer: {SWMovie_planets[round_num]['name']}")
    #continues to the next round by increasing the round_num variable
    round_num += 1
    #this line lets the user wait 1.2 seconds (1200 milliseconds) in between rounds
    #to give them time to see the correct answer for the current round
    #question calls for the next planet to be loaded after the 1200 millisecond wait time
    root.after(1200, question)

#this function gives the user a hint when called for by user when they click the "Show Hint" button
def give_hint():
    #uses global hint variable to ensure changes are made across the whole game
    global hint_used
    #updates when hint has been used for the current round
    hint_used = True
    #displays more detailed information about the planet or significant events on that planet when user needs help
    #and clicks on "Show Hint" button
    result_label.config(text=f"Hint: {SWMovie_planets[round_num]['hint']}")

#this function uses csv to save all user results in a csv file on the computer
def save_score(player_name, final_rank):
    #creates and opens a csv file to store the user's data in a permanent spot
    #"a" appends data meaning that new user scores are added in addition to existing scores
    #makes sure not to overwrite previous results
    #with automatically closes the file after writing new data
    #newline makes sure that scores are saved row by row in csv file without spaces in between results
    with open(writable_path("SWPGscores.csv"), "a", newline="") as file:
        #creates a utility called writer to write in csv file
        writer = csv.writer(file)
        #tells the writer utility to input following variables into a line
        writer.writerow([player_name, score, final_rank])

#end_game function takes the user's name and final scores and displays a GAME OVER
#message letting them see their final score and what Jedi rank they deserve based on their level of knowledge
def end_game():
    #takes name from user using .get() and strips any extra spaces using .strip()
    player_name = name_entry.get().strip()
    #names the player "Unnamed" if they did not enter a name
    if player_name == "":
        player_name = "Unnamed"
    #ranks user as Jedi Master if they score 15 points or higher in total
    if score >= 15:
        rank = "Jedi Master"
    #ranks user as Jedi Knight if they score 8 points or higher in total
    elif score >= 8:
        rank = "Jedi Knight"
    else:
        #ranks user as Padawan if they score less than 8 points
        rank = "Padawan"
    #this line saves the player's name and rank in the csv file
    save_score(player_name, rank)
    #displays game over message and shows user their final results in a message window
    messagebox.showinfo("Game Over", f"Final Score: {score}\nRank: {rank}")
    #this line closes the game window
    root.destroy()

#creates main tkinter window
root = tk.Tk()
#naming the window "Star Wars Planet Guessing Game"
root.title("Star Wars Planet Guessing Game")
#sets window default dimensions to 800pixels long by 800pixels wide leaving it unlocked for full user control
root.geometry("800x800")
#makes the main background color for tkinter GUI window all black to fit the star wars theme
root.configure(bg="black")

#creates main window title text at the top of GUI
title_label = tk.Label(root, text="Guess the Star Wars Planet", font=("Arial", 14), bg="black", fg="yellow")
#places title with vertical spacing using pixel values to determine length
title_label.pack(pady=10)
#creates a label asking for the user to enter their name
name_label = tk.Label(root, text="Enter your name:", font=("Arial", 12), bg="black", fg="yellow")
#places the label under main title
name_label.pack()
#makes a user input box 25 pixels wide for user to input their name
name_entry = tk.Entry(root, width=25)
#places user name input box under label asking for their name
name_entry.pack()
#creates a label displaying the current round
round_label = tk.Label(root, text="Round: 0", font=("Arial", 12), bg="black", fg="yellow")
#places the round label under the user name input box
round_label.pack()
#cretaes a label showing the user's score
score_label = tk.Label(root, text="Score: 0", font=("Arial", 12), bg="black", fg="red")
#places the label under the round label
score_label.pack()
#image label creates empty space for the planet picture to be displayed
image_label = tk.Label(root, text= "")
#places the picture of the star wars planet in the empty space
image_label.pack()
#creates a label that displays the clue for the respective planet
#wraplength ensures that after 350pixels the text breaks to a new line for visual improvement
clue_label = tk.Label(root, text="", wraplength=350, font=("Arial", 12), bg="black", fg="yellow")
#places label after the planet image with 15pixels of vertical space
clue_label.pack(pady=15)
#creates a user input box where user guesses the current planet based off the clue
entry = tk.Entry(root, width=25, bg="white", fg="black", insertbackground="black")
#places the input box under the clue being displayed
entry.pack()
#creates a button called "Submit Guess" that calls for the function check_answer to be used when clicked
submit_button = tk.Button(root, text="Submit Guess", command=check_answer)
#places the submit button under the user input box for the planet they are guessing with 5 pixels of vertical space
submit_button.pack(pady=5)
#creates a button called "Show Hint..." that calls the give_hint function when clicked
hint_button = tk.Button(root, text="Show Hint (-1 point)", command=give_hint)
#places the show hint button under the submit guess button
hint_button.pack()
#creates a label that shows the messages for correct/incorrect and the extra hint
result_label = tk.Label(root, text="", fg="blue", wraplength=350)
#places the hint label and final result label underneath the show hint button with 10pixels of vertical space
result_label.pack(pady=10)
#runs the question() function to start the game when it is opened
question()
#keeps tkinter window open to allow user interaction
root.mainloop()