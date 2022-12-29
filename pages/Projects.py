import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import time
from datetime import date
import random
import helper
import display_functions as dsf
import input_functions as inp
# Generating DataFrame

try:
    projects = pd.read_csv('projects.csv')
except Exception as e:
    projects = pd.DataFrame(columns=['Name', 'Due Date', 'Priority', 'Completed Tasks', 'Total Tasks', 'descr'])

projects = helper.clean_df(projects)  # function to clean data
tabs = st.tabs(['My Projects', 'Add Project'])
projects = helper.dates_in_data(projects)  # function to format dates
# Adding a project and updating csv
with tabs[1]:
    name = st.text_input('Project Name').capitalize()
    description = st.text_area('Description')
    today = date.today()
    due = st.date_input('Due Date', min_value=today)
    col1, col2 = st.columns(2)
    with col1:
        priority = st.slider('Project Priority', min_value=1, max_value=5, step=1)

    if st.button('submit'):
        dsf.progress()
        if name in list(projects['Name']):
            st.error('Project already exists')

        else:
            st.success('Project Added')
            projects.loc[len(projects.index)] = [name, due, priority, 0, 1, description, 0, 0, 0, 0]
            projects = helper.dates_in_data(projects)
            projects.to_csv('projects.csv')
            temp_data = pd.DataFrame(columns=['Task', 'Status'])
            temp_data.to_csv(f'projects_{name}.csv')

# select box for projects
project_list = list(projects['Name'])
project_list.insert(0, 'All projects')
proj = st.sidebar.selectbox('Manage: ', project_list)

# Displaying all projects
if proj == 'All projects':
    with tabs[0]:
        choice = st.sidebar.selectbox('Sort By:-', ['Date added', 'Due Date', 'Priority'])
        if choice == 'Date added':
            display = projects
        elif choice == 'Due Date':
            display = projects.sort_values(by='Due Date')
        else:
            display = projects.sort_values(by='Priority', ascending=False)

        names, date, priorities, completed = st.columns(4)
        with names:
            st.markdown('**Name**')
            for i in display['Name']:
                st.write(i)
                st.write('----')
        with date:
            st.markdown('**Due Date**')
            try:
                for i, j, k, p in zip(display['day'], display['month'], display['year'], display['Due Date']):
                    if p.date() < today:
                        st.write('Past due')
                    elif p.date() == today:
                        st.write('Due today')
                    else:
                        st.write(str(i), str(j), str(k))
                    st.write('----')
            except Exception as e:
                pass
        with priorities:
            st.markdown('**Priority**')
            for i in display['Priority']:
                st.write(str(i))
                st.write('----')
        with completed:
            st.markdown('**Completed**')
            for comp, total in zip(display['Completed Tasks'], display['Total Tasks']):
                percent = (comp // total) * 100
                st.write(f'{percent}%')
                st.write('----')

# Managing a project:
# Make separate dataframes for tasks and details or add task columns after details

else:
    with tabs[0]:
        proj_row = projects[projects['Name'] == proj]
        proj_descr = (proj_row['descr'].values[0])
,
        st.markdown(f'<h2 style="font-weight: bolder;text-decoration-line: underline; ">{proj}</h2>',
                    unsafe_allow_html=True)
        st.markdown(f'<h4>{proj_descr}</h4>', unsafe_allow_html=True)

        proj_data = pd.read_csv(f'projects_{proj}.csv')
        proj_data = helper.clean_df(proj_data)

        # Manage tasks inside a project
        with st.expander("Manage tasks: "):
            proj_tasks, status, functions = st.columns(3)

            with functions:
                # add task
                task_title = st.text_input('Task title')
                inp.add_task(task_title,proj_data)
                proj_data.to_csv(f'projects_{proj}.csv')
                st.write('---')

                # delete task
                temp_list = list(proj_data['Task'])
                temp_list.insert(0, 'Delete')
                selected_task = st.selectbox('select a task', temp_list)
                if st.button('Delete task permanently'):
                    proj_data.drop(proj_data.index[(proj_data["Task"] == selected_task)], axis=0, inplace=True)
                    proj_data.to_csv(f'projects_{proj}.csv')

            with proj_tasks:
                proj_data = pd.read_csv(f'projects_{proj}.csv')
                proj_data = helper.clean_df(proj_data)
                if proj_data.shape[0] == 0:
                    st.write('No tasks yet')
                else:
                    helper.completed_tasks(proj_data)
        # Status of completion
        project_completion = dsf.project_completion(proj_data)