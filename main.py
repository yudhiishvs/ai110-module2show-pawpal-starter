import os
import streamlit as st
from datetime import datetime, timedelta, time
from pawpal_system import Owner, Pet, Task, Scheduler


DATA_FILE = "pawpal_data.json"


st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")
st.title("🐾 PawPal+")
st.caption("Smart pet care scheduling with sorting, conflicts, recurrence, and persistence.")

if "owner" not in st.session_state:
    if os.path.exists(DATA_FILE):
        st.session_state.owner = Owner.load_from_json(DATA_FILE)
    else:
        st.session_state.owner = Owner("Jordan")

if "scheduler" not in st.session_state:
    st.session_state.scheduler = Scheduler()

owner = st.session_state.owner
scheduler = st.session_state.scheduler


def save_data():
    owner.save_to_json(DATA_FILE)


st.subheader("Owner")
owner.name = st.text_input("Owner name", value=owner.name)

st.divider()

st.subheader("Add a Pet")
with st.form("pet_form"):
    pet_name = st.text_input("Pet name")
    species = st.selectbox("Species", ["dog", "cat", "bird", "rabbit", "other"])
    care_notes = st.text_input("Care notes")
    pet_submit = st.form_submit_button("Add Pet")

if pet_submit:
    if pet_name.strip():
        owner.add_pet(Pet(pet_name.strip(), species, care_notes.strip()))
        save_data()
        st.success(f"Added pet: {pet_name}")
    else:
        st.warning("Please enter a pet name.")

if owner.pets:
    st.write("Current pets")
    st.table(
        [
            {"Name": pet.name, "Species": pet.species, "Care Notes": pet.care_notes}
            for pet in owner.pets
        ]
    )
else:
    st.info("No pets added yet.")

st.divider()

st.subheader("Add a Task")
if not owner.pets:
    st.warning("Add a pet first.")
else:
    with st.form("task_form"):
        selected_pet_name = st.selectbox("Choose pet", [pet.name for pet in owner.pets])
        description = st.text_input("Task description", value="Morning walk")
        task_date = st.date_input("Task date", value=datetime.now().date())
        default_time = (datetime.now() + timedelta(minutes=30)).time().replace(second=0, microsecond=0)
        task_time = st.time_input("Task time", value=default_time)
        duration_minutes = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
        priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)
        frequency = st.selectbox("Frequency", ["once", "daily", "weekly"])
        task_submit = st.form_submit_button("Add Task")

    if task_submit:
        if description.strip():
            scheduled_dt = datetime.combine(task_date, task_time)
            task = Task(
                description=description.strip(),
                scheduled_time=scheduled_dt,
                frequency=frequency,
                duration_minutes=int(duration_minutes),
                priority=priority,
            )
            pet = owner.find_pet(selected_pet_name)
            if pet:
                pet.add_task(task)
                save_data()
                st.success(f"Added task '{description}' for {selected_pet_name}.")
        else:
            st.warning("Please enter a task description.")

st.divider()

st.subheader("All Tasks")
all_tasks = owner.get_all_tasks()

if all_tasks:
    st.dataframe(
        [
            {
                "Pet": task.pet_name,
                "Task": task.description,
                "Time": task.scheduled_time.strftime("%Y-%m-%d %H:%M"),
                "Duration": task.duration_minutes,
                "Priority": task.priority,
                "Frequency": task.frequency,
                "Completed": "✅" if task.completed else "⏳",
            }
            for task in scheduler.sort_tasks_by_time(all_tasks)
        ],
        use_container_width=True,
    )
else:
    st.info("No tasks yet.")

st.divider()

st.subheader("Build Today's Schedule")
strategy = st.selectbox(
    "Scheduling strategy",
    ["time", "priority", "weighted"],
    help="Weighted uses priority + urgency together.",
)

if st.button("Generate schedule"):
    schedule = scheduler.generate_schedule(owner, strategy=strategy)

    if not schedule:
        st.warning("No tasks scheduled for today.")
    else:
        st.success(f"Generated today's schedule using '{strategy}' strategy.")
        st.table(
            [
                {
                    "Time": task.scheduled_time.strftime("%H:%M"),
                    "Pet": task.pet_name,
                    "Task": task.description,
                    "Priority": task.priority,
                    "Duration": f"{task.duration_minutes} min",
                    "Status": "✅" if task.completed else "⏳",
                }
                for task in schedule
            ]
        )

        conflicts = scheduler.detect_conflicts(schedule)
        if conflicts:
            for conflict in conflicts:
                st.warning(conflict)
        else:
            st.info("No conflicts detected.")

        with st.expander("Why this schedule was chosen"):
            for explanation in scheduler.explain_schedule(schedule):
                st.write(f"- {explanation}")

st.divider()

st.subheader("Next Available Slot Finder")
if all_tasks:
    desired_date = st.date_input("Desired date", value=datetime.now().date(), key="slot_date")
    desired_time = st.time_input(
        "Desired start time",
        value=time(hour=9, minute=0),
        key="slot_time",
    )
    desired_duration = st.number_input(
        "Desired task duration (minutes)",
        min_value=1,
        max_value=240,
        value=20,
        key="slot_duration",
    )

    if st.button("Find next available slot"):
        desired_dt = datetime.combine(desired_date, desired_time)
        slot = scheduler.find_next_available_slot(all_tasks, desired_dt, int(desired_duration))
        st.success(
            f"Next available {desired_duration}-minute slot starts at {slot.strftime('%Y-%m-%d %H:%M')}."
        )

st.divider()

col1, col2 = st.columns(2)

with col1:
    if st.button("Save data"):
        save_data()
        st.success("Data saved to JSON.")

with col2:
    if st.button("Reload saved data"):
        if os.path.exists(DATA_FILE):
            st.session_state.owner = Owner.load_from_json(DATA_FILE)
            st.success("Reloaded data from JSON. Refresh the page if needed.")
        else:
            st.warning("No saved data file found.")