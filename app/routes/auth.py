from flask import Blueprint, render_template, redirect, url_for
from flask_injector import inject
from app.services.author import AuthorService
from app.services.user import UserService
from flask_login import login_required
from app.forms.login_form import LoginForm
from app.forms.signup_form import SignupForm
from app.forms.author.delete import DeleteForm
from app.forms.user.promote import PromoteForm
from flask_login import current_user

auth = Blueprint("auth", __name__)

@auth.route("/profile")
@login_required
def profile():
    author = current_user
    print(author.username)
    return render_template("/author/profile.html", author=author)



@auth.route("/login", methods=["GET", "POST"])
@inject
def login(author_service: AuthorService):
    load = 2
    login_form = LoginForm()

    error_message = ""

    if login_form.validate_on_submit():
        if author_service.login(login_form.username.data, login_form.password.data):

            return redirect(url_for("auth.profile"))

        error_message = "incorrect username or password"

    return render_template("author/loginauthor.html", form=login_form, error_message=error_message)

@auth.route("/logout")
@login_required
@inject
def logout(author_service: AuthorService):
    author_service.logout()
    
    return redirect(url_for("dashboard.home"))

@auth.route("/delete", methods=["GET","POST"])
@inject
def delete(author_service: AuthorService):
    delete_form = DeleteForm()
    error_message = ""

    if delete_form.validate_on_submit():
       print("Deleting")
       author = author_service.get_by_username(delete_form.username.data)
       if(author):
        author_service.delete(
            author
            )

       return redirect(url_for("dashboard.home"))
       
    print("no Deleting")
    return render_template("author/delete.html", form=delete_form, error_message=error_message)


@auth.route("/promotetoAuthor", methods=["GET","POST"])
@inject
def promotetoAuthor(user_service: UserService,author_service: AuthorService):
    promote_form = PromoteForm()
    error_message = ""

    if promote_form.validate_on_submit():

        print("Promoting")
        user = user_service.get_by_username(promote_form.username.data)
        if(user):
            author_service.create(name=user.name, username=user.username, password=user.password)
            user_service.delete(user)

            return redirect(url_for("dashboard.home"))
       
    print("no Deleting")
    return render_template("user/promoteAuthor.html", form=promote_form, error_message=error_message)

