import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

bank=pd.read_csv("C:/Users/snair/Documents/Data Science Assignment/Project/bank.csv")

bank_stats=bank.describe()
bank.columns

bank.isna().sum()
bank[bank.duplicated()] #15 duplicates
bank.drop_duplicates(inplace=True) #Duplicate records removed
bank=bank.reset_index(drop=True)

#Removing $ symbol
def numerize(x):
    return float(x.replace("$","").replace(",",""))

bank["DisbursementGross"]=bank["DisbursementGross"].map(lambda x: numerize(x))
bank["BalanceGross"]=bank["BalanceGross"].map(lambda x: numerize(x))
bank["ChgOffPrinGr"]=bank["ChgOffPrinGr"].map(lambda x: numerize(x))
bank["GrAppv"]=bank["GrAppv"].map(lambda x: numerize(x))
bank["SBA_Appv"]=bank["SBA_Appv"].map(lambda x: numerize(x))


#OUTPUT VARIABLE ---> MIS_STATUS

sns.countplot(x='MIS_Status',data=bank)
bank['MIS_Status'].value_counts()

len(bank.loc[(bank.ChgOffPrinGr>0) & (bank.MIS_Status=='P I F')]) #1319
len(bank.loc[(bank.ChgOffPrinGr==0) & (bank.MIS_Status=='CHGOFF')]) #164

x=[] # store the row id of records having MIS_Status as NA
for i in range(len(bank)):
    if bank['MIS_Status'][i] not in ['CHGOFF','P I F']:
        x.append(i)
                
a=bank.iloc[x,[18,22,23]]#analysing the related variables
#IF ChgOffPrinGr > 0 then it would be a defaulter

#Replacing the NA values of MIS_Status by comparing with values in ChgOffPrinGr
for i in range(len(bank)):
    if bank['MIS_Status'][i] not in ['CHGOFF','P I F']:
        if bank['ChgOffPrinGr'][i]>0:
            bank['MIS_Status'][i]='CHGOFF'
        else:
            bank['MIS_Status'][i]='P I F'

#Null values imputed

#creating output variable
bank['default']=bank['MIS_Status'].map({'P I F':0,'CHGOFF':1})


plt.rcParams.update({'figure.figsize':(12,8)})

sns.countplot(x='default',data=bank)
bank['default'].value_counts()       # approx 40000 defaulters and 110000 non defaulters


len(bank['Name'].unique())
len(bank['City'].unique())
len(bank['State'].unique())
len(bank['Zip'].unique())
len(bank['Bank'].unique())
len(bank['BankState'].unique())
len(bank['CCSC'].unique())
len(bank['ApprovalDate'].unique())
len(bank['ApprovalFY'].unique())
len(bank['Term'].unique())
len(bank['NoEmp'].unique())
len(bank['NewExist'].unique()) #3 categories
len(bank['CreateJob'].unique())
len(bank['RetainedJob'].unique())
len(bank['FranchiseCode'].unique())
len(bank['UrbanRural'].unique())#0-unidentified
len(bank['RevLineCr'].unique()) #wrong entries present
len(bank['LowDoc'].unique()) #wrong entries present
len(bank['ChgOffDate'].unique())
len(bank['DisbursementDate'].unique())
len(bank['DisbursementGross'].unique())
len(bank['BalanceGross'].unique()) #only 3 unique values
len(bank['MIS_Status'].unique()) 
len(bank['ChgOffPrinGr'].unique()) 
len(bank['GrAppv'].unique())
len(bank['SBA_Appv'].unique())



####  NewExist  ####
sns.countplot(x='NewExist',data=bank)   
bank['NewExist'].value_counts() #0-->128 wrong entries
sns.countplot(x='default',hue='NewExist',data=bank)#Existing business more than new business in dataset
bank[['NewExist','default']].groupby(['NewExist']).mean().sort_values(by='default',ascending=False)
#existing business has a little more chance to default than new business
#Imputing with mode
bank.loc[(bank.NewExist !=1) & (bank.NewExist !=2),'NewExist']=1



####  FranchiseCode  ####
len(bank.loc[bank['FranchiseCode']>1])#5260 businesses have franchises
bank['Franchise']=0
bank.loc[bank.FranchiseCode>1,'Franchise']=1
bank['Franchise'].unique()

sns.countplot(x='default',hue='Franchise',data=bank)# only few have franchises
bank[['default','Franchise']].groupby(['Franchise']).mean().sort_values(by='Franchise',ascending=True)
#defaulting chances are less for businesses with franchises



