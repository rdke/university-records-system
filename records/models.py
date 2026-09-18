from django.db import models


class Department(models.Model):
	name = models.CharField(max_length=100, unique=True)
	faculty = models.CharField(max_length=100)

	def __str__(self):
		return self.name


class Programme(models.Model):
	name = models.CharField(max_length=100, unique=True)
	degree_awarded = models.CharField(max_length=50)
	duration_years = models.PositiveSmallIntegerField()

	def __str__(self):
		return self.name


class Lecturer(models.Model):
	name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	department = models.ForeignKey(Department, on_delete=models.PROTECT)

	def __str__(self):
		return self.name


class Student(models.Model):
	class GraduationStatus(models.TextChoices):
		ENROLLED = 'enrolled', 'Enrolled'
		GRADUATED = 'graduated', 'Graduated'
		WITHDRAWN = 'withdrawn', 'Withdrawn'

	name = models.CharField(max_length=100)
	birth_date = models.DateField()
	email = models.EmailField(unique=True)
	phone = models.CharField(max_length=20, blank=True)
	programme = models.ForeignKey(Programme, on_delete=models.PROTECT)
	year_of_study = models.PositiveSmallIntegerField()
	graduation_status = models.CharField(
		max_length=10,
		choices=GraduationStatus.choices,
		default=GraduationStatus.ENROLLED,
	)
	advisor = models.ForeignKey(Lecturer, on_delete=models.PROTECT)

	def __str__(self):
		return self.name


class Staff(models.Model):
	class EmploymentType(models.TextChoices):
		FULL_TIME = 'full-time', 'Full-time'
		PART_TIME = 'part-time', 'Part-time'

	name = models.CharField(max_length=100)
	job_title = models.CharField(max_length=100)
	department = models.ForeignKey(Department, on_delete=models.PROTECT)
	employment_type = models.CharField(max_length=10, choices=EmploymentType.choices)
	contract_end_date = models.DateField(blank=True, null=True)
	salary = models.DecimalField(max_digits=10, decimal_places=2)

	def __str__(self):
		return self.name


class Course(models.Model):
	course_code = models.CharField(max_length=10, unique=True)
	name = models.CharField(max_length=100)
	description = models.TextField(blank=True)
	department = models.ForeignKey(Department, on_delete=models.PROTECT)
	programmes = models.ManyToManyField(Programme, related_name='courses', blank=True)
	lecturers = models.ManyToManyField(Lecturer, related_name='courses', blank=True)
	prerequisites = models.ManyToManyField('self', symmetrical=False, blank=True)
	level = models.PositiveSmallIntegerField()
	credits = models.PositiveSmallIntegerField()
	schedule = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return f'{self.course_code} - {self.name}'


class Enrollment(models.Model):
	student = models.ForeignKey(Student, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	grade = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

	class Meta:
		constraints = [
			models.UniqueConstraint(fields=['student', 'course'], name='unique_enrollment'),
			models.CheckConstraint(condition=models.Q(grade__gte=0) & models.Q(grade__lte=100), name='grade_range'),
		]

	def __str__(self):
		return f'{self.student} - {self.course.course_code}'


class ResearchProject(models.Model):
	title = models.CharField(max_length=200)
	lead_lecturer = models.ForeignKey(Lecturer, on_delete=models.PROTECT)
	students = models.ManyToManyField(
		Student,
		related_name='research_projects',
		blank=True,
	)
	funding_source = models.CharField(max_length=100, blank=True)

	def __str__(self):
		return self.title


class LecturerQualification(models.Model):
	lecturer = models.ForeignKey(Lecturer, on_delete=models.CASCADE)
	qualification = models.CharField(max_length=150)

	class Meta:
		constraints = [
			models.UniqueConstraint(
				fields=['lecturer', 'qualification'],
				name='unique_lecturer_qualification',
			),
		]

	def __str__(self):
		return f'{self.lecturer} - {self.qualification}'


class DisciplinaryRecord(models.Model):
	student = models.ForeignKey(
		Student,
		on_delete=models.CASCADE,
		related_name='disciplinary_records',
	)
	incident_date = models.DateField()
	description = models.TextField()

	def __str__(self):
		return f'{self.student} - {self.incident_date}'
