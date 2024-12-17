# Daily NASA Wallpaper Setter

This Python script updates the user's wallpaper to NASA's daily astronomical picture using the NASA APOD API.
I have tried to use parameters wherever possible, so this can be customised to use other APIs and themes.

## Running the Script Daily

Prerequisites:

* A working Python environment with pip installed
* A cloned version of main.py

To run the script automatically each day on Windows, follow the below steps:

1. Turn the script into an exe file, so users without a Python environment can run it.
    * Install pyinstaller using `pip install -U pyinstaller`.
    * In the directory where the main.py script lives, run `pyinstaller your_program.py`.
2. Open the Windows Task Scheduler.
3. Right click on 'Task Scheduler Library'. Select 'Create Task'.
4. Under 'General':
    * Give the task a name
    * I used 'Users' for the user account field, but this could be changed.
    * Select Windows version under 'Configure for'.
    * (Optional) Check 'Run with highest priviledges.
    * Leave the rest as is.
5. Set when to run the script by creating a new trigger under 'Triggers'.
6. Under 'Actions', create an action and point it to the main.exe under dist/main created during the build process (step 1).
7. Settings under 'Settings' and 'Conditions' are optional.
