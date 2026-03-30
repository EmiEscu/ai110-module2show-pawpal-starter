from datetime import date, time
from typing import Dict, List, Optional


# Maps timeOfDay constraint strings to (start, end) time ranges (exclusive end).
_TIME_OF_DAY_RANGES: Dict[str, tuple] = {
    "morning": (time(6, 0), time(12, 0)),
    "afternoon": (time(12, 0), time(17, 0)),
    "evening": (time(17, 0), time(21, 0)),
}

# Default hour daily plans begin (8:00 AM).
PLAN_START_HOUR = 8


class Action:
    """Represents a subscription or service paid for a specific pet."""

    def __init__(
        self,
        actionId: str,
        petId: str,
        serviceName: str,
        serviceType: str,
        cost: float,
        frequency: str,
        startDate: date,
        endDate: Optional[date],
        status: str = "active",
    ) -> None:
        self.actionId = actionId
        self.petId = petId
        self.serviceName = serviceName
        self.serviceType = serviceType
        self.cost = cost
        self.frequency = frequency
        self.startDate = startDate
        self.endDate = endDate
        self.status = status

    def activate(self) -> None:
        self.status = "active"

    def cancel(self) -> None:
        self.status = "cancelled"

    def renew(self) -> None:
        self.status = "active"
        self.endDate = None

    def updateStatus(self, status: str) -> None:
        self.status = status

    def isActive(self) -> bool:
        """True if status is active and today falls within the action's date range."""
        if self.status != "active":
            return False
        today = date.today()
        if today < self.startDate:
            return False
        if self.endDate is not None and today > self.endDate:
            return False
        return True

    def isDueToday(self, targetDate: date) -> bool:
        """
        True if this action is due on targetDate based on its frequency.
        Supported frequencies: daily, weekly, monthly, one-time.
        """
        if not self.isActive():
            return False
        delta = (targetDate - self.startDate).days
        if delta < 0:
            return False
        freq = self.frequency.lower()
        if freq == "daily":
            return True
        if freq == "weekly":
            return delta % 7 == 0
        if freq == "monthly":
            return targetDate.day == self.startDate.day
        if freq == "one-time":
            return targetDate == self.startDate
        return False


class Task:
    """Represents an individual care activity assigned to a pet."""

    def __init__(
        self,
        taskId: str,
        title: str,
        category: str,
        durationMin: int,
        priority: int,
        status: str,
        assignedPetId: str,
        dueDate: Optional[date],
    ) -> None:
        self.taskId = taskId
        self.title = title
        self.category = category
        self.durationMin = durationMin
        self.priority = priority
        self.status = status
        self.assignedPetId = assignedPetId
        self.dueDate = dueDate

    def markComplete(self) -> None:
        self.status = "complete"

    def updatePriority(self, priority: int) -> None:
        self.priority = priority

    def updateDuration(self, durationMin: int) -> None:
        self.durationMin = durationMin

    def assignToPet(self, petId: str) -> None:
        self.assignedPetId = petId

    def getDetails(self) -> dict:
        return {
            "taskId": self.taskId,
            "title": self.title,
            "category": self.category,
            "durationMin": self.durationMin,
            "priority": self.priority,
            "status": self.status,
            "assignedPetId": self.assignedPetId,
            "dueDate": self.dueDate,
        }


class Constraint:
    """Represents a limitation or preference for a pet."""

    def __init__(
        self,
        constraintId: str,
        petId: str,
        constraintType: str,
        description: str,
        priority: int,
        maxDurationMin: Optional[int],
        timeOfDay: Optional[str],
    ) -> None:
        self.constraintId = constraintId
        self.petId = petId
        self.constraintType = constraintType
        self.description = description
        self.priority = priority
        self.maxDurationMin = maxDurationMin
        self.timeOfDay = timeOfDay

    def updateConstraint(self, **kwargs) -> None:
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def getPriority(self) -> int:
        return self.priority

    def isApplicable(
        self,
        task: Task,
        accumulated_min: int = 0,
        scheduled_time: Optional[time] = None,
    ) -> bool:
        """
        Returns True if this constraint blocks the given task.

        Checks:
          - maxDurationMin: blocks if the task alone exceeds the limit, OR if
            adding it would push the pet's accumulated scheduled time over the limit.
          - timeOfDay: blocks if scheduled_time falls outside the allowed window
            (morning / afternoon / evening). Skipped when scheduled_time is None.
        """
        if self.maxDurationMin is not None:
            if task.durationMin > self.maxDurationMin:
                return True
            if accumulated_min + task.durationMin > self.maxDurationMin:
                return True
        if self.timeOfDay is not None and scheduled_time is not None:
            allowed = _TIME_OF_DAY_RANGES.get(self.timeOfDay.lower())
            if allowed and not (allowed[0] <= scheduled_time < allowed[1]):
                return True
        return False


