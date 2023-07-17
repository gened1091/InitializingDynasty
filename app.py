import os

from flask import Flask, redirect, render_template, request
from flask_session import Session
import numpy as np
import pandas as pd
import random
from helpers import get_normal_in_range, cap_0_100

# Configure application
app = Flask(__name__)
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Define the structure of an NPC class instance (the game objects that the player manipulates)
class NPC:
    """This is used when instantiating NPCs in global Pandas DataFrame each time the webpage is loaded"""
    def __init__(self, crime=0, reliability=0, agriculture=0, trade=0, office=0, district = 0):
        self.crime = crime
        self.reliability = reliability
        self.agriculture = agriculture
        self.trade = trade
        self.office = office
        self.district = district
    
    """This is used to initialize player values randomly each time a new game is started"""
    def set_default_values(self):
        self.crime = get_normal_in_range(60, 10)
        self.reliability = get_normal_in_range(40, 10)
        self.agriculture = get_normal_in_range(50, 10)
        self.trade = get_normal_in_range(50, 10)
        self.office = get_normal_in_range(50, 10)
        self.district = random.randint(1,3)
    
    """This is used to get DISPLAY values for an NPC object, depending on surveillance accuracy"""
    def surveillance(self, surveillance):
        
        return {"crime": cap_0_100(self.crime + random.uniform(-1, 1)*surveillance),
                "reliability": cap_0_100(self.reliability + random.uniform(-1, 1)*surveillance),
                "agriculture": cap_0_100(self.agriculture + random.uniform(-1, 1)*surveillance),
                "trade": cap_0_100(self.trade + random.uniform(-1, 1)*surveillance),
                "office": cap_0_100(self.office + random.uniform(-1, 1)*surveillance),
                "district": self.district}


# Create data structures and global variables that control function of game
population = 25
initial_money = 10000
current_move = 0
current_surveillance_tier = 0
ag_const = 100/33
tr_const = 80/33
off_const = 150/33
tiers = [25, 20, 15, 10, 5]
tier_costs = [0, 2500, 3000, 3700, 4700]
reward_costs = [100, 400, 900]
punish_costs = [4, 10, 15]
direct_effects = [2, 6, 12]
secondary_effects = [0.8, 2.4, 4.8]
npc_data = [NPC() for i in np.arange(population)]
society_data = pd.DataFrame({'efficiency': [], 'money': [], 'unrest': []})


# Define functions to aggregate societal/NPC data in various ways
def get_efficiency():
    """get the society's efficiency score based on npc_data global list """
    avg_reliability = np.mean([npc.reliability for npc in npc_data])
    avg_crime = np.mean([npc.crime for npc in npc_data])

    total_agriculture = np.sum([npc.agriculture for npc in npc_data if npc.district == 1])
    total_trade = np.sum([npc.trade for npc in npc_data if npc.district == 2])
    total_office = np.sum([npc.office for npc in npc_data if npc.district == 3])
    avg_productivity = (total_agriculture + total_trade + total_office) / population

    return round((avg_reliability - avg_crime + avg_productivity)/2)

def get_unrest(prev_unrest = 0):
    """get the society's unrest score based on npc_data global list """
    avg_reliability = np.mean([npc.reliability for npc in npc_data])
    avg_crime = np.mean([npc.crime for npc in npc_data])
    unrest_decrease_rate = (avg_crime-avg_reliability)/400 + 0.75

    return round(unrest_decrease_rate*prev_unrest + (avg_crime-avg_reliability)*0.1)



# Define functions to control flow between HTML pages
@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    return render_template("index.html")

@app.route("/learn", methods=["GET", "POST"])
def learn():
    return render_template("learn.html")


@app.route("/play_start", methods=["GET", "POST"])
def play_start():
    global current_move
    global current_surveillance_tier
    global npc_data
    global society_data

    """RESET CODE: ensure the game always starts with random NPC values and fixed society values"""
    current_move = 1
    current_surveillance_tier = 0
    for i in np.arange(population):
        npc_data[i].set_default_values()
    society_data = pd.DataFrame({'efficiency': [get_efficiency()], 'money': [initial_money], 'unrest': [get_unrest()]})

    return render_template("play_start.html")


