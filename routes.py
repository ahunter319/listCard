from listCard import app, db
from listCard.models import User, Project, Item
from listCard.forms import LoginForm, RegisterForm, AddItemForm, AddProjectForm, AddCommentForm, ChangePasswordForm, \
    DeleteAccountForm, SetThemeForm
from flask import render_template, url_for, redirect, flash, Response
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
import pdfkit
from werkzeug.wsgi import FileWrapper
from io import BytesIO


# Configure PDFkit
path_wkhtmltopdf = "C:/Program Files/wkhtmltopdf/bin/wkhtmltopdf.exe"
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)


# Context Processors
@app.context_processor
def current_year_processor():
    """
    Gets current year and passes to all templates, so that footer will always have correct current year.
    """
    year = datetime.now().year
    return dict(year=year)


@app.context_processor
def theme_processor():
    """
    Gets theme from user and passes to all templates.
    """
    if current_user.is_authenticated:
        theme = current_user.theme
        loc = url_for('static', filename=f'{theme}.css')
        return dict(theme=loc)
    else:
        return dict(theme='dark')


# Routes to serve html
@app.route('/')
@app.route('/home')
def home_page():
    """
    Serves homepage if no user is logged in. If there is a logged-in user, it will redirect to their dashboard.
    """

    if current_user.is_authenticated:
        return redirect(url_for("dashboard_page"))
    return render_template("home.html")


@app.route("/dashboard", methods=["GET", "POST"])
@login_required
def dashboard_page():
    """
    Serves a user's dashboard, which displays all currently active projects.
    """

    projects = Project.query.filter_by(user_id=current_user.id, archived=False).all()
    add_project_form = AddProjectForm()

    if add_project_form.validate_on_submit():
        new_project = Project(name=add_project_form.project_name.data,
                              description=add_project_form.project_description.data,
                              user_id=current_user.id)
        db.session.add(new_project)
        db.session.commit()
        return redirect(url_for('dashboard_page'))
    
    return render_template("dashboard.html", projects=projects, add_project_form=add_project_form)


@app.route('/project/<proj_id>', methods=["GET", "POST"])
@login_required
def project_page(proj_id):
    """
    Serves a single project, with items laid out according to completion status.
    :param proj_id: id of project to be accessed
    """

    current_project = Project.query.filter_by(id=proj_id).first()

    # redirect to dash if no project, or if given project is archived
    if not current_project or current_project.archived:
        return redirect(url_for('dashboard_page'))

    add_item_form = AddItemForm()
    add_comment_form = AddCommentForm()

    if add_item_form.validate_on_submit():
        new_item = Item(name=add_item_form.item_name.data, project_id=proj_id)
        db.session.add(new_item)

        # update last change time-stamp and commit
        current_project.update_stamp()

        return redirect(url_for('project_page', proj_id=proj_id))

    elif add_comment_form.validate_on_submit():
        current_project.add_comment(add_comment_form.comment.data)
        current_project.update_stamp()

        return redirect(url_for('project_page', proj_id=proj_id))
    else:
        items = Item.query.filter_by(project_id=proj_id).all()
        return render_template("project.html", items=items, current_project=current_project,
                               add_item_form=add_item_form, add_comment_form=add_comment_form)


@app.route("/archive", methods=["GET"])
@login_required
def archive_page():
    """
    Serves a user's archive page, which displays only projects that have been archived.
    """

    archived_projects = Project.query.filter_by(user_id=current_user.id, archived=True).all()
    return render_template("archive.html", archived_projects=archived_projects)


@app.route("/archived/<proj_id>", methods=["GET"])
@login_required
def archived_project_page(proj_id):
    """
    Serves a project within the user's archive.
    :param proj_id: project to be accessed
    """

    current_project = Project.query.filter_by(id=proj_id).first()

    # redirect to archive if no project, or if given project isn't actually archived
    if not current_project or not current_project.archived:
        return redirect(url_for('archive_page'))

    items = Item.query.filter_by(project_id=proj_id).all()

    return render_template("archived_project.html", items=items, current_project=current_project)


@app.route('/settings', methods=["GET", "POST"])
@login_required
def settings_page():
    return render_template("settings.html")


