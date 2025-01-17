# h4g_helloworld
## Motivation
The Singapore Book Council’s administrators face significant challenges in efficiently organising and scheduling meetings among multiple participants. By focusing on the core functionality of scheduling meetings, we prioritised solving a critical pain point that directly impacts productivity and time management.

This targeted approach ensures that administrators can seamlessly coordinate schedules, reduce time spent on logistical tasks, and dedicate more attention to their primary responsibilities. 

## Aim
Our solution is a smart meeting scheduler that simplifies the process of finding the best time for a meeting. By considering participants' availability, preferences, and existing commitments, our system automatically suggests optimal meeting slots. 

This ensures a hassle-free and efficient way to coordinate meetings, saving time and improving productivity.

## User Stories
As a user, I am able to schedule meetings by selecting participants, so that the system automatically checks their availability and adds the event to their Google Calendar. This eliminates the need for manual invitations and reduces the time spent coordinating schedules.

## Feature 1: User Authentication
The web app requires users to sign in through their Google accounts to ensure secure access and seamless functionality. This not only verifies user identity but also enables integration with the Google Calendar API, allowing the app to check availability, create events, and send invites directly to participants’ calendars.

Using Google Sign-In makes the onboarding process easier by eliminating the need for separate accounts, while also maintaining the necessary security.

![Sign In Screen](https://github.com/user-attachments/assets/cc02164e-922d-40c7-a11c-1b62387f695a)

## Feature 2: Scheduling Meetings

The web app offers a seamless and efficient way for users to schedule meetings with multiple participants. Through an intuitive form interface, users can input essential details such as the meeting name, preferred dates, and times, as well as specify the participants to be invited. The form is designed to simplify the scheduling process, thus allowing users to focus on collaboration rather than logistics.

![Image](https://github.com/user-attachments/assets/4974ee30-2316-4cbb-80c0-b94812d35800)

A key aspect of the application is its integration with the Google Calendar API, which ensures that all meetings are automatically synchronised with participants' calendars. This integration not only streamlines the scheduling process but also reduces the manual effort required to send invitations or verify availability.
To optimise meeting arrangements, the system incorporates intelligent features that enhance scheduling efficiency. It checks the Google Calendar schedules of all participants, identifying any time slots marked as "busy" and avoiding conflicts. 

![Image](https://github.com/user-attachments/assets/abe31712-e1b3-4a5e-b4fb-9ce742d3e13b)

In addition to resolving scheduling conflicts, the system enforces sensible time constraints to promote work-life balance and operational efficiency. Meetings are automatically restricted to take place only during office hours, starting no earlier than 9:00 AM and ending no later than 5:00 PM. Furthermore, the system ensures that no meetings are scheduled on weekends, respecting participants' personal time.

Once a suitable time slot is identified, the app completes the process by adding the meeting directly to all participants' Google Calendars. This eliminates the need for users to manually create calendar events or send separate invitations, saving valuable time and reducing errors.

## Planned Future Improvements

While we have completed the prototype for scheduling meetings, below are some of the planned features that we aim to complete in order to elevate our current system into one that is more robust and complete, ensuring a one-stop solution for Singapore Book Council’s staff.

### Feature 3: Creating Tasks and Automating Reminders

We aim to design the system such that creating tasks would align seamlessly with sending reminders. When users create a task, it is instantly added to their to-do list for easy tracking. Additionally, the system automatically generates reminders and syncs them with users’ Google Calendars, ensuring deadlines are never missed.

This streamlined approach enhances productivity by combining task management and scheduling, allowing users to stay organized and focused without the need for manual follow-ups or external reminder tools.

### Feature 4: Generate Summaries of Email Threads

We aim to incorporate a feature that generates concise summaries of lengthy email threads, saving users the time and effort of reading through extensive correspondences. By providing clear and actionable insights from long email exchanges, this functionality will help users stay informed and focused while improving overall productivity.

### Feature 5: AI Integration

There is potential to introduce AI-based smart scheduling, which prioritises meetings based on urgency, participants' roles, and past availability patterns. Further, it can be expanded to integrate with Slack, Microsoft Teams, and other productivity tools for a fully connected workflow.


## Tech Stack:
Django
Python
HTML
Google Calendar API

