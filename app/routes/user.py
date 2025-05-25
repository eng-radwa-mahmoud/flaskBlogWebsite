from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required
from flask_injector import inject
from app.services.user import UserService
from app.forms.login_form import LoginForm
from app.forms.signup_form import SignupForm
from app.forms.user.delete import DeleteForm
from app.forms.user.promote import PromoteForm


user = Blueprint("user", __name__)

@user.route("/profile")
@login_required
def profile():
    return render_template("/user/profile.html")

@user.route("/signup", methods=["GET", "POST"])
@inject
def signup(user_service: UserService):
    signup_form = SignupForm()

    if signup_form.validate_on_submit():
        if not user_service.get_by_username(username=signup_form.username.data):
            user_service.signup(
                signup_form.name.data,
                signup_form.username.data,
                signup_form.password.data
            )

        return redirect(url_for("user.login"))

    return render_template("signup.html", form=signup_form)

@user.route("/login", methods=["GET", "POST"])
@inject
def login(user_service: UserService):
    
    login_form = LoginForm()

    error_message = ""


    if login_form.validate_on_submit():
        if user_service.login(login_form.username.data, login_form.password.data):
            

            return redirect(url_for("user.profile"))

        error_message = "incorrect username or password"

    return render_template("login.html", form=login_form, error_message=error_message)

@user.route("/logout")
@login_required
@inject
def logout(user_service: UserService):
    user_service.logout()
    
    return redirect(url_for("dashboard.home"))

@user.route("/delete", methods=["GET","POST"])
@inject
def delete(user_service: UserService):
    delete_form = DeleteForm()
    error_message = ""
    print(delete_form.errors)
    if delete_form.validate_on_submit():
       print("Deleting")
       user = user_service.get_by_username(delete_form.username.data)
       if(user):
        user_service.delete(
            user
            )

        return redirect(url_for("dashboard.home"))
       
    print("no Deleting")
    return render_template("user/delete.html", form=delete_form, error_message=error_message)

@user.route("/promotetoAdmin", methods=["GET","POST"])
@inject
def promotetoAdmin(user_service: UserService):
    promote_form = PromoteForm()
    error_message = ""

    if promote_form.validate_on_submit():
        
        print("Promoting")
        user = user_service.get_by_username(promote_form.username.data)
        if(user):

            user_service.promote(user)
            return redirect(url_for("dashboard.home"))
       
    print("no Deleting")
    return render_template("user/promote.html", form=promote_form, error_message=error_message)