####  UrbanRural  ####
sns.countplot(x='UrbanRural',data=bank)
bank['UrbanRural'].value_counts()
sns.countplot(x='default',hue='UrbanRural',data=bank)#more cases of urban; majority of unidentified is in non-default 
bank[['UrbanRural','default']].groupby(['UrbanRural']).mean().sort_values(by='default',ascending=False)
#urban business more likely to default



####  RevLineCr  ####
sns.countplot(x='RevLineCr',data=bank)
bank['RevLineCr'].value_counts() #0-23659 , T-4819 , (`)-2 , (,)-1
sns.countplot(x='default',hue='RevLineCr',data=bank)#RevLine of credit not availbale for majority of the businesses
bank[['RevLineCr','default']].groupby(['RevLineCr']).mean().sort_values(by='default',ascending=False)
#Y and N almost equally likely to default
#Imputing the wrong entries to 0
bank.loc[(bank.RevLineCr!='Y')&(bank.RevLineCr!='N')&(bank.RevLineCr!='0'),'RevLineCr']='0'
#creating dummy variable
bank['RevLineCr_yes']=bank['RevLineCr'].map({'N':0,'Y':1,'0':2})



####  LowDoc  ####
sns.countplot(x='LowDoc',data=bank)
bank['LowDoc'].value_counts() #C-83 , 1-1
sns.countplot(x='default',hue='LowDoc',data=bank)#majority businesses are not under LowDoc
bank[['LowDoc','default']].groupby(['LowDoc']).mean().sort_values(by='default',ascending=False)
# if covered under LowDoc, very unlikely to default
#Imputing with mode
bank.loc[(bank.LowDoc !='Y') & (bank.LowDoc !='N'),'LowDoc']='N'   
#creating dummy variable
bank['LowDoc_yes']=bank['LowDoc'].map({'N':0,'Y':1})


####  ChgOffDate  ####
def chgoff(x):
    try:
        if len(x):
            return 1
    except:
        return 0

bank['ChgOffDate_Yes']=bank['ChgOffDate'].map(lambda x: chgoff(x))  
pd.crosstab(bank.default,bank.ChgOffDate_Yes)            
#ChgOffDate present implies it is a defaulter,and if absent, non defaulter with very few exceptions



####  BalanceGross ####
sns.countplot(x='BalanceGross',data=bank)
bank['BalanceGross'].value_counts() #only 2 values, rest are 0
bank.loc[bank.BalanceGross != 0,'default']#both non-default
#Hence irrelevant for prediction
#bank.drop(['BalanceGross'],axis=1,inplace=True)



####  ChgOffPrinGr  ####
sns.countplot(x=bank['default'],hue=bank['ChgOffPrinGr']==0)
#ChgOffPrinGr=0 implies non defaulter and ChgOffPrinGr>0 implies defaulter 

len(bank.loc[(bank.ChgOffPrinGr>0) & (bank.MIS_Status=='P I F')]) #1319
len(bank.loc[(bank.ChgOffPrinGr==0) & (bank.MIS_Status=='CHGOFF')]) #164           

pd.crosstab(bank.default,bank.ChgOffPrinGr==0)
# if not defaulter then very less chance to have chargeoff amount
# if a defaulter then there are very few cases where the amount is not chargedoff



####  State  ####
sns.countplot(x='State',data=bank)
bank['State'].value_counts()
bank[['State','default']].groupby(['State']).mean().sort_values(by='default',ascending=False)
#FL state has highest probabilty to default and VT least
#Imputing the 2 NA values
a=bank.loc[bank.State.isna()]
bank.loc[bank.State.isna(),'City']
bank.loc[bank.State.isna(),'BankState']#JOHNSTOWN-->NY
bank.loc[bank.Zip==8070,'State']
bank.loc[bank.Name=='SO. JERSEY DANCE/MERRYLEES','State']
#PENNSVILLE-->NJ

bank.loc[bank.City=='PENNSVILLE','State']='NJ'
bank.loc[bank.City=='JOHNSTOWN       NY','State']='NY'

#Replacing the States with their probability values(Mean Encoding)
x=bank[['State','default']].groupby(['State']).mean().sort_values(by='default',ascending=False)
x['State']=x.index
x=x.set_index(np.arange(0,51,1))
for i in range(len(x)):
    bank=bank.replace(to_replace =x.State[i], value =x.default[i]) 
    print(i)

#saving the encoded values to system
import pickle
x.rename(columns={"default":"Value"},inplace=True)
os.chdir("C:/Users/snair/Documents/Data Science Assignment/Project")
pickle.dump(x,open('state.pkl','wb'))



####  City  ####
bank['City'].value_counts()
bank[['City','default']].groupby(['City']).mean().sort_values(by='default',ascending=False)



####  Bank  ####
bank['Bank'].value_counts()
bank[['Bank','default']].groupby(['Bank']).mean().sort_values(by='default',ascending=False)



