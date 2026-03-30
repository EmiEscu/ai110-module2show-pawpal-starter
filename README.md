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

## Smarter Scheduling

Beyond the core daily plan, PawPal+ includes several scheduling improvements built on top of the base `DailyPlan` and `User` logic:

- **Sort by time** — `User._sortByTime()` orders any list of tasks chronologically using their `"HH:MM"` string attribute as a lambda key. Tasks with no time set fall to the end automatically.
- **Filter tasks** — `User.filterTasks(status, petName)` returns a focused subset of the task list. Either argument is optional; passing both applies AND logic (e.g. pending tasks for a specific pet only).
- **Recurring tasks** — `Task` now accepts a `frequency` attribute (`"daily"` or `"weekly"`). When `User.completeTask()` is called, it marks the task complete and automatically appends a new pending instance to the task list with the next due date calculated via Python's `timedelta`.
- **Conflict detection** — `DailyPlan.detectConflicts()` scans all scheduled task pairs for time-window overlaps using minutes-from-midnight arithmetic. Conflicts are stored in `plan.conflicts` and surfaced as plain-language warnings at the bottom of `getSummary()` — no crash, just visibility.

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
