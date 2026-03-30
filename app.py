import streamlit as st
from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")

st.markdown("Plan pet care tasks, build a smart daily schedule, and spot conflicts easily.")

if "owner" not in st.session_state:
    st.session_state.owner = Owner("Jordan")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler

st.subheader("Owner")
owner_name = st.text_input("Owner name", value=owner.name)
owner.name = owner_name

st.divider()

st.subheader("Add a Pet")
with st.form("pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "bird", "other"])
    care_notes = st.text_input("Care notes", value="")
    pet_submitted = st.form_submit_button("Add Pet")

    if pet_submitted:
        if pet_name.strip():
            owner.add_pet(Pet(pet_name.strip(), species, care_notes.strip()))
            st.success(f"{pet_name} was added.")
        else:
            st.warning("Please enter a pet name.")

if owner.pets:
    st.write("Current pets:")
    st.table(
        [{"Name": pet.name, "Species": pet.species, "Care Notes": pet.care_notes} for pet in owner.pets]
    )
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")
if not owner.pets:
    st.warning("Add at least one pet before adding tasks.")
else:
    with st.form("task_form"):
        selected_pet_name = st.selectbox("Choose pet", [pet.name for pet in owner.pets])
        task_description = st.text_input("Task description", value="Morning walk")
        task_date = st.date_input("Task date", value=datetime.now().date())
        task_time = st.time_input("Task time", value=datetime.now().time().replace(second=0, microsecond=0))
        duration_minutes = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"], index=0)

        task_submitted = st.form_submit_button("Add Task")

        if task_submitted:
            scheduled_time = datetime.combine(task_date, task_time)

            task = Task(
                description=task_description.strip(),
                scheduled_time=scheduled_time,
                frequency=frequency,
                duration_minutes=int(duration_minutes),
                priority=priority,
            )

            matching_pet = next((pet for pet in owner.pets if pet.name == selected_pet_name), None)

            if matching_pet and task_description.strip():
                matching_pet.add_task(task)
                st.success(f"Task '{task_description}' added for {selected_pet_name}.")
            else:
                st.warning("Please enter a valid task description.")

st.divider()

st.subheader("All Tasks")
all_tasks = owner.get_all_tasks()

if all_tasks:
    st.table(
        [
            {
                "Pet": task.pet_name,
                "Task": task.description,
                "Time": task.scheduled_time.strftime("%Y-%m-%d %H:%M"),
                "Duration": task.duration_minutes,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Completed": task.completed,
            }
            for task in scheduler.sort_tasks_by_time(all_tasks)
        ]
    )
else:
    st.info("No tasks added yet.")

st.divider()

st.subheader("Build Today's Schedule")
prioritize = st.checkbox("Prioritize by task priority instead of only time")

if st.button("Generate schedule"):
    schedule = scheduler.generate_schedule(owner, prioritize=prioritize)

    if not schedule:
        st.warning("No tasks scheduled for today.")
    else:
        st.success("Today's schedule generated successfully.")
        st.table(
            [
                {
                    "Time": task.scheduled_time.strftime("%H:%M"),
                    "Pet": task.pet_name,
                    "Task": task.description,
                    "Priority": task.priority,
                    "Duration": f"{task.duration_minutes} min",
                    "Completed": task.completed,
                }
                for task in schedule
            ]
        )

        conflicts = scheduler.detect_conflicts(schedule)
        if conflicts:
            for warning in conflicts:
                st.warning(warning)
        else:
            st.info("No schedule conflicts detected.")

        with st.expander("Why this schedule was generated"):
            for explanation in scheduler.explain_schedule(schedule):
                st.write(f"- {explanation}")
