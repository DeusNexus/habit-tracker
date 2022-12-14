import os
import questionary as quest
from time import sleep
from datetime import datetime
from Database import db_api as api
from Utils import interval_to_seconds

#Function to Clear Terminal
clear = lambda : os.system('tput reset')

#Text Styling
from Utils import style

#Return to the user screen
def return_user_screen(state):
    sleep(1*state["SLEEP_SPEED"])
    print('[!] Returning back to User Screen...')
    sleep(1*state["SLEEP_SPEED"])
    clear()
    state["user_screen"](state)

#Do new habit, print information, show options and go through questionary style to fill out the details
def new(state):
    '''The new screen is used for creating new habits, which can be normal or dynamic. It receives the User-object, active_user, from the user_screen view and also the user_screen function that renders the main menu when exiting the view screen.'''
    clear()
    print(style('[New Screen]','UNDERLINE'))
    print('Create new habits; give them a proper title, description and interval. Optionally you can add more details if you wish which can be used to filter the habit.\n')
    questions = ['Regular Habit - Fixed Deadlines','Dynamic Habit - Specify how often to check in before deadline'] + ['Go Back to User Screen']
    ans = quest.select('Choose what kind of Habit you want to create:', questions,style=state['qstyle']).ask()

    def questionary(is_dynamic:bool):
        #user input
        title_ask = interval_ask = milestone_ask = checkin_num_before_deadline_ask = cost_ask = start_from_ask = True

        while(title_ask):
            #Test user input
            title = quest.text('What will be the title of the new habit? E.g. Gym Workout',style=state['qstyle']).ask()
            if len(title) > 2: 
                title_ask = False
            else:
                print('Please use 3 or more characters for a title!')

        #Test user input
        description = quest.text('Provide a description? E.g. Leg day',style=state['qstyle']).ask()

        while(interval_ask):
            #Test user input
            interval = quest.text('Define an interval for the habit. You can use any whole number followed by m/H/D/W/M/Y; e.g. 3D or 1W or 30m',style=state['qstyle']).ask()
            try :
                interval_to_seconds(interval)
                interval_ask = False
            except ValueError:
                print('Please input a valid interval format. E.g: <int><char> like 15m, 2H, 5D, 1W, 6M, 2Y')

        if(is_dynamic):
            while(checkin_num_before_deadline_ask):
                #Test user input
                try:
                    checkin_num_before_deadline = int(quest.text('How often do you want to perform the habit before a deadline? Type an integer numer; e.g. 1, 3, 5',style=state['qstyle']).ask())
                    #When int is < 0, try again.
                    if(checkin_num_before_deadline < 1 ):
                        print('Please provide a integer larger than 0!')
                    #When valid, set loop to false and continue outer code
                    else:
                        checkin_num_before_deadline_ask = False
                except ValueError as e:
                    #If string does not represent a valid int, ask again (return to top of while-loop)
                    print('Please use an integer value for how many times you need to checkin before the deadline. E.g. 1, 3, 10')
        
        #If its not dynamic, set None value
        else:
            checkin_num_before_deadline = None

        optional = quest.confirm("Fill out optional fields? E.g. active, difficulity, category, moto, importance, milestone target.",style=state['qstyle']).ask()

        #No optional questions -> Fill default values
        active = True
        start_from = datetime.now()
        difficulity = None
        category = None
        moto = None
        importance = None
        milestone = None
        cost = 0

        #If optional is True, fill out more details, default will be overriden
        if(optional):
            active = quest.confirm("Do you directly want to set the habit to active?",style=state['qstyle']).ask()
            if(active):
                start_from = datetime.now()
            else:
                while(start_from_ask):
                    try:
                        #Test user input
                        start_from_res = quest.text('Provide a start date when you want it to become active? Please follow the format YYYY-MM-DD HH:mm, e.g. 2050-03-28 15:35.',style=state['qstyle']).ask()
                        start_from = datetime.strptime(start_from_res+'.000001', "%Y-%m-%d %H:%M:%S.%f")
                        start_from_ask = False
                    except ValueError as e:
                        print('Please provide a valid date in the format YYYY-MM-DD HH:MM:SS, e.g. 2030-01-28 12:13:14')

            use_difficulity = quest.confirm('Do you want to set a difficulity?',style=state['qstyle']).ask()
            if(use_difficulity):
                difficulity = quest.select("How difficult do you find it to perform?",['1','2','3','4','5'],style=state['qstyle']).ask()

            #Test user input
            use_category = quest.confirm('Do you want to assign this habit to a common category? Similar habits will be grouped together. E.g.: Eduction, Sport, Hobby',style=state['qstyle']).ask()
            if(use_category):
                category = quest.text('Specify the category for this habit',style=state['qstyle']).ask()

            #Test user input
            use_moto = quest.confirm('Do you want to set a moto?',style=state['qstyle']).ask()
            if(use_moto):
                moto = quest.text('What is your moto you would like to remind yourself of to keep doing the habit?').ask()

            use_importance = quest.confirm('Do you want to set importance?',style=state['qstyle']).ask()
            if(use_importance):
                importance = quest.select("How important do you find it to perform?",['1','2','3','4','5'],style=state['qstyle']).ask()

            use_milestone = quest.confirm("Do you want to set a milestone achievement? It will display message each time when you reached n multiple streak of your milestone.",style=state['qstyle']).ask()
            if(use_milestone):
                while(milestone_ask):
                    #Test user input
                    try:
                        milestone = int(quest.text("Set milestone target for multiple successes. E.g. 5 for 5 consequent succesfull checkins!",style=state['qstyle']).ask())
                        if(milestone < 1):
                            print('You need to specify a milestone of atleast 1 or higher.')
                        else:
                            milestone_ask = False
                    except ValueError as e:
                        print("Use an integer to specify the milestone target.")
            
            use_cost = quest.confirm("Would you like to associate a cost for the habit? E.g. the habit will calculate the total spend cost each time you checked in.",style=state['qstyle']).ask()
            if(use_cost):
                while(cost_ask):
                    #Test user input
                    try:
                        cost = float(quest.text("Please specify how much the habit costs per time you do it/check in.",style=state['qstyle']).ask())
                        if(not cost > 0):
                            print('Please specify a positive number for the cost.')
                        else:
                            cost_ask = False
                    except ValueError as e:
                        print("Use a correct float number to define your habit cost! E.g.: 1, 2.50, 9.99")
                
        #Create habit with user input
        try:
            habit_index = len(state["active_user"].habits)
            #When habit_id = None is passed it automatically generates one.
            state["active_user"].create_habit(title, description, interval, active, start_from, difficulity, category, moto, importance, milestone, is_dynamic, checkin_num_before_deadline,None,state["active_user"].user_id,cost)
            #Insert the habit into the db
            api.db_habits_insert([
                {
                    'user_id':state["active_user"].user_id,
                    'habit_id':state["active_user"].habits[habit_index].habit_id,
                    'title':title,
                    'description':description,
                    'interval':interval,
                    'active':'True' if active else 'False',
                    'start_from':start_from,
                    'difficulity':difficulity,
                    'category':category,
                    'moto':moto,
                    'importance':importance,
                    'milestone_streak':milestone,
                    'is_dynamic':'True' if is_dynamic else 'False',
                    'checkin_num_before_deadline':checkin_num_before_deadline,
                    'dynamic_count':state["active_user"].habits[habit_index].dynamic_count,
                    'created_on':state["active_user"].habits[habit_index].created_on,
                    'prev_deadline':state["active_user"].habits[habit_index].prev_deadline,
                    'next_deadline':state["active_user"].habits[habit_index].next_deadline,
                    'streak':state["active_user"].habits[habit_index].streak,
                    'success':state["active_user"].habits[habit_index].success,
                    'fail':state["active_user"].habits[habit_index].fail,
                    'cost':cost,
                    'cost_accum':0
                }
            ])
            print('[*] Added your habit!')
        except Exception as e:
            print('[!] Failed to add habit, an error occured!')
            print(e)
    
    #Regular habit
    if(ans == questions[0]):
        sleep(1*state["SLEEP_SPEED"])
        questionary(is_dynamic=False)

        #Show habit before submit? Then return to user screen
        return_user_screen(state)

    #Dynamic Habit
    elif(ans == questions[1]):
        sleep(1*state["SLEEP_SPEED"])
        questionary(is_dynamic=True)

        #Show habit before submit? Then return to user screen
        return_user_screen(state)

    elif(ans == 'Go Back to User Screen'):
        return_user_screen(state)