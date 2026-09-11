from flask import (
    Blueprint,
    current_app,
    render_template,
    request,
    redirect,
    url_for
)

from bson import ObjectId

from services.user_service import UserService


users_bp = Blueprint(
    "users",
    __name__,
    url_prefix="/users"
)


@users_bp.route("/")
def users():
    mongo = current_app.config["MONGO_SERVICE"]
    user_service = UserService(mongo)

    search = request.args.get("search", "").strip()
    department = request.args.get("department", "").strip()
    role = request.args.get("role", "").strip()

    users_list = user_service.get_users(
        search=search,
        department=department,
        role=role
    )

    departments = user_service.get_departments()
    roles = user_service.get_roles()

    return render_template(
        "users/list.html",
        users=users_list,
        departments=departments,
        roles=roles,
        search=search,
        selected_department=department,
        selected_role=role
    )


@users_bp.route("/create", methods=["GET", "POST"])
def create_user():
    mongo = current_app.config["MONGO_SERVICE"]
    user_service = UserService(mongo)

    errors = []

    if request.method == "POST":

        first_name = request.form.get(
            "first_name", ""
        ).strip()

        last_name = request.form.get(
            "last_name", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip()

        department = request.form.get(
            "department", ""
        ).strip()

        role = request.form.get(
            "role", ""
        ).strip()

        interests_text = request.form.get(
            "interests", ""
        ).strip()

        interests = [
            item.strip()
            for item in interests_text.split(",")
            if item.strip()
        ]

        if not first_name:
            errors.append("First name is required.")

        if not last_name:
            errors.append("Last name is required.")

        if not email or "@" not in email:
            errors.append("A valid email is required.")

        if not department:
            errors.append("Department is required.")

        if role not in [
            "student",
            "faculty",
            "staff",
            "admin"
        ]:
            errors.append("Invalid role.")

        if not errors:
            result = user_service.create_user(
                first_name,
                last_name,
                email,
                department,
                role,
                interests
            )

            if result is None:
                errors.append(
                    "A user with this email already exists."
                )
            else:
                return redirect(
                    url_for("users.users")
                )

        form = request.form.to_dict()

    else:
        form = {}

    return render_template(
        "users/form.html",
        page_title="Create User",
        form=form,
        errors=errors
    )


@users_bp.route("/<user_id>")
def user_details(user_id):
    mongo = current_app.config["MONGO_SERVICE"]
    user_service = UserService(mongo)

    try:
        object_id = ObjectId(user_id)
    except Exception:
        return "Invalid user ID", 400

    user = user_service.get_user_details(
        object_id
    )

    if not user:
        return "User not found", 404

    return render_template(
        "users/details.html",
        user=user
    )


@users_bp.route(
    "/<user_id>/edit",
    methods=["GET", "POST"]
)
def edit_user(user_id):
    mongo = current_app.config["MONGO_SERVICE"]
    user_service = UserService(mongo)

    try:
        object_id = ObjectId(user_id)
    except Exception:
        return "Invalid user ID", 400

    user = user_service.get_user_by_id(
        object_id
    )

    if not user:
        return "User not found", 404

    errors = []

    if request.method == "POST":

        first_name = request.form.get(
            "first_name", ""
        ).strip()

        last_name = request.form.get(
            "last_name", ""
        ).strip()

        email = request.form.get(
            "email", ""
        ).strip()

        department = request.form.get(
            "department", ""
        ).strip()

        role = request.form.get(
            "role", ""
        ).strip()

        interests_text = request.form.get(
            "interests", ""
        ).strip()

        interests = [
            item.strip()
            for item in interests_text.split(",")
            if item.strip()
        ]

        if not first_name:
            errors.append("First name is required.")

        if not last_name:
            errors.append("Last name is required.")

        if not email or "@" not in email:
            errors.append("A valid email is required.")

        if not department:
            errors.append("Department is required.")

        if role not in [
            "student",
            "faculty",
            "staff",
            "admin"
        ]:
            errors.append("Invalid role.")

        if not errors:
            result = user_service.update_user(
                object_id,
                first_name,
                last_name,
                email,
                department,
                role,
                interests
            )

            if result is None:
                errors.append(
                    "A user with this email already exists."
                )
            else:
                return redirect(
                    url_for(
                        "users.user_details",
                        user_id=object_id
                    )
                )

        form = request.form.to_dict()

    else:
        form = {
            "first_name": user.get(
                "firstName", ""
            ),
            "last_name": user.get(
                "lastName", ""
            ),
            "email": user.get(
                "email", ""
            ),
            "department": user.get(
                "department", ""
            ),
            "role": user.get(
                "role", ""
            ),
            "interests": ", ".join(
                user.get("interests", [])
            )
        }

    return render_template(
        "users/form.html",
        page_title="Edit User",
        form=form,
        errors=errors
    )


@users_bp.route(
    "/<user_id>/delete",
    methods=["POST"]
)
def delete_user(user_id):
    mongo = current_app.config["MONGO_SERVICE"]
    user_service = UserService(mongo)

    try:
        object_id = ObjectId(user_id)
    except Exception:
        return "Invalid user ID", 400

    result = user_service.delete_user(
        object_id
    )

    if not result["success"]:
        return result["message"], 400

    return redirect(
        url_for("users.users")
    )