import numpy as np
import pandas as pd
import streamlit as st
import seaborn as sns
import altair as alt
import matplotlib.pyplot as plt

st.set_option('deprecation.showPyplotGlobalUse', False)

# loading Dataset 
data = pd.read_csv('new_train.csv');
st.title('Portugese Bank Term Deposit Analysis')
df = data.rename(columns={'y': 'campaign_result','poutcome':'previous_outcome'})
options = [
            'What type of job customers who subscribed to term deposits do?',
            'What is the education qualification of the above same group?',
            'Does age have an influence on the customer decision?',
            'Which campaign was more successful?',
            'What are the different types of Relationships?']


selection = st.sidebar.radio('Select the page to view', options)
df.replace(999, -1, inplace=True)

if selection == 'dataframe':
    st.write(df)
    
if selection == 'What type of job customers who subscribed to term deposits do?':

    job = df['job'][df['campaign_result'] == "yes"].value_counts()
    deposit = df['job'][df['campaign_result'] == "yes"].value_counts().keys()

    plt.figure(figsize=(13, 8))
    plt.title("Jobs and Term Deposit")
    plt.ylabel("Deposit Count")
    plt.xlabel("Jobs")
    plt.xticks(fontsize=9, rotation=90)
    plt.subplots_adjust(bottom=0.19)
    plt.bar(deposit, job)
    st.pyplot()
    
if selection == 'What is the education qualification of the above same group?':
    
    job = df['education'][df['campaign_result'] == "yes"].value_counts()
    deposit = df['education'][df['campaign_result'] == "yes"].value_counts().keys()

    plt.figure(figsize=(13, 8))
    plt.title("Education and Term Deposit")
    plt.ylabel("Deposit Count")
    plt.xlabel("Education")
    plt.xticks(fontsize=9, rotation=90)
    plt.subplots_adjust(bottom=0.19)
    plt.bar(deposit, job)
    st.pyplot()
    
if selection == 'What are the different types of Relationships?':
    
    cat_var= df.select_dtypes(include= ["object"]).columns
    plt.style.use("ggplot")
    for column in cat_var:
        plt.figure(figsize=(20,4))
        plt.subplot(121)
        df[column].value_counts().plot(kind="bar")
        plt.xlabel(column)
        plt.ylabel("number of customers")
        plt.title(column)
        st.pyplot()

if selection == 'Does age have an influence on the customer decision?':
    df2 = df
    df2["age_group"] = pd.cut(x=df2['age'], bins=[0,15,30,45,60,75,90,105], labels=["0-15","15-30","30-45","45-60","60-75","75-90","90-105"])
    labels = ["0-15","15-30","30-45","45-60","60-75","75-90","90-105"]
    
    yes = df2['age_group'][df2['campaign_result'] == "yes"].value_counts()
    no = df2['age_group'][df2['campaign_result'] == "no"].value_counts()
    deposit = df2['age_group'][df2['campaign_result'] == "yes"].value_counts().keys()

    x = np.arange(len(deposit))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    rects1 = ax.bar(x - width/2, yes, width, label='Yes')
    rects2 = ax.bar(x + width/2, no, width, label='No')

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel('Customer Decision')
    ax.set_title('Decision by Age')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()
    st.pyplot()
    
    
if selection == 'Which campaign was more successful?':
    
    plt.clf()
    plt.title("Success Rate")
    options = ['success']
    df1 = df[df['previous_outcome'].isin(options)]
    df1['month'] = pd.Categorical(df1['month'], ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec'])
    df1=df1.sort_values("month")
    df1['day_of_week'] = pd.Categorical(df1['day_of_week'], ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun'])
    df1.sort_values("day_of_week")
    opt = st.selectbox("Select among month and week:", ['Month', 'Week'])
    plt.style.use("ggplot")
    plt.figure(figsize=(20,4))
    plt.subplot(121)
    if opt == 'Month':
        Legend=['Success']
        sns.countplot(df1['month'], hue=df1["previous_outcome"])   
        plt.xticks(rotation=90)
        plt.xlabel('month')
        plt.ylabel("number of customers")
        plt.title("Monthly Succes Rate(MSR)")
        plt.legend(Legend,loc=1)
        st.pyplot()

    if opt == 'Week':
        Legend=['Success','Failure']
        sns.countplot(df1['day_of_week'], hue=df1["previous_outcome"],palette=sns.color_palette("tab10") )    
        plt.xticks(rotation=90)
        plt.xlabel('Week')
        plt.ylabel("number of customers")
        plt.title("Weekly Succes Rate(WSR)")
        plt.legend(Legend,loc=1)
        st.pyplot()
