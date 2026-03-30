from datetime import date, time
from pawpal_system import User, Pet, Task, DailyPlan, Scheduler

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

# --- Create Tasks OUT OF ORDER (intentionally scrambled times) ---
today = date.today()

# Added last but scheduled earliest — tests that sort_by_time overrides insertion order
evening_play = Task(
    taskId="t5",
    title="Evening Playtime",
    category="enrichment",
    durationMin=15,
    priority=2,
    status="pending",
    assignedPetId="p2",
    dueDate=today,
    time="18:00",
)

# Middle of the day
afternoon_walk = Task(
    taskId="t6",
    title="Afternoon Walk",
    category="exercise",
    durationMin=25,
    priority=3,
    status="complete",   # complete — used to test status filter
    assignedPetId="p1",
    dueDate=today,
    time="13:30",
)

# Earliest in the day but added third
morning_walk = Task(
    taskId="t1",
    title="Morning Walk",
    category="exercise",
    durationMin=30,
    priority=3,
    status="pending",
    assignedPetId="p1",
    dueDate=today,
    time="08:00",
)

# No time set — should sort to the end
grooming = Task(
    taskId="t4",
    title="Brush & Groom",
    category="grooming",
    durationMin=20,
    priority=2,
    status="pending",
    assignedPetId="p2",
    dueDate=today,
    time=None,
)

# Late morning
medication = Task(
    taskId="t3",
    title="Flea & Tick Medication",
    category="health",
    durationMin=5,
    priority=4,
    status="pending",
    assignedPetId="p1",
    dueDate=today,
    time="10:45",
)

# Early morning but added last
feeding = Task(
    taskId="t2",
    title="Breakfast Feeding",
    category="feeding",
    durationMin=10,
    priority=5,
    status="pending",
    assignedPetId="p2",
    dueDate=today,
    time="07:30",
)

# Add tasks in scrambled order to prove sorting works
owner.addTask(evening_play)
owner.addTask(afternoon_walk)
owner.addTask(morning_walk)
owner.addTask(grooming)
owner.addTask(medication)
owner.addTask(feeding)

# --- Generate and Print Today's Schedule ---
plan = owner.generateDailyPlan()

print("=" * 48)
print("        PAWPAL+ — TODAY'S SCHEDULE")
print("=" * 48)
print(plan.getSummary())
print()
print("--- Scheduling Reasoning ---")
print(plan.getReasoning())
print("=" * 48)

# --- Demonstrate _sortByTime ---
all_tasks = owner.getTasks()
sorted_by_time = Scheduler(owner).sortByTime(all_tasks)

print()
print("=" * 48)
print("   SORT BY TIME (all tasks, chronological)")
print("=" * 48)
for task in sorted_by_time:
    time_label = task.time if task.time is not None else "No time set"
    print(f"  {time_label}  |  {task.title}  [{task.status}]")

# --- Demonstrate filterTasks: by status ---
print()
print("=" * 48)
print("   FILTER — Pending tasks only")
print("=" * 48)
pending_tasks = owner.filterTasks(status="pending")
for task in pending_tasks:
    print(f"  [{task.status}]  {task.title}  (pet id: {task.assignedPetId})")

print()
print("=" * 48)
print("   FILTER — Completed tasks only")
print("=" * 48)
completed_tasks = owner.filterTasks(status="complete")
for task in completed_tasks:
    print(f"  [{task.status}]  {task.title}  (pet id: {task.assignedPetId})")

# --- Demonstrate filterTasks: by pet name ---
print()
print("=" * 48)
print("   FILTER — Tasks for Buddy")
print("=" * 48)
buddy_tasks = owner.filterTasks(petName="Buddy")
for task in buddy_tasks:
    print(f"  {task.title}  [{task.status}]  @ {task.time or 'No time set'}")

print()
print("=" * 48)
print("   FILTER — Tasks for Luna")
print("=" * 48)
luna_tasks = owner.filterTasks(petName="Luna")
for task in luna_tasks:
    print(f"  {task.title}  [{task.status}]  @ {task.time or 'No time set'}")

# --- Demonstrate filterTasks: combined (status + pet name) ---
print()
print("=" * 48)
print("   FILTER — Pending tasks for Buddy (combined)")
print("=" * 48)
buddy_pending = owner.filterTasks(status="pending", petName="Buddy")
for task in buddy_pending:
    print(f"  {task.title}  [{task.status}]  @ {task.time or 'No time set'}")

print()
print("=" * 48)

# -------------------------------------------------------
# CONFLICT DETECTION — manually build a plan with tasks
# that start at overlapping times to verify the scheduler
# catches and reports the collision.
#
# NOTE: generateDailyPlan() schedules tasks sequentially
# (no gaps), so overlaps only occur when a plan is built
# or edited by hand — exactly what detectConflicts() guards
# against.
# -------------------------------------------------------

print("   CONFLICT DETECTION TEST")
print("=" * 48)

conflict_plan = DailyPlan(today, "u1")

# Buddy: 60-min morning walk starting at 08:00 → ends 09:00
long_walk = Task(
    taskId="c1",
    title="Long Morning Walk",
    category="exercise",
    durationMin=60,
    priority=3,
    status="pending",
    assignedPetId="p1",
    dueDate=today,
)

# Luna: 20-min feeding starting at 08:30 → ends 08:50 (overlaps walk)
early_feed = Task(
    taskId="c2",
    title="Breakfast Feeding",
    category="feeding",
    durationMin=20,
    priority=5,
    status="pending",
    assignedPetId="p2",
    dueDate=today,
)

# Buddy: 45-min grooming starting at 08:45 → ends 09:30 (overlaps both)
overlap_groom = Task(
    taskId="c3",
    title="Full Grooming Session",
    category="grooming",
    durationMin=45,
    priority=2,
    status="pending",
    assignedPetId="p1",
    dueDate=today,
)

# Manually assign overlapping start times to the plan
conflict_plan.scheduledTasks = [long_walk, early_feed, overlap_groom]
conflict_plan.scheduledStartTimes = {
    "c1": time(8, 0),   # 08:00 – 09:00
    "c2": time(8, 30),  # 08:30 – 08:50  ← overlaps c1
    "c3": time(8, 45),  # 08:45 – 09:30  ← overlaps both c1 and c2
}
conflict_plan.totalDurationMin = sum(t.durationMin for t in conflict_plan.scheduledTasks)

conflict_plan.conflicts = conflict_plan.detectConflicts()

print(conflict_plan.getSummary())
print()
print("=" * 48)
