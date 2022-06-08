import array
from re import I
from unittest import result
import streamlit as st
import pandas as pd
import datetime
from io import StringIO 
import numpy as np
import plotly.express as px
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from PIL import Image
image = Image.open('true.png')

st.title('TRUE - Analysis Data')
# st.write("""
#     Over SLA
# """)

st.sidebar.image(image)

st.sidebar.title("Filter Data")

country_list = ["All","R1LN-PSN-NOP","R1LN-SKT-NOP","R1LN-KPP-NOP", "R1LN-TAK-NOP","R1LN-PCB-NOP","R1LN-PCT-NOP","R1LN-UTR-NOP"]
severity_list = ["All","NSA1", "NSA2", "NSA3", "NSA4", "PSA3","SA1", "SA2","SA3","SA4","SA5","SA6"]


select = st.sidebar.selectbox('NOP :', country_list, key='1')
select_severity = st.sidebar.selectbox('Severity:', severity_list, key='1')


week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
def date_change(date):
    return date.strftime("%Y-%m-%d")
def day_change(date):
    return date.strftime("%A")
def index_arr(day):
    return week.index(day)

with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a file",type=["xls","xlsx"])

if uploaded_file is not None:
    try:
        dataframe = pd.read_excel(uploaded_file,sheet_name="Raw Data Ticket ROM_3")
    except Exception as e:
        st.error("Error : Sheet ที่ชื่อว่า Raw Data Ticket ROM_3 หรือ Column ในไฟล์ไม่สมบูรณ์ กรุณาตรวจสอบครับ")
    with st.container():
        df = dataframe.sort_values(by="Fault Date")

        start_d = st.sidebar.date_input("Start Fault Date",pd.to_datetime(df['Fault Date'].iloc[0]))
        #find start value
        end_d = st.sidebar.date_input("End Fault Date",pd.to_datetime(df['Fault Date'].iloc[-1]))
                #find end value

        if start_d > end_d:
            st.sidebar.error('กรุณาตรวจสอบวันที่ให้ถูกต้องครับ')
        else:
            pass
    
        dataSync = df.loc[(df['Over/Within'] == "Over") & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]
        dataWithin = df.loc[(df['Over/Within'] == "Within") & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]
        #dataSyncAll = df[df['Over/Within'] == "Over"]
        #.str.contains("ball")
        #.str[:10]
        if select == "All" and select_severity == "All":
            df = dataframe.sort_values(by="Fault Date")
            dataSync = df.loc[(df['Over/Within'] == "Over") & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]
            dataWithin = df.loc[(df['Over/Within'] == "Within") & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]

        else:
            if select != "All" and select_severity == "All":
                df = dataframe.sort_values(by="Fault Date")
                dataSync = df.loc[(df['Over/Within'] == "Over") & (df['Activity'] == select) & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]
                dataWithin = df.loc[(df['Over/Within'] == "Within") & (df['Activity'] == select) & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]

            if select_severity != "All" and select == "All":
                df = dataframe.sort_values(by="Fault Date")
                dataSync = df.loc[(df['Over/Within'] == "Over") & (df['Severity'] == select_severity) & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]
                dataWithin = df.loc[(df['Over/Within'] == "Within") & (df['Severity'] == select_severity) & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]

            if select_severity != "All" and select != "All":
                df = dataframe.sort_values(by="Fault Date")
                dataSync = df.loc[(df['Over/Within'] == "Over") & (df['Activity'] == select) & (df['Severity'] == select_severity) & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]
                dataWithin = df.loc[(df['Over/Within'] == "Within") & (df['Activity'] == select) & (df['Severity'] == select_severity) & (pd.to_datetime(df['Fault Date']) >= pd.to_datetime(start_d)) & (pd.to_datetime(df['Fault Date']) <= pd.to_datetime(end_d))]

        st.success("Summary Over SLA")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("NSA1", str(len(dataSync.loc[(dataSync['Severity'] == "NSA1")])))
        col2.metric("NSA2", str(len(dataSync.loc[(dataSync['Severity'] == "NSA2")])))
        col3.metric("NSA3", str(len(dataSync.loc[(dataSync['Severity'] == "NSA3")])))
        col4.metric("NSA4", str(len(dataSync.loc[(dataSync['Severity'] == "NSA4")])))
        col5.metric("PSA3", str(len(dataSync.loc[(dataSync['Severity'] == "PSA3")])))

        col6, col7, col8 = st.columns(3)
        col6.metric("SA1", str(len(dataSync.loc[(dataSync['Severity'] == "SA1")])))
        col7.metric("SA2", str(len(dataSync.loc[(dataSync['Severity'] == "SA2")])))
        col8.metric("SA3", str(len(dataSync.loc[(dataSync['Severity'] == "SA3")])))

        col9, col10, col11 = st.columns(3)
        col9.metric("SA4", str(len(dataSync.loc[(dataSync['Severity'] == "SA4")])))
        col10.metric("SA5", str(len(dataSync.loc[(dataSync['Severity'] == "SA5")])))
        col11.metric("SA6", str(len(dataSync.loc[(dataSync['Severity'] == "SA6")])))
        st.subheader('Data Table')
        st.write(dataSync)

        nop_list = []
        nop_list_within = []

        for index, value in dataSync.iterrows():
            nop_list.append([value['Activity'],date_change(value['Fault Date']),day_change(value['Fault Date'])])
        for index, value in dataWithin.iterrows():
            nop_list_within.append([value['Activity'],date_change(value['Fault Date']),day_change(value['Fault Date'])])

        date_list = []
        
        week_data = []
        #first value -> last value.count / 7
        #loop day push in week
        #check first date_change then return index array

        #find first day start
        # first = day_change(dataSyncAll.iloc[0][3])

        # #append week to last array
        # chk,cwk = 0,0
        # wek = []
        # j = 1
        # day_in_week = []
        # for v in nop_list:
        #     #check first loop
        #     if chk < 1:
        #         i = index_arr(first)
        #         chk = chk + 1
        #     if i <= 6:
        #         if v[1] not in day_in_week:
        #             day_in_week.append(v[1])
        #         i = i + 1
        #     else:
        #         wek.append(["Week" + str(j),day_in_week])
        #         day_in_week = []
        #         i = 0
        #         j = j + 1
        #         #return week = week + 1
        #         #new week
        # #print(wek)

        for v in nop_list:
            if v[1] not in date_list:
                date_list.append(v[1])

        #first value -> saturday

        data_clean = []

        pcb, tak, psn, skt, kpp, pct, utr = 0,0,0,0,0,0,0
        pcb_w, tak_w, psn_w, skt_w, kpp_w, pct_w, utr_w = 0,0,0,0,0,0,0
        n_list = ['R1LN-PCB-NOP','R1LN-TAK-NOP','R1LN-PSN-NOP','R1LN-SKT-NOP','R1LN-KPP-NOP','R1LN-PCT-NOP','R1LN-UTR-NOP']
        lldot = []

        llwithin = []
        #loop for date
        for d in date_list:
            for n in nop_list:
                #check in week?
                #return function find_week
                #Loop value = value +1 in week
                if n[1] == d:
                    if n[0] == 'R1LN-PCB-NOP':
                        pcb = pcb + 1
                    if n[0] == 'R1LN-TAK-NOP':
                        tak = tak + 1
                    if n[0] == 'R1LN-PSN-NOP':
                        psn = psn + 1
                    if n[0] == 'R1LN-SKT-NOP':
                        skt = skt + 1
                    if n[0] == 'R1LN-KPP-NOP':
                        kpp = kpp + 1
                    if n[0] == 'R1LN-PCT-NOP':
                        pct = pct + 1
                    if n[0] == 'R1LN-UTR-NOP':
                        utr = utr + 1
                else:
                    pass

            list_dot = [pcb, tak, psn, skt, kpp, pct, utr]
            lldot.append(list_dot)

            pcb, tak, psn, skt, kpp, pct, utr = 0,0,0,0,0,0,0

        for d in date_list:
            for n in nop_list_within:
                #check in week?
                #return function find_week
                #Loop value = value +1 in week
                if n[1] == d:
                    if n[0] == 'R1LN-PCB-NOP':
                        pcb_w = pcb_w + 1
                    if n[0] == 'R1LN-TAK-NOP':
                        tak_w = tak_w + 1
                    if n[0] == 'R1LN-PSN-NOP':
                        psn_w = psn_w + 1
                    if n[0] == 'R1LN-SKT-NOP':
                        skt_w = skt_w + 1
                    if n[0] == 'R1LN-KPP-NOP':
                        kpp_w = kpp_w + 1
                    if n[0] == 'R1LN-PCT-NOP':
                        pct_w = pct_w + 1
                    if n[0] == 'R1LN-UTR-NOP':
                        utr_w = utr_w + 1
                else:
                    pass
            
            list_within = [pcb_w, tak_w, psn_w, skt_w, kpp_w, pct_w, utr_w]
            llwithin.append(list_within)

            pcb_w, tak_w, psn_w, skt_w, kpp_w, pct_w, utr_w = 0,0,0,0,0,0,0
            
  
        a = np.array(lldot)
        a.resize(7,len(date_list))

        b = np.array(llwithin)
        b.resize(7,len(date_list))
        #print(b)

        fig2 = go.Figure()

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        if select == "All":
            fig.add_trace(
                go.Scatter(x=date_list, y=a[0], name="PCB-Over",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[1], name="TAK-Over",mode='lines+markers'),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[2], name="PSN-Over",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[3], name="SKT-Over",mode='lines+markers'),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[4], name="KPP-Over",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[5], name="PCT-Over",mode='lines+markers'),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[6], name="UTR-Over",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
            )
            fig.update_layout(
                xaxis_title='Month',
                yaxis_title='Over Fault')
            
        else:
            if select == "R1LN-PCB-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[0], name="PCB-Over",mode='lines+markers',line=dict(dash='dot',color="#990F02")),secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=date_list, y=b[0], name="PCB-Within",mode='lines+markers',line=dict(color="#5DBB63")),secondary_y=False,
                )
                fig.add_trace(go.Bar(
                    y=a[0],
                    x=date_list,
                    name='PCB-Bar-Over',
                    marker_color="#990F02",
                    opacity=0.5,
                    width=[3]
                ))
                fig.add_trace(go.Bar(
                    y=b[0],
                    x=date_list,
                    name='PCB-Bar-Within',
                    opacity=0.5,
                    marker_color="#5DBB63",
                    width=[3]
                ))
                fig2.update_layout(title="Analysis By Province PCB")
                fig2.add_bar(x=date_list,y=a[0],name="PCB-Over",marker_color="#BC544B")
                fig2.add_bar(x=date_list,y=b[0],name="PCB-Within",marker_color="#1F456E")
                fig2.update_layout(barmode="relative")

            if select == "R1LN-TAK-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[1], name="TAK-Over",mode='lines+markers',line=dict(dash='dot',color="#990F02")),secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=date_list, y=b[1], name="TAK-Within",mode='lines+markers',line=dict(color="#5DBB63")),secondary_y=False,
                )
                fig.add_trace(go.Bar(
                    y=a[1],
                    x=date_list,
                    name='TAK-Bar-Over',
                    marker_color="#990F02",
                    opacity=0.5,
                    width=[3]
                ))
                fig.add_trace(go.Bar(
                    y=b[1],
                    x=date_list,
                    name='TAK-Bar-Within',
                    opacity=0.5,
                    marker_color="#5DBB63",
                    width=[3]
                ))
                fig2.update_layout(title="Analysis By Province PCB")
                fig2.add_bar(x=date_list,y=a[1],name="TAK-Over",marker_color="#BC544B")
                fig2.add_bar(x=date_list,y=b[1],name="TAK-Within",marker_color="#1F456E")
                fig2.update_layout(barmode="relative")
            if select == "R1LN-PSN-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[2], name="PSN-Over",mode='lines+markers',line=dict(dash='dot',color="#990F02")),secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=date_list, y=b[2], name="PSN-Within",mode='lines+markers',line=dict(color="#5DBB63")),secondary_y=False,
                )
                fig.add_trace(go.Bar(
                    y=a[2],
                    x=date_list,
                    name='PSN-Bar-Over',
                    marker_color="#990F02",
                    opacity=0.5,
                    width=[3]
                ))
                fig.add_trace(go.Bar(
                    y=b[2],
                    x=date_list,
                    name='PSN-Bar-Within',
                    opacity=0.5,
                    marker_color="#5DBB63",
                    width=[3]
                ))
                fig2.update_layout(title="Analysis By Province PSN")
                fig2.add_bar(x=date_list,y=a[2],name="PSN-Over",marker_color="#BC544B")
                fig2.add_bar(x=date_list,y=b[2],name="PSN-Within",marker_color="#1F456E")
                fig2.update_layout(barmode="relative")
            if select == "R1LN-SKT-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[3], name="SKT-Over",mode='lines+markers',line=dict(dash='dot',color="#990F02")),secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=date_list, y=b[3], name="SKT-Within",mode='lines+markers',line=dict(color="#5DBB63")),secondary_y=False,
                )
                fig.add_trace(go.Bar(
                    y=a[3],
                    x=date_list,
                    name='SKT-Bar-Over',
                    marker_color="#990F02",
                    opacity=0.5,
                    width=[3]
                ))
                fig.add_trace(go.Bar(
                    y=b[3],
                    x=date_list,
                    name='SKT-Bar-Within',
                    opacity=0.5,
                    marker_color="#5DBB63",
                    width=[3]
                ))
                fig2.update_layout(title="Analysis By Province SKT")
                fig2.add_bar(x=date_list,y=a[3],name="SKT-Over",marker_color="#BC544B")
                fig2.add_bar(x=date_list,y=b[3],name="SKT-Within",marker_color="#1F456E")
                fig2.update_layout(barmode="relative")
            if select == "R1LN-KPP-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[4], name="KPP-Over",mode='lines+markers',line=dict(dash='dot',color="#990F02")),secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=date_list, y=b[4], name="KPP-Within",mode='lines+markers',line=dict(color="#5DBB63")),secondary_y=False,
                )
                fig.add_trace(go.Bar(
                    y=a[4],
                    x=date_list,
                    name='KPP-Bar-Over',
                    marker_color="#990F02",
                    opacity=0.5,
                    width=[3]
                ))
                fig.add_trace(go.Bar(
                    y=b[4],
                    x=date_list,
                    name='KPP-Bar-Within',
                    opacity=0.5,
                    marker_color="#5DBB63",
                    width=[3]
                ))
                fig2.update_layout(title="Analysis By Province KPP")
                fig2.add_bar(x=date_list,y=a[4],name="KPP-Over",marker_color="#BC544B")
                fig2.add_bar(x=date_list,y=b[4],name="KPP-Within",marker_color="#1F456E")
                fig2.update_layout(barmode="relative")
            if select == "R1LN-PCT-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[5], name="PCT-Over",mode='lines+markers',line=dict(dash='dot',color="#990F02")),secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=date_list, y=b[5], name="PCT-Within",mode='lines+markers',line=dict(color="#5DBB63")),secondary_y=False,
                )
                fig.add_trace(go.Bar(
                    y=a[5],
                    x=date_list,
                    name='PCT-Bar-Over',
                    marker_color="#990F02",
                    opacity=0.5,
                    width=[3]
                ))
                fig.add_trace(go.Bar(
                    y=b[5],
                    x=date_list,
                    name='PCT-Bar-Within',
                    opacity=0.5,
                    marker_color="#5DBB63",
                    width=[3]
                ))
                fig2.update_layout(title="Analysis By Province PCT")
                fig2.add_bar(x=date_list,y=a[5],name="PCT-Over",marker_color="#BC544B")
                fig2.add_bar(x=date_list,y=b[5],name="PCT-Within",marker_color="#1F456E")
                fig2.update_layout(barmode="relative")
            if select == "R1LN-UTR-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[6], name="UTR-Over",mode='lines+markers',line=dict(dash='dot',color="#990F02")),secondary_y=False,
                )
                fig.add_trace(
                    go.Scatter(x=date_list, y=b[6], name="UTR-Within",mode='lines+markers',line=dict(color="#5DBB63")),secondary_y=False,
                )
                fig.add_trace(go.Bar(
                    y=a[6],
                    x=date_list,
                    name='UTR-Bar-Over',
                    marker_color="#990F02",
                    opacity=0.5,
                    width=[3]
                ))
                fig.add_trace(go.Bar(
                    y=b[6],
                    x=date_list,
                    name='UTR-Bar-Within',
                    opacity=0.5,
                    marker_color="#5DBB63",
                    width=[3]
                ))
                fig2.update_layout(title="Analysis By Province UTR")
                fig2.add_bar(x=date_list,y=a[6],name="UTR-Over",marker_color="#BC544B")
                fig2.add_bar(x=date_list,y=b[6],name="UTR-Within",marker_color="#1F456E")
                fig2.update_layout(barmode="relative")
            fig.update_layout(title='Graph Analysis Over SLA',
                xaxis_title='Month',
                yaxis_title='Over Fault')
        st.subheader('Graph Analysis')
        st.write(fig)
        if select != "All":
            st.write(fig2)




