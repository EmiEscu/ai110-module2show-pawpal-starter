import uuid
import streamlit as st
from pawpal_system import User, Pet, Task, Scheduler

st.set_page_config(page_title="PawPal+", page_icon="🐾", layout="centered")

st.title("🐾 PawPal+")

# ---------------------------------------------------------------------------
# Owner vault — persists User instances across Streamlit re-runs within the
# same browser session.  Keyed by owner name so returning users resume their
# existing object instead of getting a blank one.
# ---------------------------------------------------------------------------
if "owner_vault" not in st.session_state:
    st.session_state.owner_vault = {}   # { owner_name: User }

if "current_owner_key" not in st.session_state:
    st.session_state.current_owner_key = None


def get_or_create_owner(name: str, email: str, phone: str) -> User:
    """Return the existing User from the vault, or create and store a new one."""
    vault = st.session_state.owner_vault
    if name in vault:
        return vault[name]
    new_owner = User(userId=str(uuid.uuid4()), name=name, email=email, phone=phone)
    vault[name] = new_owner
    return new_owner


# ---------------------------------------------------------------------------
# Owner / pet setup
# ---------------------------------------------------------------------------
st.subheader("Owner Profile")

col_a, col_b = st.columns(2)
with col_a:
    owner_name = st.text_input("Owner name", value="Jordan")
with col_b:
    owner_email = st.text_input("Email", value="jordan@example.com")

owner_phone = st.text_input("Phone", value="555-0100")

if st.button("Load / Create Profile"):
    owner = get_or_create_owner(owner_name, owner_email, owner_phone)
    st.session_state.current_owner_key = owner_name
    if len(owner.getPets()) == 0:
        # First time — seed the pet from the inputs below (collected after this block,
        # so we use defaults here; user can update via the pet section).
        st.info(f"New profile created for **{owner_name}**. Add a pet below.")
    else:
        st.success(
            f"Welcome back, **{owner.name}**! "
            f"Loaded {len(owner.getPets())} pet(s) and {len(owner.getTasks())} task(s)."
        )

# Resolve active owner (None if profile has not been loaded yet)
current_owner: User | None = (
    st.session_state.owner_vault.get(st.session_state.current_owner_key)
    if st.session_state.current_owner_key
    else None
)

st.divider()

# ---------------------------------------------------------------------------
# Pet setup (only shown once an owner profile is active)
# ---------------------------------------------------------------------------
st.subheader("Pet Info")

pet_name = st.text_input("Pet name", value="Mochi")
species   = st.selectbox("Species", ["dog", "cat", "other"])

if st.button("Add Pet") and current_owner is not None:
    existing_names = {p.name for p in current_owner.getPets()}
    if pet_name in existing_names:
        st.warning(f"**{pet_name}** is already registered to {current_owner.name}.")
    else:
        new_pet = Pet(
            petId=str(uuid.uuid4()),
            name=pet_name,
            age=0,
            gender="unknown",
            breed=species,
            isAble=True,
            groomingNeeds="standard",
        )
        current_owner.addPet(new_pet)
        st.success(f"Added **{pet_name}** to {current_owner.name}'s profile.")
elif st.session_state.current_owner_key is None:
    st.caption("Load a profile first to add pets.")

if current_owner and current_owner.getPets():
    st.write("Registered pets:", ", ".join(p.name for p in current_owner.getPets()))

st.divider()

# ---------------------------------------------------------------------------
# Task management
# ---------------------------------------------------------------------------
st.subheader("Tasks")
st.caption("Tasks are stored on the owner object and survive Streamlit re-runs.")

col1, col2, col3 = st.columns(3)
with col1:
    task_title = st.text_input("Task title", value="Morning walk")
with col2:
    duration = st.number_input("Duration (minutes)", min_value=1, max_value=240, value=20)
with col3:
    priority = st.selectbox("Priority", ["low", "medium", "high"], index=2)

_PRIORITY_MAP = {"low": 1, "medium": 2, "high": 3}

