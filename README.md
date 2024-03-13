# Task Manager 3000
## Review
This web application allows you effectively manage your task separating them on different lists.
Tasks can be prioritized if you need them to be so. You also allowed to set them deadlines and mark 
them as done. If task is no more needed you can simply delete it.
## What about technical details?
The app uses **Django** framework as base and **Python 3.11**. As linter goes **flake8**. To simplify
AJAX requests **htmx** was used. To avoid writing authentication **allauth** library was taken.
## Launch
To launch this project locally follow this few steps (git and Python are requested for successful
launch):
1. Open terminal and paste the following command 
    ``git clone https://github.com/AleksandrZhukovin/test_task``. It will copy all the files to your 
    directory.
2. Create and activate virtual environment for project with ``python -m venv venv`` ``venv/bin/activate`` 
   (or use specific version of these commands depending on your OS and the venv dir).
3. Use command ``cd test_task/to_do_list`` to move to the project dir.
4. To install all necessary libraries use ``pip install -r requirements.txt``.
5. Make DB migrations with ``python manage.py makemigrations`` ``python manage.py migrate``.
6. Now you are ready to use the app by using command ``python manage.py runserver``.
## In case you edit code
After changing code don't forget to check if it matches config file for linter. Use ``flake8 <project_dir>``
command to see what semantic problems with code you have.
After adding code don't forget to test it. Add your test to **test** pocket in **to_do_list_app**.
You can launch tests with ``python manage.py test`` or in case you want specific test to be used
`python manage.py test to_do_list_app.path_to_your_file_class_method`.