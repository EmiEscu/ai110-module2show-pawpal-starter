# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Features

- **Priority-based scheduling** — Tasks are sorted by priority (highest first) before being added to the daily plan, so the most important care activities are always scheduled first.
- **Chronological sorting** — `Scheduler.sortByTime()` orders tasks by their `"HH:MM"` start time attribute. Tasks without a scheduled time fall to the end automatically.
- **Clock-based start times** — The daily plan assigns real wall-clock start times to every task (beginning at 8:00 AM by default) using a running cursor that advances by each task's duration.
- **Constraint enforcement** — Pet-level constraints (max duration, time-of-day windows) are evaluated before a task is added to the plan. Duration limits accumulate per pet across the session, so a pet with a 30-minute walk cap cannot exceed it across multiple tasks.
- **Time-of-day filtering** — Constraints can restrict tasks to morning (6–12), afternoon (12–17), or evening (17–21) windows; tasks scheduled outside the allowed window are excluded.
- **Conflict detection** — `DailyPlan.detectConflicts()` scans every pair of scheduled tasks for time-window overlaps using minutes-from-midnight arithmetic. Detected conflicts are stored and surfaced as plain-language warnings in the plan summary — no crash, just visibility.
- **Daily and weekly recurrence** — Tasks can carry a `frequency` of `"daily"` or `"weekly"`. When `User.completeTask()` is called, the task is marked complete and a new pending instance with the next due date (`today + 1 day` or `today + 7 days`) is automatically appended to the task list.
- **Task filtering** — `User.filterTasks(status, petName)` returns a focused subset of the task list. Either argument is optional; passing both applies AND logic (e.g., only pending tasks for a specific pet).
- **Cascade deletion** — Removing a pet from a user's profile automatically removes all tasks assigned to that pet, keeping data consistent.
- **Scheduled reasoning** — Every generated plan includes a human-readable explanation of why tasks were ordered the way they were.

<a href="/course_images/ai110/productImg1.png" target="_blank"><img src='/course_images/ai110/productImg1.png' alt='Product Image 1' width=500px></a>
<a href="/course_images/ai110/productimg2.png" target="_blank"><img src='/course_images/ai110/productimg2.png' alt='Product Image 2' width=500px></a>

## Smarter Scheduling

Beyond the core daily plan, PawPal+ includes several scheduling improvements built on top of the base `DailyPlan` and `User` logic:

- **Sort by time** — `User._sortByTime()` orders any list of tasks chronologically using their `"HH:MM"` string attribute as a lambda key. Tasks with no time set fall to the end automatically.
- **Filter tasks** — `User.filterTasks(status, petName)` returns a focused subset of the task list. Either argument is optional; passing both applies AND logic (e.g. pending tasks for a specific pet only).
- **Recurring tasks** — `Task` now accepts a `frequency` attribute (`"daily"` or `"weekly"`). When `User.completeTask()` is called, it marks the task complete and automatically appends a new pending instance to the task list with the next due date calculated via Python's `timedelta`.
- **Conflict detection** — `DailyPlan.detectConflicts()` scans all scheduled task pairs for time-window overlaps using minutes-from-midnight arithmetic. Conflicts are stored in `plan.conflicts` and surfaced as plain-language warnings at the bottom of `getSummary()` — no crash, just visibility.

## Testing PawPal+

### Run the tests

```bash
python -m pytest tests/test_pawpal.py -v
```

### What the tests cover

| Test | Description |
|---|---|
| `test_mark_complete_changes_status` | Verifies that calling `markComplete()` on a task changes its status from `"pending"` to `"complete"`. |
| `test_add_task_increases_pet_task_count` | Confirms that adding a task via `User.addTask()` makes it retrievable and associated with the correct pet. |
| `test_sort_by_time_returns_chronological_order` | Checks that `User._sortByTime()` returns tasks sorted in ascending order by their scheduled time (`"HH:MM"`). |
| `test_daily_task_recurrence_creates_next_day_task` | Confirms that completing a `frequency="daily"` task automatically creates a new pending task with a due date of tomorrow and appends it to the user's task list. |
| `test_detect_conflicts_flags_overlapping_tasks` | Verifies that `DailyPlan.detectConflicts()` returns at least one warning when two tasks share an overlapping time window. |

### Confidence Level

**4 / 5 stars**

The core scheduling behaviors — task completion, recurrence, chronological ordering, and conflict detection — are all covered and passing. The rating stops short of 5 stars because edge cases like weekly recurrence, constraint filtering interactions, and tasks that span midnight are not yet tested. As those scenarios gain tests, confidence can move to a full 5.

---

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.
