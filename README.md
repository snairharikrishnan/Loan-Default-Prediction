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
