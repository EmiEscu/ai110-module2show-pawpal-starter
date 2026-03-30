# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
My initial UML design has the Parent class being the user account. This user class owns everything holding the userId, name
email, phones, and all the different pets that are registered. Then this parent has two children classes, Pet and Task. The pet class includes all the different attributes
such as petId, name, age, gender, type, breed, etc. With a bunch of different update, remove, and get methods, such as update Medication, Remove Info, or get constraints.
Then this Pet Class has two children of its own, Contraints and Actions, both of which are composition to the pet since if the pet is destroyed, then these cannot exist. Lastly there was a Task Class that was tied with the contraint and is dependent on the constraints that must be done to keep the pet safe, as well as another Dependent which is the DailyPlan
which is generated daily.

- What classes did you include, and what responsibilities did you assign to each?
Classes that I included were:

 Super Class User : Responsible setting up info such as user information and pet. This class gives method that allows the user to remove or add pets as well as add task 
 or generate them 

 User -> Pet (Child of User): This class is incharge of going more into detail of the pet. This is the section where the user will add more details about a single pet adding details
 such as breed, age, name, Medications list, contraints, actions, etc. This class has all the methods the user needs to make any updates such as removing or adding medication and 
 geetting any information

 User -> Pet -> Actions (Child of Pet): This class has all the actions that need to be done and includes all the services the user has purchased as well as the cost and frequency. This class has different methods, but mainly focused on payment and service status

 User -> Pet -> Constraints (Child of Pet): Constraints includes all the different problems we might encounter with a pet and what we should look out for. This allows the user to state any disabilities the pet may have and allows us to better attend their pet

 User -> Task (Child of User): In the User class the client can add task we should attend to and those task will then be brought down to the Task class. Once in the task class the actions will transfer over to all the pets of the user (or just one pet) so this will be directed association 

 User -> DailyPlan (Dependency): A daily plan is generated only when the user requests one. DailyPlan then has an aggregation relationship with Task — it groups and schedules existing tasks, but doesn't own them. The tasks exist independently whether or not a plan has been created.
**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

One of the design changes was in the user class, more specifically the generateDailyPlan method. This is because of the bottleneck that it presents. Due to workload such as sorting by priority, Fetching the pets contraints, passing that to task and much more, it becomes too much reponsibility for one method with no scheduler abstraction and one of the change implementations was breaking it down and adding helpers to it.

There is also some missing logic, for example there is no link between Action and Task. Something that should be there since how will the task get done if it never goes into action. 

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?
The schedulers considers many different constraints, for example, priority, max duration per pet, time of day, conflict detection and the due date.

The priority came to what matters the most to the pet. If something is more urgent or critical that will take priority consern over other factors. 

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?
One tradeoff that the scheduler makes is the Priority. When something has high priority it pushes everything back no matter the time in the day. This is important because for a new pet owner, the cost of accidentally skipping a medication or feeding because the optimizer rearranged things is much worse than occassionally losing a grooming slot due to a window mismatch.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?
I used ai tools during this project for a lot of things, specially since i was doing this project close to the deadline. I used it to design the UML diagram, brainstorm diffent functions for the classes, debugging and refactoring when I would make implementations or adding classes such as the schedular class close to the end. I would also use AI to help with the heavy lifting such as initiating the skeleton for all the classes. The prompts i would use are the ones given to us in the assignment, but I think that the reason why that worked so well for me was because I made sure to specify on the CLAUDE file lots of context about the project. I would also ask questions to claude of how the classes worked together and the purpose for some of the changes.

The most helpful kinds of prompts or questions where prompts that were broken down for the specific task. Rather then telling claude to build all the classes or check what was wrong with the code, I would pin down a class and ask it to explain what was going on and identify any potential issues the code had with its logic and algorithm. 

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?
One of the things was the way the AI was making the scheduleer, for some reason it was making super complex logic that made no sense. I told the AI to go back and simplify the logic and explain the changes it made and why. 
---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?
I ran the program multiple times and tested it myself. Although it had passed all the test given, I still wanted to make sure that there was no program crashing code in the files. I think it was important to test how it generated the shedule because if something like the priority ranking was incorrect, there would be no reason to use that system.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?
I really am not too confident on my scheduler working correctly. I ran it a couple of times and found some edge cases and issues. The first thing I disliked was the layout. For being a small application (layout wise), it used a vertical format which took too much space. I would have group the login, and pet section together, and below that added the task and generator. Also another issue was that there was no way to remove the pets, the date due wasnt set properly, there was also no way of editing any of the information or updating info for the user, and more little edge cases that if I had more time I would address.
---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?
I think that the part of the project I was most satisfied with was the generation system. I think that the AI did a good job in that field and was able to create a calendar/schedule which was effective and clean.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?
I would improve pretty much everything if I had another shot at this. First I would start with the design of the website, I would take more time setting up the UML diagram and making sure that all the functions and attributes as well as relationships make sense and are not just there. I would also break the classes down a bit more to reduce the complexity of everything and not have huge classes. 

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
AI is only as powerful as the fundational knowledge you have. I made the mistake of leaving this project till the final minute, so i wasnt able to truly understand what was going on, or spend time actually reviewing the AI and questioning why it made the changes it did or why it wrote why it did.