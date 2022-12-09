import pandas as pd
import streamlit as st
import matplotlib as pyplot
import time





# Generating DataFrame
try:
    projects = pd.read_csv('projects.csv')
except Exception as e:
    projects = pd.DataFrame(columns=['Name', 'Due Date', 'Priority','Completed Tasks','Total Tasks','descr'])

try:
    projects.drop(['Unnamed: 0'],axis=1,inplace=True)
except Exception as e:
    pass
tabs = st.tabs(['My Projects','Add Project'])





# Handling Date and Time
projects['Due Date']=pd.to_datetime(projects['Due Date'])
projects['year'] = projects['Due Date'].dt.year
projects['month'] = projects['Due Date'].dt.month_name()
projects['day'] = projects['Due Date'].dt.day
projects['hour'] = projects['Due Date'].dt.hour




# Adding a project and updating csv
with tabs[1]:
    name = st.text_input('Project Name').capitalize()
    description = st.text_area('Description')
    due = st.date_input('Due Date')
    col1,col2 = st.columns(2)
    with col1:
        priority = st.slider('Project Priority',min_value=1,max_value=5,step=1)

    if st.button('submit'):
        progress = st.progress(0)
        for i in range(100):
            time.sleep(0.01)
            progress.progress(i+1)
        if name in list(projects['Name']):
            st.error('Project already exists')

        else:
            st.success('Project Added')
            projects.loc[len(projects.index)] = [name,due,priority,0,1,description,0,0,0,0]
            projects.to_csv('projects.csv')




# select box for projects
project_list = list(projects['Name'])
project_list.insert(0,'All projects')
proj=st.sidebar.selectbox('Manage: ',project_list)




# Displaying all projects
if proj=='All projects':
    with tabs[0]:
        choice=st.sidebar.selectbox('Sort By:-',['Date added','Due Date','Priority'])
        if choice == 'Date added':
            display = projects
        elif choice == 'Due Date':
            display = projects.sort_values(by='Due Date')
        else:
            display = projects.sort_values(by='Priority',ascending=False)

        names, date, priorities,completed = st.columns(4)
        with names:
            st.markdown('**Name**')
            for i in display['Name']:
                st.write(i)
                st.write('----')
        with date:
            st.markdown('**Due Date**')
            for i,j,k in zip(display['day'],display['month'],display['year']):
                st.write(str(i),str(j),str(k))
                st.write('----')
        with priorities:
            st.markdown('**Priority**')
            for i in display['Priority']:
                st.write(str(i))
                st.write('----')
        with completed:
            st.markdown('**Completed**')
            for comp,total in zip(display['Completed Tasks'],display['Total Tasks']):
                percent = (comp//total)*100
                st.write(f'{percent}%')
                st.write('----')


#Managing a project:
else:
    pass


