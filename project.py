import sys, re, csv, rich, os, time
from console import console

class Poll:
    
    def __init__(self,question,option1,option1vote,option2,option2_vote,status):
        self.question = question
        self.option1 = option1
        self.option1vote = option1vote
        self.option2 = option2
        self.option2_vote = option2_vote
        self.status = status
        
    def __str__(self):
        
        console.print(f"Question 1: {self.question}",style="bold magenta",justify="left")
    
class User:
    
    def __init__(self, username, votedPolls):
        self.username = username
        self.votedPolls = votedPolls
        
    def __str__(self):
        return self.username
    
    # @property
    # def username(self):
    #     return self._username
    
    # @username.setter
    # def username(self, username):
        
    #     if match := re.search("^[a-zA-Z0-9_]+$",username.strip(),re.IGNORECASE):
    #         self._username = username
    #     else:
    #         console.print("Username can only contain a-z, A-Z, 0-9 and _",style="bold red",justify="center")
    
# Global Variables
programState = "login"

usersList = []
currentUser = None

completedPollsList = []
onGoingPollsList = []

current_dir = os.path.dirname(__file__)
csv_dir = os.path.join(current_dir, "csv")
users_csv_file = os.path.join(csv_dir, "users.csv")
polls_csv_file = os.path.join(csv_dir,"polls.csv")


administratorState = False
currentUser = None


def main():
    
    clear_screen()

    global programState
    
    initial_data_allocation()
    
    
    console.rule("")
    console.print("WELCOME TO THE POLL!\n Enter [blue]'quit'[/] any time to exit.",style="bold magenta on black",justify="center")
    console.rule("")
    
    while True:
        
        match programState:
            case "login":
                console.print("[1] Login as an Admin\n[2] Login or Sign Up with an Username",style="bold blue",justify="center")
                
                try:
                    signUpOption = console.input("[bold red]How would you like to proceed? (Enter in 1 or 2): [/]")
                except (EOFError,KeyboardInterrupt):
                    print("\n")
                    sys.exit()
                
                if match := re.search("^1|2$",signUpOption.strip(),re.IGNORECASE):
                    programState = "admin_login" if signUpOption == "1" else "user_login"    
            case "admin_login":
                admin_login()
            case "user_login":
                user_login()      
            case "home":
                home_panel()
            case "admin_panel":
                admin_panel()
            case "completed_polls":
                completed_polls()
                break
            case "ongoing_polls":
                ongoing_polls()
            case "new_poll":
                new_poll_panel()    
            case _:
                pass
            
    
def initial_data_allocation():
    
    global users_csv_file, usersList, csv_dir
    
    usernameList = []
    uservotedPollsList = []
    
    # Reading Users from Users csv
    with open(users_csv_file) as file:
        
        reader = csv.reader(file)
        
        for row in reader:
            
            usernameList.append(User(row[0],uservotedPollsList))
    
        
    for user in usernameList:
        new_user_csv_file = os.path.join(csv_dir,f"Users/{user.username}.csv")
        
        if os.path.exists(new_user_csv_file):
            with open(new_user_csv_file,'r') as file:
                
                reader = csv.reader(file)
                
                for row in reader:
                    
                    if row[0]:
                        uservotedPollsList.append(row[0])
                     
        
    for user in usernameList:
        
        usersList.append(User(user.username,uservotedPollsList))
        
        
    # Reading Polls from Polls.csv
    
    polls_csv_file = os.path.join(csv_dir,"polls.csv")
    
    with open(polls_csv_file) as file:
        
        reader = csv.DictReader(file)
        
        for row in reader:
            
            if row["status"] == "on_going":
                onGoingPollsList.append(Poll(row["question"],row["option1"],row["option1_vote"],row["option2"],row["option2_vote"],row["status"]))
            elif row["status"] == "completed":
                completedPollsList.append(Poll(row["question"],row["option1"],row["option1_vote"],row["option2"],row["option2_vote"],row["status"]))
        