####  BankState  ####
sns.countplot(x='BankState',data=bank)
bank['BankState'].value_counts() #Most banks in NC least in PR
bank[['BankState','default']].groupby(['BankState']).mean().sort_values(by='default',ascending=False)# VA highest, MA least
#Bank in VA state has highest probabilty to default and MA least



####  ApprovalFY  ####
sns.countplot(x='ApprovalFY',data=bank)# more approvals in 1997-1998 and 2004-2007
bank['ApprovalFY'].value_counts() #highest no of approvals in 2006 least in 1962,65,66 
sns.countplot(x='default',hue='ApprovalFY',data=bank)
bank[['ApprovalFY','default']].groupby(['ApprovalFY']).mean().sort_values(by='ApprovalFY',ascending=True)
# if loan is approved before 1982, high probability to default; 1997-2003 very less chance to default 

len(bank.loc[(bank['ApprovalFY']<=1980)])# only 305 approvals before 1980
len(bank.loc[(bank['ApprovalFY']>1980) & (bank['ApprovalFY']<1990)])
len(bank.loc[(bank['ApprovalFY']>1990) & (bank['ApprovalFY']<2003)])
len(bank.loc[(bank['ApprovalFY']>2003)])

bank['ApprovalFY_bin']=pd.cut(bank['ApprovalFY'],bins=[1960,1980,1990,2003,2010],labels=[1,2,3,4])
sns.countplot(x='default',hue='ApprovalFY_bin',data=bank)
bank[['default','ApprovalFY_bin']].groupby(['ApprovalFY_bin']).mean().sort_values(by='ApprovalFY_bin',ascending=True)



####  ApprovalDate  ####
bank['ApprovalMonth']=''  #date mapped to month and day
bank['ApprovalDay']=''
for i in range(len(bank)):
    bank['ApprovalMonth'][i]=bank['ApprovalDate'][i][3:6]    
    bank['ApprovalDay'][i]=int(bank['ApprovalDate'][i][:2])
    if i%5000==0:
        print(i)

sns.countplot(x='default',hue='ApprovalMonth',data=bank)
bank[['default','ApprovalMonth']].groupby(['ApprovalMonth']).mean().sort_values(by='default',ascending=False)
#equally likely

sns.countplot(x='ApprovalDay',data=bank)
bank[['default','ApprovalDay']].groupby(['ApprovalDay']).mean().sort_values(by='ApprovalDay',ascending=True)
#no pattern, equally likely
#Hence ApprovalDate is irrelavant



####  Term  ####
sorted(bank['Term'].unique()) # min=0 , max=480
sns.distplot(bank['Term'])
sns.boxplot(x='default',y='Term',data=bank)

len(bank.loc[(bank['Term']==0)])
len(bank.loc[(bank['Term']==0) & (bank['default']==1)]) #189/202 = 0.935
#If term = 0, almost surely defaults
len(bank.loc[(bank['Term']<=60)])
len(bank.loc[(bank['Term']<=60) & (bank['default']==1)])
len(bank.loc[(bank['Term']>120) & (bank['Term']<=180)])
len(bank.loc[(bank['Term']>120) & (bank['Term']<=180)& (bank['default']==1)])
len(bank.loc[(bank['Term']>300) & (bank['Term']<=360)])
len(bank.loc[(bank['Term']>300) & (bank['Term']<=360) & (bank['default']==1)])
len(bank.loc[(bank['Term']>360)])
len(bank.loc[(bank['Term']>360) & (bank['default']==1)])

bank['Term_bin']=0
bank['Term_bin']=pd.cut(bank['Term'],bins=[-1,60,120,180,240,300,360,480],labels=[1,2,3,4,5,6,7])
#cutting the dataframe to 5 year terms ie 60 months each;last bin 10 years

sns.countplot(x='default',hue='Term_bin',data=bank)#more defaulters for 0-5 year term; more non defaulters for 5-40 year term
bank[['default','Term_bin']].groupby(['Term_bin']).mean().sort_values(by='Term_bin',ascending=True)
#for 0-5 and 30-40 more chance of defaulting; for 5-30 less chance of defaulting
p=pd.DataFrame(bank[['default','Term_bin']].groupby(['Term_bin']).mean())
plt.title("Term VS probability to default")
plt.xlabel("Five year Terms")
plt.ylabel("Probability to default")
plt.bar(p.index,p.default,color='crimson')


####  NoEmp  ####
sorted(bank['NoEmp'].unique())# min=0 ; max=9999
sns.distplot(bank['NoEmp'])
sns.boxplot(x='default',y='NoEmp',data=bank)

