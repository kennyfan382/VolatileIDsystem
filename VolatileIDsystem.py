#Secure leaves: Type 1001 on certain areas if you want to go back to menu E.g if you enter in the wrong command and have not got a unique ID

from datetime import date
import sys
import time
import random
import re
import os
import csv


def enter_csv(): #verify that the user has a file to do any of the csv operations
   while True:
    path = input("Please enter the directory to your csv file (remember to end it in .csv) E.g 'Documents/ID/IDsysdata.csv': ").strip() #Cant be enter_input as it uses the .lower() method (directory needs to be absolute)
    if not os.path.exists(path):
        print(f"Error: csv file not found at '{path}'")
        continue
    else: 
        return path

def load_data(path):
    with open(path, 'r') as f: #Open file and give it a var name
        reader = csv.reader(f) #var that reads file
        try:
            for row in reader: #begin writing all the content in the respective dictionaries
                ip = int(row[0]) #uid is always in the first row
                uid.append(ip)
                names.update({ip:row[1]})
                birth_dates.update({ip:row[2]})
                home_countries.update({ip:row[3]})
                sex.update({ip:row[4]}) 
                occupation.update({ip:row[5]})
                date_made.update({ip:row[6]})
                if ip in recent_append:
                    recent_append.update({ip:row[7]})
        except(IndexError, ValueError) as e:
            print("")

def save_data(path):
    with open(path, 'w') as f:
        writer = csv.writer(f)
        for id in uid: #Write all of the respective data that is currently held in the program through a loop of the uid list
            if id in recent_append:
                writer.writerow([id, names[id], birth_dates[id], home_countries[id], sex[id], occupation[id], date_made[id], recent_append[id]])
            else:
                writer.writerow([id, names[id], birth_dates[id], home_countries[id], sex[id], occupation[id], date_made[id]])

def intro():
    print("\n")
    title = "ID system"
    sub_title = "Created by Aidan Hammond"
    for i in title:
        print(i, end='', flush = True) #prints each char 1 by 1 (making it slowly appear on the same line)
        time.sleep(0.1)
    print("\n")
    for i in sub_title:
        print(i, end='', flush = True)
        time.sleep(0.1)
    print("\n")
intro()

def enter_input(text, type): #Text = What the input says   Type = What type the input needs
    while True:
        try:
            user_input = input(text).strip().lower() #What makes this function recognised as an input when called 
            if type == int:
                return int(user_input)
            elif type == str:
                if user_input.isdigit(): #If it is not a string within the string condition 
                    raise ValueError("That is not a string. We need strings")
                return user_input  # return the string as it is
        except ValueError as ValErr:
            print(ValErr) #Shows the value error along with input
        except TypeError as TyErr:
            print(TyErr) #Same as value error except

#Define the user info
names = {} #Open to all names!
days = [f"{i:02}" for i in range(1, 32)] #Creates a list of numbers 01 to 31
months = [f"{i:02}" for i in range(1, 13)] #Same method, but list is 01 to 12
birth_dates = {}
def check_bday(id): #Ensure the format and range of birthday are accurate
    birthday = enter_input("Please enter your date of birth (format example: 07-04-2006): ", str)
    format = r"^\d{2}-\d{2}-\d{4}$" #2 ints, /, 2 ints, /, 4 ints
    check_format = re.match(format, birthday) #Ensure Input matches the expression format
    if check_format:
        day, month, year = map(int, birthday.split('-')) #Ints specified before forward slash will be vars day, month and year
        day_str = str(day).zfill(2) #if the day is not 2 digits a zero is put before it (same for month_str shown below)
        month_str = str(month).zfill(2)
        if day_str in days and month_str in months and year >= 1900 and year <= 2025:
            birth_dates.update({id:birthday})
        else:
            print("Date numbers out of range")
            time.sleep(1)
            check_bday(id)
    else:
        print("Not valid format/birthday")
        time.sleep(1)
        check_bday(id)
home_countries = {} #Open to all countries
sex = {}
def check_sex(id): #Ensure the correct sex is identified
    es = enter_input("Please enter the sex you were assigned at birth (m, f or intersex): ", str)
    if es == "m" or es == "f" or es == "intersex":
        sex.update({id:es})
    else:
        print("This is not a valid sex (What was assigned to you at birth)")
        time.sleep(1)
        check_sex(id)
occupation = {} #Open to all occupations
date_made = {} 
recent_append = {} #Date of when the data was most recently modified

uid = [] #User ID to access their information matching variable names in dictionaries above

