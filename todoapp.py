from datetime import datetime
import re
import json

def main():
    show_menu()
    while True:
        num = input('Choose what you wish to do on this app: ')
        if num == '1':
            add_task(tasks)
        elif num == '2':
            view_tasks(tasks)
        elif num == '3':
            delete_tasks(tasks)
        elif num == '4':
            edit_task(tasks)
        elif num == '5':
            change_status(tasks)
        elif num == '6':
            due_dates(tasks)
        elif num == '7':
            add_category(tasks)
        elif num == '8':
            filter_tasks(tasks)
        else:
            print('Please choose one of the valid options among the task numbers on the menu!')

        cont = input('Do you want to go again? (y/n): ')

        if cont == 'n':
            break

def show_menu():
    print('''----Welcome to your task manager app----
1. Add task 
2. View current tasks 
3. Remove task 
4. Edit task 
5. Update task status 
6. Add due date for long term tasks
7. Add category a task
8. Filter tasks based on your choice        
--------------------------
          ''')

try: 
    with open("/workspaces/tasks.json", "r") as f:
        tasks = json.load(f)
except FileNotFoundError:
    tasks = []

#defining a function for choosing the task which the user wishes to work on , will be called for all functions
def choose():
    try: 
        choice = int(input('Select which task you wish to edit (pick its number): '))
        if choice not in range(1, len(tasks) + 1):
            print('Please enter a valid number!')
            return None
    except ValueError:
        print('Please enter a number!')
    return choice

def add_task(tasks):
    while True: 
        task_name = input('Please enter the name of the task at hand: ').lower()
        task_priority = input('Define task priority(high/medium/low): ').lower()
        task_status = input('Enter the status of the task(finished/unfinished): ').lower()
         
        if task_priority in ['low', 'medium', 'high']  and task_status in ['finished', 'unfinished']:  
            tasks.append({
                'name': task_name,
                'priority': task_priority,
                'status': task_status, 
                'date': None,
                'category': 'Not defined'
            })
            print('Task added successfully!')
        else:
            print('Please enter something valid')
        
        cont = input('Continue? (y/n): ')

        if cont == 'n':
            break

def view_tasks(tasks):
    if not tasks:
        print('Your task list is currently empty.')
    else:
        for i, task in enumerate(tasks):
            print(f"{i + 1}.{task['name'].capitalize()}.--> Details: (priority: {task['priority']}), (status: {task['status']}), (due date: {task['date']}), (category: {task['category']})")

def change_status(tasks):
    view_tasks(tasks)
    choice = choose()
    for indx, task in enumerate(tasks):
        if choice == indx + 1:
            if task['status'] == 'finished':
                print('Task status has already been defined as finished.')
            else:
                task['status'] = 'finished'
                print('Task status changed successfully!') 

def delete_tasks(tasks):
    choice = choose()
    for indx, task in enumerate(tasks):
        if choice == indx + 1:
            tasks.remove(task)
            print('Task deleted successfully!')

def due_dates(tasks):
    if not tasks:
        print('No tasks yet!')
        return None
    
    choice = choice()

    datestr = input('Please enter the date(DD-MM-YYYY): ')
    if not re.search(r'\d{2}-\d{2}-\d{4}', datestr):
        print('Invalid input!')
    else:
        date = datetime.strptime(datestr, '%d-%m-%Y')
        tasks[choice - 1]['date'] = date
        print('Due date assigned successfully!')

def add_category(tasks):
    if not tasks:
        print('No tasks yet!')
        return None
    
    choice = choose()
    print('Choose the category of your task. If you want to add your category, type self')
    catg = input('[personal/work/school/shopping]: ')
    if catg == 'self':
        self_catg = input('Please write the category: ')
        tasks[choice - 1]['category']  = self_catg
    else:
        tasks[choice - 1]['category']  = catg
    print('Task category added successfully!')

def edit_task(tasks):
    choice = choose()
    which = input('Decide what property of your task you wish to edit(name/priority/status/due/category): ').lower()
    new = input('Insert the new value: ').lower()

    if which not in ['name', 'priority', 'status', 'due', 'category']:
        print('Choose a vaild attribute!')
    else:
        match which:
            case 'name':
                tasks[choice - 1]['name'] = new
            case 'priority':
                if new in ['low', 'medium', 'high']:  
                    tasks[choice - 1]['priority'] = new  
                else:
                    print('Please choose a valid option!')
            case 'status':
                if new in ['finished', 'unfinished']:
                    tasks[choice - 1]['status'] = new
                else:
                    print('Please choose a valid option!')
            case 'due':
                try: 
                    new_date = datetime.strptime(new, '%d-%m-%Y')
                    tasks[choice - 1]['date'] = new
                except ValueError:
                    print('Please use a valid format.')          
            case 'category':
                tasks[choice - 1]['category'] = new
    print('Task edited successfully!')

def filter_tasks(tasks):
    attribute = input('Choose based on what you want the tasks to be filtered: ').lower()
    if attribute not in ['priority', 'status', 'category']:
        print('Please enter a valid attribute.')
    else:
        options = list(set(task[f'task_{attribute}'] if attribute == 'category' else task[attribute] for task in tasks))
        which = input(f'Choose the {attribute} to filter by: ').lower()  

        if which not in options:
            print('Please enter an existing option')
        else:
            for task in tasks:
                value = task['category'] if attribute == 'category' else task[attribute]
                if value == which:
                    print(task['name'])

if __name__ == '__main__':
    main()

with open("/workspaces/tasks.json", "w") as f:
    json.dump(tasks, f, indent = 4)