len(bank.loc[bank['NoEmp']>100]) # only 829 businesses have more than 100 employees
len(bank.loc[bank['NoEmp']<=5]) # 98194 have 5 or less employees
len(bank.loc[bank['NoEmp']<=10]) #122309
len(bank.loc[(bank['NoEmp']>30) & (bank['NoEmp']<=100)])
len(bank.loc[(bank['NoEmp']>100) & (bank['NoEmp']<=10000)])

bank['Emp_bin']=0 # Slicing number of employees into groups
emp_bin=[-1,5,10,15,20,30,100,1000,10000]
emp_lab=list(range(1,9))
bank['Emp_bin']=pd.cut(bank['NoEmp'],bins=emp_bin,labels=emp_lab)

sns.countplot(x='default',hue='Emp_bin',data=bank)#both follow same pattern 
bank[['default','Emp_bin']].groupby(['Emp_bin']).mean().sort_values(by='default',ascending=False)
# as the number of employees increase chances of default decrease
p=pd.DataFrame(bank[['default','Emp_bin']].groupby(['Emp_bin']).mean())
plt.title("Number of Employees VS probability to default")
plt.xlabel("Number of Employees in bins")
plt.ylabel("Probability to default")
plt.bar(p.index,p.default,color='crimson')



####  CreateJob ####
sorted(bank['CreateJob'].unique()) #min=0 ; max=3000
sns.boxplot(x='default',y='CreateJob',data=bank)

len(bank.loc[bank['CreateJob']>100])# only 44 businesses create more than 100 jobs
len(bank.loc[(bank['CreateJob']>10) & (bank['CreateJob']<=100)])# only 3541 business creates jobs between 10 and 100
len(bank.loc[(bank['CreateJob']>5) & (bank['CreateJob']<=10)])# 4130
len(bank.loc[bank['CreateJob']==0]) # no jobs created for 113064 businesses

bank['CreateJob_bin']=0
bank['CreateJob_bin']=pd.cut(bank['CreateJob'],bins=[-1,0,5,10,100,400,3000],labels=[0,1,2,3,4,5])
sns.countplot(x='default',hue='CreateJob_bin',data=bank)#same pattern
bank[['default','CreateJob_bin']].groupby(['CreateJob_bin']).mean().sort_values(by='CreateJob_bin',ascending=True)
#chances of default is least when jobs created is between 10 and 400; highest when >400



####  RetainedJob  ####
sorted(bank['RetainedJob'].unique()) # min=0 ; max=9500
sns.boxplot(x='default',y='CreateJob',data=bank)

len(bank.loc[bank['RetainedJob']>100])# only 194 businesses have retained more than 100 jobs
len(bank.loc[bank['RetainedJob']<10])#135938
len(bank.loc[bank['RetainedJob']==0])#65810
len(bank.loc[(bank['RetainedJob']>100) & (bank['RetainedJob']<=400)])
len(bank.loc[bank['RetainedJob']>400])
len(bank.loc[(bank['RetainedJob']>400) & (bank['default']==1)])#no defaulters when Retainedjobs>400

bank['RetainedJob_bin']=0
bank['RetainedJob_bin']=pd.cut(bank['RetainedJob'],bins=[-1,0,5,10,100,400,9500],labels=[0,1,2,3,4,5])
sns.countplot(x='default',hue='RetainedJob_bin',data=bank)#if no jobs retained then they generally are biased to be non defaulters
bank[['default','RetainedJob_bin']].groupby(['RetainedJob_bin']).mean().sort_values(by='RetainedJob_bin',ascending=True)
#if retained jobs=0 defaulting very less;then as the jobs increases, the chances of defaulting comes down;defaulters high for 1-10 range

#Merging the two jobs
bank["TotalJobs"]=bank["CreateJob"]+bank["RetainedJob"]

bank['TotalJobs_bin']=pd.cut(bank['TotalJobs'],bins=[-1,0,5,10,100,400,9500],labels=[0,1,2,3,4,5])
sns.countplot(x='default',hue='TotalJobs_bin',data=bank)
bank[['default','TotalJobs_bin']].groupby(['TotalJobs_bin']).mean().sort_values(by='TotalJobs_bin',ascending=True)


####  DisbursementDate  ####

def extract_year(x):  #extracting the year alone from date
    try:
        return datetime.strptime(x,"%d-%b-%y").year
    except:
        return 0

bank['DisbursementYear']=bank["DisbursementDate"].map(lambda x: extract_year(x))

sns.countplot(x='DisbursementYear',data=bank)
bank['DisbursementYear'].value_counts() # highest in 2006
bank.loc[bank.DisbursementYear<2000]
bank.loc[bank.DisbursementYear>2010,'default'] # if disbursed after 2010,mostly wont default
bank[['default','DisbursementYear']].groupby(['DisbursementYear']).mean().sort_values(by='DisbursementYear',ascending=True)

