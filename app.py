from flask import Flask,request,render_template 
import os
import pandas as pd
import numpy as np
import pickle

app=Flask(__name__)

os.getcwd()
#os.chdir('C:\\Users\\snair\\Documents\\Data Science Assignment\\Project\\Deployment')
model=pickle.load(open('model.pkl','rb'))
sc=pickle.load(open('sc.pkl','rb'))

prob= [0.36843241, 0.36666022, 0.34706022, 0.33791431, 0.32278584,
       0.31489362, 0.29731993, 0.29448663, 0.28612997, 0.28314311,
       0.2816092 , 0.27611444, 0.27437223, 0.26975566, 0.26765799,
       0.25641026, 0.25422521, 0.25266642, 0.25051419, 0.25038052,
       0.24454148, 0.242497  , 0.24070848, 0.23775727, 0.23741935,
       0.23363095, 0.23332144, 0.23002646, 0.22674419, 0.22384971,
       0.21773612, 0.21682243, 0.21378899, 0.20707071, 0.20456467,
       0.20225564, 0.19552239, 0.19487179, 0.19324456, 0.18851757,
       0.18421053, 0.18238342, 0.17855968, 0.17059891, 0.15519663,
       0.14317181, 0.14186851, 0.12367491, 0.12205567, 0.12084592,
       0.11460957]


state=['FL', 'MI', 'GA', 'NV', 'IL', 'AK', 'AL', 'AZ', 'SC', 'NJ', 'CA',
       'TN', 'IN', 'NY', 'CO', 'DC', 'TX', 'NC', 'VA', 'KS', 'DE', 'AR',
       'WA', 'OK', 'OR', 'KY', 'MD', 'OH', 'MS', 'PA', 'MO', 'LA', 'MA',
       'RI', 'CT', 'ID', 'NM', 'HI', 'UT', 'IA', 'WV', 'NH', 'WI', 'NE',
       'MN', 'ND', 'ME', 'WY', 'MT', 'SD', 'VT']


state_value=pd.DataFrame(columns=["State","Value"])
state_value["State"]=state
state_value["Value"]=prob

response=['CA','1997','80','4','2','0','0','0','55000','55000','50000','0','0','1','2000']


@app.route('/predict',methods=['POST'])
def predict():
    response=[x for x in request.form.values()]
    a=float(state_value.loc[state_value.State==response[0],'Value'])
    response[0]=a

    response=np.array(response).reshape(1,-1)
    response=sc.transform(response)
    pred=model.predict(response)
    
    if pred==1:
        return render_template("index.html",predicted="The person defaults")
    return render_template("index.html",predicted="The person doesn't default")

@app.route('/')
def home():
    return render_template("index.html")


if __name__=="__main__":
    app.run(debug=True)
    