import os
import questionary as quest
from time import sleep
from datetime import datetime

#Function to Clear Terminal
clear = lambda : os.system('tput reset')

def new(active_user,user_screen):
    '''The new screen is used for creating new habits, which can be normal or dynamic. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[New Screen]')
    questions = ['Regular Habit - Fixed Deadlines)','Dynamic Habit - Specify how often to check in before deadline','Go back to User Screen']
    ans = quest.select('Choose what kind of Habit you want to create:', questions).ask()

    def questionary(is_dynamic:bool):
        #user input
        title = quest.text('What will be the title of the new habit? E.g. Daily Gym Workout').ask()
        description = quest.text('Provide a description? E.g. 60 minuts of cardio').ask()
        interval = quest.text('Define an interval for the habit. You can use any whole number followed by m/H/D/W/M/Y; e.g. 3D or 1W or 30m').ask()
        if(is_dynamic):
            checkin_num_before_deadline = quest.text('How often do you want to perform the habit before a deadline? Type an integer numer; e.g. 1, 3, 5').ask()
        else:
            checkin_num_before_deadline = 1
        active = quest.confirm("Do you directly want to set the habit to active?").ask()
        if(active):
            start_from = datetime.now()
        else:
            start_from = quest.text('Provide a start date when you want it to become active? Please follow the format YYYY/MM/DD HH:mm, e.g. 2050/03/28 15:35.').ask()
        difficulity = quest.select("How difficult do you find it to perform?",['1','2','3','4','5']).ask()
        category = quest.text('Do you want to assign this habit to a common category? Similar habits will be grouped together. E.g.: Eduction, Sport, Hobby').ask()
        moto = quest.text('What is your moto you would like to remind yourself of to keep doing the habit?').ask()
        importance = quest.select("How important do you find it to perform?",['1','2','3','4','5']).ask()
        push_notif = quest.confirm("Do you want to receive push notifications to your email for this habit?").ask()
        milestone = quest.text("Set milestone target for multiple successes. E.g. 5 for 5 consequent succesfull checkins!").ask()
        style = 0

        #Create habit with user input
        try:
            active_user.create_habit(title, description, interval, active, start_from, difficulity, category, moto, importance, push_notif, milestone, style, is_dynamic, checkin_num_before_deadline)
            print('[*] Added your habit!')
        except Exception as e:
            print('[!] Failed to add habit, an error occured!')
            print(e)

    
    #Regular habit
    if(ans == questions[0]):
        sleep(1)
        is_dynamic = False
        questionary(is_dynamic)

        #Show habit before submit? Then return to user screen
        sleep(1)
        print('Returning back to User Screen...')
        sleep(1)
        user_screen(active_user)

    #Dynamic Habit
    elif(ans == questions[1]):
        sleep(1)
        is_dynamic = True
        questionary(is_dynamic)

        #Show habit before submit? Then return to user screen
        sleep(1)
        print('Returning back to User Screen...')
        sleep(1)
        user_screen(active_user)

    elif(ans==questions[2]):
        clear()
        sleep(1)
        print('Returning back to User Screen...')
        sleep(1)
        user_screen(active_user)