@app.route("/play", methods=["GET", "POST"])
def play():
    global current_move
    global current_surveillance_tier
    global npc_data
    global society_data

    if request.method == "GET":
        # Get current state of society
        current_status = society_data.iloc[society_data.shape[0]-1]
        optimization=0
        
    if request.method == "POST":
        action_in_ag = False
        action_in_tr = False
        action_in_off = False
        current_move += 1
        current_status = society_data.iloc[society_data.shape[0]-1]
        # Get current societal attributes to modify based on user input
        new_efficiency = current_status.efficiency
        new_money = current_status.money
        new_unrest = current_status.unrest
  
        # If user decides to change surveillance tier, alter tier and charge appropriate amount
        tier = int(request.form.get("surveillance"))
        if tier > current_surveillance_tier:
            current_surveillance_tier = tier
            new_money -= tier_costs[current_surveillance_tier]
        
        new_unrest = get_unrest(new_unrest)

        for i in range(population):
            # Enact user parameters for act NPCs
            action = request.form.get(f"action{i}") #string saying reward/punish
            severity = int(request.form.get(f"severity{i}")) #int either 1, 2, 3
            relocation = int(request.form.get(f"location{i}")) #int either 1, 2, 3
           
            # Enact location change
            if relocation != npc_data[i].district:
                npc_data[i].district = relocation
        

            # Check for action
            if action != "leave":
                # Check for action in district
                if npc_data[i].district == 1:
                    action_in_ag = True  
                elif npc_data[i].district == 2:
                    action_in_tr = True
                elif npc_data[i].district == 3:
                    action_in_off = True

                # reward and punish actions
                if action == "reward":  
                    # Direct Effects
                    new_money -= reward_costs[severity]
                    npc_data[i].reliability += direct_effects[severity]
                    # Secondary Effects
                    for j in range(population):
                        if i != j and npc_data[i].district == npc_data[j].district:
                            npc_data[j].reliability += secondary_effects[severity]

                if action == "punish":
                    # Direct Effects
                    new_unrest += punish_costs[severity]
                    npc_data[i].crime -= direct_effects[severity]
                    # Secondary Effects
                    for j in range(population):
                        if i != j and npc_data[i].district == npc_data[j].district:
                            npc_data[j].reliability += secondary_effects[severity]

        for i in range(population):
            if action_in_ag == False or action_in_tr == False or action_in_off == False:
                npc_data[i].reliability -= 1
                npc_data[i].crime += 1

            # Reset values to 0 if < 0
            if npc_data[i].reliability < 0:
                npc_data[i].reliability = 0
            if npc_data[i].crime < 0:
                npc_data[i].crime = 0


        avg_reliability = np.mean([npc.reliability for npc in npc_data])
        avg_crime = np.mean([npc.crime for npc in npc_data])

        ag_align_total = [npc.agriculture for npc in npc_data if npc.district==1]
        if len(ag_align_total) > 0:
            ag_align = np.mean(ag_align_total)
        else:
            ag_align = 0

        tr_align_total = [npc.trade for npc in npc_data if npc.district==2]
        if len(tr_align_total) > 0:
            tr_align = np.mean(tr_align_total)
        else:
            tr_align = 0

        off_align_total = [npc.office for npc in npc_data if npc.district==3]
        if len(off_align_total) > 0:
            off_align = np.mean(off_align_total)
        else:
            off_align = 0

        ag_income = (ag_const)*(avg_reliability - avg_crime + ag_align)
        tr_income = (tr_const)*(avg_reliability - avg_crime + tr_align)
        off_income = (off_const)*(avg_reliability - avg_crime + off_align)
        new_money += round(ag_income + tr_income + off_income)


        optimization = round(new_money/(initial_money + (2000 * (ag_const + tr_const + off_const))) * 70 - new_unrest/2 + ((ag_align + tr_align + off_align)/3 * 3/10))
        if optimization == 100:
            return render_template("play_win.html", moves=current_move-1)
        if new_unrest >= 100:
            return render_template("play_lose.html")
        if new_money <= 0:
            return render_template("play_bankrupt.html")


        # Add a new row to society_data corresponding to user's move, update current_status as well
        current_status = {'efficiency': get_efficiency(), 'money': new_money, 'unrest': new_unrest}
        society_data = society_data.append(current_status, ignore_index=True)

    return render_template("play.html", npc_data = [npc.surveillance(surveillance=tiers[current_surveillance_tier]) for npc in npc_data], current_move = current_move, society_data = current_status, current_tier = current_surveillance_tier, tiers=tiers, tier_costs=tier_costs, optimization=optimization)
