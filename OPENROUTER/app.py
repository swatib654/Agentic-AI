import streamlit as st
import math

def calculate():
    try:
        expression = st.session_state.expression
        # Replace common mathematical function names with their math module equivalents
        expression = expression.replace('^', '**')
        expression = expression.replace('sqrt', 'math.sqrt')
        expression = expression.replace('sin', 'math.sin')
        expression = expression.replace('cos', 'math.cos')
        expression = expression.replace('tan', 'math.tan')
        expression = expression.replace('log', 'math.log10') # Common log base 10
        expression = expression.replace('ln', 'math.log') # Natural log

        result = eval(expression)
        st.session_state.expression = str(result)
    except Exception as e:
        st.session_state.expression = "Error"

def append_to_expression(char):
    if st.session_state.expression == "Error":
        st.session_state.expression = ""
    st.session_state.expression += str(char)

def clear_expression():
    st.session_state.expression = ""

def backspace():
    if st.session_state.expression != "Error":
        st.session_state.expression = st.session_state.expression[:-1]

st.title("Advanced Calculator")

if 'expression' not in st.session_state:
    st.session_state.expression = ""

st.text_input("Expression", value=st.session_state.expression, key="input_expression", on_change=None, disabled=True)

# Define buttons for an advanced calculator layout
button_layout = [
    ["C", "del", "(", ")"],
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["0", ".", "=", "+"],
    ["sqrt", "sin", "cos", "tan"],
    ["log", "ln", "^", "pi"]
]

for row_buttons in button_layout:
    cols = st.columns(len(row_buttons))
    for i, button_label in enumerate(row_buttons):
        with cols[i]:
            if button_label == "=":
                st.button(button_label, on_click=calculate, use_container_width=True)
            elif button_label == "C":
                st.button(button_label, on_click=clear_expression, use_container_width=True)
            elif button_label == "del":
                st.button(button_label, on_click=backspace, use_container_width=True)
            elif button_label == "pi":
                st.button(button_label, on_click=append_to_expression, args=(str(math.pi),), use_container_width=True)
            else:
                st.button(button_label, on_click=append_to_expression, args=(button_label,), use_container_width=True)
