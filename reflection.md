# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

- Briefly describe your initial UML design.
- What classes did you include, and what responsibilities did you assign to
each?

My initial UML design used four main classes: `Owner`, `Pet`, `Task`, and
`Scheduler`. I chose these classes because they matched the project
requirements and gave the system a clear object-oriented structure.

The `Task` class was responsible for storing the details of a single pet care
activity, including its description, scheduled time, duration, priority,
frequency, and completion status. The `Pet` class was responsible for storing
identifying information about a pet and managing the tasks assigned to that
pet. The `Owner` class represented the user and managed a collection of pets.
The `Scheduler` class handled the main planning logic by retrieving tasks
across pets, organizing them into a daily plan, and explaining the reasoning
behind the schedule.

**b. Design changes**

- Did your design change during implementation?
- If yes, describe at least one change and why you made it.

Yes, my design changed during implementation. In the beginning, the scheduler
mainly focused on retrieving tasks and sorting them by time. As I continued,
I realized that the project required the scheduler to do more than simple
ordering, so I expanded it to support filtering, conflict detection,
recurring task handling, weighted scheduling, and next available slot logic.

I also added JSON persistence so that owner, pet, and task data could be
saved and reloaded between runs. I made these changes because they made the
system more practical, improved the connection between the backend and the
Streamlit UI, and made the final implementation align more strongly with the
project rubric.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority,
preferences)?
- How did you decide which constraints mattered most?

My scheduler considers several constraints, including scheduled time, task
priority, task duration, recurrence frequency, overlapping conflicts, and
urgency in the weighted scheduling strategy. I also treated owner available
time as an important design consideration, even though my current scheduler
uses it in a lightweight way rather than as a hard limit.

I decided that time and priority mattered most because they are the most
important factors for a busy pet owner trying to stay organized. A task such
as medication should be treated as more urgent than a low-priority grooming
task, and the scheduled time matters because the app is supposed to produce a
daily plan that makes sense in real use. Duration also mattered because it
affects whether tasks overlap and whether a new task can fit into the plan.

**b. Tradeoffs**

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

One tradeoff my scheduler makes is that the weighted scheduling feature uses a
simple heuristic instead of a full optimization algorithm. It combines
priority and urgency in a readable way, but it does not try to compute a
globally optimal schedule.

I think this tradeoff is reasonable for this scenario because PawPal+ is meant
to be understandable, practical, and easy to maintain. A lightweight
heuristic is much easier to explain, test, and debug, while still providing
smarter behavior than plain chronological sorting. For a pet care assistant,
that balance between intelligence and simplicity is appropriate.

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design
brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

I used AI tools throughout the project for brainstorming the UML design,
turning the UML into Python class skeletons, refining method structure,
debugging issues, generating tests, and improving documentation. AI was most
helpful when I used it to move from a rough design idea to a more complete
implementation that still matched the assignment requirements.

The most helpful prompts were the ones that were specific and constrained.
For example, prompts that explicitly referenced the four required classes and
asked for scheduling logic across multiple pets gave better results than
broad, open-ended prompts. Focused prompts reduced unnecessary complexity and
made it easier to keep the design aligned with the rubric.

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

One moment where I did not accept an AI suggestion as-is was when it started
adding extra abstractions and additional classes that were not necessary for
the project. Even though some of those ideas were interesting, I rejected
them because the assignment was centered on the four required classes:
`Owner`, `Pet`, `Task`, and `Scheduler`, and I wanted the design to stay
clean and focused.

I evaluated AI suggestions by comparing them against the rubric, checking
whether they made the design harder to explain, and testing whether they
actually improved the system. I verified correctness by running the CLI demo
and using `pytest` to check important behaviors such as sorting, recurrence,
conflict detection, and task management.

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

I tested several key behaviors in the system, including whether
`mark_complete()` correctly updated a task’s completion status, whether
adding a task to a pet increased the pet’s task count, whether sorting by
time returned tasks in chronological order, whether filtering returned the
correct tasks, whether recurring daily tasks created the next instance,
whether conflict detection identified overlapping tasks, and whether saving
and loading JSON preserved the system data.

These tests were important because they covered the most meaningful parts of
the scheduler’s behavior. The project depends on correct task storage,
retrieval, ordering, recurrence, and validation across multiple pets, so
those were the areas where correctness mattered most. Testing these behaviors
gave me more confidence that the schedule generation logic was working as
intended.

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

I am fairly confident that my scheduler works correctly for the main project
requirements because I verified it using both automated tests and the
end-to-end CLI demo. The tests check important behaviors directly, and the
demo helped confirm that the overall workflow made sense from the user’s
perspective.

If I had more time, I would test additional edge cases such as an owner with
no pets, a pet with no tasks, many overlapping tasks in one schedule, tasks
with identical times and priorities, recurring tasks near midnight, and more
advanced cases involving the owner’s available time and preferences.

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

The part of this project I am most satisfied with is the scheduler design. I
think it ended up being both practical and clear. It does more than store
data because it can sort, filter, detect conflicts, handle recurring tasks,
and explain the reasoning behind the generated schedule. I am also satisfied
that the final design stayed centered on the required object-oriented
structure instead of becoming unnecessarily complicated.

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

If I had another iteration, I would improve the way owner constraints are
used, especially available time and preferences. I would also add fuller task
editing in the Streamlit UI and possibly redesign the weighted scheduling
logic so it could make even better decisions when many important tasks
compete for time in the same day.

**c. Key takeaway**

- What is one important thing you learned about designing systems or working
with AI on this project?

One important thing I learned is that working with AI still requires strong
human judgment. AI was very useful for brainstorming, drafting, debugging,
and testing support, but I still had to decide which suggestions matched the
project requirements, which ideas were too complex, and how to verify that
the final system actually worked correctly. That made me realize that even
when using powerful AI tools, the human still has to act as the lead
architect.
