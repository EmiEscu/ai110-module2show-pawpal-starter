from datetime import date
from pawpal_system import User, Pet, Task

# --- Create Owner ---
owner = User(
    userId="u1",
    name="Alex Rivera",
    email="alex@example.com",
    phone="555-0100",
)

# --- Create Pets ---
buddy = Pet(
    petId="p1",
    name="Buddy",
    age=4,
    gender="Male",
    breed="Golden Retriever",
    isAble=True,
    groomingNeeds="weekly brushing",
)

luna = Pet(
    petId="p2",
    name="Luna",
    age=2,
    gender="Female",
    breed="Beagle",
    isAble=True,
    groomingNeeds="monthly bath",
)

owner.addPet(buddy)
owner.addPet(luna)

# --- Create Tasks (different times via priority/duration) ---
today = date.today()

morning_walk = Task(
    taskId="t1",
    title="Morning Walk",
    category="exercise",
    durationMin=30,
    priority=3,
    status="pending",
    assignedPetId="p1",
    dueDate=today,
)

feeding = Task(
    taskId="t2",
    title="Breakfast Feeding",
    category="feeding",
    durationMin=10,
    priority=5,
    status="pending",
    assignedPetId="p2",
    dueDate=today,
)

medication = Task(
    taskId="t3",
    title="Flea & Tick Medication",
    category="health",
    durationMin=5,
    priority=4,
    status="pending",
    assignedPetId="p1",
    dueDate=today,
)

grooming = Task(
    taskId="t4",
    title="Brush & Groom",
    category="grooming",
    durationMin=20,
    priority=2,
    status="pending",
    assignedPetId="p2",
    dueDate=today,
)

owner.addTask(morning_walk)
owner.addTask(feeding)
owner.addTask(medication)
owner.addTask(grooming)

# --- Generate and Print Today's Schedule ---
plan = owner.generateDailyPlan()

print("=" * 45)
print("       PAWPAL+ — TODAY'S SCHEDULE")
print("=" * 45)
print(plan.getSummary())
print()
print("--- Scheduling Reasoning ---")
print(plan.getReasoning())
print("=" * 45)
