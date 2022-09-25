import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')

import Classes.Analytics as Analytics

def view(active_user,user_screen):
    '''The view screen is used to display habits of the user and give various options to see all, an individual or filtered habits. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print('[View Screen]')
    if( len(active_user.habits) == 0 ): 
        print('You currently do not have any habits to view!')
        sleep(1)
        print('[!] Returning to User Screen...')
        sleep(2)
        clear()
        user_screen(active_user)
    else:
        options = ['All Habits','Individual Habit', 'Filter Criteria']
        ans = quest.select('Menu Options:', options).ask()
        if(ans == options[0]):
            for habit in active_user.habits:
                habit.info_habit()
                print('Streak:',habit.streak)
                print('Highest Streak for Habit: ', Analytics.habit_longest_streak(habit.checkins))

            print('longest_streak: ', Analytics.total_longest_streak(active_user.habits))
            print('most_punctual_sec: ', Analytics.most_punctual(active_user.habits))
            print('most_late_sec: ', Analytics.most_late(active_user.habits))
            sleep(2)
            print('[!] Returning to User Screen...')
            sleep(1)
            clear()
            user_screen(active_user)
            pass

        elif(ans == options[1]):
            print('Not Yet Implemented')
            sleep(8)
            print('[!] Returning to User Screen...')
            sleep(1)
            clear()
            user_screen(active_user)
            pass
        elif(ans == options[2]):
            print('Not Yet Implemented')
            sleep(2)
            print('[!] Returning to User Screen...')
            sleep(1)
            clear()
            user_screen(active_user)
            pass
        