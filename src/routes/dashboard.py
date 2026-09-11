from flask import Blueprint, current_app, render_template

from services.dashboard_service import DashboardService


dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def dashboard():
    mongo = current_app.config["MONGO_SERVICE"]

    dashboard_service = DashboardService(mongo)

    data = dashboard_service.get_dashboard_data()

    return render_template(
        "dashboard.html",
        **data
    )