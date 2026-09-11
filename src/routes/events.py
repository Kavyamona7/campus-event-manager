from flask import Blueprint, current_app, render_template, request

from services.event_service import EventService

from bson import ObjectId
from flask import Blueprint, current_app, render_template, request, redirect, url_for

from datetime import datetime, timezone

from bson import ObjectId

from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    request,
    url_for
)


events_bp = Blueprint(
    "events",
    __name__,
    url_prefix="/events"
)


@events_bp.route("/")
def events():
    """Display all events with optional filters."""

    mongo = current_app.config["MONGO_SERVICE"]

    event_service = EventService(mongo)

    # Read filters from the URL
    title = request.args.get("title", "")
    category = request.args.get("category", "")
    status = request.args.get("status", "")
    tag = request.args.get("tag", "")
    sort_order = request.args.get("sort", "asc")

    # Retrieve events
    events = event_service.get_events(
        title=title,
        category=category,
        status=status,
        tag=tag,
        sort_order=sort_order
    )

    # Retrieve filter options
    categories = event_service.get_categories()
    tags = event_service.get_tags()

    return render_template(
        "events/list.html",
        events=events,
        categories=categories,
        tags=tags,
        title=title,
        selected_category=category,
        selected_status=status,
        selected_tag=tag,
        sort_order=sort_order
    )

@events_bp.route("/create", methods=["GET", "POST"])
def create_event():
    """Display and process the create-event form."""

    mongo = current_app.config["MONGO_SERVICE"]
    event_service = EventService(mongo)

    organizers = event_service.get_organizers()

    if request.method == "POST":

        title = request.form.get("title", "")
        description = request.form.get("description", "")
        category = request.form.get("category", "")
        tags = request.form.get("tags", "").split(",")

        start_date_raw = request.form.get("start_date", "")
        end_date_raw = request.form.get("end_date", "")

        capacity_raw = request.form.get("capacity", "")

        building = request.form.get("building", "")
        room = request.form.get("room", "")
        campus = request.form.get("campus", "")

        organizer_raw = request.form.get("organizer_id", "")

        errors = []

        # Basic validation
        if not title.strip():
            errors.append("Title is required.")

        if not description.strip():
            errors.append("Description is required.")

        if not category.strip():
            errors.append("Category is required.")

        # Capacity validation
        try:
            capacity = int(capacity_raw)

            if capacity <= 0:
                errors.append(
                    "Capacity must be greater than 0."
                )

        except ValueError:
            capacity = None
            errors.append(
                "Capacity must be a valid integer."
            )

        # Date validation
        try:
            start_date = datetime.fromisoformat(
                start_date_raw
            ).replace(tzinfo=timezone.utc)

            end_date = datetime.fromisoformat(
                end_date_raw
            ).replace(tzinfo=timezone.utc)

            if end_date < start_date:
                errors.append(
                    "End date cannot be before start date."
                )

        except ValueError:
            start_date = None
            end_date = None

            errors.append(
                "Please provide valid start and end dates."
            )

        # Organizer validation
        try:
            organizer_id = ObjectId(organizer_raw)

        except Exception:
            organizer_id = None

            errors.append(
                "Please select a valid organizer."
            )

        if not building.strip():
            errors.append("Building is required.")

        if not room.strip():
            errors.append("Room is required.")

        if not campus.strip():
            errors.append("Campus is required.")

        # Create event if validation passed
        if not errors:

            event_service.create_event(
                title=title,
                description=description,
                category=category,
                tags=tags,
                start_date=start_date,
                end_date=end_date,
                capacity=capacity,
                building=building,
                room=room,
                campus=campus,
                organizer_id=organizer_id
            )

            return redirect(
                url_for("events.events")
            )

        return render_template(
            "events/form.html",
            page_title="Create Event",
            organizers=organizers,
            errors=errors,
            form=request.form
        )

    return render_template(
        "events/form.html",
        page_title="Create Event",
        organizers=organizers,
        errors=[],
        form={}
    )

