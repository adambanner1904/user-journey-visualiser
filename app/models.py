from enum import Enum

from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy import ForeignKey
from app import db


class Base(DeclarativeBase):
    pass


class Project(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, init=False)
    name: Mapped[str] = mapped_column(unique=True)

    # to many
    services: Mapped[list["Service"]] = relationship(back_populates="project"
                                                     , cascade="all, delete, delete-orphan"
                                                     , default_factory=list)
    journeys: Mapped[list["Journey"]] = relationship(back_populates="project"
                                                     , cascade="delete, delete-orphan"
                                                     , default_factory=list)


class Service(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"), init=False)
    name: Mapped[str] = mapped_column(unique=True)
    base_url: Mapped[str] = mapped_column(unique=True)

    # to 1
    project: Mapped["Project"] = relationship(back_populates="services", default=None)
    # to many
    endpoints: Mapped[list["Endpoint"]] = relationship(back_populates="service", cascade="all, delete, delete-orphan", default_factory=list)


class Journey(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    project_id: Mapped[int] = mapped_column(ForeignKey("project.id"))

    # to 1
    project: Mapped["Project"] = relationship(back_populates="journeys")


class Endpoint(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    url: Mapped[str]
    service_id: Mapped[int] = mapped_column(ForeignKey("service.id"), init=False)

    # to 1
    service: Mapped["Service"] = relationship(back_populates="endpoints", init=False)

    # to many
    sources: Mapped[list["Link"]] = relationship(back_populates="source"
                                                 , default_factory=list
                                                 , primaryjoin="Endpoint.id==Link.target_node_id")
    targets: Mapped[list["Link"]] = relationship(back_populates="target"
                                                 , default_factory=list
                                                 , primaryjoin="Endpoint.id==Link.source_node_id")

    # has default
    has_explicit_event: Mapped[bool] = mapped_column(default=False)


class Link(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    source_node_id: Mapped[int] = mapped_column(ForeignKey("endpoint.id"))
    target_node_id: Mapped[int] = mapped_column(ForeignKey("endpoint.id"))

    # to 1
    source: Mapped["Endpoint"] = relationship(back_populates="sources"
                                              , primaryjoin="Link.source_node_id==Endpoint.id"
                                              , viewonly=True)
    target: Mapped["Endpoint"] = relationship(back_populates="targets"
                                              , primaryjoin="Link.target_node_id==Endpoint.id"
                                              , viewonly=True)

    # has default
    method: Mapped[str] = mapped_column(default="GET")


class Method(Enum):
    GET = 'GET'
    POST = 'POST'