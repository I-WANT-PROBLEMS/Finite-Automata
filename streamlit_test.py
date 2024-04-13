import streamlit as st
from PIL import Image
from deterministic_automata import *
from pyformlang.regular_expression import Regex as Regular_Expression
from graphviz import Digraph
import time
# import numpy as np
import pandas as pd
# import networkx as nx


st.set_page_config(layout="wide",page_icon="random",page_title="FA Playground",initial_sidebar_state="expanded")
with st.sidebar:
    initial_input = st.selectbox("Select Input Type",["Regular Expression","DFA","NFA"])

st.markdown("<h1 style='text-align: center; color: gold;'>End Sem Project</h1><h2 style='text-align: center; color: white;'>FA Playground</h2>\
<h3 style='text-align: center; color: cyan;'><br><u>Team - 20</u><br>Kunisetty Jaswanth<br>Pranav Ramachandrula<br>S Sruthi</h3>", unsafe_allow_html=True)

def draw_graph(graph,states,this_list,start_state,final_states):
    for i in states:
        if i == start_state:
            graph.node(str(i),shape="circle")
        elif i in final_states:
            graph.node(str(i),shape="doublecircle")
        else:
            graph.node(str(i),shape="circle")
    for i in this_list:
        graph.edge(str(i[0]),str(i[1]),label=str(i[2]))
    graph.node('??',shape="point",style="invisible")
    graph.edge('??',str(start_state))
    # graph.remove_node('??')
    # graph.render("graph",format="png")
    st.graphviz_chart(graph)

if initial_input == "Regular Expression":
    
    st.write("Input Instructions:\n 1. Use '|' or '+' for Union\
        \n2. Use '.' for Concatenation\n3. Use '*' for Kleene Closure\
        \n4. Use '$' for epsilon\n5. '(' and ')' can be used for grouping\
        \n6. All other inputs can be considered as a part of RegExp")
    add_regex = st.text_input("Enter Regular Expression: ")
    add_text = st.text_input("Enter Text: ")

    if add_regex and add_text is not None:
        a = Regular_Expression(add_regex)

        cols_s = st.columns(3)
        with cols_s[0]:
            if st.button("Check"):
                with st.spinner("Checking..."):
                    time.sleep(1)
                st.write("Is accepts: ",a.accepts(add_text))
                
        with cols_s[1]:
            if st.button("To NFA"):

                reg_nfa = a.to_epsilon_nfa()
                reg_nfa_1 = reg_nfa.to_dict()
                reg_nfa_ = {}
                list1_ = []
                for key, value in reg_nfa_1.items():
                    reg_nfa_[str(key)] = value

                for i in reg_nfa_.keys():
                    for j in reg_nfa_[i].keys():
                        # print(j)
                        for l in reg_nfa_[i][j]:
                            temp_list = [i,l,j]
                            list1_.append(temp_list)
                with st.spinner("Converting..."):
                    time.sleep(1)
                draw_graph(Digraph(),reg_nfa.states,list1_,list(reg_nfa.start_states)[0],reg_nfa.final_states)
                # img = Image.open("graph.png")
                # st.image(img, caption="DFA", use_column_width=False)
                
        with cols_s[2]:
            if st.button("To DFA"):
                reg_dfa = a.to_epsilon_nfa().to_deterministic()
                reg_dfa_1 = reg_dfa.to_dict()
                reg_dfa_ = {}
                list1_ = []

                for key, value in reg_dfa_1.items():
                    reg_dfa_[str(key)] = value

                for key, value in reg_dfa_.items():
                    reg_dfa_[key] = {str(key): str(value) for key, value in value.items()}

                for i in reg_dfa_.keys():
                    for j in reg_dfa_[i].keys():
                        # print(j)
                        for l in reg_dfa_[i][j]:
                            temp_list = [i,reg_dfa_[i][j],j]
                            list1_.append(temp_list)
                list1_ = remove_duplicate_lists(list1_)
                
                with st.spinner("Converting..."):
                    time.sleep(1)
                draw_graph(Digraph(),reg_dfa.states,list1_,list(reg_dfa.start_states)[0],reg_dfa.final_states)
                # img = "graph.png"
                # st.image(img, caption="DFA", use_column_width=False)


