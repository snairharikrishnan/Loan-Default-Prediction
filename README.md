# Loan-Default-Prediction
## Business Problem
A Bank accepts deposits from customers and from the corpus thus available, it lends to borrowers who want to carry out certain business activities for growth and profit. 
It is often seen that due to some reasons like failure of business, huge financial losses or the company becoming delinquent/bankrupt, the loans are not Paid in Full. 
The bank then has to either Charge-Off/Write Off the loan or have to seek other measures to retrieve their due payment. Increased Non-Performing Assets(NPAs) for the bank
severely affects the health of the bank, even threatening the national economy. The bank is thus faced with the problem of identifying those borrowers who can pay up their 
due amount, and not lending to borrowers who are likely to default.

## Overview
A classification model is bulit which classifies the customers to two categories(will default/will not default). It is then deployed using Flask and Heroku. The employees of the bank has to enter certain details related to the new loan applicant in the html form. On submission the alogorithm predicts whether the applicant would be a potential defaulter or not and then the prediction would be displayed. If the chances are high for the applicant to default on the loan, then the bank could reject the loan application citing various reasons. Hence the financial health of the bank can be improved. 

## Demo
Link: [https://loan-default-pred-api.herokuapp.com](https://loan-default-pred-api.herokuapp.com/)

![](/static/form_image.jpg)

## Project Architecture
![](/static/architecture.JPG)
### Problem Definition : 
To predict whether the loan applicant would default on the loan or not
### Data Gathering : 
Data provided by the training team
### Data Clensing : 
Numerized the amount feature which had $ symbols, removed duplicates, imputed missing values
### EDA : 
Defined the dependent variable, found various relations between different features
### Feature Engineering : 
Converted few variables to a different form to suite the prediction
### Model Building : 
Built different models on the data, and evaluated the accuracies
### Model Selection : 
Selected the XGB model which gave the highest accuracy
### Deployment : 
Made the application file using Flask framework and deployed using Heroku  

## Technologies Used
<img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png" width=280> <img target="_blank" src="https://flask.palletsprojects.com/en/1.1.x/_images/flask-logo.png" width=180> <img target="_blank" src="https://number1.co.za/wp-content/uploads/2017/10/gunicorn_logo-300x85.png" width=280>  
