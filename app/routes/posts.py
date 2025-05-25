from flask import Blueprint, render_template, redirect, url_for, jsonify
from flask_injector import inject
from app.services.posts import Postservice
from app.forms.posts.create_form import CreateForm
from app.forms.posts.edit_form import EditForm
from flask_login import current_user


posts = Blueprint("posts", __name__)

@posts.route("/")
@inject
def list_all(post_service: Postservice):
    return render_template("posts/list.html", posts=post_service.get_all())

@posts.route("/create")
def create():
    return render_template("/posts/create.html", form=CreateForm())

@posts.route("/", methods=["POST"])
@inject
def store(post_service: Postservice):
    create_form = CreateForm()

    if create_form.validate_on_submit():
        post_service.create(
            title=create_form.title.data,
            content=create_form.content.data,
            id = current_user.id
        )

        return redirect(url_for("posts.list_all"))

    return render_template("/posts/create.html", form=create_form)

@posts.route("/<public_id>")
@inject
def view(post_service: Postservice, public_id):
    post = post_service.get_by_public_id(public_id)

    if not post:
        return redirect(url_for("posts.list_all"))

    return render_template("posts/view.html", post=post)

@posts.route("/<public_id>/edit")
@inject
def edit(post_service: Postservice, public_id):
    post = post_service.get_by_public_id(public_id)

    if not post:
        return redirect(url_for("posts.list_all"))

    edit_form = EditForm()
    edit_form.title.data = post.title
    edit_form.content.data = post.content
    

    return render_template("posts/edit.html", form=edit_form, post=post)

@posts.route("/<public_id>", methods=["POST"])
@inject
def update(post_service: Postservice, public_id):
    post = post_service.get_by_public_id(public_id)

    if not post:
        return redirect(url_for("posts.list_all"))

    edit_form = EditForm()

    if edit_form.validate_on_submit():
        post_service.update(
            post,
            edit_form.title.data ,
            edit_form.content.data 
        )

        return redirect(url_for("posts.list_all"))

    return render_template("posts/view.html", post=post)

@posts.route("/<public_id>", methods=["DELETE"])
@inject
def delete(post_service: Postservice, public_id):
    post = post_service.get_by_public_id(public_id)

    if post:
        post_service.delete(post)

    return jsonify({"msg": "post deleted successfully"})