if initial_input == "DFA":
    a = Deterministic_automata()

    # st.title("DFA")

    add_in = st.file_uploader("Upload Transitions",accept_multiple_files=False)

    if add_in is not None:
        for line in add_in:
            try:
                line = line.decode("utf-8")
                line = line.replace("(","").replace(")","").replace(" ","").replace("\n","")
                # st.write(str(line))
                a.add_transition(*transition_input(line))
            except:
                st.error("Invalid Input")
                st.stop()

    
    states = [str(s) for s in list(a.get_nodes())]

    start_state = st.radio("Select Initial State",states,horizontal=True,key="DFA")
    in_final = st.multiselect("Select Final States",states)
    # print(type(start_state))
    a.add_start_state(start_state)

    for i in in_final:
        a.add_final_state(i)
    final_states = a.get_final_states()

    this_list = a.get_trans_list()
    # print(this_list)

    if st.button(label="Is input DFA?",key="DFA_check"):
        with st.spinner("Checking..."):
            time.sleep(1)
        st.write(a.is_dfa())

    if st.button(label="Is given DFA minimal?"):

        dict1 = a.get_transition_table()
        a.minimize()
        print(a.get_nodes())
        for x in list(a.get_nodes()):
            if x not in states:
                # print(x)
                var = x
                a.remove_state(x)
        print(a.get_nodes())
        dfa_min = a.get_transition_table()
        list1 = []
        # print(dfa_min)
        # del dfa_min[var]
        # print(dfa_min)
        for key, value in dfa_min.items():
            dfa_min[key] = {str(key): str(value) for key, value in value.items()}

        for i in dfa_min.keys():
            for j in dfa_min[i].keys():
                # print(j)
                for l in dfa_min[i][j]:
                    temp_list = [i,l,j]
                    list1.append(temp_list)
        temp_dfa = Deterministic_automata()
        list1 = remove_duplicate_lists(list1)
        for i in list1:
            temp_dfa.add_transition(*i)
        dict2 = temp_dfa.get_transition_table()
        # print(dict1)
        # print(dict2)
        # print(a.get_transition_table())
        with st.spinner("Checking..."):
            time.sleep(1)
        if dict1 == dict2:
            st.write("Yes")
        else:
            st.write("No")

    cols = st.columns(3)
    with cols[0]:
        DFA_view = st.button(label="Show DFA")


        if DFA_view is True:
            with st.spinner("Drawing..."):
                time.sleep(1)
            draw_graph(Digraph(),a.get_nodes(),this_list,start_state,final_states)
            # img = Image.open("graph.png")
            # st.image(img, caption="DFA", use_column_width=False)
            # print(a.get_nodes())


    with cols[1]:
        DFA_table = st.button(label="Show Table")

        if DFA_table:
            t_dict = a.get_transition_table()
            t_dict = pd.DataFrame(t_dict)
            t_dict = t_dict.rename(columns={start_state:"-> "+start_state})
            for each in final_states:
                t_dict = t_dict.rename(columns={str(each):"*"+str(each)})
                if each == str(start_state):
                    t_dict = t_dict.rename(columns={"-> "+start_state:"-> *"+start_state})
            t_dict = pd.DataFrame(t_dict).transpose()       

            print(start_state)
            # t_dict = dict([(value,key) for key, value in t_dict.items()])
            with st.spinner("Drawing..."):
                time.sleep(1)
            st.table(t_dict)
            # print(t_dict)

    with cols[2]:
        DFA_min = st.button(label="Show Minimized DFA")
        with st.spinner("Minimizing..."):
            time.sleep(0.5)
        if DFA_min:
            # st.write(a.get_nodes())
            a.minimize()
            print(a.get_trans_list())
            for x in list(a.get_nodes()):
                if x not in states:
                    # print(x)
                    var = x
                    a.remove_state(str(x))
            dfa_min = a.get_transition_table()
            list1 = []
            # print(dfa_min)    
            # del dfa_min[var]
            # print(dfa_min)
            for key, value in dfa_min.items():
                dfa_min[key] = {str(key): str(value) for key, value in value.items()}
            for i in dfa_min.keys():
                for j in dfa_min[i].keys():
                    # print(j)
                    for l in dfa_min[i][j]:
                        temp_list = [i,l,j]
                        list1.append(temp_list)

            dfa_min = Deterministic_automata()
            for i in list1:
                dfa_min.add_transition(*i)
            print(dfa_min.get_nodes())
            with st.spinner("Minimizing..."):
                time.sleep(1)
            draw_graph(Digraph(),dfa_min.get_nodes(),list1,start_state,final_states)
            # img = Image.open("graph.png")
            # st.image(img, caption="Minimized DFA", use_column_width=False)
            # print(a.get_nodes())

    
    if st.button(label="To Regular Expression",key="DFA_regex"):

        a.minimize()
        # print(a.get_nodes())
        final_states_min = a.get_final_states()
        start_state_min = a.get_start_state()
        # print(a.get_transition_table())
        for x in list(a.get_nodes()):
            if x not in states:
                # print(x)
                var = x
                a.remove_state(str(x))
        dfa_min = a.get_transition_table()
        list1 = []
        # print(dfa_min)
        del dfa_min[var]
        # print(dfa_min)
        for key, value in dfa_min.items():
            dfa_min[key] = {str(key): str(value) for key, value in value.items()}
        for i in dfa_min.keys():
            for j in dfa_min[i].keys():
                # print(j)
                for l in dfa_min[i][j]:
                    temp_list = [str(i),str(l),str(j)]
                    list1.append(temp_list)
        # print(list1)
        dfa_min = Deterministic_automata()
        for i in list1:
            dfa_min.add_transition(*i)
        for i in final_states_min:
            dfa_min.add_final_state(str(i))
        dfa_min.add_start_state(start_state_min)

        with st.spinner("Converting..."):
            time.sleep(1)
        # print(dfa_min.get_nodes())
        st.write(dfa_min.to_regex())
        # print(a.to_regex())


    with st.form(key="input_form"):

        input_string = st.text_input(label="Enter String")
        submit = st.form_submit_button(label="Submit")
        
        # st.write(a.is_accepts(input_string))
        with st.spinner("Checking..."):
            time.sleep(1)
        st.write(a.is_accepts(input_string))
        # print(a.get_trans_list())
    # print(type(a.get_transition_table()))




