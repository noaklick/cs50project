# cs50project
Carbon Footprint Calculator. Designed a website for users to track their daily carbon-emitting actions and track how their carbon footprint changes over time. Built with Flask, HTML, Python, SQL, Jinja, and Matplotlib. Final Project for CS 50.

Carbon Footprint: A CS50 Final Project by Noa Kligfeld and Ben Fisher

Welcome to Carbon Footprint! Our website is designed to help users minimize their carbon footprints. One of our primary goals was to increase awareness of daily actions which emit carbon. The questions we ask are users about their daily actions are the same questions we hope they begin to ask themselves. Rather than merely a tool for logging data, our site aims to train users to think daily about their carbon usage.

Video link: https://youtu.be/dTKtkIwddJ4

To use our website, please set the email account information for carbonfootprintcs50@gmail.com as environment variables. This feature will allow the website to send confirmation emails to user when they register. As the email account will only be used for the purposes of this assignment, we are comfortable including the account information in this document.

Before opening the website, please type the following into the terminal: $ export MAIL_DEFAULT_SENDER=carbonfootprintcs50@gmail.com $ export MAIL_PASSWORD=noaandben

To run the website, cd into project/carbon and type $ flask run into the terminal. Click the link that appears.

The website will take you to the Welcome page, where users can learn about carbon. This page gives information about carbon and also incentivizes users to stay on our website and explore its features.

From the Welcome page, users can:

Calculate the carbon emissions from a set of actions
This is intended to allow users to test our features before making the decision to register
Log in
Create an account
Creating an account will prompt a confirmation email to be sent to the user's email address
If users create an account, they will be able to Log, Calculate or view History.

The Log page will allow users to log their daily activities. It will take users to a page to see how much carbon their actions emitted
The History page will allow users to see their history of logged activities and carbon output. It is intended to prompt reflection about their progress
Users can also see a graph of their carbon output measured against time.
The amount of carbon from food is also graphed. This is to emphasize just how much carbon is emitted from food.
The Calculate page, which looks similar to the Log page, will allow users to calculate the carbon emitted from a set of actions WITHOUT logging it.
For example, they can check to see how much carbon a set of actions would theoretically emit as part of the decision-making process
if users do not input anything into any of the input boxes in either the log or calculate page and click log, it will prompt the user to put in an input.
This is because the input boxes are required and using javascript it will alert the user if nothing is inputted. We hope you enjoy our website!
