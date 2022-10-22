import os
import questionary as quest
from time import sleep
#Function to Clear Terminal
clear = lambda : os.system('tput reset')
from Database import db_api as api

def delete(state):
        '''The delete screen is used for deleting habits. Habits list is printed and user can select which one to permanently remove. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
        clear()
        print('[Delete Screen]')

        #In case no habits are available, show message and return to user_screen
        if( len(state["active_user"].habits) == 0 ): 
            print('You currently do not have any habits to delete!')
            sleep(1*state["SLEEP_SPEED"])
            print('[!] Returning to User Screen...')
            sleep(2*state["SLEEP_SPEED"])
            clear()
            state["user_screen"](state)

        #If user has habits, show the list of titles so one can be selected for deletion.
        else:
            habits:list = state["active_user"].habits
            print('Total Available Habits: ',len(habits))
            habit_strings:list =  [habit.title for habit in habits] + ['Go Back to User Screen']
            ans = quest.select('Be careful, which habit would you like to permanently delete?', habit_strings).ask()
            
            #Option Return
            if(ans == 'Go Back to User Screen'):
                sleep(1*state["SLEEP_SPEED"])
                print('[!] Returning to User Screen...')
                sleep(2*state["SLEEP_SPEED"])
                clear()
                state["user_screen"](state)
            
            #If a habit title is selected, continue to delete habit.
            else:
                print('Showing each habit: ...')
                #Habit to Delete
                h2d = None
                index = 0
                #Go over the habits until we find the user specified title (take note that habits with same title would always delete the first one!)
                for habit in state["active_user"].habits:
                    if ans == habit.title:
                        h2d = habit
                        print('Habit at Index: ',index)
                        #Exit the loop so we don't increment the index further.
                        break
                    else:
                        #If habit title not yet equal, increment index and compare next one in list.
                        index += 1

                sleep(1*state["SLEEP_SPEED"])
                print(f'Deleting "{h2d.title}" habit with id: {h2d.habit_id}...')

                #Remove habit from memory, since habit instance also includes the checkins list we don't have to remove these specifically from memory.
                state["active_user"].habits.pop(index)

                #Habit to remove from db
                print('Deleting habits from database..')
                api.db_habits_delete(h2d.habit_id)

                #Remove all checkins for the habit_id
                print('Deleting checkins for habit from database...')
                api.db_checkins_delete(h2d.habit_id)

                #state["active_user"].delete_habit(habit_id)
                sleep(1*state["SLEEP_SPEED"])
                print('[!] Returning to User Screen...')
                sleep(2*state["SLEEP_SPEED"])
                clear()
                state["user_screen"](state)

