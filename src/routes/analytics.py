from flask import Blueprint, current_app, render_template

from services.analytics_service import AnalyticsService


analytics_bp = Blueprint(
    "analytics",
    __name__,
    url_prefix="/analytics"
)


@analytics_bp.route("/")
def analytics():
    mongo = current_app.config["MONGO_SERVICE"]
    analytics_service = AnalyticsService(mongo)

    data = analytics_service.get_all_analytics()

    return render_template(
        "analytics/index.html",
        data=data
    )