from app.models import Method, Project, Service, Endpoint
from flask import Blueprint, render_template, session
from app import db
projects = Blueprint("projects"
                        , __name__
                        , template_folder="templates"
                        , static_folder="static")

@projects.route("/")
def index():
    return render_template("project_index.html")

@projects.route("/create-project-endpoints", methods=['POST'])
def create_project():
    project_name: str = session.get("project_name")
    services: list[dict] = session.get("services")
    # connections: list[tuple[str, str, Method]] = session.get("connections")
    project = Project(name=project_name)
    for service_obj in services:
        service = Service(name=service_obj['name']
                          , base_url=service_obj['base_url'])
        for endpoint_obj in service_obj:
            endpoint = Endpoint(url=endpoint_obj['url'])
            service.append(endpoint)
        project.append(service)
    db.session.commit()