# Helper Routes
@app.route("/update/<proj_id>/<item_id>/<status>", methods=["GET"])
@login_required
def update_status(proj_id, item_id, status):
    """
    Updates the status of a project's item. Redirects to project page.
    :param proj_id: id of project to be accessed
    :param item_id: id of item to be updated
    :param status: new status of item
    """
    valid = ["TODO", "DOING", "DONE"]

    # Get project and redirect to dash if it doesn't exist or is archived
    current_project = Project.query.filter_by(id=proj_id).first()
    if not current_project or current_project.archived:
        flash("Could not perform action. Incorrect information given", category="danger")
        return redirect(url_for('dashboard_page'))

    # Get item and redirect to dash if it doesn't exist
    item_obj = Item.query.filter_by(id=item_id).first()
    if not item_obj:
        flash("Could not perform action. Incorrect information given", category="danger")
        return redirect(url_for('dashboard_page'))

    # Ensure valid status
    if status not in valid:
        flash("Could not perform action. Incorrect information given", category="danger")
        return redirect(url_for('dashboard_page'))

    item_obj.change_item_status(status)

    # update last change time-stamp and commit
    current_project.update_stamp()

    return redirect(url_for('project_page', proj_id=proj_id))


@app.route('/remove/<proj_id>/<item_id>', methods=["GET"])
@login_required
def remove_item(proj_id, item_id):
    """
    Removes an item from a project. Redirects to project page.
    :param proj_id: id of the project to be accessed
    :param item_id: id of the item to be deleted
    """

    # Get project and ensure it exists and isn't archived
    current_project = Project.query.filter_by(id=proj_id).first()
    if not current_project or current_project.archived:
        flash("Could not perform action. Incorrect information given", category="danger")
        return redirect(url_for("dashboard_page"))

    # Get item and ensure it exists
    item_obj = Item.query.filter_by(id=item_id).filter_by(project_id=proj_id).first()
    if not item_obj:
        flash("Could not perform action. Incorrect information given", category="danger")
        return redirect(url_for("dashboard_page"))

    # Delete item
    item_obj.delete_item()

    # update last change time-stamp and commit
    current_project.update_stamp()

    return redirect(url_for('project_page', proj_id=proj_id))


@app.route('/remove_project/<proj_id>', methods=["GET"])
@login_required
def remove_project(proj_id):
    """Removes a project from user's dashboard entirely. Redirects to dashboard page.
    :param proj_id: the project to be accessed
    """

    # Get project and ensure it exists
    proj_obj = Project.query.filter_by(id=proj_id).first()
    if not proj_obj or proj_obj.archived:
        flash("Could not perform action. Incorrect information given", category="danger")
        return redirect(url_for("dashboard_page"))

    db.session.delete(proj_obj)
    db.session.commit()
    return redirect(url_for('dashboard_page'))


@app.route('/update_archived_status/<proj_id>/<status>', methods=["GET"])
@login_required
def update_archived_status(proj_id, status):
    """
    Changes the 'archived' value for a user's project in the database. Default upon project creation is False. Redirects
    to dashboard page.
    :param proj_id: the project to be accessed
    :param status: 0 will update archived to False
    """
    proj_obj = Project.query.filter_by(id=proj_id).first()
    if proj_obj:
        if status == '0':
            proj_obj.archive_status(False)
        else:
            proj_obj.archive_status(True)
        return redirect(url_for('dashboard_page'))


@app.route("/report/<proj_id>", methods=["GET", "POST"])
@login_required
def report_page(proj_id):
    """
    Generates and sends report for specified project by rendering html content and converting to pdf.
    :param proj_id: id number of project to be reported
    """

    # Get project object from id
    project = Project.query.filter_by(id=proj_id).first()

    if project:

        # Check if project belongs to user
        if current_user.id != project.user_id:
            flash("You do not have access to that project.", category="info")
            return redirect(url_for('dashboard_page'))

        # Get data for report
        items = Item.query.filter_by(project_id=proj_id).all()
        file_name = f"{project.name}_report.pdf"
        dates = get_dates(proj_id)

        # Generate html page
        page = render_template("report.html", project=project, items=items, dates=dates)

        # Convert html to pdf
        # css = url_for('static', filename='report.css')
        css = "C:/Users/ahunt/PycharmProjects/ListCard/listCard/static/report.css"

        options = {
            'page-size': 'A4',
            'margin-top': '0.75in',
            'margin-right': '0.75in',
            'margin-bottom': '0.75in',
            'margin-left': '0.75in',
            'encoding': "UTF-8",
            'custom-header': [
                ('Accept-Encoding', 'gzip')
            ]
        }

        # Returning pdf as attachment
        pdf = pdfkit.from_string(page, output_path=False, options=options, configuration=config, css=css)
        buff = BytesIO(pdf)
        wrapped = FileWrapper(buff)
        headers = {"Content-disposition": f"attachment; filename={file_name}"}
        response = Response(wrapped, mimetype='application/pdf', direct_passthrough=True, headers=headers)
        return response

    else:
        flash("Project does not exist.", category="info")
        return redirect(url_for('dashboard_page'))


