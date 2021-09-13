Carbon Footprint: A CS50 Final Project by Noa Kligfeld and Ben Fisher

Our website uses Flask, html, python, jinja, sql, and matplotlib.
We use flask mail to send confirmation emails when users register,
werkzeug to hash passwords, and email_validator to make sure users input valid email address when registering.

To build our website, we build on what we accomplished in CS50 Finance.

Registering
When users register, they must provide a name, valid email address, and two matching passwords.
To validate the email address, we used a library.
There must not already be an account made with that email address.
Sucessfully registering will prompt a confirmation email sent to the user.
The user will now be stored in the users table of the carbon database.
After registering, the user will be redirected to the login page.

Logging In
To log in, users must provide an email address and password. The website will remember which user has logged in.
The user will be redirected to the Welcome Page.

The Database
There are two tables in carbon.db. One stores the name, email, and hashed password of each user.
Each user has a unique user id.
The data table stores everything inputted through the Log page. Each row has a unique
id of the log, the user id corresponding with the user who logged it, and the relevant information
about the carbon emissions and the user's activities. Only the Log page will store data in the table.
The Calculate page will calculate how much carbon actions would emit, but does NOT store
anything. This makes it ideal for non-users as well as users who want to make informed decisions
about their carbon-emitting activities.

Log
If the user reaches the route via POST, the Log function collects input from an html form,
calculates the carbon it would emit, and stores the data in the data table of carbon.db.
It then takes the user to a Logged page which tells the user how much carbon their actions emitted.
If the user reaches the route via GET, the form is displayed.
If the user does not type in anything into the input box then it will alert that the input is invalid.

History
The History function accesses the current user's data from the SQL
database and uses a jinja for loop to display the information in a table.
If user has not yet logged any data, nohistory.html is displayed.
Additionally, a graph displaying the user's carbon output against time is displayed. The graph uses
matplotlib. Each graph is stored in the static folder under the name "plot" + the user's id. This
ensures that multiple users on the site simultaneously will not cause graphs to be overwritten.
The graph displays total carbon as well as carbon from food.

