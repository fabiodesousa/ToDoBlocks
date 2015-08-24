# ToDoBlocks
Time blocking to-do helper. Integrates Trello and Slack.  
Blocking time off for specific tasks is the basic idea behind the productivity system that ToDoBlocks facilitates. The user sets up a trello board with the following lists:  
- Incoming
- Today
- This Week
- Later
- Done
## MVP
Each new task for the user gets sent to Incoming. As soon as possible, the user sets a date and time for that task to get done. Once a day (or more), ToDoBlocks goes through all of the cards on the Trello board that have dates, and moves them to the appropriate list (tasks due today go into the Today list, and so on). After sorting the cards, ToDoBlocks then messages the user on Slack with the schedule for the day.
## Later features
- Respond to the Slackbot to mark tasks as done (or send back to incoming if needs rescheduling)
- Waiting On list integration (tasks that you're waiting on someone to get back to you for you to complete)
- Reminder message of the next task as it arrives
- Add task to incoming (with a / command?)
## Dream features
- Integrate Asana as well
## Reasoning
I really enjoy using Trello (and Asana for work), but I find myself forgetting to actually use them. Productivity systems are about behavior change, and I find that I get platform fatigue even if I like all of the platforms I'm using. I figured that the productivity system I use emphasizes time blocking, which means I can get a daily report (and possibly reminders) on the one platform I'm guaranteed to be using—Slack.  
With ToDoBlocks, I'll be able to look at my Trello board only once. At the end of the day, I can add to my incoming list, add dates/times to tasks, and end on the satisfying note of archiving tasks I have completed.
