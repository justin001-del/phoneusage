import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


with open("assets/style.css") as f:
    st.write('css loaded')
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html= True)

st.title("Phone tracker")

st.markdown("📂upload cs or Enter manually")
            

uploaded_file= st.file_uploader("upload here",type=["csv"])
user_manual=st.checkbox("i want to enter manually")


if uploaded_file is not None:
     usage_df=pd.read_csv(uploaded_file)
     st.success("csv uploded successfully")

elif user_manual:
    d={
        "Date": ["2025-06-01"],
        "ScreenTime_h": [0],
        "ScreenTime_m": [0],
        "TopApp": [""],
        "TopAppUsage_h": [0],
        "TopAppUsage_m": [0],
}
    default_data= pd.DataFrame(d)
    usage_df=st.data_editor(default_data, num_rows="dynamic", use_container_width=True)
    st.info("you can add more rows manually")
    if len(usage_df) > 7:
        st.error("enter no more than 7 rows (1 day each)")
        
        st.write("delete extra rows by clicking each rows manaually")
        st.stop()


else:
    st.warning("Please upload a CSV or choose to enter data manually.")
    st.stop()


usage_df['total_screentime_m']= usage_df['ScreenTime_h']*60 +usage_df['ScreenTime_m']

weekly_usage = usage_df.groupby('Date')['total_screentime_m'].mean()
duration = (weekly_usage.sum() /60).astype(int)

st.write(f"Your total screen time is {duration} hoursthis week ⏱️")
st.write(weekly_usage.reset_index())

hrs_wasted1=(weekly_usage.max())/60
date1=weekly_usage.idxmax()

hrs_wasted2=(weekly_usage.min())/60
date2=weekly_usage.idxmin()


if(hrs_wasted1<=5):
    st.write(f" you have used for {hrs_wasted1} hrs ,on {date1} , not bad , doing well 👍")

elif(hrs_wasted1>=6 and hrs_wasted1<=8):
    st.write(f" you have used for {hrs_wasted1} hrs ,on {date1}, you wanna win? good joke🤷‍♀️")

else:
    st.write(f'you have used for {hrs_wasted1} hrs ,on {date1}, are you proud eh? 😁')


a=(weekly_usage.mean()/60).astype(int)
if(a>=5):
    st.write(f" congrtas ! you have spent {a} hrs avg on ur mobile")

else:
    st.write(f"💕😊,{a} that is ur avg phone , Good")

usage_df['total_TopAppUsage_m']=(usage_df["TopAppUsage_h"]*60) +(usage_df['TopAppUsage_m'])

top=usage_df.groupby('TopApp')['total_TopAppUsage_m'].sum()
st.write(top)

good=["ChatGPT" ,"google"]
bad = ["Instagram", "YouTube"]
st.write(good)
st.write(bad)

top_max=top.max()
top_index=top.idxmax()


if(top_index in bad):
    st.write(f"u have wasted this much time on {top_max /60} hrs, on {top_index}")

else:
    st.write("✌️")


usage_df['neutral_timespent'] =(usage_df['total_screentime_m'])-usage_df['total_TopAppUsage_m'] 



neutral=usage_df.groupby('Date')['neutral_timespent'].mean().reset_index()
neutral.index= range(1,len(neutral)+1)
st.write(neutral)


day = st.number_input(
    "Select the day you want to know about the neutral time (1 to 7)",
    min_value=1,
    max_value=7,
    step=1
)


try:
    j=neutral.loc[day]
    time=int(j['neutral_timespent'])
    date=j['Date']
    st.write(f"u have used ur phone for {time}hrs, on neutral things at {date} , neither on productivity and produvtivity eaters ")
except KeyError:
    st.write("pls select numbers between 1 to 7")


i=usage_df['Date']
xpos=np.arange(len(i))


fig,(ax1,ax3)=plt.subplots(1, 2, figsize=(15,5))  # Creates the first of three subplots in a 1-row layout

colors1 = ['red' if val >=400 else 'blue' for val in usage_df['total_screentime_m']]


ax1.bar(xpos,usage_df['total_screentime_m'], color=colors1)
ax1.set_xlabel('days')
ax1.set_ylabel('mins')
ax1.set_title("total screen time per date")

  
    
colors2 = ['red' if val >300 else 'blue' for val in usage_df['neutral_timespent']]

ax3.bar(xpos,usage_df['neutral_timespent'],color=colors2)
ax3.set_xlabel('days')
ax3.set_ylabel('mins')
ax3.set_title('time spent neither on good apps nor on bad apps')
st.pyplot(fig)



usage_df['total_screentime_m'].dtype
top_3 = usage_df.nlargest(3, 'total_screentime_m').reset_index()
st.write(top_3)