# Pet selector for task assignment
pet_options = (
    {p.name: p.petId for p in current_owner.getPets()} if current_owner else {}
)
assigned_pet_label = st.selectbox(
    "Assign to pet",
    options=list(pet_options.keys()) if pet_options else ["(load a profile first)"],
)

if st.button("Add Task"):
    if current_owner is None:
        st.warning("Load a profile before adding tasks.")
    elif not pet_options:
        st.warning("Add a pet before adding tasks.")
    else:
        new_task = Task(
            taskId=str(uuid.uuid4()),
            title=task_title,
            category="general",
            durationMin=int(duration),
            priority=_PRIORITY_MAP[priority],
            status="pending",
            assignedPetId=pet_options[assigned_pet_label],
            dueDate=None,
        )
        current_owner.addTask(new_task)
        st.success(f"Task **{task_title}** added.")

# Display tasks from the owner object, sorted by priority via Scheduler
if current_owner:
    tasks = current_owner.getTasks()
    if tasks:
        scheduler = Scheduler(current_owner)
        sorted_tasks = scheduler.sortByPriority(tasks)

        _PRIORITY_LABEL = {1: "Low", 2: "Medium", 3: "High"}
        pet_id_to_name = {p.petId: p.name for p in current_owner.getPets()}

        rows = []
        for t in sorted_tasks:
            rows.append({
                "Title": t.title,
                "Pet": pet_id_to_name.get(t.assignedPetId, t.assignedPetId),
                "Priority": _PRIORITY_LABEL.get(t.priority, str(t.priority)),
                "Duration (min)": t.durationMin,
                "Status": t.status.capitalize(),
                "Due Date": str(t.dueDate) if t.dueDate else "—",
            })

        st.write("Current tasks (sorted by priority):")
        st.dataframe(rows, use_container_width=True)
    else:
        st.info("No tasks yet. Add one above.")
else:
    st.info("Load a profile to see tasks.")

st.divider()

# ---------------------------------------------------------------------------
# Schedule generation
# ---------------------------------------------------------------------------
st.subheader("Build Schedule")

if st.button("Generate Schedule"):
    if current_owner is None:
        st.warning("Load a profile first.")
    elif not current_owner.getTasks():
        st.warning("Add at least one task before generating a schedule.")
    else:
        plan = current_owner.generateDailyPlan()
        pet_id_to_name = {p.petId: p.name for p in current_owner.getPets()}

        # ── Conflict warnings ──────────────────────────────────────────────
        if plan.conflicts:
            st.error(
                f"**{len(plan.conflicts)} scheduling conflict(s) detected.** "
                "Review and adjust task times or durations before following this plan."
            )
            for raw_msg in plan.conflicts:
                # Replace petId tokens with human-readable pet names
                friendly = raw_msg
                for pid, pname in pet_id_to_name.items():
                    friendly = friendly.replace(f"pet: {pid}", f"pet: {pname}")
                st.warning(friendly.strip())
        else:
            st.success(f"Schedule generated for {plan.date} — no conflicts found!")

        # ── Scheduled task table ───────────────────────────────────────────
        if plan.scheduledTasks:
            _PRIORITY_LABEL = {1: "Low", 2: "Medium", 3: "High"}
            schedule_rows = []
            for task in plan.scheduledTasks:
                start = plan.scheduledStartTimes.get(task.taskId)
                schedule_rows.append({
                    "Time": start.strftime("%I:%M %p") if start else "—",
                    "Task": task.title,
                    "Pet": pet_id_to_name.get(task.assignedPetId, task.assignedPetId),
                    "Priority": _PRIORITY_LABEL.get(task.priority, str(task.priority)),
                    "Duration (min)": task.durationMin,
                })
            st.table(schedule_rows)
        else:
            st.info("No tasks could be scheduled — check pet constraints.")

        with st.expander("Scheduling reasoning"):
            st.text(plan.getReasoning())