# User Handling
@app.route("/signup", methods=["GET", "POST"])
def signup_page():
    """
    Renders the sign-up page, accepts sign-up form and adds new user to database. New user is then signed in and
    redirected to their dashboard.
    """
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        email=form.email.data,
                        password=form.password.data)
        db.session.add(new_user)
        db.session.commit()

        login_user(new_user)
        flash(f"Account created successfully. Welcome, {new_user.username}.", category="info")
        return redirect(url_for('dashboard_page'))

    if form.errors:
        for error_message in form.errors.values():
            flash(f"Error creating new user: {error_message}", category="danger")

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login_page():
    """
    Logs user in by checking for presence of username in database as well as correctness of given password against
    stored user password. Redirects to user's dashboard if given details are correct.
    """
    form = LoginForm()

    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success. Welcome, {attempted_user.username}', category='success')
            return redirect(url_for('dashboard_page'))
        else:
            flash('Invalid username and/or password. Please try again.', category='danger')
    return render_template("login.html", form=form)


@app.route('/logout', methods=["GET"])
@login_required
def logout_page():
    """
    Logs out the current user. Redirects to homepage upon successful log-out.
    """

    logout_user()
    flash("Log out successful.", category="info")
    return redirect(url_for("home_page"))


@app.route('/change_password', methods=["GET", "POST"])
@login_required
def change_password_page():
    """
    Changes a user's password in the database. Redirects to logout page if password change is successful.
    """

    change_form = ChangePasswordForm()
    user_obj = User.query.filter_by(id=current_user.id).first()

    if change_form.validate_on_submit():
        # Get data from form
        curr_pass = change_form.curr_pass.data
        new_pass = change_form.new_pass.data
        conf_pass = change_form.conf_new_pass.data
        # Check if correct current password
        if user_obj.check_password_correction(attempted_password=curr_pass):
            # Confirm new password
            if new_pass == conf_pass:
                user_obj.password = new_pass
                db.session.commit()
                return redirect(url_for("logout_page"))
            else:
                flash("Passwords don't match. Please try again", category='danger')
        else:
            flash("Invalid password. Please try again", category='danger')

    return render_template('change_password.html', change_form=change_form)


@app.route('/delete_account', methods=["GET", "POST"])
@login_required
def delete_account_page():
    """
    Deletes a user's account from database. Redirects to home page once account is deleted.
    """

    delete_form = DeleteAccountForm()

    if delete_form.validate_on_submit():
        password = delete_form.password.data
        if current_user.check_password_correction(attempted_password=password):
            db.session.delete(current_user)
            db.session.commit()
            logout_user()
            return redirect(url_for("home_page"))
        else:
            flash("Unable to delete account. Invalid password.", category='danger')

    return render_template("delete_account.html", delete_form=delete_form)


@app.route('/set_theme', methods=["GET", "POST"])
@login_required
def set_theme_page():
    """
    Changes a user's color theme preference.
    """

    theme_form = SetThemeForm()
    if theme_form.validate_on_submit():
        current_user.theme = theme_form.theme.data
        db.session.commit()
    return render_template('set_theme.html', theme_form=theme_form)


# Functions
def get_dates(proj_id):
    """
    Get date-times from project and drop seconds after decimal.
    :param proj_id: id of project to be accessed
    :return: dictionary of formatted date-times as strings
    """

    project = Project.query.filter_by(id=proj_id).first()
    created = str(project.creation_date)
    updated = str(project.last_update)
    reported = str(datetime.now())

    dates = {
        "created": created.split(".")[0],
        "updated": updated.split(".")[0],
        "reported": reported.split(".")[0]
    }
    return dates
