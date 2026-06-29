from flask import Blueprint, render_template, request
from datetime import datetime, timedelta
from services.revision_service import generate_time_revision

time_bp = Blueprint("time", __name__)


@time_bp.route("/time")
def time_revision():

    return render_template("time.html")

@time_bp.route("/time/today")
def today_revision():

    today = datetime.now().strftime("%Y-%m-%d")

    data = generate_time_revision(today, today)

    return render_template(
        "revision.html",
        title="📅 Today's Revision",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )


@time_bp.route("/time/yesterday")
def yesterday_revision():

    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    data = generate_time_revision(yesterday, yesterday)

    return render_template(
        "revision.html",
        title="📅 Yesterday's Revision",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )

@time_bp.route("/time/week")
def last_week_revision():

    today = datetime.now().strftime("%Y-%m-%d")

    last_week = (datetime.now() - timedelta(days=6)).strftime("%Y-%m-%d")

    data = generate_time_revision(last_week, today)

    return render_template(
        "revision.html",
        title="📅 Last 7 Days Revision",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )

@time_bp.route("/time/month")
def last_month_revision():

    today = datetime.now().strftime("%Y-%m-%d")

    last_month = (datetime.now() - timedelta(days=29)).strftime("%Y-%m-%d")

    data = generate_time_revision(last_month, today)

    return render_template(
        "revision.html",
        title="📅 Last 30 Days Revision",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )


@time_bp.route("/time/custom", methods=["POST"])
def custom_revision():

    start_date = request.form["start_date"]

    end_date = request.form["end_date"]

    data = generate_time_revision(start_date, end_date)

    return render_template(
        "revision.html",
        title=f"📅 Revision ({start_date} → {end_date})",
        back_url="/time",
        back_text="⬅ Back to Time-wise Revision",
        files=data["files"],
        summary=data["summary"],
        concepts=data["concepts"],
        keywords=data["keywords"],
        questions=data["questions"]
    )