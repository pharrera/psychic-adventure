from orm_base import Base
from sqlalchemy import Column, Integer, UniqueConstraint, String, Sequence
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List


class Department(Base):
    """An organization within a particular college within a university. Each
    department offers one or more major fields of study to its students, and
    within each major, some number of courses. Each course is offered on
    a regular basis as a scheduled section of a given course.
    """

    __tablename__ = "departments"

    department_id: Mapped[int] = mapped_column('department_id', Integer, Sequence('department_id_seq'),
                                               primary_key=True)
    abbreviation: Mapped[str] = mapped_column('abbreviation', String, nullable=False)
    name: Mapped[str] = mapped_column('name', String(50), nullable=False)
    chair_name: Mapped[str] = mapped_column('chair_name', String(80))
    building: Mapped[str] = mapped_column('building', String(10))
    office: Mapped[int] = mapped_column('office', Integer)
    description: Mapped[str] = mapped_column('description', String(80))

    # Relationships
    majors: Mapped[List["Major"]] = relationship('Major', back_populates="department")
    courses: Mapped[List["Course"]] = relationship('Course', back_populates="department")

    # Unique constraint on name
    __table_args__ = (UniqueConstraint("abbreviation", name="departments_uk_01"),)

    def __init__(self, abbreviation: str, name: str):
        self.abbreviation = abbreviation
        self.name = name

    def add_course(self, course):
        if course not in self.courses:
            self.courses.append(course)

    def remove_course(self, course):
        if course in self.courses:
            self.courses.remove(course)

    def get_courses(self):
        return self.courses

    def __str__(self):
        return f"Department abbreviation: {self.abbreviation}, name: {self.name}, number of courses offered: {len(self.courses)}"