#Imputation
bank['DisbursementYear'].value_counts()#2 wrong years(2048 & 2066)
a=bank.loc[bank.DisbursementYear==0]
bank.loc[bank.DisbursementYear==0,'default'].value_counts()# mostly defaulters
bank[['default','DisbursementYear']].groupby(['DisbursementYear']).mean().sort_values(by='DisbursementYear',ascending=True)

bank.loc[bank.ApprovalFY==bank.DisbursementYear,['ApprovalFY','DisbursementYear']]
bank.loc[bank.ApprovalFY<bank.DisbursementYear]
x=bank.loc[bank.ApprovalFY>bank.DisbursementYear,['ApprovalFY','DisbursementYear']]
#for about 77% records,DisbursementYear = ApprovalFY
#Hence imputing the NA values and the 2 wrong values with the approval year
   
for i in range(len(bank)):
    if (bank.DisbursementYear[i]==0) or (bank.DisbursementYear[i]>2013): 
        bank.DisbursementYear[i]=bank.ApprovalFY[i]

bank['DisbursementYear_bin']=0
bank['DisbursementYear_bin']=pd.cut(bank['DisbursementYear'],bins=[1960,1984,1998,2003,2008,2013],labels=[1,2,3,4,5])

sns.countplot(x='default',hue='DisbursementYear_bin',data=bank)#most dates are between 1984-1998 and 2003-2008
bank[['default','DisbursementYear_bin']].groupby(['DisbursementYear_bin']).mean().sort_values(by='DisbursementYear_bin',ascending=True)
#1970-1984 and 2003-2008 high chances of default; for rest, chances of default reduces by the years
 


####  DisbursementGross  ####
sns.distplot(bank['DisbursementGross'])#right skewed ie more datapoints to the lower side
sns.boxplot(x='default',y='DisbursementGross',data=bank)

bank.loc[bank['DisbursementGross']<10000]#4556
bank.loc[(bank['DisbursementGross']>10000) & (bank['DisbursementGross']<50000)]#45252
bank.loc[(bank['DisbursementGross']>50000) & (bank['DisbursementGross']<100000)]#26979
bank.loc[(bank['DisbursementGross']>100000) & (bank['DisbursementGross']<1000000)]#48080
bank.loc[(bank['DisbursementGross']>1000000) & (bank['DisbursementGross']<4100000)]#1751

sns.catplot(x='default',y='DisbursementGross',hue='MIS_Status',kind='bar',data=bank)
sns.countplot(bank.DisbursementGross>500000,hue=(bank.default==1))

bank.loc[bank.DisbursementGross<100000]
bank.loc[(bank.DisbursementGross<100000) & (bank.default==1)]#27192/92610=0.293
bank.loc[(bank.DisbursementGross>=100000) & (bank.DisbursementGross<1000000)]
bank.loc[(bank.DisbursementGross>=100000) & (bank.DisbursementGross<1000000)&(bank.default==1)]#11698/55057=0.212
bank.loc[(bank.DisbursementGross>=1000000)]
bank.loc[(bank.DisbursementGross>=1000000) & (bank.default==1)]#252/2317=0.108
#As DisbursementGross increases, chances of default decreases

bank['LargeAmount']=0
for i in range(len(bank)):
    if (bank.DisbursementGross[i]>=100000) & (bank.DisbursementGross[i]<1000000):
        bank.LargeAmount[i]=1
    elif (bank.DisbursementGross[i]>=1000000):
        bank.LargeAmount[i]=2



####  GrAppv  ####
sns.distplot(bank['GrAppv'])#right skewed        
               
len(bank.loc[bank.DisbursementGross>bank.GrAppv])#comparing with DisbursementGross     
len(bank.loc[bank.DisbursementGross<bank.GrAppv])    
len(bank.loc[bank.DisbursementGross==bank.GrAppv])    

len(bank.loc[(bank.DisbursementGross>bank.GrAppv) & (bank.default==1)]) #15820/42218 = 0.374   
len(bank.loc[(bank.DisbursementGross<bank.GrAppv) & (bank.default==1)]) #2223/8287   = 0.268   
len(bank.loc[(bank.DisbursementGross==bank.GrAppv)& (bank.default==1)]) #21099/99479 = 0.212
# when DisbursementGross > gross approved then high chances to default; least chance when DisbursementGross = approved gross   

bank['GrAppv_Disbursement']=0   # 1 when GrAppv is less, 2 when GrAppv is more, 0 when equal
for i in range(len(bank)):
    if bank.GrAppv[i] < bank.DisbursementGross[i]:
        bank.GrAppv_Disbursement[i]=1
    elif bank.GrAppv[i] > bank.DisbursementGross[i]:
        bank.GrAppv_Disbursement[i]=2