@events_bp.route("/<event_id>/edit", methods=["GET", "POST"])
def edit_event(event_id):
    mongo = current_app.config["MONGO_SERVICE"]
    event_service = EventService(mongo)

    # Validate MongoDB ObjectId
    try:
        object_id = ObjectId(event_id)
    except Exception:
        return "Invalid event ID", 400

    event = event_service.get_event_by_id(object_id)

    if not event:
        return "Event not found", 404

    organizers = event_service.get_organizers()
    errors = []

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        category = request.form.get("category", "").strip()
        tags_raw = request.form.get("tags", "")
        start_date_raw = request.form.get("start_date", "")
        end_date_raw = request.form.get("end_date", "")
        capacity_raw = request.form.get("capacity", "")
        building = request.form.get("building", "").strip()
        room = request.form.get("room", "").strip()
        campus = request.form.get("campus", "").strip()
        organizer_id_raw = request.form.get("organizer_id", "")

        tags = [tag.strip() for tag in tags_raw.split(",") if tag.strip()]

        # Basic validation
        if not title:
            errors.append("Title is required.")

        if not description:
            errors.append("Description is required.")

        if not category:
            errors.append("Category is required.")

        try:
            capacity = int(capacity_raw)
            if capacity <= 0:
                errors.append("Capacity must be greater than 0.")
        except ValueError:
            capacity = 0
            errors.append("Capacity must be a valid number.")

        try:
            start_date = datetime.fromisoformat(start_date_raw).replace(
                tzinfo=timezone.utc
            )
            end_date = datetime.fromisoformat(end_date_raw).replace(
                tzinfo=timezone.utc
            )

            if end_date < start_date:
                errors.append("End date cannot be before start date.")

        except ValueError:
            start_date = None
            end_date = None
            errors.append("Please provide valid start and end dates.")

        try:
            organizer_id = ObjectId(organizer_id_raw)
        except Exception:
            organizer_id = None
            errors.append("Please select a valid organizer.")

        if not building:
            errors.append("Building is required.")

        if not room:
            errors.append("Room is required.")

        if not campus:
            errors.append("Campus is required.")

        form = request.form.to_dict()

        if errors:
            return render_template(
                "events/form.html",
                page_title="Edit Event",
                form=form,
                organizers=organizers,
                errors=errors
            )

        event_service.update_event(
            object_id,
            title,
            description,
            category,
            tags,
            start_date,
            end_date,
            capacity,
            building,
            room,
            campus,
            organizer_id
        )

        return redirect(url_for("events.events"))

    # Convert MongoDB dates into datetime-local format
    form = {
        "title": event.get("title", ""),
        "description": event.get("description", ""),
        "category": event.get("category", ""),
        "tags": ", ".join(event.get("tags", [])),
        "capacity": event.get("capacity", ""),
        "start_date": event["startDate"].strftime("%Y-%m-%dT%H:%M"),
        "end_date": event["endDate"].strftime("%Y-%m-%dT%H:%M"),
        "building": event.get("location", {}).get("building", ""),
        "room": event.get("location", {}).get("room", ""),
        "campus": event.get("location", {}).get("campus", ""),
        "organizer_id": str(event.get("organizerId", ""))
    }

    return render_template(
        "events/form.html",
        page_title="Edit Event",
        form=form,
        organizers=organizers,
        errors=errors
    )
@events_bp.route("/<event_id>/delete", methods=["POST"])
def delete_event(event_id):
    mongo = current_app.config["MONGO_SERVICE"]
    event_service = EventService(mongo)

    try:
        object_id = ObjectId(event_id)
    except Exception:
        return "Invalid event ID", 400

    event = event_service.get_event_by_id(object_id)

    if not event:
        return "Event not found", 404

    event_service.delete_event(object_id)

    return redirect(url_for("events.events"))

@events_bp.route("/<event_id>")
def event_details(event_id):
    mongo = current_app.config["MONGO_SERVICE"]
    event_service = EventService(mongo)

    try:
        object_id = ObjectId(event_id)
    except Exception:
        return "Invalid event ID", 400

    event = event_service.get_event_details(object_id)

    if not event:
        return "Event not found", 404

    registered_users = event_service.get_registered_users(
        event.get("registrations", [])
    )

    users = event_service.get_registration_users()

    return render_template(
        "events/details.html",
        event=event,
        registered_users=registered_users,
        users=users
    )

@events_bp.route("/<event_id>/register", methods=["POST"])
def register_for_event(event_id):
    mongo = current_app.config["MONGO_SERVICE"]
    event_service = EventService(mongo)

    try:
        object_id = ObjectId(event_id)
    except Exception:
        return "Invalid event ID", 400

    user_id = request.form.get("user_id")

    try:
        user_object_id = ObjectId(user_id)
    except Exception:
        return "Invalid user ID", 400

    if not mongo.users.find_one({"_id": user_object_id}):
        return "User not found", 404

    result = event_service.register_user(
        object_id,
        user_object_id
    )

    if not result["success"]:
        return result["message"], 400

    return redirect(
        url_for(
            "events.event_details",
            event_id=object_id
        )
    )


@events_bp.route(
    "/<event_id>/cancel/<user_id>",
    methods=["POST"]
)
def cancel_registration(event_id, user_id):
    mongo = current_app.config["MONGO_SERVICE"]
    event_service = EventService(mongo)

    try:
        event_object_id = ObjectId(event_id)
        user_object_id = ObjectId(user_id)
    except Exception:
        return "Invalid ID", 400

    result = event_service.cancel_registration(
        event_object_id,
        user_object_id
    )

    if not result["success"]:
        return result["message"], 404

    return redirect(
        url_for(
            "events.event_details",
            event_id=event_object_id
        )
    )
