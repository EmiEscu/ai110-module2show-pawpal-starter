from datetime import date
from typing import List, Optional


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
        status: str,
        startDate: date,
        endDate: Optional[date],
    ) -> None:
        self.actionId = actionId
        self.petId = petId
        self.serviceName = serviceName
        self.serviceType = serviceType
        self.cost = cost
        self.frequency = frequency
        self.status = status
        self.startDate = startDate
        self.endDate = endDate

    def activate(self) -> None:
        pass

    def cancel(self) -> None:
        pass

    def renew(self) -> None:
        pass

    def updateStatus(self, status: str) -> None:
        pass

    def isActive(self) -> bool:
        pass


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
        pass

    def updatePriority(self, priority: int) -> None:
        pass

    def updateDuration(self, durationMin: int) -> None:
        pass

    def assignToPet(self, petId: str) -> None:
        pass

    def getDetails(self) -> dict:
        pass


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
        pass

    def getPriority(self) -> int:
        pass

    def isApplicable(self, task: Task) -> bool:
        pass


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
        pass

    def updateInfo(self, **kwargs) -> None:
        pass

    def removeInfo(self, field: str) -> None:
        pass

    def addMedication(self, medication: str) -> None:
        pass

    def removeMedication(self, medication: str) -> None:
        pass

    def addAction(self, action: Action) -> None:
        pass

    def removeAction(self, actionId: str) -> None:
        pass

    def getActions(self) -> List[Action]:
        pass

    def addConstraint(self, constraint: Constraint) -> None:
        pass

    def getConstraints(self) -> List[Constraint]:
        pass


class DailyPlan:
    """The output of the scheduling logic — a sorted, reasoned schedule for the day."""

    def __init__(self, date: date) -> None:
        self.date = date
        self.scheduledTasks: List[Task] = []
        self.totalDurationMin: int = 0
        self.reasoning: str = ""

    def addTask(self, task: Task) -> None:
        pass

    def removeTask(self, taskId: str) -> None:
        pass

    def reorder(self) -> None:
        pass

    def getSummary(self) -> str:
        pass

    def getReasoning(self) -> str:
        pass


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
        pass

    def removePet(self, petId: str) -> None:
        pass

    def getPets(self) -> List[Pet]:
        pass

    def addTask(self, task: Task) -> None:
        pass

    def removeTask(self, taskId: str) -> None:
        pass

    def getTasks(self) -> List[Task]:
        pass

    def generateDailyPlan(self) -> DailyPlan:
        pass
