---
files: [app.py]
window: [terminal]
---

# Initializing a Dynasty

## Quick Overview

Implement a website via which users can learn about the ancient Chinese philosophy of legalism and partake in a game that simulates running such a society (whereby the user must try to optimize this society by building overall virtue through rewards/punishments and by organizing simulated 'citizens' according to their strengths).


## User Manual

### Website Description and Functionality

The user is automatically directed to a homepage, `index.html`.  From here, they can access two webpages, `learn.html` (a static webpage containing paragraphs of education about the philosophy of legalism) as well as `play_start.html`, which contains instructions for how to play the simulation game and a button at the bottom of the page to launch the game.

Launching the game takes the user to `play.html`, where they are offered a variety of possible moves to influence their society.  These moves are all controlled via selection forms, so there is no possibility for users including erroneous inputs that could cause the underlying Python code to malfunction.  Each time that the user is ready to implement their move, they can click a button at the bottom of the webpage that reloads `play.html`, but updating all values shown to correspond to the user's latest move.

If the user wins, they are taken to `play_win.html`, where they are given the opportunity to restart the game (be redirected to `play_start.html`) if they like.  If they lose, they are taken to either `play_lose.html` (if their unrest score reaches 100) or to `play_bankrupt.html` (if their society runs out of money), with each page also providing a button to restart the game at `play_start.html`.

All webpages extend the layout contained in `layout.html`, all the style code is contained in `styles.css` or obtained from Bootstrap libraries, and all underlying functionality is controlled via `app.py` and `helpers.py`.  There are no SQL databases or other files associated with this code that were of our creation.


### Running the Code

Go to the directory corresponding to this problem (should be `final_project/`) and type `flask run` into the terminal to start Flask's built-in server.  A URL should be displayed in the terminal by Flask; click on it to launch the website using Flask's server.

From here, nothing additional needs to be done to run the code.  There are no SQL databases associated with this code, nor any other features beyond those that are accessible on the website once it is launched by Flask.  The only runtime issues that could arise involve Flask not being properly configured in the code environment in which the web app is trying to run, where certain installation commands (such as `python -m pip install flask`) may need to be executed in the user's terminal to set it up properly.

### Image Sources:

We had two externally-sourced images used in our code, the background image (https://i0.wp.com/asiatimes.com/wp-content/uploads/2020/02/Fig-1-Selden-Map-c-Bodleian-Library-University-of-Oxford.jpg?fit=1200%2C675&ssl=1) as well as the tab icon image (https://www.clipartmax.com/png/middle/1-11913_clipart-chinese-dragon-dragon-red-clip-art-at-clker-chinese-new-year.png).  The citation links to these images are also contained in the portions of code where they are used.


## Walkthrough

[YouTube Video Tutorial](http://www.youtube.com/watch?v=Pya5TPt5Y- "Initializing a Dynasty")

## Author

Isaac Jirak, Jack Bruce
