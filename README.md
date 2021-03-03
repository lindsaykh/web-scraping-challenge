## web-scraping-challenge
UNC CH BC HW

#Summary:
The code here first scrapes info regarding mars exploration using pandas methodology in a jupyter notebook.
Then, similar code is used to create a python function that scrapes the same information to post via flask
on a website. 

The jupyter notebook can be run as-is. To look at the html, app.py should be run in your terminal and should 
be able to access the 'templates' folder that contains the index.html file. The app.py runs the scrape_mars.py
function, places the scraped data into a dictionary, then places that dictionary as a collection in a mongo db
called mars_db. 

After running app.py in your terminal, you should be able to open your local directory and click on the button
saying "Get New Data!" which will run a new scrape. The website (index.html) will be updated with new images
and Mars-related article clips and facts from the scrape websites.

#References:

for render_template/etc. in flask:
https://flask.palletsprojects.com/en/1.1.x/quickstart/

for comparison/overall help:
https://github.com/goldenb85/web-scraping-challenge/blob/master/Missions_to_Mars/templates/index.html