def admin_login():
    
    global programState, administratorState
    
    clear_screen()
    
    console.print("ADMIN LOGIN",style="bold blue",justify="center")
    
    while True:
        try:
            adminUsername = console.input("Enter Admin Username: ")
        except (EOFError,KeyboardInterrupt):  
            print("\n")
            sys.exit()
        
        if adminUsername == "quit":
            programState = "login"
            clear_screen()
            break
    
        try:
            adminPassword = console.input("Enter Admin Password: ")
        except (EOFError,KeyboardInterrupt):
            print("\n")
            sys.exit()
        
        if adminPassword == "quit":
            programState = "login"
            clear_screen()
            break
    
        if adminUsername == "admin" and adminPassword == "admin":
            programState = "admin_panel"
            administratorState = True
            break
        else:
            console.print("Incorrect Username or Password!! Try Again. Enter [bold magenta]quit[/] to exit",style="bold red",justify="center")
    
def clear_screen():
    
    time.sleep(0.3)
    os.system('cls')    

def user_login():
    
    
    global programState, users_csv_file, currentUser
    
    clear_screen()
    
    console.print("USER LOGIN",style="bold blue",justify="center")
    
    while True:
        
        try:
            username = console.input("Enter Username: ")
        except (EOFError,KeyboardInterrupt):
            print("\n")
            sys.exit()
        
        if username == "quit":
            programState = "login"
            clear_screen()
            break
        
        allUsers = [user.username for user in usersList]
        
        if username in allUsers:
            programState = "home"
            currentUser = username
            clear_screen()
            break
        
        currentUser = username
        user  = User(username,[])
        
        usersList.append(user)
        
        
        with open(users_csv_file,"a+",newline='') as file:
            
            writer = csv.writer(file)
            
            writer.writerow([username])
            
        programState = "home"
        break  

def home_panel():
    
    global programState
    
    clear_screen()
    
    console.print("USER PANEL",style="bold blue",justify="center")
    
    console.print("[1] Completed Polls\n[2] On Going Polls",style="bold blue",justify="center")
    
    while True:
        try:
            homeOption = console.input("[bold red]How would you like to proceed? (Enter in 1 or 2): [/]")
        except (EOFError,KeyboardInterrupt):
            print("\n")
            sys.exit()
    
        if match := re.search("^1|2$",homeOption.strip(),re.IGNORECASE):
            if homeOption == "1":
                programState = "completed_polls"
                break
            else:
                programState = "ongoing_polls"
                break
        
def admin_panel():
    
    global programState
    
    clear_screen()
    
    console.print("ADMIN PANEL",style="bold blue ",justify="center")
    
    console.print("[1] Completed Polls\n[2] On Going Polls\n [3] Add New Poll",style="bold blue",justify="center")
    
    while True:
        try:
            homeOption = console.input("[bold red]How would you like to proceed? (Enter in 1, 2 or 3): [/]")
        except (EOFError,KeyboardInterrupt):
            print("\n")
            sys.exit()
            
        if homeOption.strip() == "quit":
            programState = "login"
            break
    
        if match := re.search("^1|2|3$",homeOption.strip(),re.IGNORECASE):
            if homeOption == "1":
                programState = "completed_polls"
                break
            elif homeOption == "2":
                programState = "ongoing_polls"
                break
            else:
                programState = "new_poll"
                break
             
def completed_polls():

    clear_screen()
    
