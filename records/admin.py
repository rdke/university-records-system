from django.contrib import admin

from .models import (
	Course,
	CourseMaterial,
	Department,
	DepartmentResearchArea,
	DisciplinaryRecord,
	Enrollment,
	Lecturer,
	LecturerExpertise,
	LecturerQualification,
	LecturerResearchInterest,
	Committee,
	Publication,
	Programme,
	ProjectFunding,
	ProjectOutcome,
	ResearchGroup,
	ResearchProject,
	Society,
	Staff,
	Student,
)


admin.site.register(
	[
		Committee,
		Course,
		CourseMaterial,
		Department,
		DepartmentResearchArea,
		DisciplinaryRecord,
		Enrollment,
		Lecturer,
		LecturerExpertise,
		LecturerQualification,
		LecturerResearchInterest,
		Publication,
		Programme,
		ProjectFunding,
		ProjectOutcome,
		ResearchGroup,
		ResearchProject,
		Society,
		Staff,
		Student,
	]
)
