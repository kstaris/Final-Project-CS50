# True car price calculator
#### Video Demo:  https://youtu.be/UJQ8USHiNac
#### Description:
  This is a calculator that gives you a simple way to calculate the true cost of car ownership. Usually, we think of just the initial price (or leasing) and fuel price when we think about it. But there are a few more expenses to consider. It is especially interesting if you are considering buying a new or used car and are wondering if it makes sense for you to switch to an electric vehicle. After looking online, I realised that there are calculators that give you the opportunity to calculate the true car ownership price, but they miss some of the parameters I find important or do not allow to save and compare cars.
#### Contents:
  The web app is designed using Flask framework. Templates folder contains all the html files, static folder contains the style sheet.
##### app.py
  This is the main backend file with all the logic and where all the templates are rendered.
##### helpers.py
  This file contains 2 functions that are takend from CS50 finance problemset - apology() and login_required(). Since they already had all the necessary funcionality I did not see a reason to develop them from scratch.
##### cars.db
  A sqlite3 database that contains 3 tables. One for the cars that users have saved, one for usernames and passwords and one for the available car manufacturers, models and years.
##### *Templates*
##### Index:
  On the first page I have made a form that you have to fill to find out the price. The car manufacturer, models and years are provided from a database. These are necessary to fill only if you wish to save your query. If you don't know what to input for some of these parameters, you can opt to have it filled with average values and then adjust them to your preferences. The monthly price changes dynamically on each value change so it is easier for you to see what matters more. If you have logged in, you can also save your results in database and go to "Saved searches".
  To generate options for model and year page uses a XMLHttpRequest method. I chose to use this insetead of form just to explore a different method.
  To calculate the monthly price and update all the input fields javascript is used.
##### Saved queries:
  In saved queries page you can see all the cars that you have saved. From here you can edit or delete any of the cars. If you want to compare cars, you can do so for up to 3 cars. You must check the cars that you want to compare and click the "Compare" button. A table will be generated that displays all the selected car parameters.
  All the functionality of this page is acheived by using flask Jinja2
##### Edit:
  Edit page looks very similar to index page, but here you have an "edit" instead of "save" button. Once you click it the values for the chosen car are updated.
  Functionally this page is very similar to index page.
##### Login, register and apology
  These templates are from CS50 finance problem set. I chose not to make them from scratch since these already did the necessay job.
