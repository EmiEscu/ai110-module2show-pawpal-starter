import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from pawpal_system import Task, Pet, User


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
