DROP DATABASE IF EXISTS university;
CREATE DATABASE university;
USE university;

CREATE TABLE department (
  department_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  faculty VARCHAR(100) NOT NULL
);

CREATE TABLE programme (
  programme_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  degree_awarded VARCHAR(50) NOT NULL,
  duration_years TINYINT NOT NULL
);

CREATE TABLE lecturer (
  lecturer_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  department_id INT NOT NULL,
  FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE student (
  student_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  birth_date DATE NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  phone VARCHAR(20),
  programme_id INT NOT NULL,
  year_of_study TINYINT NOT NULL,
  graduation_status ENUM('enrolled','graduated','withdrawn') NOT NULL DEFAULT 'enrolled',
  advisor_lecturer_id INT NOT NULL,
  FOREIGN KEY (programme_id) REFERENCES programme (programme_id),
  FOREIGN KEY (advisor_lecturer_id) REFERENCES lecturer (lecturer_id)
);

CREATE TABLE staff (
  staff_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  job_title VARCHAR(100) NOT NULL,
  department_id INT NOT NULL,
  employment_type ENUM('full-time','part-time') NOT NULL,
  contract_end_date DATE,
  salary DECIMAL(10,2) NOT NULL,
  emergency_contact_name VARCHAR(100) NOT NULL,
  emergency_contact_phone VARCHAR(20) NOT NULL,
  FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE course (
  course_id INT AUTO_INCREMENT PRIMARY KEY,
  course_code VARCHAR(10) NOT NULL UNIQUE,
  name VARCHAR(100) NOT NULL,
  description TEXT,
  department_id INT NOT NULL,
  level TINYINT NOT NULL,
  credits TINYINT NOT NULL,
  schedule VARCHAR(50),
  FOREIGN KEY (department_id) REFERENCES department (department_id)
);

CREATE TABLE society (
  society_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE committee (
  committee_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE research_group (
  research_group_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL UNIQUE,
  head_lecturer_id INT NOT NULL UNIQUE,
  FOREIGN KEY (head_lecturer_id) REFERENCES lecturer (lecturer_id)
);

CREATE TABLE project (
  project_id INT AUTO_INCREMENT PRIMARY KEY,
  title VARCHAR(200) NOT NULL,
  lead_lecturer_id INT NOT NULL,
  research_group_id INT NOT NULL,
  FOREIGN KEY (lead_lecturer_id) REFERENCES lecturer (lecturer_id),
  FOREIGN KEY (research_group_id) REFERENCES research_group (research_group_id)
);

CREATE TABLE publication (
  publication_id INT AUTO_INCREMENT PRIMARY KEY,
  lecturer_id INT NOT NULL,
  project_id INT,
  title VARCHAR(200) NOT NULL,
  published_date DATE NOT NULL,
  FOREIGN KEY (lecturer_id) REFERENCES lecturer (lecturer_id),
  FOREIGN KEY (project_id) REFERENCES project (project_id)
);

CREATE TABLE student_disciplinary_record (
  student_disciplinary_record_id INT AUTO_INCREMENT PRIMARY KEY,
  student_id INT NOT NULL,
  incident_date DATE NOT NULL,
  description TEXT NOT NULL,
  FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE
);

CREATE TABLE lecturer_qualification (
  lecturer_id INT NOT NULL,
  qualification VARCHAR(150) NOT NULL,
  PRIMARY KEY (lecturer_id, qualification),
  FOREIGN KEY (lecturer_id) REFERENCES lecturer (lecturer_id) ON DELETE CASCADE
);

CREATE TABLE lecturer_expertise (
  lecturer_id INT NOT NULL,
  expertise VARCHAR(100) NOT NULL,
  PRIMARY KEY (lecturer_id, expertise),
  FOREIGN KEY (lecturer_id) REFERENCES lecturer (lecturer_id) ON DELETE CASCADE
);

CREATE TABLE lecturer_research_interest (
  lecturer_id INT NOT NULL,
  research_interest VARCHAR(100) NOT NULL,
  PRIMARY KEY (lecturer_id, research_interest),
  FOREIGN KEY (lecturer_id) REFERENCES lecturer (lecturer_id) ON DELETE CASCADE
);

CREATE TABLE department_research_area (
  department_id INT NOT NULL,
  research_area VARCHAR(100) NOT NULL,
  PRIMARY KEY (department_id, research_area),
  FOREIGN KEY (department_id) REFERENCES department (department_id) ON DELETE CASCADE
);

CREATE TABLE course_prerequisite (
  course_id INT NOT NULL,
  prerequisite_course_id INT NOT NULL,
  PRIMARY KEY (course_id, prerequisite_course_id),
  FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE,
  FOREIGN KEY (prerequisite_course_id) REFERENCES course (course_id)
);

CREATE TABLE course_material (
  course_id INT NOT NULL,
  material VARCHAR(150) NOT NULL,
  PRIMARY KEY (course_id, material),
  FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE
);

CREATE TABLE project_funding (
  project_id INT NOT NULL,
  funding_source VARCHAR(100) NOT NULL,
  PRIMARY KEY (project_id, funding_source),
  FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE
);

CREATE TABLE project_outcome (
  project_id INT NOT NULL,
  outcome VARCHAR(200) NOT NULL,
  PRIMARY KEY (project_id, outcome),
  FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE
);

CREATE TABLE student_course (
  student_id INT NOT NULL,
  course_id INT NOT NULL,
  grade DECIMAL(5,2) CONSTRAINT grade_range CHECK (grade BETWEEN 0 AND 100),
  PRIMARY KEY (student_id, course_id),
  FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE,
  FOREIGN KEY (course_id) REFERENCES course (course_id)
);

CREATE TABLE lecturer_course (
  lecturer_id INT NOT NULL,
  course_id INT NOT NULL,
  PRIMARY KEY (lecturer_id, course_id),
  FOREIGN KEY (lecturer_id) REFERENCES lecturer (lecturer_id),
  FOREIGN KEY (course_id) REFERENCES course (course_id) ON DELETE CASCADE
);

CREATE TABLE programme_course (
  programme_id INT NOT NULL,
  course_id INT NOT NULL,
  PRIMARY KEY (programme_id, course_id),
  FOREIGN KEY (programme_id) REFERENCES programme (programme_id) ON DELETE CASCADE,
  FOREIGN KEY (course_id) REFERENCES course (course_id)
);

CREATE TABLE student_society (
  student_id INT NOT NULL,
  society_id INT NOT NULL,
  PRIMARY KEY (student_id, society_id),
  FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE,
  FOREIGN KEY (society_id) REFERENCES society (society_id) ON DELETE CASCADE
);

CREATE TABLE lecturer_committee (
  lecturer_id INT NOT NULL,
  committee_id INT NOT NULL,
  PRIMARY KEY (lecturer_id, committee_id),
  FOREIGN KEY (lecturer_id) REFERENCES lecturer (lecturer_id) ON DELETE CASCADE,
  FOREIGN KEY (committee_id) REFERENCES committee (committee_id) ON DELETE CASCADE
);

CREATE TABLE project_student (
  project_id INT NOT NULL,
  student_id INT NOT NULL,
  PRIMARY KEY (project_id, student_id),
  FOREIGN KEY (project_id) REFERENCES project (project_id) ON DELETE CASCADE,
  FOREIGN KEY (student_id) REFERENCES student (student_id) ON DELETE CASCADE
);