class Pet:
    """Represents a pet owned by a user."""

    def __init__(
        self,
        petId: str,
        name: str,
        age: int,
        gender: str,
        breed: str,
        isAble: bool,
        groomingNeeds: str,
    ) -> None:
        self.petId = petId
        self.name = name
        self.age = age
        self.gender = gender
        self.breed = breed
        self.isAble = isAble
        self.groomingNeeds = groomingNeeds
        self.medications: List[str] = []
        self.constraints: List[Constraint] = []
        self.actions: List[Action] = []

    def addInfo(self, **kwargs) -> None:
        for key, value in kwargs.items():
            setattr(self, key, value)

    def updateInfo(self, **kwargs) -> None:
        self.addInfo(**kwargs)

    def removeInfo(self, field: str) -> None:
        if hasattr(self, field):
            delattr(self, field)

    def addMedication(self, medication: str) -> None:
        if medication not in self.medications:
            self.medications.append(medication)

    def removeMedication(self, medication: str) -> None:
        self.medications = [m for m in self.medications if m != medication]

    def addAction(self, action: Action) -> None:
        self.actions.append(action)

    def removeAction(self, actionId: str) -> None:
        self.actions = [a for a in self.actions if a.actionId != actionId]

    def getActions(self) -> List[Action]:
        return list(self.actions)

    def addConstraint(self, constraint: Constraint) -> None:
        self.constraints.append(constraint)

    def getConstraints(self) -> List[Constraint]:
        return list(self.constraints)


class DailyPlan:
    """The output of the scheduling logic — a sorted, reasoned schedule for the day."""

    def __init__(self, date: date, userId: str) -> None:
        self.date = date
        self.userId = userId
        self.scheduledTasks: List[Task] = []
        self.scheduledStartTimes: Dict[str, time] = {}  # taskId -> clock start time
        self.totalDurationMin: int = 0
        self.reasoning: str = ""
        self._cursorMin: int = PLAN_START_HOUR * 60  # running clock in minutes from midnight

    def addTask(self, task: Task) -> None:
        start_h, start_m = divmod(self._cursorMin, 60)
        self.scheduledStartTimes[task.taskId] = time(start_h % 24, start_m)
        self.scheduledTasks.append(task)
        self.totalDurationMin += task.durationMin
        self._cursorMin += task.durationMin

    def removeTask(self, taskId: str) -> None:
        self.scheduledTasks = [t for t in self.scheduledTasks if t.taskId != taskId]
        self.scheduledStartTimes.pop(taskId, None)
        self.totalDurationMin = sum(t.durationMin for t in self.scheduledTasks)

    def reorder(self) -> None:
        """Re-sort scheduled tasks by priority and recompute start times."""
        self.scheduledTasks.sort(key=lambda t: t.priority, reverse=True)
        cursor = PLAN_START_HOUR * 60
        for task in self.scheduledTasks:
            start_h, start_m = divmod(cursor, 60)
            self.scheduledStartTimes[task.taskId] = time(start_h % 24, start_m)
            cursor += task.durationMin
        self._cursorMin = cursor

    def getSummary(self) -> str:
        if not self.scheduledTasks:
            return f"No tasks scheduled for {self.date}."
        lines = [f"Daily Plan — {self.date} ({self.totalDurationMin} min total):"]
        for task in self.scheduledTasks:
            start = self.scheduledStartTimes.get(task.taskId)
            start_str = start.strftime("%I:%M %p") if start else "?"
            lines.append(f"  {start_str}  {task.title} ({task.durationMin} min)")
        return "\n".join(lines)

    def getReasoning(self) -> str:
        return self.reasoning


