import json
from collections import deque
from datetime import datetime


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


# Global record queue for teachers
record_queue = deque()


def add_teacher():
    name = input("Enter teacher's name: ")
    emp_id = input("Enter teacher's ID: ")
    subject = input("Enter subject: ")
    department = input("Enter department: ")
    email = input("Enter the teacher's email: ")
    teacher = Teacher(name, emp_id, subject, department, email)
    record_queue.append(teacher)
    print(f"✅ Teacher '{name}' added successfully.\n")


def view_all_records():
    if not record_queue:
        print("📂 No records found.\n")
        return
    print(" All Teacher Records ")
    for i, teacher in enumerate(record_queue, start=1):
        data = teacher.to_dict()
        print(
            f"{i}. Teacher: {data['name']} - "
            f"ID: {data['emp_id']} - "
            f"Subject: {data['subject']} - "
            f"Department: {data['department']} - "
            f"Email: {data['email']} - "
            f"Date: {data['entry_date']}"
        )
    print()


def save_records(filename="teacher_records.json"):
    with open(filename, "w") as f:
        json.dump([teacher.to_dict() for teacher in record_queue], f, indent=4)
    print("💾 Records saved successfully.\n")


def load_records(filename="teacher_records.json"):
    try:
        with open(filename, "r") as f:
            data = json.load(f)
            record_queue.clear()
            for item in data:
                if item['type'] == 'Teacher':
                    teacher = Teacher(
                        item['name'],
                        item['emp_id'],
                        item['subject'],
                        item['department'],
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
        print("====== Teacher Record Management System ======")
        print("1. Add Teacher")
        print("2. View All Records")
        print("3. Save Records")
        print("4. Exit")
        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            add_teacher()
        elif choice == '2':
            view_all_records()
        elif choice == '3':
            save_records()
        elif choice == '4':
            save_records()
            print("👋 Exiting. Goodbye!")
            break
        else:
            print("❌ Invalid choice. Try again.\n")


if __name__ == "__main__":
    main()