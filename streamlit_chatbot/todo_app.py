import streamlit as st

# Initialize session state to store tasks
if "tasks" not in st.session_state:
    st.session_state.tasks = []

# Function to add a task
def add_task():
    task = st.session_state.task_input.strip()
    if task and task not in st.session_state.tasks:
        st.session_state.tasks.append({"task": task, "completed": False})
        st.session_state.task_input = ""  # Clear input after adding

# Function to delete a task
def delete_task(index):
    st.session_state.tasks.pop(index)

# Streamlit UI
st.title("📝 To-Do List App")

# Task input form
st.text_input(
    "Add a new task", 
    key="task_input", 
    on_change=add_task,
    placeholder="E.g., Learn Streamlit..."
)

# Display tasks
st.divider()
st.subheader("Your Tasks")

for i, task in enumerate(st.session_state.tasks):
    col1, col2 = st.columns([0.8, 0.2])
    with col1:
        # Checkbox to mark completion
        completed = st.checkbox(
            task["task"], 
            value=task["completed"],
            key=f"task_{i}",
            on_change=lambda i=i: st.session_state.tasks[i].update({"completed": not st.session_state.tasks[i]["completed"]})
        )
    with col2:
        # Delete button
        if st.button("❌", key=f"delete_{i}"):
            delete_task(i)

# Show completion stats
completed_tasks = sum(task["completed"] for task in st.session_state.tasks)
st.caption(f"✅ {completed_tasks}/{len(st.session_state.tasks)} tasks completed")