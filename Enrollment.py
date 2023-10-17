from orm_base import Base
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

class Enrollment(Base):
    __tablename__ = 'enrollments'

    student_id = Column(Integer, ForeignKey('students.student_id'), primary_key=True)
    section_id = Column(Integer, ForeignKey('sections.section_id'), primary_key=True)
    # Add any additional fields for Enrollment if needed

    student = relationship("Student", back_populates="enrollments")
    section = relationship("Section", back_populates="enrollments")