if initial_input == "NFA":
    b = Nondeterministic_automata()

    # def draw_graph(graph,states,this_list,start_state,final_states):
    #     for i in states:
    #         if i == start_state:
    #             graph.node(str(i),shape="circle")
    #         if i in final_states:
    #             graph.node(str(i),shape="doublecircle")
    #         else:
    #             graph.node(str(i),shape="circle")
    #     for i in this_list:
    #         graph.edge(str(i[0]),str(i[1]),label=str(i[2]))
    #     graph.node('??',shape="point",style="invisible")
    #     graph.edge('??',str(start_state))
    #     # graph.remove_node('??')
    #     graph.render("graph",format="png")


    add_in = st.file_uploader("Upload Transitions",accept_multiple_files=False,key="NFA")

    if add_in is not None:
        for line in add_in:
            try:
                line = line.decode("utf-8")
                line = line.replace("(","").replace(")","").replace(" ","").replace("\n","")
                # st.write(str(line))
                b.add_transition(*transition_input(line))
            except:
                st.error("Error in input file")
                st.stop()
                            

    states = [str(s) for s in list(b.get_nodes())]

    start_state_nfa = st.radio("Select Initial State",states,horizontal=True,key="NFA_radio")
    in_final_nfa = st.multiselect("Select Final States",states,key="NFA_select")
    # print(type(start_state_nfa))
    b.add_start_state(start_state_nfa)

    for i in in_final_nfa:
        b.add_final_state(i)
    final_states = b.get_final_states()

    this_list_nfa = b.get_trans_list()

    cols = st.columns(3)
    with cols[0]:
        NFA_view = st.button(label="Show NFA",key="NFA_button")

        if NFA_view is True:
            with st.spinner("Drawing..."):
                time.sleep(1)
            draw_graph(Digraph(),b.get_nodes(),this_list_nfa,start_state_nfa,final_states)
            # img = Image.open("graph.png")
            # st.image(img, caption="NFA", use_column_width=False)
            # print(b.get_nodes())
            # print(this_list_nfa)


    with cols[1]:
        NFA_table = st.button(label="Show Table",key="NFA_table")

        if NFA_table:
            t_dict = b.get_transition_table()
            t_dict = pd.DataFrame(t_dict)
            t_dict = t_dict.rename(columns={start_state_nfa:"-> "+start_state_nfa})
            for each in final_states:
                t_dict = t_dict.rename(columns={str(each):"*"+str(each)})
                if each == str(start_state_nfa):
                    t_dict = t_dict.rename(columns={"-> "+start_state_nfa:"-> *"+start_state_nfa})
            t_dict = pd.DataFrame(t_dict).transpose()

            print(start_state_nfa)
            # t_dict = dict([(value,key) for key, value in t_dict.items()])
            with st.spinner("Drawing..."):
                time.sleep(1)
            st.table(t_dict)
            # print(t_dict)
    with cols[2]:
        if st.button("To DFA",key="NFA_to_DFA"):

            c = b.get_deterministic_automata()
            print(c.to_dict())
            mm = b.get_nodes()
            print(c.states)
            c.minimize()
            print(c.states)
            finals = c.final_states
            # var = []
            # for x in list(c.states):
            #     if x not in mm:
            #         var.append(x)
            #         c._remove_state(x)
            # print(c.states)
            dfa_conv = c.to_dict()
            # print(dfa_conv)
            print(finals)
            list1_min = []
            k_str = {}

            for key, value in dfa_conv.items():
                k_str[str(key)] = value

            print(k_str)
            for key, value in k_str.items():
                k_str[key] = {str(key): str(value) for key, value in value.items()}
            print(k_str)
            for i in k_str.keys():
                for j in k_str[i].keys():
                    for l in k_str[i][j]:
                        list1_min.append([i,k_str[i][j],j])
            print(list1_min)
            list1_min1 = remove_duplicate_lists(list1_min)
            print(list1_min1)
            dfa_conv = DeterministicFiniteAutomaton()
            for i in list1_min1:
                dfa_conv.add_transition(i[0],i[2],i[1])
            for i in finals:
                dfa_conv.add_final_state(i)
            dfa_conv.add_start_state(start_state_nfa)
            # for i in list1_min1:
            #     print(i[0],i[1],i[2])
                # dfa_conv.add_transition(i[0],i[1],i[2])
            # print(dfa_conv.get_nodes())
            # # print(c.start_state,c.final_states)
            with st.spinner("Converting..."):
                time.sleep(1)
            draw_graph(Digraph(),dfa_conv.states,list1_min1,start_state_nfa,finals)
            # img = Image.open("graph.png")
            # st.image(img, caption="Minimized DFA", use_column_width=False)
        
    if st.button("To Regular Expression"):
        with st.spinner("Converting..."):
            time.sleep(1)
        st.write(b.get_regular_expression())

    if st.button("Is given NFA Deterministic?"):
        with st.spinner("Checking..."):
            time.sleep(1)        
        st.write(b.is_deterministic())

    with st.form(key="input_form_NFA"):
        input_string = st.text_input(label="Enter String")
        submit = st.form_submit_button(label="Submit")
        with st.spinner("Checking..."):
            time.sleep(1)
        st.write(b.is_accepts(input_string))


