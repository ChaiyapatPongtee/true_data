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

st.title('TRUE - Analysis Data')
st.write("""
    Over SLA
""")

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
uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    dataframe = pd.read_excel(uploaded_file.name,sheet_name=1)
    with st.container():
        st.warning("Summary Over SLA")
        col1, col2, col3, col4, col5 = st.columns(5)
        col1.metric("NSA1", str(len(dataframe.loc[(dataframe['Severity'] == "NSA1") & (dataframe['Over/Within'] == "Over")])))
        col2.metric("NSA2", str(len(dataframe.loc[(dataframe['Severity'] == "NSA2") & (dataframe['Over/Within'] == "Over")])))
        col3.metric("NSA3", str(len(dataframe.loc[(dataframe['Severity'] == "NSA3") & (dataframe['Over/Within'] == "Over")])))
        col4.metric("NSA4", str(len(dataframe.loc[(dataframe['Severity'] == "NSA4") & (dataframe['Over/Within'] == "Over")])))
        col5.metric("PSA3", str(len(dataframe.loc[(dataframe['Severity'] == "PSA3") & (dataframe['Over/Within'] == "Over")])))

        col6, col7, col8 = st.columns(3)
        col6.metric("SA1", str(len(dataframe.loc[(dataframe['Severity'] == "SA1") & (dataframe['Over/Within'] == "Over")])))
        col7.metric("SA2", str(len(dataframe.loc[(dataframe['Severity'] == "SA2") & (dataframe['Over/Within'] == "Over")])))
        col8.metric("SA3", str(len(dataframe.loc[(dataframe['Severity'] == "SA3") & (dataframe['Over/Within'] == "Over")])))

        col9, col10, col11 = st.columns(3)
        col9.metric("SA4", str(len(dataframe.loc[(dataframe['Severity'] == "SA4") & (dataframe['Over/Within'] == "Over")])))
        col10.metric("SA5", str(len(dataframe.loc[(dataframe['Severity'] == "SA5") & (dataframe['Over/Within'] == "Over")])))
        col11.metric("SA6", str(len(dataframe.loc[(dataframe['Severity'] == "SA6") & (dataframe['Over/Within'] == "Over")])))
    

    with st.container():
        df = dataframe.sort_values(by="Fault Date")
        dataSyncAll = df[df['Over/Within'] == "Over"]

        if select == "All" and select_severity == "All":
            df = dataframe.sort_values(by="Fault Date")
            dataSync = df[df['Over/Within'] == "Over"]
        else:
            if select != "All" and select_severity == "All":
                df = dataframe.sort_values(by="Fault Date")
                dataSync = df.loc[(df['Over/Within'] == "Over") & (df['Activity'] == select & (df['Fault Date'] >= start_d) & (df['Fault Date'] <= end_d))]
            if select_severity != "All" and select == "All":
                df = dataframe.sort_values(by="Fault Date")
                dataSync = df.loc[(df['Over/Within'] == "Over") & (df['Severity'] == select_severity)]
            if select_severity != "All" and select != "All":
                df = dataframe.sort_values(by="Fault Date")
                dataSync = df.loc[(df['Over/Within'] == "Over") & (df['Activity'] == select) & (df['Severity'] == select_severity)]

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
        fig.add_trace(
            go.Scatter(x=date_list, y=a[0], name="PCB",mode='lines+markers',line_shape='spline'),secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=date_list, y=a[1], name="TAK",mode='lines+markers',line_shape='spline'),secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=date_list, y=a[2], name="PSN",mode='lines+markers',line_shape='spline'),secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=date_list, y=a[3], name="SKT",mode='lines+markers',line_shape='spline'),secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=date_list, y=a[4], name="KPP",mode='lines+markers',line_shape='spline'),secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=date_list, y=a[5], name="PCT",mode='lines+markers',line_shape='spline'),secondary_y=False,
        )
        fig.add_trace(
            go.Scatter(x=date_list, y=a[6], name="UTR",mode='lines+markers',line_shape='spline'),secondary_y=False,
        )
        fig.update_layout(title='Graph Analysis Over SLA',
                   xaxis_title='Month',
                   yaxis_title='Over Fault')
        st.subheader('Graph Analysis')
        st.write(fig)