sns.countplot(x='default',hue='GrAppv_Disbursement',data=bank)
bank[['default','GrAppv_Disbursement']].groupby(['GrAppv_Disbursement']).mean().sort_values(by='default',ascending=False)
#when GrAppv < DisbursementGross highest probabilty to default


  
####  SBA_Appv  ####
sns.distplot(bank['SBA_Appv'])#right skewed
     
len(bank.loc[bank.DisbursementGross>bank.SBA_Appv]) #comparing with DisbursementGross  
len(bank.loc[bank.DisbursementGross<bank.SBA_Appv])    
len(bank.loc[bank.DisbursementGross==bank.SBA_Appv])    
        
len(bank.loc[(bank.DisbursementGross>bank.SBA_Appv) & (bank.default==1)])  #38875/140123 = 0.277    
len(bank.loc[(bank.DisbursementGross<bank.SBA_Appv) & (bank.default==1)])  #253/2519     = 0.100    
len(bank.loc[(bank.DisbursementGross==bank.SBA_Appv) & (bank.default==1)]) #14/7342      = 0.001 
#highest probability to default when SBA_Appv is less than DisbursementGross; least when both are equal
  
bank['SBA_Appv_Disbursement']=0   # 1 when SBA_Appv is less, 2 when SBA_Appv is more, 0 when equal
for i in range(len(bank)):
    if bank.SBA_Appv[i] < bank.DisbursementGross[i]:
        bank.SBA_Appv_Disbursement[i]=1
    elif bank.SBA_Appv[i] > bank.DisbursementGross[i]:
        bank.SBA_Appv_Disbursement[i]=2

sns.countplot(x='default',hue='SBA_Appv_Disbursement',data=bank)
bank[['default','SBA_Appv_Disbursement']].groupby(['SBA_Appv_Disbursement']).mean().sort_values(by='default',ascending=False)
#chances of default negligible when SBA_Appv = DisbursementGross; highest when SBA_Appv < DisbursementGross

len(bank.loc[bank.SBA_Appv>bank.GrAppv])#Gross approved amount never less than SBA approved    
len(bank.loc[bank.SBA_Appv<bank.GrAppv])    
len(bank.loc[bank.SBA_Appv==bank.GrAppv])#8094    

#####################################################################

bank['NewExist'].value_counts()
a=bank.loc[(bank.NewExist !=1) & (bank.NewExist !=2)]
x=bank.loc[(bank.NewExist ==1),['NoEmp', 'NewExist', 'CreateJob','RetainedJob']]

bank.loc[(bank.ApprovalFY ==2006),'NewExist'].value_counts()
sns.countplot(bank.CreateJob_bin,hue=bank.NewExist)
bank.loc[(bank.CreateJob_bin ==0),'NewExist'].value_counts()

sns.countplot(bank.NewExist,hue=bank.NoEmp>100)
sns.countplot(bank.NewExist,hue=bank.CreateJob>100)
#no relation found
#Hence imputing with mode



bank['LowDoc'].value_counts()
a=bank.loc[(bank.LowDoc !='Y') & (bank.LowDoc !='N')]
bank.loc[(bank.LowDoc !='Y') & (bank.LowDoc !='N'),'State'].value_counts()
bank.loc[(bank.LowDoc !='Y') & (bank.LowDoc !='N'),'BankState'].value_counts()
bank.loc[(bank.LowDoc !='Y') & (bank.LowDoc !='N'),'ApprovalFY'].value_counts()
bank.loc[(bank.LowDoc !='Y') & (bank.LowDoc !='N'),'DisbursementYear'].value_counts()

bank.loc[(bank.ApprovalFY==1998),'default'].value_counts()
bank.loc[(bank.State=='TX'),'default'].value_counts()
bank.loc[(bank.ApprovalFY==2006),'LowDoc'].value_counts()#when ApprovalFY=2006 ,LowDoc never Y 
bank.loc[(bank.DisbursementYear==2006),'LowDoc'].value_counts()

a=bank.loc[(bank.LowDoc !='Y') & (bank.LowDoc !='N') & (bank.ApprovalFY!=2006)]
a.State.value_counts()
a.BankState.value_counts()
a.ApprovalFY.value_counts()
a.DisbursementYear.value_counts()
a.RevLineCr.value_counts()
#No clear relation for LowDoc with any other feature
#Hence imputation done with mode