class User:
    """Central class representing a PawPal+ user."""

    def __init__(
        self,
        userId: str,
        name: str,
        email: str,
        phone: str,
    ) -> None:
        self.userId = userId
        self.name = name
        self.email = email
        self.phone = phone
        self.pets: List[Pet] = []
        self.taskList: List[Task] = []

    def addPet(self, pet: Pet) -> None:
        self.pets.append(pet)

    def removePet(self, petId: str) -> None:
        """Remove the pet and cascade-delete all tasks assigned to it."""
        self.pets = [p for p in self.pets if p.petId != petId]
        self.taskList = [t for t in self.taskList if t.assignedPetId != petId]

    def getPets(self) -> List[Pet]:
        return list(self.pets)

    def addTask(self, task: Task) -> None:
        self.taskList.append(task)

    def removeTask(self, taskId: str) -> None:
        self.taskList = [t for t in self.taskList if t.taskId != taskId]

    def getTasks(self) -> List[Task]:
        return list(self.taskList)

    def getPetById(self, petId: str) -> Optional[Pet]:
        """Look up a pet by ID. Used internally to resolve Task.assignedPetId."""
        for pet in self.pets:
            if pet.petId == petId:
                return pet
        return None

    # --- Private scheduling helpers ---

    def _getPendingTasks(self, targetDate: date) -> List[Task]:
        """Return tasks that are not yet complete and are due on or before targetDate."""
        return [
            task for task in self.taskList
            if task.status != "complete"
            and (task.dueDate is None or task.dueDate <= targetDate)
        ]

    def _applyConstraints(self, tasks: List[Task]) -> List[Task]:
        """
        Filter out tasks blocked by their pet's constraints.
        Tracks accumulated scheduled minutes per pet so maxDurationMin
        is evaluated against the running total, not just the individual task.
        Also passes the task's projected start time so timeOfDay constraints
        can be enforced.
        """
        eligible: List[Task] = []
        pet_accumulated: Dict[str, int] = {}  # petId -> total minutes already scheduled

        # Compute the projected start time for the next task based on cursor.
        cursor_min = PLAN_START_HOUR * 60

        for task in tasks:
            pet = self.getPetById(task.assignedPetId)
            start_h, start_m = divmod(cursor_min, 60)
            scheduled_time = time(start_h % 24, start_m)

            if pet is None:
                eligible.append(task)
                cursor_min += task.durationMin
                continue

            accumulated = pet_accumulated.get(task.assignedPetId, 0)
            blocked = any(
                c.isApplicable(task, accumulated_min=accumulated, scheduled_time=scheduled_time)
                for c in pet.constraints
            )
            if not blocked:
                eligible.append(task)
                pet_accumulated[task.assignedPetId] = accumulated + task.durationMin
                cursor_min += task.durationMin

        return eligible

    def _sortByPriority(self, tasks: List[Task]) -> List[Task]:
        """Sort tasks descending by priority (higher number = scheduled first)."""
        return sorted(tasks, key=lambda t: t.priority, reverse=True)

    def _buildReasoning(self, tasks: List[Task]) -> str:
        """Produce a human-readable explanation of why tasks were ordered this way."""
        if not tasks:
            return "No tasks scheduled for today."
        lines = ["Tasks ordered by priority (highest first):"]
        for i, task in enumerate(tasks, 1):
            pet = self.getPetById(task.assignedPetId)
            pet_label = pet.name if pet else task.assignedPetId
            lines.append(
                f"  {i}. [Priority {task.priority}] {task.title} "
                f"for {pet_label} ({task.durationMin} min)"
            )
        return "\n".join(lines)

    def generateDailyPlan(self) -> DailyPlan:
        """
        Generate a DailyPlan for today by:
          1. Collecting pending tasks due today or earlier
          2. Sorting by priority so high-priority tasks are evaluated first
          3. Filtering out tasks blocked by pet constraints (with time + duration context)
          4. Building the plan with real clock-based start times
          5. Recording reasoning for the final order
        """
        today = date.today()
        plan = DailyPlan(today, self.userId)

        pending = self._getPendingTasks(today)
        sorted_pending = self._sortByPriority(pending)   # sort before constraint pass
        eligible = self._applyConstraints(sorted_pending)

        for task in eligible:
            plan.addTask(task)

        plan.reasoning = self._buildReasoning(eligible)
        return plan
