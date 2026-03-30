from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any
import json


PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}
PRIORITY_WEIGHT = {"high": 3, "medium": 2, "low": 1}


@dataclass
class Task:
    """Represents a pet care task."""

    description: str
    scheduled_time: datetime
    frequency: str  # "once", "daily", "weekly"
    duration_minutes: int
    priority: str  # "low", "medium", "high"
    pet_name: str = ""
    completed: bool = False

    def mark_complete(self) -> Optional["Task"]:
        """Mark task complete and return the next recurring task if needed."""
        self.completed = True

        if self.frequency == "daily":
            return Task(
                description=self.description,
                scheduled_time=self.scheduled_time + timedelta(days=1),
                frequency=self.frequency,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                pet_name=self.pet_name,
            )

        if self.frequency == "weekly":
            return Task(
                description=self.description,
                scheduled_time=self.scheduled_time + timedelta(weeks=1),
                frequency=self.frequency,
                duration_minutes=self.duration_minutes,
                priority=self.priority,
                pet_name=self.pet_name,
            )

        return None

    def reschedule(self, new_time: datetime) -> None:
        """Update the scheduled time for the task."""
        self.scheduled_time = new_time

    def is_due_today(self) -> bool:
        """Return whether the task is scheduled for today."""
        return self.scheduled_time.date() == datetime.now().date()

    def end_time(self) -> datetime:
        """Return the end time based on duration."""
        return self.scheduled_time + timedelta(minutes=self.duration_minutes)

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the task to a dictionary."""
        return {
            "description": self.description,
            "scheduled_time": self.scheduled_time.isoformat(),
            "frequency": self.frequency,
            "duration_minutes": self.duration_minutes,
            "priority": self.priority,
            "pet_name": self.pet_name,
            "completed": self.completed,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Task":
        """Create a Task from a dictionary."""
        return cls(
            description=data["description"],
            scheduled_time=datetime.fromisoformat(data["scheduled_time"]),
            frequency=data["frequency"],
            duration_minutes=data["duration_minutes"],
            priority=data["priority"],
            pet_name=data.get("pet_name", ""),
            completed=data.get("completed", False),
        )


@dataclass
class Pet:
    """Represents a pet owned by the user."""

    name: str
    species: str
    care_notes: str = ""
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Add a task to this pet."""
        task.pet_name = self.name
        self.tasks.append(task)

    def remove_task(self, task: Task) -> None:
        """Remove a task from this pet."""
        if task in self.tasks:
            self.tasks.remove(task)

    def get_tasks(self) -> List[Task]:
        """Return all tasks for this pet."""
        return self.tasks

    def list_incomplete_tasks(self) -> List[Task]:
        """Return only incomplete tasks for this pet."""
        return [task for task in self.tasks if not task.completed]

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the pet to a dictionary."""
        return {
            "name": self.name,
            "species": self.species,
            "care_notes": self.care_notes,
            "tasks": [task.to_dict() for task in self.tasks],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Pet":
        """Create a Pet from a dictionary."""
        pet = cls(
            name=data["name"],
            species=data["species"],
            care_notes=data.get("care_notes", ""),
        )
        pet.tasks = [Task.from_dict(task_data) for task_data in data.get("tasks", [])]
        return pet


@dataclass
class Owner:
    """Represents the owner who manages multiple pets."""

    name: str
    available_minutes: int = 180
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to the owner."""
        self.pets.append(pet)

    def get_all_tasks(self) -> List[Task]:
        """Return all tasks across all pets."""
        all_tasks: List[Task] = []
        for pet in self.pets:
            all_tasks.extend(pet.get_tasks())
        return all_tasks

    def find_pet(self, pet_name: str) -> Optional[Pet]:
        """Find a pet by name."""
        for pet in self.pets:
            if pet.name.lower() == pet_name.lower():
                return pet
        return None

    def save_to_json(self, filename: str) -> None:
        """Save owner, pets, and tasks to JSON."""
        data = {
            "name": self.name,
            "available_minutes": self.available_minutes,
            "pets": [pet.to_dict() for pet in self.pets],
        }
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)

    @classmethod
    def load_from_json(cls, filename: str) -> "Owner":
        """Load owner, pets, and tasks from JSON."""
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)

        owner = cls(
            name=data["name"],
            available_minutes=data.get("available_minutes", 180),
        )
        owner.pets = [Pet.from_dict(pet_data) for pet_data in data.get("pets", [])]
        return owner