bank['RevLineCr'].value_counts()
a=bank.loc[(bank.RevLineCr!='Y')&(bank.RevLineCr!='N')&(bank.RevLineCr!='0')]
bank.loc[(bank.ApprovalFY ==1998),'RevLineCr'].value_counts()
sns.countplot(bank.UrbanRural,hue=bank.RevLineCr)
sns.countplot(bank.Term_bin,hue=bank.RevLineCr)#if urban,more having revline credit;if rural more not having
sns.countplot(bank.LowDoc,hue=bank.RevLineCr)#if under LowDoc, then no revline credit
a[a.LowDoc=='Y']
a=bank.loc[(bank.RevLineCr!='Y')&(bank.RevLineCr!='N')&(bank.RevLineCr!='0')&(bank.RevLineCr!='T')]
sns.countplot(bank.RevLineCr,hue=bank.LargeAmount)
pd.crosstab(bank.RevLineCr,bank.LargeAmount)




max(bank.DisbursementGross)
bank[['Term_bin','SBA_Appv']].groupby(['Term_bin']).mean().sort_values(by='Term_bin',ascending=False)
bank[['Term_bin','GrAppv']].groupby(['Term_bin']).mean().sort_values(by='Term_bin',ascending=False)
bank[['Emp_bin','SBA_Appv']].groupby(['Emp_bin']).mean().sort_values(by='Emp_bin',ascending=False)
bank[['CreateJob_bin','SBA_Appv']].groupby(['CreateJob_bin']).mean().sort_values(by='CreateJob_bin',ascending=False)
bank[['RetainedJob_bin','SBA_Appv']].groupby(['RetainedJob_bin']).mean().sort_values(by='RetainedJob_bin',ascending=False)

bank.loc[bank.SBA_Appv<50000]
bank.loc[(bank.SBA_Appv<50000) & (bank.default==1)]#30041/92203=0.325

bank.loc[(bank.SBA_Appv>=50000) & (bank.SBA_Appv<100000)]
bank.loc[(bank.SBA_Appv>=50000) & (bank.SBA_Appv<100000)&(bank.default==1)]#5457/23740=0.229

bank.loc[(bank.SBA_Appv>=100000) & (bank.SBA_Appv<500000)]
bank.loc[(bank.SBA_Appv>=100000) & (bank.SBA_Appv<500000)&(bank.default==1)]#4458/28214=0.158

bank.loc[(bank.SBA_Appv>=500000)]
bank.loc[(bank.SBA_Appv>=500000) & (bank.default==1)]#510/5827=0.087


#UrbanRural-wrong values 
#RevLineCr-wrong values 
##############################################################################
####  Feature Selection  ####
bank.columns

features=['default','State','Term','NoEmp','NewExist',
          'TotalJobs','UrbanRural','DisbursementGross',
          'GrAppv','SBA_Appv','Franchise','RevLineCr_yes','LowDoc_yes']
          


bank_clensed=bank[features]

os.getcwd()
os.chdir("C:/Users/snair/Documents/Data Science Assignment/Project")
bank_clensed.to_csv("bank_clean",encoding='utf-8')

bank_clensed=pd.read_csv("C:\\Users\\snair\\Documents\\Data Science Assignment\\Project\\bank_clean.csv")
#bank_clensed.drop(['UrbanRural'],axis=1,inplace=True)
###############################################################################
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.model_selection import train_test_split 
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import RandomizedSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from xgboost import XGBClassifier
from sklearn.svm import SVC
from sklearn.preprocessing import StandardScaler

X=bank_clensed.iloc[:,1:]
Y=bank_clensed.iloc[:,0]

corr_mat=bank_clensed.corr()
top_features=corr_mat.index
sns.heatmap(bank_clensed[top_features].corr(),annot=True,cmap='RdYlGn')

#sc=StandardScaler()
#std_data=sc.fit_transform(bank.drop('default',axis=1))
#df=pd.DataFrame(std_data)
#df['out']=bank['default']
#sns.pairplot(df,hue='out')

feature_sel=ExtraTreesClassifier(n_jobs=-1)
feature_sel.fit(X,Y)
score=list(feature_sel.feature_importances_)
col=list(bank_clensed.columns)
col.pop(0)
score_dict={col[i]:score[i] for i in range(len(col))}
{k: v for k, v in sorted(score_dict.items(), key=lambda item: item[1],reverse=True)}

#Train-Test-Split
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.25,random_state=0)

#Standardization
sc=StandardScaler()
x_train=sc.fit_transform(x_train)
x_test=sc.transform(x_test)


####  Model Building  ####

#Logistic regresssion
model=LogisticRegression()
model.fit(x_train,y_train)

pred=model.predict(x_train)
pd.crosstab(pred,y_train)
np.mean(pred==y_train)#83%

pred=model.predict(x_test)
pd.crosstab(pred,y_test)
np.mean(pred==y_test)#83%



