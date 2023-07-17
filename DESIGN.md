## Overview

"Initializing a Dynasty" runs off of flask via a combination of Python, CSS, and HTML code. This format allows us to create a platform for a user in which they can explore the ideas implemented in the code and explained in the web app while also having a comfortable view of the simulation on a browser. On the web-app, users have the options of learning more about Legalism or interacting with the main feature, the simulation. Under Play Game, users will be directed to how to play the game, then to running the simulation. Once the simulation 

## Elements

### app.py

The structure of the game starts with an NPC (following the imported files and the Flask configuation), which is a defined data type that holds all of the information for a citizen's data. The true values for each metric of a citizen are initialize first into the global Pandas dataframe which is used to conveniently hold of all the variables for all NPCs. These metrics are then drawn from a random distribution to get a variety in the data between citizens. The means vary between the qualities at a predetermined difference to balance the simulation. Lastly, each citizen is assigned randomly to one of three districts. 

Within the NPC data structure are also the display values (the values that the user will actually see) which are caluclated under the function surveillance. Surveillance returns a dictionary with each entry having a key value of some number within the error bars determined by the users current level of surveillance. This is accomplished by drawing a random number from a uniform distribution between -1 and 1 and multiplying that by the degree of surveillance. This is then added to the true metric value. This value is then passed to a function cap_0_100 that makes sure the value is within 0 and 100 and adjusts it if not and then rounds the number to the nearest integer.

Next are all of the global variables:
1. population determines how many NPCs there are
2. initial money is how much money the user starts with
3. current_move is the counter for how many rounds the user has simulated
4. current_surveillance_tier keeps track of how much surveillance the user has bought
5. ag_const, tr_const, and off_const are the predetermined constants for how much profit each district makes
6. tiers holds the size of the error bars in order of the degree of surveillance
7. tier_costs represents the cost of each tier of surveillance
8. reward_costs and punish_costs hold the cost for each degree of reward or punishment
9. direct_effects holds the values for implementing a change in the selected NPCs metrics
10. secondary_effects holds the values for implementing a change in the NPCs who are also in the same district as the selected NPC
11. NPC_data holds the information for every npc in a quickly accessible array
12. society data holds the variables for the efficiency, money, and unrest for every rounds

The function get_efficiency is used to determine how efficient the society is for a given round. The efficiency is calculated from a predetermined equation relating the NPCs district skill with their crime and reliability.

The function get_unrest is used to calculate a round's current unrest according to a predetermined equation.

Under app.route("/play...) the GET request method returns the page with the NPCs loaded in play_start. The POST request method executes the parameters inputted by the user. If the user changes the tier, then that is update using an if statement. Then the parameters for each NPC are processed. The action, severity, and location choices are loaded for a given NPC. If the location is different, then it is implemented, if the action is not Leave Alone, then the code checks where this action takes place. If the action is a reward, then it implements the reward effects both on the selected NPC and all the NPC with the same district assignment. Likewise for punish. 

Next, the function sees if there is an action in each district and if not, inflicts a penalty. If any values are outside of a parameters, then they are reset to be within the parameters.

Next the profit for each district is calculated. The [district]_align_total calculates how much the NPCs' skills match their district and uses this value to with the average crime and average reliability to calculate the total profit for each district. 

The optimization score is calculated using a predetermined equation. If any of the stop conditions are met, i.e. optimization = 100 to win or unrest = 100 or money = 0 to lose. If these are not met, then the new values are inputted into the dataframe and the page is reloaded with the updates. 

### layout.html

This webpage forms the basis for our entire site; all other HTML pages extend this.

The `head` portion of this file contains code to import the necessary Bootstrap libraries, configure other necessary metadata aspects of our webpage (like adjusting the size to the user's screen width), and set the displayed title and icon for the webpage (as it would appear in a browser tab).

The `body` portion of this file contains code to configure our navbar, which is the same across all our webpages.  This navbar remains stuck to the top of the page should the user scroll, and contains links to `index.html` (the navbar anchor) as well as `learn.html` and `play_start.html`.  It also contains an open container where HTML files extending `layout.html` can insert other content via Jinja.

### index.html

This is a static webpage; it does not receive anything from our Python code to display, nor does it contain any forms.  The content of the page is a large display of our project title to welcome the user as well as two cards (using Bootstrap formatting) that explain the two main components of our site (the educational and simulation components) and contain buttons to direct the user to `learn.html` and `play_start.html`.

### learn.html

This is another completely static webpage; it contains a full explanation of the philosophies of legalism for the user to read through, with some hidden hints about how to win at the game sprinkled in.

### play_start.html

This webpage contains the instructions for how to play our game as well as a button to launch the game (i.e. access `play.html`)...this is the only way the game can be started.  In the instruction portion of our page, we utilize a lot of Bootstrap-formatted forms to demonstrate to the user what they will be expected to input in each round of the game (of course, the forms on this page don't actually generate any responses, nor is there a submit button...they are purely for visual demonstration of game features).

### play.html

This webpage controls the game aspect of our website.  At the top of the page, the current round as well as the current vital metrics for the user's society are displayed (overall score, efficiency, social unrest level, and funds).  All of the display values are passed from `app.py` and integrated via Jinja.  Below, the page displays all NPC information to the user (including the built-in error associated with the user's surveillance level...all of these values are also passed from `app.py` and integrated via Jinja) in the form of Bootstrap-formatted 'progress bars'.  It also gives the user options to purchase higher surveillance levels, as well as reassign a NPC to a different district or reward/punish each NPC with varying degrees of severity.  

The entire section of this page starting with the surveillance level purchase options and spanning down to the 'simulate next month' button is contained within a single form.  The form collects everything that the user changes about their society (i.e. surveillance level purchases, reassignments of NPCs, punishments/rewards of NPCs) and submits it to be used in `app.py` once the 'simulate next month' button is pressed.  `play.html` is then _reloaded_ with the updated values obtained from `app.py`.

### play_win.html, play_lose.html, play_bankrupt.html

These three webpages are only accessed after a game is completed, depending on the outcome: if the user's overall score reaches 100, if the user's social unrest metric reaches 100, or if the user exhausts their money, respectively.  Each webpage contains a message explaining the outcome that occurred as well as a button to take the user back to `play_start.html` to begin another round of the game, if they so desire.  `play_win.html` also displays the number of rounds it took the user to win the game, in an attempt to encourage the user to beat this score that they have achieved in future rounds.

### styles.css

The first section of this stylesheet contains code to format our navbar, as implemented from the Bootstrap library.  This includes setting the background color, the color of the navbar anchor (link to `index.html`) and navbar buttons, as well as adding a hover functionality to the navbar buttons that causes the text to change to white and the button background to change to red.

The second section of this stylesheet contains code to format our tables, of which there are a lot in our website (on account of how we formatted the displays of our game).  This code sets padding and ensures that alternating lines of the table have different background colors so that it is easier to distinguish between adjacent rows.

Then, we include CSS code to add a fixed background image (of an ancient Chinese map, link to the image source included in the CSS file) on all of our webpages, as well as some additional formatting for padding in `mb-5` code blocks.  We also set all large text colors (i.e. of `h3`, `h4`, and `h5`) to be dark green.

Finally, we have some CSS code devoted to adding good padding to sections of our code devoted to showing large amounts of text as well as Bootstrap-sourced 'cards'.