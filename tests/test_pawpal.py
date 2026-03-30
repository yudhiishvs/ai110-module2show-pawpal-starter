from datetime import datetime, timedelta
from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task("Feed Buddy", datetime.now(), "once", 10, "high")
    task.mark_complete()
    assert task.completed is True


def test_add_task_to_pet_increases_task_count():
    pet = Pet("Buddy", "Dog")
    task = Task("Walk Buddy", datetime.now(), "daily", 30, "medium")

    before = len(pet.get_tasks())
    pet.add_task(task)
    after = len(pet.get_tasks())

    assert after == before + 1


def test_sort_tasks_by_time_returns_chronological_order():
    scheduler = Scheduler()
    now = datetime.now()

    task1 = Task("Task 1", now + timedelta(hours=3), "once", 10, "low")
    task2 = Task("Task 2", now + timedelta(hours=1), "once", 10, "high")
    task3 = Task("Task 3", now + timedelta(hours=2), "once", 10, "medium")

    result = scheduler.sort_tasks_by_time([task1, task2, task3])

    assert result == [task2, task3, task1]


def test_filter_tasks_by_pet_name():
    scheduler = Scheduler()
    now = datetime.now()

    task1 = Task("Feed Buddy", now, "once", 10, "high", pet_name="Buddy")
    task2 = Task("Feed Whiskers", now, "once", 10, "high", pet_name="Whiskers")

    result = scheduler.filter_tasks([task1, task2], pet_name="Buddy")

    assert len(result) == 1
    assert result[0].pet_name == "Buddy"


def test_daily_recurrence_creates_new_task_for_next_day():
    task = Task("Feed Buddy", datetime.now(), "daily", 10, "high", pet_name="Buddy")

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.scheduled_time.date() == (task.scheduled_time + timedelta(days=1)).date()


def test_conflict_detection_finds_overlapping_tasks():
    scheduler = Scheduler()
    start = datetime.now().replace(second=0, microsecond=0)

    task1 = Task("Walk Buddy", start, "once", 30, "medium", pet_name="Buddy")
    task2 = Task("Medicine", start + timedelta(minutes=10), "once", 10, "high", pet_name="Whiskers")

    conflicts = scheduler.detect_conflicts([task1, task2])

    assert len(conflicts) == 1
    assert "overlaps" in conflicts[0]


def test_owner_save_and_load_json(tmp_path):
    filename = tmp_path / "pawpal.json"

    owner = Owner("Jordan")
    pet = Pet("Buddy", "Dog")
    task = Task("Feed Buddy", datetime.now(), "daily", 10, "high")
    pet.add_task(task)
    owner.add_pet(pet)

    owner.save_to_json(str(filename))
    loaded = Owner.load_from_json(str(filename))

    assert loaded.name == "Jordan"
    assert len(loaded.pets) == 1
    assert loaded.pets[0].name == "Buddy"
    assert len(loaded.pets[0].tasks) == 1
