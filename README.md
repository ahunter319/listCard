# List-Card
***
List Card is an online project tracking resource designed to help users stay organized and get more done. It's easy to
get started and simple to use, while providing basic progress tracking.

***
### General Info
This is a website where a user can register and login to a private account and create and manage todo-list projects. 
Each project can be opened in order to see the task-cards with their listed items. There is a card for each status and 
each item can be moved back or forth along the cards. There's also a progress bar that automatically updates whenever an 
item is added/removed from the DONE card. User can add as many items as they wish. At any point user can generate a 
status report for the project, which they can save as a pdf for their own tracking purposes. When they are done with the 
project they can either leave it, delete it, or archive it. Archived projects can be viewed under the archive section 
and rolled back to the dashboard as desired. User's color-theme and password can be adjusted from the Settings page. 
They can also delete their account from this page if desired.

***
### How to Use
List Card is hosted at (http://ahunter319.pythonanywhere.com/). You can register with a dummy email to try it out if you'd like. Though the site is built to require a user be logged in to use, it was built for practice, and the security of your projects and/or login information cannot be guarunteed. If you'd like to build the site on your own machine and host it locally, follow the standard practices for Flask applications. 

***
### Technologies
This website is written in Python, using the Flask framework and Bootstrap and hosted on PythonAnywhere
* [Flask](https://pypi.org/project/Flask/): Version 2.1.1
* [Flask Login](https://pypi.org/project/Flask-Login/): Version 0.6.0
* [Flask SQLAlchemy](https://pypi.org/project/Flask-SQLAlchemy/): Version 2.5.1
* [Flask Bcrypt](https://pypi.org/project/Flask-Bcrypt/): Version 1.0.1
* [Flask WTF](https://pypi.org/project/Flask-WTF/): Version 1.0.1
* [WTForms](https://pypi.org/project/WTForms/): Version 3.0.1
* [Bootstrap](https://getbootstrap.com/): Version 5.1.3
* [pdfKit](https://pypi.org/project/pdfkit/): Version 1.0.0
* [wkhtmltopdf](https://wkhtmltopdf.org/downloads.html#stable): Version 0.12.6

A big thanks to all the creators, maintainers, and documenters of these technologies!
