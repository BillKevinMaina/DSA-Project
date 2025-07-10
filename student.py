import json
from collections import deque
from datetime import datetime


class Student:
    def __init__(self, name, id_no, email, grade=None):
        self.name = name
        self.id_no = id_no
        self.grade = grade
        self.email = email
        self.entry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.grades = {}

    def to_dict(self):
        return {
            'type': 'Student',
            'name': self.name,
            'id_no': self.id_no,
            'grade': self.grade,
            'email': self.email,
            'entry_date': self.entry_date,
            'grades': self.grades,
        }
    
    def add_grade(self, subject, grade):
        if subject not in self.grades:
            self.grades[subject] = []
        self.grades[subject].append({
            'grade': grade,
            'date': datetime.now().isoformat()
        })
        self.calculate_gpa()

    def calculate_gpa(self):
        total = 0
        count = 0
        for subject_grades in self.grades.values():
            for entry in subject_grades:
                try:
                    total += float(entry['grade'])
                    count += 1
                except ValueError:
                    continue  # skip if grade is not a number
        self.grade = round(total / count, 2) if count else None


class Teacher:
    def __init__(self, name, emp_id, subject, department, email):
        self.name = name
        self.emp_id = emp_id
        self.subject = subject
        self.department = department
        self.email = email
        self.entry_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            'type': 'Teacher',
            'name': self.name,
            'emp_id': self.emp_id,
            'subject': self.subject,
            'department': self.department,
            'email': self.email,
            'entry_date': self.entry_date
        }


# Global record queue for students and teachers
record_queue = deque()


def add_student():
    name = input("Enter student name: ")
    id_no = input("Enter admission/id number: ")
    email = input("Kindly input the student school email")
    student = Student(name, id_no, email)
    
    record_queue.append(student)
    print(f" Student '{name}' added successfully.\n")


def add_teacher():
    name = input("Enter teacher's name: ")
    emp_id = input("Enter teacher's ID: ")
    subject = input("Enter subject: ")
    email = input("Enter the teacher's email: ")
    teacher = Teacher(name, emp_id, subject, None, email)
    record_queue.append(teacher)
    print(f"✅ Teacher '{name}' added successfully.\n")


def grade_student():
    id_no = input("Enter admission/id number of student to grade: ")
    found = False
    for item in record_queue:
        if isinstance(item, Student) and item.id_no == id_no:
            grade = input("Enter grade: ")
            item.grade = grade
            print(f"✅ Grade updated for student '{item.name}' to {grade}, .\n")
            found = True
            break
    if not found:
        print("❌ Student not found.\n")


def view_all_records():
    if not record_queue:
        print("📂 No records found.\n")
        return
    print(" All Records ")
    for i, item in enumerate(record_queue, start=1):
        data = item.to_dict()
        print(
            f"{i}. {data['type']}: {data['name']} - "
            f"{data.get('id_no', data.get('emp_id'))} - "
            f"Date: {data['entry_date']} - "
            f"Grade: {data.get('grade', '')}"
        )
    print()


def save_records(filename="records.json"):
    with open(filename, "w") as f:
        json.dump([item.to_dict() for item in record_queue], f, indent=4)
    print("💾 Records saved successfully.\n")


def load_records(filename="records.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            for item in data:
                if item['type'] == 'Student':
                    student = Student(
                        item['name'],
                        item['id_no'],
                        item['grade'],
                        item['email']
                    )
                    student.entry_date = item['entry_date']
                    record_queue.append(student)
                elif item['type'] == 'Teacher':
                    teacher = Teacher(
                        item['name'],
                        item['emp_id'],
                        item['subject'],
                        item['Department'],
                        item['email']
                    )
                    teacher.entry_date = item['entry_date']
                    record_queue.append(teacher)
        print("📂 Records loaded successfully.\n")
    except FileNotFoundError:
        print("⚠️ No saved records found. Starting fresh.\n")


def main():
    load_records()
    while True:
        print("====== Grading & Record Queue System ======")
        print("1. Add Student")
        print("2. Add Teacher")
        print("3. Grade Student")
        print("4. View All Records")
        print("5. Save Records")

        print("6. Exit")
        choice = input("Enter your choice (1-6): ")

        if choice == '1':
            add_student()
        elif choice == '2':
            add_teacher()
        elif choice == '3':
            grade_student()
        elif choice == '4':
            view_all_records()
        elif choice == '5':
            save_records()
        elif choice == '6':
            save_records()
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()
