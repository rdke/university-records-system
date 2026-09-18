from django.contrib import admin

from .models import (
	Course,
	Department,
	DisciplinaryRecord,
	Enrollment,
	Lecturer,
	LecturerQualification,
	Programme,
	ResearchProject,
	Staff,
	Student,
)


admin.site.register(
	[
		Course,
		Department,
		DisciplinaryRecord,
		Enrollment,
		Lecturer,
		LecturerQualification,
		Programme,
		ResearchProject,
		Staff,
		Student,
	]
)
