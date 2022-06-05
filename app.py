import array
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
st.write("""
    Over SLA
""")

st.sidebar.image(image)

st.sidebar.title("Filter Data")

country_list = ["All","R1LN-PSN-NOP","R1LN-SKT-NOP","R1LN-KPP-NOP", "R1LN-TAK-NOP","R1LN-PCB-NOP","R1LN-PCT-NOP","R1LN-UTR-NOP"]
severity_list = ["All","NSA1", "NSA2", "NSA3", "NSA4", "PSA3","SA1", "SA2","SA3","SA4","SA5","SA6"]

# start_d = st.sidebar.date_input(
#      "Start Fault Date",
#      datetime.datetime.now())

# end_d = st.sidebar.date_input(
#      "End Fault Date",
#      datetime.datetime.now())

select = st.sidebar.selectbox('NOP :', country_list, key='1')
select_severity = st.sidebar.selectbox('Severity:', severity_list, key='1')

# if start_d <= end_d:
#     st.sidebar.success('Start date: `%s` \n\nEnd date: `%s`' % (start_d, end_d))
# else:
#     st.sidebar.error('Error: End date must fall after start date.')


def date_change(date):
    return date.strftime("%Y-%m-%d")
with open('style.css') as f:
    st.markdown(f'<style>{f.read()}</style>',unsafe_allow_html=True)
uploaded_file = st.file_uploader("Choose a file",type=["xls","xlsx"])

if uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file,sheet_name=1)
        
    with st.container():
        df = dataframe.sort_values(by="Fault Date")
        dataSyncAll = df[df['Over/Within'] == "Over"]

        if select == "All" and select_severity == "All":
            df = dataframe.sort_values(by="Fault Date")
            dataSync = df[df['Over/Within'] == "Over"]
        else:
            if select != "All" and select_severity == "All":
                df = dataframe.sort_values(by="Fault Date")
                dataSync = df.loc[(df['Over/Within'] == "Over") & (df['Activity'] == select)]
            if select_severity != "All" and select == "All":
                df = dataframe.sort_values(by="Fault Date")
                dataSync = df.loc[(df['Over/Within'] == "Over") & (df['Severity'] == select_severity)]
            if select_severity != "All" and select != "All":
                df = dataframe.sort_values(by="Fault Date")
                dataSync = df.loc[(df['Over/Within'] == "Over") & (df['Activity'] == select) & (df['Severity'] == select_severity)]
        
        st.warning("Summary Over SLA")
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

        for index, value in dataSyncAll.iterrows():
            nop_list.append([value['Activity'],date_change(value['Fault Date'])])
        date_list = []
        
        for v in nop_list:
            if v[1] not in date_list:
                date_list.append(v[1])

        data_clean = []

        pcb, tak, psn, skt, kpp, pct, utr = 0,0,0,0,0,0,0
        n_list = ['R1LN-PCB-NOP','R1LN-TAK-NOP','R1LN-PSN-NOP','R1LN-SKT-NOP','R1LN-KPP-NOP','R1LN-PCT-NOP','R1LN-UTR-NOP']
        lldot = []
        #loop for date
        for d in date_list:
            for n in nop_list:
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
            
  
        a = np.array(lldot)
        a.resize(7,len(date_list))

        fig = make_subplots(specs=[[{"secondary_y": True}]])
        if select == "All":
            fig.add_trace(
                go.Scatter(x=date_list, y=a[0], name="PCB",mode='lines+markers',line_shape='spline',line=dict(dash='dot')),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[1], name="TAK",mode='lines+markers',line_shape='spline'),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[2], name="PSN",mode='lines+markers',line_shape='spline',line=dict(dash='dot')),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[3], name="SKT",mode='lines+markers',line_shape='spline'),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[4], name="KPP",mode='lines+markers',line_shape='spline',line=dict(dash='dot')),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[5], name="PCT",mode='lines+markers',line_shape='spline'),secondary_y=False,
            )
            fig.add_trace(
                go.Scatter(x=date_list, y=a[6], name="UTR",mode='lines+markers',line_shape='spline',line=dict(dash='dot')),secondary_y=False,
            )
            fig.update_layout(title='Graph Analysis Over SLA',
                xaxis_title='Month',
                yaxis_title='Over Fault')
        else:
            if select == "R1LN-PCB-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[0], name="PCB",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
                )
            if select == "R1LN-TAK-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[1], name="TAK",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
                )
            if select == "R1LN-PSN-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[2], name="PSN",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
                )
            if select == "R1LN-SKT-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[3], name="SKT",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
                )
            if select == "R1LN-KPP-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[4], name="KPP",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
                )
            if select == "R1LN-PCT-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[5], name="PCT",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
                )
            if select == "R1LN-UTR-NOP":
                fig.add_trace(
                    go.Scatter(x=date_list, y=a[6], name="UTR",mode='lines+markers',line=dict(dash='dot')),secondary_y=False,
                )
            fig.update_layout(title='Graph Analysis Over SLA',
                xaxis_title='Month',
                yaxis_title='Over Fault')
        st.subheader('Graph Analysis')
        st.write(fig)