def create(): #create info and assign it to dictionaries
    nid = random.randint(0, 1000)
    if nid in uid:
        create() #Call the function again to create a NID that is not already in UID (to avoid overlapping)
    else:
        uid.append(nid)
        en = enter_input("Please enter your name: ", str) 
        names.update({nid: en}) #Name typed in is assigned to names dictionary with respective ID (repeated for certain others)
        check_bday(nid)
        ec = enter_input("Please enter your home country: ", str)
        home_countries.update({nid: ec})
        check_sex(nid)
        eo = enter_input("Please enter your current occupation: ", str)
        occupation.update({nid: eo})
        date_made.update({nid:date.today()})
        print(f"\nYour unique ID number to access this data is: {nid}\n\n")
        time.sleep(3)
        menu()

def see(): #User can see their information through entering their unique ID number
    eid = enter_input("Please enter your unique ID number: ", int)
    if eid in uid:
        print(f"name: {names[eid]}\nDate of birth: {birth_dates[eid]}\nCountry of origin: {home_countries[eid]}\nSex: {sex[eid]}\nCurrenct occupation: {occupation[eid]}")
        if eid in date_made:
            print(f"The date this information was put in: {date_made[eid]}")
        if eid in recent_append:
            print(f"Date of most recent modification: {recent_append[eid]}")
        time.sleep(5)
        print("\n")
        menu()
    if eid == 1001:
        menu()
    elif eid not in uid:
        print("not valid number in database")
        time.sleep(2)
        see()

def append_again_request(ip): #Used in the next function to ask the user if they need to append anything else
    another_append = enter_input("Would you like to append anything else? (Y/N): ", str)
    if another_append == "Y" or another_append == "y":
        append(ip)
    elif another_append == "N" or another_append == "n":
        append_modification_date = date.today()
        recent_append.update({ip:append_modification_date}) #Update RecentAppend dictionary with the most recent modification
        menu()
    elif another_append != "Y" or another_append != "y" or another_append != "N" or another_append != "n":
        print("Not valid input")
        time.sleep(1)
        append_again_request(ip) #Whole point this is a seperate function (so it can be called again inside itself)

def append(ip):
    if ip in uid:
        append_options = "Please select the number what you would like to append!\n1. names\n2. Date of birth\n3. home country\n4. Sex\n5. Occupation\n"
        for char in append_options:
            print(char, end='', flush = True)
            time.sleep(0.001)
        append_selection = enter_input("Enter Number: ", int)
        if append_selection == 1:
            name_append = enter_input("Please enter your new name: ", str)
            names.update({ip:name_append}) #The same format for the data being assigned to the ID is used
        elif append_selection == 2:
            check_bday(ip)
        elif append_selection == 3:
            home_country_append = enter_input("Please enter your new home country: ", str)
            home_countries.update({ip:home_country_append})
        elif append_selection == 4:
            check_sex(ip)
        elif append_selection == 5:
            occupation_append = enter_input("Please enter your new Occupation: ", str)
            occupation.update({ip:occupation_append})
        else:
            print("Not valid input")
            time.sleep(1)
            append(ip)
        append_again_request(ip)

def enter_append(): #User can append their details if their name matches the array #CURRENT USER PARAM ONLY USED 
    eid = enter_input("Please enter your unique ID number: ", int)
    if eid in uid:
        append(eid)
    if eid == 1001:
        menu()
    elif eid not in uid:
        print("not valid number in database")
        time.sleep(2)
        enter_append()

messages = ["Please enter your number: ", "What do you want: ", "Tell the ID man what you need: ", 
            "Remember, stay hydrated (Also enter command): ", "Just the number you need please!: ", "Numbers should be on a keyboard!: "]

def menu():
    print("Please enter a number for what you would like to do")
    time.sleep(1)   
    commands = "1: Create a new ID\n2: View your current ID\n3: Append your current ID\n4: write all data to a csv file\n5: load data from a csv file\n6: leave\n\n"
    for i in commands:
        print(i, end='', flush = True)
        time.sleep(0.05)
    random_message = random.choice(messages) #Any messsage out of the random messages dictionary can be chosen
    command = enter_input(f"{random_message}", int)
    if command == 1:
        os.system('cls') #Windows command to clear terminal
        os.system('clear') #Linux command to clear terminal
        create()
    if command == 2:
        os.system('cls')
        os.system('clear') 
        see()
    if command == 3:
        os.system('cls')
        os.system('clear')
        enter_append()
    if command == 4:
        os.system('cls')
        os.system('clear')
        save_data(enter_csv()) #User might want to save it to a different csv file
    if command == 5:
        os.system('cls')
        os.system('clear')
        load_data(enter_csv()) #User might want to load data from different csv files
    if command == 6:
        sys.exit() 
    else:
        print("Invalid Input")
        os.system('cls') 
        menu()
menu()
