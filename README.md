# CS50W Final project - Quiz website
This is a quiz website called Dino that help people create a quiz to review their lesson or to play with their friends

# Distinctiveness and Complexity
This is a project created for people to make quizzes

# What is in our files?
- Dino - main application directory
    - views.py: all functions that render Html files
    - models.py: include all of the database models. 
        - User: User database
        - Question: to save all of the question's information
        - Choices: all of the choices data
        - Answer: save all of the user's answer
        - Response: including all of the user's answer
        - Quiz: all of the quiz's data and its question
    - admin.py: register all the models to edit on the admin site
    - 

# How to run our application?
1. Open command prompt
    - Press Windows + R then type cmd and press enter
    - Search cmd in the windows search
2. Cd to the folder that have the project folder
    - Use cd command to move to the folder that have the project folder
3. Run the command
    - Run 'python manage.py runserver'