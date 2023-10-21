from orm_base import Base
from sqlalchemy import Integer, String, ForeignKey, Column, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from Enrollment import Enrollment

class Section(Base):
    """Represents a course section in a specific semester and year."""
    __tablename__ = "sections"
    section_id: Mapped[int] = mapped_column(primary_key=True)
    department_abbreviation: Mapped[str] = mapped_column(String(50), nullable=False)
    course_number: Mapped[int] = mapped_column(Integer, nullable=False)
    section_number: Mapped[int] = mapped_column(Integer, nullable=False)
    section_year: Mapped[int] = mapped_column(Integer, nullable=False)
    semester: Mapped[str] = mapped_column(String(50), nullable=False)

    # Relationships
    enrollments: Mapped[List["Enrollment"]] = relationship("Enrollment", back_populates="section")

    def __init__(self, department_abbreviation, course_number, section_number, section_year, semester):
        self.department_abbreviation = department_abbreviation
        self.course_number = course_number
        self.section_number = section_number
        self.section_year = section_year
        self.semester = semester

    def add_student(self, student):
        """Enroll a student in this section."""
        from Enrollment import Enrollment  # Avoiding cyclic imports
        enrollment = Enrollment(student=student, section=self)
        self.enrollments.append(enrollment)

    def has_student(self, student):
        """Check if a student is enrolled in this section."""
        return any(e.student == student for e in self.enrollments)

    def get_enrolled_students(self):
        """Get all students enrolled in this section."""
        return [e.student for e in self.enrollments]

    def remove_enrollment(self, student, session):
        """Remove an enrollment of a student from this section."""
        for enrollment in self.enrollments:
            if enrollment.student == student:
                self.enrollments.remove(enrollment)
                session.delete(enrollment)
                session.commit()
                break

    def has_enrollments(self):
        """Check if the section has any enrollments."""
        return bool(self.enrollments)

    def __str__(self):
        return f"{self.department_abbreviation} {self.course_number} - Section {self.section_number} ({self.semester} {self.section_year})"