def ongoing_polls():

    global programState, administratorState, csv_dir, polls_csv_file
    
    clear_screen()
    
    votedPollsIndex = []
    
    console.print("ON GOING POLL\n",style="bold blue",justify="center")
    
    for pollIndex,poll in enumerate(onGoingPollsList):
        
        if administratorState == False:
            
            # Checking if the User has voted for this particular poll...
            
            for user in usersList:
                
                if currentUser == user.username:
                    User = user
                    break
            
            if len(User.votedPolls) > 0:
                for votedPoll in User.votedPolls:

                    if votedPoll == poll.question:
                        console.print("[bold green] You have voted on this poll.✅ [/]")
                        votedPollsIndex.append(pollIndex)
                    
        console.print(f"[{pollIndex+1}.] [bold magenta] [red]Question:[/] {poll.question} [/]")
        console.print(f"\t[bold magenta] [red] Option 1:[/] {poll.option1}\t Votes: {poll.option1vote}[/]")
        console.print(f"\t[bold magenta] [red] Option 2:[/] {poll.option2}\t Votes: {poll.option2_vote}[/] \n\n")
        
    
    while True:
        
        try:
            pollInput = console.input("[bold red] Enter poll number: [/]")
        except (EOFError,KeyboardInterrupt):
            print("\n")
            sys.exit()
            
        if pollInput.strip() == "quit":
            if administratorState == False:
                programState = "home"
                break
            else:
                programState = "admin_panel"
                break
        
        if pollInput.isnumeric():
            pollIndex = int(pollInput) - 1
            
            if pollIndex in votedPollsIndex:
                console.print("[bold red] You have already voted on this poll. [/]")
                continue
            
            try:
                inputOption = console.input("[bold red] Enter option number [Answer in 1 or 2]: [/]").strip()
            except (EOFError,KeyboardInterrupt):
                print("\n")
                sys.exit()
            
            if inputOption.strip() == "quit":
                if administratorState == False:
                    programState = "home"
                    break
                else:
                    programState = "admin_panel"
                    break
            
            if match := re.search(r"^1|2$",inputOption,re.IGNORECASE):
                
                users_dir = os.path.join(csv_dir,"Users")
                
                new_user_csv_file = os.path.join(users_dir,f"{currentUser}.csv")
                
                with open(new_user_csv_file,"a+",newline='') as file:
                    
                    writer = csv.writer(file)
                    
                    writer.writerow([f"{onGoingPollsList[pollIndex].question}"])
                    
                
                if inputOption == "1":
                    onGoingPollsList[pollIndex].option1vote = int(onGoingPollsList[pollIndex].option1vote) + 1
                else:
                    onGoingPollsList[pollIndex].option2_vote = int(onGoingPollsList[pollIndex].option2_vote) + 1
                
                pollsList =  [poll for poll in onGoingPollsList]
                pollsList.extend([poll for poll in completedPollsList])
                
                
                
                with open(polls_csv_file,"w",newline='') as file:
                    
                    writer = csv.DictWriter(file,fieldnames=["question","option1","option1_vote","option2","option2_vote","status"])
                    
                    try:
                        writer.writeheader()
                    except IOError:
                        console.print("Can't write to file\n",style="bold red",justify="center")
                        sys.exit()
            
                    for poll in pollsList:
                        pollScheme = {
                        "question":poll.question,
                        "option1":poll.option1,
                        "option1_vote":poll.option1vote,
                        "option2":poll.option2,
                        "option2_vote":poll.option2_vote,
                        "status":poll.status}
                    
                        writer.writerow(pollScheme)
                    
                console.print("Successful updating of polls\n",style="bold green",justify="center")
                programState = "ongoing_polls"
                break
            
        else:
            continue
        
def new_poll_panel():
    

    
    global programState, csv_dir, polls_csv_file
    
    clear_screen()
    
    while True:
        try:
            pollQuestion = console.input("[bold red] Enter Poll Question: [/]").strip()
            pollOption1 = console.input("[bold red] Enter Option 1: [/]").strip()
            pollOption2 = console.input("[bold red] Enter Option 2: [/]").strip()
        except (EOFError,KeyboardInterrupt):
            print("\n")
            sys.exit()
            
        if pollQuestion == "quit" or pollOption1 == "quit" or pollOption2 == "quit":
            programState = "admin_panel"
            break
        
        newPoll = Poll(pollQuestion,pollOption1,0,pollOption2,0,"on_going")
        
        onGoingPollsList.append(newPoll)
        
        
        if os.stat(polls_csv_file).st_size == 0:
            with open(polls_csv_file,"a+",newline='') as file:
                writer = csv.DictWriter(file,fieldnames=["question","option1","option1_vote","option2","option2_vote","status"])
                
            try:
                writer.writeheader()
            except IOError:
                console.print("Can't write to file\n",style="bold red",justify="center")
                sys.exit()
        
        # Writing to the polls csv file 
        with open(polls_csv_file,"a+",newline='') as file:
            
            writer = csv.DictWriter(file,fieldnames=["question","option1","option1_vote","option2","option2_vote","status"])
            
            pollScheme = {
                "question":pollQuestion,
                "option1":pollOption1,
                "option1_vote":0,
                "option2":pollOption2,
                "option2_vote":0,
                "status":"on_going"
            }
            
            writer.writerow(pollScheme)
        
        programState = "admin_panel"
        break

if __name__ == "__main__":
    main()