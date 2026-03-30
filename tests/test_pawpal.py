import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from datetime import date, timedelta, time
from pawpal_system import Task, Pet, User, DailyPlan, Scheduler


def test_mark_complete_changes_status():
    """Task completion: verify that mark_complete() changes the task's status to 'complete'."""
    task = Task(
        taskId="t1",
        title="Morning Walk",
        category="exercise",
        durationMin=30,
        priority=3,
        status="pending",
        assignedPetId="p1",
        dueDate=None,
    )

    assert task.status == "pending"
    task.markComplete()
    assert task.status == "complete"


def test_add_task_increases_pet_task_count():
    """Task addition: verify that adding a task to a Pet (via User) increases that pet's task count."""
    user = User(userId="u1", name="Alex", email="alex@example.com", phone="555-0100")
    pet = Pet(petId="p1", name="Buddy", age=3, gender="male", breed="Labrador", isAble=True, groomingNeeds="low")
    user.addPet(pet)

    assert len(user.getTasks()) == 0

    task = Task(
        taskId="t2",
        title="Feeding",
        category="nutrition",
        durationMin=10,
        priority=5,
        status="pending",
        assignedPetId="p1",
        dueDate=None,
    )
    user.addTask(task)

    pet_tasks = [t for t in user.getTasks() if t.assignedPetId == pet.petId]
    assert len(pet_tasks) == 1


def test_sort_by_time_returns_chronological_order():
    """Sorting correctness: verify _sortByTime returns tasks in ascending time order."""
    user = User(userId="u1", name="Alex", email="alex@example.com", phone="555-0100")

    tasks = [
        Task(taskId="t1", title="Evening Walk", category="exercise", durationMin=30,
             priority=1, status="pending", assignedPetId="p1", dueDate=None, time="17:00"),
        Task(taskId="t2", title="Morning Meds", category="health", durationMin=5,
             priority=2, status="pending", assignedPetId="p1", dueDate=None, time="08:00"),
        Task(taskId="t3", title="Afternoon Feed", category="nutrition", durationMin=10,
             priority=3, status="pending", assignedPetId="p1", dueDate=None, time="12:30"),
    ]

    sorted_tasks = Scheduler(user).sortByTime(tasks)

    assert sorted_tasks[0].time == "08:00"
    assert sorted_tasks[1].time == "12:30"
    assert sorted_tasks[2].time == "17:00"


def test_daily_task_recurrence_creates_next_day_task():
    """Recurrence logic: completing a daily task produces a new task due tomorrow."""
    user = User(userId="u1", name="Alex", email="alex@example.com", phone="555-0100")

    original = Task(
        taskId="t1",
        title="Morning Walk",
        category="exercise",
        durationMin=30,
        priority=3,
        status="pending",
        assignedPetId="p1",
        dueDate=date.today(),
        frequency="daily",
    )
    user.addTask(original)

    next_task = user.completeTask("t1")

    assert original.status == "complete"
    assert next_task is not None
    assert next_task.dueDate == date.today() + timedelta(days=1)
    assert next_task.frequency == "daily"
    assert next_task.status == "pending"
    # The new task should be present in the user's task list
    assert any(t.taskId == next_task.taskId for t in user.getTasks())


def test_detect_conflicts_flags_overlapping_tasks():
    """Conflict detection: DailyPlan.detectConflicts flags tasks scheduled at the same time."""
    plan = DailyPlan(date=date.today(), userId="u1")

    # Both tasks get the same manual start time by injecting them directly
    task_a = Task(taskId="a1", title="Walk", category="exercise", durationMin=30,
                  priority=5, status="pending", assignedPetId="p1", dueDate=None)
    task_b = Task(taskId="b1", title="Feeding", category="nutrition", durationMin=15,
                  priority=5, status="pending", assignedPetId="p1", dueDate=None)

    # Pin both tasks to 08:00 so their windows overlap
    plan.scheduledTasks = [task_a, task_b]
    plan.scheduledStartTimes = {
        "a1": time(8, 0),
        "b1": time(8, 0),
    }

    conflicts = plan.detectConflicts()

    assert len(conflicts) > 0
    assert any("Walk" in c and "Feeding" in c for c in conflicts)
