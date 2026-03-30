# PawPal+ (Module 2 Project)

PawPal+ is a Streamlit app that helps a busy pet owner plan and manage pet care tasks. The system uses object-oriented design to organize pets, tasks, and scheduling logic, then generates a daily plan that can be viewed in both a CLI demo and a Streamlit interface.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks such as walks, feeding, meds, enrichment, and grooming
- Consider constraints such as time available, priority, and owner preferences
- Produce a daily plan and explain why it chose that plan

## What this app does

The final app allows a user to:

- Enter basic owner and pet information
- Add pet care tasks with a time, duration, priority, and frequency
- Generate a daily schedule across multiple pets
- View the schedule clearly in the Streamlit app
- See warnings when tasks conflict
- View explanations for why tasks appear in the generated plan
- Run a CLI demo to verify the backend logic
- Run automated tests for key scheduling behavior

## Core Classes

The system is built around four main classes:

### `Task`
Represents an individual pet care task.

Stores:
- description
- scheduled time
- frequency
- duration
- priority
- pet name
- completion status

Key methods:
- `mark_complete()`
- `reschedule()`
- `is_due_today()`

### `Pet`
Represents a pet owned by the user.

Stores:
- pet name
- species
- care notes
- list of tasks

Key methods:
- `add_task()`
- `remove_task()`
- `get_tasks()`

### `Owner`
Represents the owner using the app.

Stores:
- owner name
- available minutes
- list of pets

Key methods:
- `add_pet()`
- `get_all_tasks()`
- `find_pet()`

### `Scheduler`
Handles the planning logic across all pets.

Key methods:
- `get_todays_tasks()`
- `sort_tasks_by_time()`
- `sort_tasks_by_priority()`
- `filter_tasks()`
- `detect_conflicts()`
- `generate_schedule()`
- `explain_schedule()`
- `complete_task_for_pet()`

## Algorithmic Features

PawPal+ includes several scheduling features:

- **Sort by time**  
  Orders tasks chronologically for the day.

- **Sort by priority**  
  Orders tasks by priority before time.

- **Filtering**  
  Filters tasks by pet name, completion status, or priority.

- **Conflict detection**  
  Detects overlapping task times and warns the user.

- **Recurring tasks**  
  Completing a daily or weekly task automatically creates the next occurrence.

- **Weighted scheduling**  
  Uses both priority and urgency to produce a smarter schedule.

- **Next available slot finder**  
  Finds the next non-overlapping time block for a new task.

## Project Structure

```text
PawPal+/
├── app.py
├── main.py
├── pawpal_system.py
├── README.md
├── reflection.md
├── requirements.txt
├── uml_final.png
└── tests/
    └── test_pawpal.py
