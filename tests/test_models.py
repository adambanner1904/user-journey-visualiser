
from app.models import Project, Service, Endpoint
from .fixtures import test_app, clear_data, test_client
from app import db

def test_simple_insert(test_app):
    with test_app.app_context():
        project = Project(name='p800')
        db.session.add(project)
        db.session.commit()

        project_from_db = db.session.execute(db.select(Project).where(Project.name=='p800')).scalar()
        assert project.name == project_from_db.name

        clear_data(db)

def test_simple_relationship(test_app):
    with test_app.app_context():
        project = Project(name='p800'
                          , services=[
                Service(name="direct-debit-frontend"
                        , base_url="/direct-debit")
            ])
        db.session.add(project)
        db.session.commit()

        service_from_db = db.session.execute(db.select(Service).where(Service.name == 'direct-debit-frontend')).scalar()

        assert service_from_db.project.name == project.name

        clear_data(db)

def test_complex_relationship(test_app, test_client):
    with test_app.app_context():
        project = Project(
            name="sdds"
            , services=[
                Service(
                    name="direct-debit-frontend"
                    , base_url="/direct-debit"
                    , endpoints=[
                        Endpoint(
                            url="/start/journey"
                        )
                        , Endpoint(
                            url="/select-tax-to-pay"
                        )
                        , Endpoint(
                            url="/survey/submit/:traceId/from/:entrypoint"
                            , has_explicit_event=True
                        )
                    ]
                )
            ]
        )
        db.session.add(project)
        db.session.commit()
        urls = db.session.execute(db.select(Endpoint.url)).scalars()
        for url in ["/start/journey", "/select-tax-to-pay", "/survey/submit/:traceId/from/:entrypoint"]:
            assert url in urls

