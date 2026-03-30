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

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