#KNN 
neigh=KNeighborsClassifier(n_neighbors=3)
neigh.fit(x_train,y_train)
np.mean(neigh.predict(x_train)==y_train)
np.mean(neigh.predict(x_test)==y_test)

acc=[]
for i in range(3,20,2):
    neigh=KNeighborsClassifier(n_neighbors=i)
    neigh.fit(x_train,y_train)
    accuracy=np.mean(neigh.predict(x_test)==y_test)
    acc.append((i,accuracy))
    print(i)
#89.71% accuracy for 7-NN



#SVM
model=SVC()
model.fit(x_train,y_train)
pred=model.predict(x_train)
np.mean(pred==y_train)#88.88%

pred=model.predict(x_test)
np.mean(pred==y_test)#88.70%



#Decision Tree
model=DecisionTreeClassifier()
model.fit(x_train,y_train)
pred=model.predict(x_train)
np.mean(pred==y_train)#99.99%

pred=model.predict(x_test)
np.mean(pred==y_test)#91.85%



#Random Forest
model=RandomForestClassifier(n_jobs=-1)
model.fit(x_train,y_train)

pred=model.predict(x_train)
pd.crosstab(pred,y_train)
np.mean(pred==y_train)#99.99% training accuracy

pred=model.predict(x_test)
pd.crosstab(pred,y_test)
np.mean(pred==y_test)#94.07% test accuracy
model.score(x_test,y_test)
cross_val=cross_val_score(model,X,Y,cv=10,n_jobs=-1)
cross_val.mean()#mean accuracy of 92.5%

#XGB
model=XGBClassifier(n_jobs=-1)
model.fit(x_train,y_train)
pred=model.predict(x_train)
np.mean(pred==y_train)#95.5%

pred=model.predict(x_test)
np.mean(pred==y_test)#94.36%
model.score(x_test,y_test)
cross_val=cross_val_score(model,X,Y,cv=10,n_jobs=-1)
cross_val.mean()#mean accuracy of 94.2%

###########################################################################

####  Hyperparameter Tuning  ####

#Random Forest
model=RandomForestClassifier(n_jobs=-1)
params={
        'max_depth':[3,5,10,None],
        'criterion':['gini','entropy'],
        'n_estimators':[100,200,300,400,500],
        'max_features':['auto', 'sqrt', 'log2'],
        'bootstrap':[True,False],
        'ccp_alpha':[0.0,0.1,0.2,0.3,0.5]
        }

search=RandomizedSearchCV(estimator=model,param_distributions=params,n_iter=20,n_jobs=-1,cv=5,scoring='roc_auc')
search.fit(X,Y)

search.best_estimator_
search.best_params_
search.best_score_

model=RandomForestClassifier(n_jobs=-1,n_estimators=200)
model.fit(x_train,y_train)
pred=model.predict(x_test)
pd.crosstab(pred,y_test)
np.mean(pred==y_test)#94.07% test accuracy

for i in range(100,1000,100):
    model=RandomForestClassifier(n_jobs=-1,n_estimators=i)
    model.fit(x_train,y_train)
    print((i,model.score(x_test,y_test)))



#XGBoost
x=np.arange(0.1,0.6,0.02)
for i in x:
    model=XGBClassifier(n_jobs=-1,learning_rate=i)
    model.fit(x_train,y_train)
    print((i,model.score(x_test,y_test)))
    
    
model=XGBClassifier(n_jobs=-1,learning_rate=0.52)
model.fit(x_train,y_train)
model.score(x_train,y_train)#96.25
model.score(x_test,y_test)#94.58

for i in range(0,500,100):
    model=XGBClassifier(n_jobs=-1,learning_rate=0.52,n_estimators=i)
    model.fit(x_train,y_train)
    print((i,model.score(x_test,y_test)))


model=XGBClassifier(n_jobs=-1,learning_rate=0.52,n_estimators=100)
model.fit(x_train,y_train)
model.score(x_train,y_train)#96.25
model.score(x_test,y_test)#94.58
cross_val=cross_val_score(model,X,Y,cv=10,n_jobs=-1)
cross_val.mean()#mean accuracy of 94.2%



####  Training on whole Dataset  ####

model=XGBClassifier(n_jobs=-1,learning_rate=0.52,n_estimators=100)
sc=StandardScaler()
X_std=sc.fit_transform(X)
model.fit(X_std,Y)


####  Saving model in system  ####
import pickle
pickle.dump(model,open('model.pkl','wb'))
pickle.dump(sc,open('sc.pkl','wb'))

####  Load model  ####
model=pickle.load(open('model.pkl','rb'))

####  testing  ####
response=[0.24,80,4,2,0,0,55000,55000,50000,0,0,1]
response=np.array(response).reshape(1,-1)
response=sc.transform(response)
model.predict(response)

#########################################################################




