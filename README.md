# List-Card
***
List Card is an online project tracking resource designed to help users stay organized and get more done. It's easy to
get started and simple to use, while providing basic progress tracking.
***

### Table of Contents
1. [General Info](#general-info)
2. [Technologies](#technologies)
3. [Installation](#installation)
4. [FAQs](#faqs)

<a name="general-info"></a>
### General Info

***

Status: Complete

This is a website where a user can register and login to a private account and create and manage todo-list projects. 
Each project can be opened in order to see the task cards with their listed items. There is a card for each status and 
each item can be moved back or forth along the cards. There's also a progress bar that automatically updates whenever an 
item is added/removed from the DONE card. User can add as many items as they wish. At any point user can generate a 
status report for the project, which they can save as a pdf for their own tracking purposes. When they are done with the 
project they can either leave it, delete it, or archive it. Archived projects can be viewed under the archive section 
and rolled back to the dashboard as desired. User's color-theme and password can be adjusted from the Settings page. 
They can also delete their account from this page if desired.

<a name="technologies"></a>
### Technologies
***
This website is written in Python, using the Flask framework and Bootstrap.
* [Flask](https://pypi.org/project/Flask/): Version 2.1.1
* [Flask Login](https://pypi.org/project/Flask-Login/): Version 0.6.0
* [Flask SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/): Version 2.5.1
* [Flask Bcrypt](https://pypi.org/project/Flask-Bcrypt/): Version 1.0.1
* [Flask WTF](https://pypi.org/project/Flask-WTF/): Version 1.0.1
* [WTForms](https://pypi.org/project/WTForms/): Version 3.0.1
* [Bootstrap](https://getbootstrap.com/): Version 5.1.3

<a name="installation"></a>
### Installation
***

The main folder contains the todoList package folder, the venv folder, and the run.py file. User, or hosting(eventually) runs run.py, which imports app from todoList package, and runs app. 

#### File Tree

> flaskTODO
	>> todoList
		>>> static
			>>>> js
				>>>>> modal_script.js
		>>> templates
			>>>> includes
				>>>>> addItemModal.html
				>>>>> archive_modal.html
				>>>>> delete_fromproject.html
				>>>>> delete_modal.html
				>>>>> modals.html
			>>>> archived_project.html
			>>>> base.html
			>>>> dashboard.html
			>>>> home.html
			>>>> login.html
			>>>> project.html
			>>>> register.html
		>>> __init_.py
		>>> forms.py
		>>> models.py
		>>> routes.py
		>>> todoList.db
	>> venv
	>> run.py

<a name="faqs"></a>
### FAQs
***
No one has asked any questions yet! Be the first!
