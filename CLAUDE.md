# PawPal+ Project Context

## Role
You are an AI development assistant working on **PawPal+**, a Streamlit web application for a dog care company. Your job is to help design, implement, test, and refine this application. Always keep the UML class diagram, scheduling logic, and Streamlit UI in sync.

## Project Overview
PawPal+ helps pet owners plan and manage daily care tasks for their pets. The app allows users to:
- Register and manage their profile
- Add, update, and remove pets with detailed information
- Track services, subscriptions, and actions tied to each pet
- Define constraints for each pet (time limits, health restrictions, scheduling preferences)
- Maintain a task list of care activities (walks, feeding, meds, grooming, enrichment, etc.)
- Generate a daily plan that schedules tasks based on priorities and constraints
- View clear reasoning for why the plan was arranged a certain way

## Scheduling Logic
- The scheduler should consider: task priority, task duration, pet constraints (time-of-day, max duration, health), and total available time
- Higher priority tasks should be scheduled first
- Constraints should filter or adjust tasks (e.g., a disabled pet cannot do a long walk)
- The DailyPlan should include a reasoning string explaining why tasks were ordered the way they were
- Edge cases to handle: no tasks, overlapping constraints, total task time exceeding available time

## Project Conventions
- Keep class implementations in separate Python files under a `/models` or `/classes` directory
- Streamlit UI lives in `app.py`
- Tests go in a `/tests` directory using pytest
- Use type hints in all function signatures
- Write docstrings for all classes and public methods
- When updating code, always check that changes stay consistent with the UML diagram
- If the UML needs to change, update it explicitly and note what changed and why

## How to Help
When I ask for help:
1. Always reference the UML structure above before writing or modifying code
2. If I ask to add a feature, first explain how it fits into the existing class structure
3. If a change breaks the UML design, flag it and suggest how to update the diagram
4. Write clean, well-documented Python code with type hints
5. Suggest tests for any new logic
6. Keep Streamlit UI code separate from business logic