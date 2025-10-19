How the Telegram Bot Works
This Telegram bot is designed to allow an admin to assign tasks to users based on their Telegram usernames and enables users to view their assigned tasks. It uses the python-telegram-bot library (v20.x or higher) and stores tasks in a JSON file (tasks.json). Here's a breakdown of its functionality:
Key Features:

Admin Task Assignment:

The admin (identified by a specific Telegram user ID, ADMIN_ID) can assign tasks to users using the /settask command.
Example: /settask aminhunter Study book, Call client, Write report

aminhunter is the username (without @).
Tasks are provided as a comma-separated list.


The tasks are saved in a tasks.json file under the user's username.


Task Viewing:

Users can view their tasks by sending the /start command, which displays a button labeled "Today Task."
Clicking the button shows the tasks assigned to their username (e.g., @aminhunter).
If no tasks are assigned, the bot replies: "No tasks assigned yet 😴."
If the user doesn't have a Telegram username, they get: "You don't have a username! Please set one in Telegram 😅."


Task Deletion:

The admin can delete tasks for a user using the /deletetask command.
Example: /deletetask aminhunter

This removes all tasks associated with @aminhunter from tasks.json.




Data Storage:

Tasks are stored in a JSON file (tasks.json) with a structure like:
json{
  "aminhunter": ["Study book", "Call client", "Write report"],
  "anotheruser": ["Task 1", "Task 2"]
}



Security and Access Control:

Only the admin (matching ADMIN_ID) can use /settask and /deletetask.
The bot checks if the provided username exists in Telegram before assigning tasks.
File operations (reading/writing to tasks.json) are thread-safe using a Lock to prevent race conditions.



How to Use the Bot:

Setup:

Replace TOKEN in the code with your bot's token from @BotFather.
Replace ADMIN_ID with your Telegram user ID (get it from @userinfobot).
Ensure Python 3.7+ and python-telegram-bot (v20.x or higher) are installed.


Running the Bot:

Save the bot code in a file (e.g., main.py).
Run it with: python main.py.
The bot will start and print: "🤖 Bot is running and waiting..."


Assigning Tasks (Admin):

Send: /settask username task1, task2, task3

Example: /settask aminhunter Study book, Call client, Write report
Bot response: "✅ Tasks saved for @aminhunter."
Errors:

Invalid format: "Wrong format! Example: /settask aminhunter task1, task2, task3"
Invalid username: "User @aminhunter not found or an error occurred!"






Viewing Tasks (User):

Send /start and click the "Today Task" button.
Bot shows tasks or a message if none are assigned.


Deleting Tasks (Admin):

Send: /deletetask username

Example: /deletetask aminhunter
Bot response: "🗑 Tasks for @aminhunter deleted." or "No tasks found for @aminhunter!"





Technical Details:

Library: Uses python-telegram-bot (v20.x) for Telegram API interaction.
Asyncio: The bot uses asyncio for asynchronous handling of Telegram updates.
JSON Storage: Tasks are stored in tasks.json, with thread-safe file operations using threading.Lock.
Error Handling:

Checks for valid usernames using context.bot.get_chat.
Handles file errors (e.g., missing tasks.json) and invalid inputs.
Gracefully stops the bot on KeyboardInterrupt (Ctrl+C).


Environment Variables: Uses os.getenv for the bot token to improve security.

Setup Scripts:
To make the bot portable across systems, two setup scripts were provided:

Linux/Mac (setup.sh):

Checks if Python 3 is installed; if not, installs it using apt/yum/dnf (Linux) or Homebrew (Mac).
Upgrades pip and installs python-telegram-bot.
Run with: chmod +x setup.sh && ./setup.sh.


Windows (setup.ps1):

Checks for Python; if not installed, downloads and installs Python 3.12 silently.
Upgrades pip and installs python-telegram-bot.
Run with PowerShell: .\setup.ps1 (may require Set-ExecutionPolicy RemoteSigned).



Notes:

Prerequisites: The system needs internet access for downloading Python and packages.
Permissions: Setup scripts may require admin/root privileges for installing Python.
Testing: Test the setup scripts in a virtual machine to avoid unintended changes.
Limitations:

The bot requires users to have a Telegram username.
Only one admin is supported (extendable with code changes).
Task storage is file-based; for scalability, consider a database like SQLite.



Potential Improvements:

Automated Task Reminders: Send daily task notifications to users.
Multiple Admins: Allow multiple Telegram IDs to manage tasks.
Task Scheduling: Add deadlines or specific dates for tasks.
Logging: Add detailed logging for debugging.
Database: Replace JSON with SQLite for better scalability.