class Scheduler:
    """Generates, sorts, filters, validates, and explains schedules."""

    def get_todays_tasks(self, owner: Owner) -> List[Task]:
        """Return tasks scheduled for today across all pets."""
        return [task for task in owner.get_all_tasks() if task.is_due_today()]

    def sort_tasks_by_time(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by scheduled time."""
        return sorted(tasks, key=lambda task: task.scheduled_time)

    def sort_tasks_by_priority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks by priority, then by time."""
        return sorted(
            tasks,
            key=lambda task: (
                PRIORITY_ORDER.get(task.priority.lower(), 99),
                task.scheduled_time,
            ),
        )

    def filter_tasks(
        self,
        tasks: List[Task],
        pet_name: Optional[str] = None,
        completed: Optional[bool] = None,
        priority: Optional[str] = None,
    ) -> List[Task]:
        """Filter tasks by pet name, completion status, and/or priority."""
        filtered = tasks

        if pet_name is not None:
            filtered = [task for task in filtered if task.pet_name.lower() == pet_name.lower()]

        if completed is not None:
            filtered = [task for task in filtered if task.completed == completed]

        if priority is not None:
            filtered = [task for task in filtered if task.priority.lower() == priority.lower()]

        return filtered

    def detect_conflicts(self, tasks: List[Task]) -> List[str]:
        """Detect overlapping tasks and return warning messages."""
        warnings: List[str] = []
        sorted_tasks = self.sort_tasks_by_time(tasks)

        for i in range(len(sorted_tasks)):
            for j in range(i + 1, len(sorted_tasks)):
                task_a = sorted_tasks[i]
                task_b = sorted_tasks[j]

                overlap = task_a.scheduled_time < task_b.end_time() and task_b.scheduled_time < task_a.end_time()

                if overlap:
                    warnings.append(
                        f"Conflict: '{task_a.description}' for {task_a.pet_name} overlaps with "
                        f"'{task_b.description}' for {task_b.pet_name}."
                    )

        return warnings

    def generate_schedule(self, owner: Owner, strategy: str = "time") -> List[Task]:
        """Generate today's schedule using a chosen strategy."""
        tasks = self.get_todays_tasks(owner)

        if strategy == "priority":
            return self.sort_tasks_by_priority(tasks)

        if strategy == "weighted":
            return self.weighted_schedule(tasks)

        return self.sort_tasks_by_time(tasks)

    def weighted_schedule(self, tasks: List[Task]) -> List[Task]:
        """Prioritize tasks using priority and urgency together."""
        now = datetime.now()

        def score(task: Task) -> tuple:
            hours_until = max((task.scheduled_time - now).total_seconds() / 3600, 0)
            urgency_bucket = 0 if hours_until <= 2 else 1 if hours_until <= 6 else 2
            return (-PRIORITY_WEIGHT.get(task.priority.lower(), 0), urgency_bucket, task.scheduled_time)

        return sorted(tasks, key=score)

    def find_next_available_slot(
        self,
        tasks: List[Task],
        desired_start: datetime,
        duration_minutes: int,
    ) -> datetime:
        """Find the next non-overlapping slot after the desired start time."""
        sorted_tasks = self.sort_tasks_by_time(tasks)
        candidate = desired_start
        proposed_end = candidate + timedelta(minutes=duration_minutes)

        for task in sorted_tasks:
            if proposed_end <= task.scheduled_time:
                return candidate

            if candidate < task.end_time() and proposed_end > task.scheduled_time:
                candidate = task.end_time()
                proposed_end = candidate + timedelta(minutes=duration_minutes)

        return candidate

    def explain_schedule(self, tasks: List[Task]) -> List[str]:
        """Explain why each task appears in the schedule."""
        explanations = []
        for task in tasks:
            explanations.append(
                f"{task.description} for {task.pet_name} is scheduled at "
                f"{task.scheduled_time.strftime('%H:%M')} because it is a "
                f"{task.priority}-priority {task.frequency} task lasting "
                f"{task.duration_minutes} minutes."
            )
        return explanations

    def complete_task_for_pet(self, pet: Pet, task: Task) -> Optional[Task]:
        """Complete a task and add the next recurring task if needed."""
        next_task = task.mark_complete()
        if next_task is not None:
            pet.add_task(next_task)
        return next_task