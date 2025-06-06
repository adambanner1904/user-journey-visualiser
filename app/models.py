from sqlalchemy.orm import Mapped, mapped_column, MappedAsDataclass, DeclarativeBase, relationship
from sqlalchemy import ForeignKey
from app import db


class Base(DeclarativeBase, MappedAsDataclass):
    pass

class Project(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)

    # to many
    services: Mapped[list["Service"]] = relationship(back_populates="Service.project", cascade="delete, delete-orphan")
    journeys: Mapped[list["Journey"]] = relationship(back_populates="project", cascade="delete, delete-orphan")

class Service(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))

    # to 1
    project: Mapped["Project"] = relationship(back_populates="services")
    # to many
    endpoints: Mapped[list["Endpoint"]] = relationship(back_populates="service", cascade="delete, delete-orphan")


class Journey(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))

    # to 1
    project: Mapped["Project"] = relationship(back_populates="journeys")

class Endpoint(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column()
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"))

    # to 1
    service: Mapped["Service"] = relationship(back_populates="endpoints")

    # to many
    sources: Mapped[list["Link"]] = relationship(back_populates="source")
    targets: Mapped[list["Link"]] = relationship(back_populates="target")

    # has default
    has_explicit_event: Mapped[bool] = mapped_column(default=False)


class Link(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    source_node_id: Mapped[int] = mapped_column(ForeignKey("endpoint.id"))
    target_node_id: Mapped[int] = mapped_column(ForeignKey("endpoint.id"))

    # to 1
    source: Mapped["Endpoint"] = relationship(back_populates="sources")
    target: Mapped["Endpoint"] = relationship(back_populates="targets")

    # has default
    method: Mapped[str] = mapped_column(default="GET")
