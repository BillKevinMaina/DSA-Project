import tkinter as tk
from tkinter import ttk, messagebox
try:
    import sv_ttk
except ImportError:
    sv_ttk = None
from advanced_linked_list import SchoolSystem
from fee_manager import FeeStack
from school_map import find_shortest_path, get_locations, school_map
from student import Student, Teacher, record_queue, save_records, load_records

class SchoolApp:
    def __init__(self, root):
        self.root = root
        self.root.title("School Management System")
        self.root.geometry("800x600")
        
        # Initialize empty data structures
        self.school_system = SchoolSystem()  # Empty student list
        self.fee_stack = FeeStack()         # Empty fee stack
        try:
            load_records()  # Load existing records if available
        except:
            record_queue.clear()  # Start empty if no file exists
        
        # Apply modern theme if available
        if sv_ttk:
            sv_ttk.set_theme("light")

        # Create tabbed interface
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, padx=10, fill="both", expand=True)

        # Set up tabs
        self.create_student_tab()
        self.create_fee_tab()
        self.create_navigation_tab()
        self.create_records_tab()

    def create_student_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Student Management")

        # Input fields
        ttk.Label(tab, text="Student ID:").grid(row=0, column=0, padx=5, pady=5,
                                               sticky="e")
        self.student_id_entry = ttk.Entry(tab)
        self.student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Name:").grid(row=1, column=0, padx=5, pady=5,
                                          sticky="e")
        self.student_name_entry = ttk.Entry(tab)
        self.student_name_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Grade:").grid(row=2, column=0, padx=5, pady=5,
                                           sticky="e")
        self.student_grade_entry = ttk.Entry(tab)
        self.student_grade_entry.grid(row=2, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(tab, text="Add Student", command=self.add_student).grid(
            row=3, column=0, columnspan=2, pady=10)
        ttk.Button(tab, text="Transfer Student",
                   command=self.transfer_student).grid(
                       row=4, column=0, columnspan=2, pady=5)
        ttk.Button(tab, text="Remove Student",
                   command=self.remove_student).grid(
                       row=5, column=0, columnspan=2, pady=5)
        ttk.Button(tab, text="View Students",
                   command=self.view_students).grid(
                       row=6, column=0, columnspan=2, pady=5)

        # Output area
        self.student_output = tk.Text(tab, height=10, width=60)
        self.student_output.grid(row=7, column=0, columnspan=2, padx=5, pady=10)
        self.student_output.config(state="disabled")

    def create_fee_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Fee Management")

        # Input fields
        ttk.Label(tab, text="Student ID:").grid(row=0, column=0, padx=5, pady=5,
                                                sticky="e")
        self.fee_student_id_entry = ttk.Entry(tab)
        self.fee_student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Amount ($):").grid(row=1, column=0, padx=5, pady=5,
                                                sticky="e")
        self.fee_amount_entry = ttk.Entry(tab)
        self.fee_amount_entry.grid(row=1, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(tab, text="Add Payment", command=self.add_payment).grid(
            row=2, column=0, columnspan=2, pady=10)
        ttk.Button(tab, text="View Balance", command=self.view_balance).grid(
            row=3, column=0, columnspan=2, pady=5)
        ttk.Button(tab, text="View Payment History",
                   command=self.view_payment_history).grid(
                       row=4, column=0, columnspan=2, pady=5)

        # Output area
        self.fee_output = tk.Text(tab, height=10, width=60)
        self.fee_output.grid(row=5, column=0, columnspan=2, padx=5, pady=10)
        self.fee_output.config(state="disabled")

    def create_navigation_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="School Navigation")

        # Dropdowns
        ttk.Label(tab, text="Start Location:").grid(row=0, column=0, padx=5,
                                                    pady=5, sticky="e")
        self.start_location = ttk.Combobox(tab, values=get_locations())
        self.start_location.grid(row=0, column=1, padx=5, pady=5)
        self.start_location.set("Main Gate")

        ttk.Label(tab, text="End Location:").grid(row=1, column=0, padx=5,
                                                  pady=5, sticky="e")
        self.end_location = ttk.Combobox(tab, values=get_locations())
        self.end_location.grid(row=1, column=1, padx=5, pady=5)
        self.end_location.set("Lab")

        # Button
        ttk.Button(tab, text="Find Shortest Path", command=self.find_path).grid(
            row=2, column=0, columnspan=2, pady=10)

        # Output area
        self.nav_output = tk.Text(tab, height=10, width=60)
        self.nav_output.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        self.nav_output.config(state="disabled")

    def create_records_tab(self):
        tab = ttk.Frame(self.notebook)
        self.notebook.add(tab, text="Records Management")

        # Student form
        ttk.Label(tab, text="Student Name:").grid(row=0, column=0, padx=5,
                                                  pady=5, sticky="e")
        self.record_student_name = ttk.Entry(tab)
        self.record_student_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Student ID:").grid(row=1, column=0, padx=5, pady=5,
                                                sticky="e")
        self.record_student_id = ttk.Entry(tab)
        self.record_student_id.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Email:").grid(row=2, column=0, padx=5, pady=5,
                                        sticky="e")
        self.record_student_email = ttk.Entry(tab)
        self.record_student_email.grid(row=2, column=1, padx=5, pady=5)

        # Teacher form
        ttk.Label(tab, text="Teacher Name:").grid(row=3, column=0, padx=5,
                                                  pady=5, sticky="e")
        self.record_teacher_name = ttk.Entry(tab)
        self.record_teacher_name.grid(row=3, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Teacher ID:").grid(row=4, column=0, padx=5, pady=5,
                                                sticky="e")
        self.record_teacher_id = ttk.Entry(tab)
        self.record_teacher_id.grid(row=4, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Subject:").grid(row=5, column=0, padx=5, pady=5,
                                             sticky="e")
        self.record_teacher_subject = ttk.Entry(tab)
        self.record_teacher_subject.grid(row=5, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Department:").grid(row=6, column=0, padx=5, pady=5,
                                                sticky="e")
        self.record_teacher_dept = ttk.Entry(tab)
        self.record_teacher_dept.grid(row=6, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Email:").grid(row=7, column=0, padx=5, pady=5,
                                           sticky="e")
        self.record_teacher_email = ttk.Entry(tab)
        self.record_teacher_email.grid(row=7, column=1, padx=5, pady=5)

        # Grading form
        ttk.Label(tab, text="Grade Student ID:").grid(row=8, column=0, padx=5,
                                                      pady=5, sticky="e")
        self.grade_student_id = ttk.Entry(tab)
        self.grade_student_id.grid(row=8, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Subject:").grid(row=9, column=0, padx=5, pady=5,
                                             sticky="e")
        self.grade_subject = ttk.Entry(tab)
        self.grade_subject.grid(row=9, column=1, padx=5, pady=5)

        ttk.Label(tab, text="Grade:").grid(row=10, column=0, padx=5, pady=5,
                                           sticky="e")
        self.grade_value = ttk.Entry(tab)
        self.grade_value.grid(row=10, column=1, padx=5, pady=5)

        # Buttons
        ttk.Button(tab, text="Add Student", command=self.add_record_student).grid(
            row=11, column=0, columnspan=2, pady=5)
        ttk.Button(tab, text="Add Teacher", command=self.add_record_teacher).grid(
            row=12, column=0, columnspan=2, pady=5)
        ttk.Button(tab, text="Grade Student",
                command=self.grade_record_student).grid(
                    row=13, column=0, columnspan=2, pady=5)
        ttk.Button(tab, text="View Records", command=self.view_records).grid(
            row=14, column=0, columnspan=2, pady=5)
        ttk.Button(tab, text="Save Records", command=self.save_all_records).grid(
            row=15, column=0, columnspan=2, pady=5)

        # Output area
        self.records_output = tk.Text(tab, height=10, width=60)
        self.records_output.grid(row=16, column=0, columnspan=2, padx=5, pady=10)
        self.records_output.config(state="disabled")

    # Student Management Methods
    def add_student(self):
        try:
            student_id = int(self.student_id_entry.get())
            name = self.student_name_entry.get().strip()
            grade = int(self.student_grade_entry.get())
            if not name or student_id < 0 or grade < 0:
                raise ValueError("Invalid input")
            self.school_system.add_student(student_id, name, grade)
            messagebox.showinfo("Success", f"Student {name} added!")
            self.student_id_entry.delete(0, tk.END)
            self.student_name_entry.delete(0, tk.END)
            self.student_grade_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter valid ID (integer), name, and grade (integer)."
            )

    def transfer_student(self):
        try:
            student_id = int(self.student_id_entry.get())
            to_grade = int(self.student_grade_entry.get())
            if self.school_system.transfer_student(student_id, to_grade):
                messagebox.showinfo(
                    "Success",
                    f"Student ID {student_id} transferred to grade {to_grade}."
                )
            else:
                messagebox.showerror("Error", "Student not found.")
            self.student_id_entry.delete(0, tk.END)
            self.student_grade_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter valid ID and grade (integers)."
            )

    def remove_student(self):
        try:
            student_id = int(self.student_id_entry.get())
            if self.school_system.students.remove('id', student_id):
                messagebox.showinfo(
                    "Success",
                    f"Student ID {student_id} removed."
                )
            else:
                messagebox.showerror("Error", "Student not found.")
            self.student_id_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter a valid student ID (integer)."
            )

    def view_students(self):
        self.student_output.config(state="normal")
        self.student_output.delete(1.0, tk.END)
        current = self.school_system.students.head
        output = "Students:\n"
        while current:
            data = current.data
            output += (
                f"ID: {data['id']}, Name: {data['name']}, "
                f"Grade: {data['grade']}\n"
            )
            current = current.next
        self.student_output.insert(tk.END, output)
        self.student_output.config(state="disabled")

    # Fee Management Methods
    def add_payment(self):
        try:
            student_id = self.fee_student_id_entry.get().strip()
            amount = float(self.fee_amount_entry.get())
            if not student_id or amount <= 0:
                raise ValueError("Invalid input")
            self.fee_stack.push(student_id, amount)
            messagebox.showinfo(
                "Success",
                f"Payment of ${amount:.2f} added for {student_id}."
            )
            self.fee_student_id_entry.delete(0, tk.END)
            self.fee_amount_entry.delete(0, tk.END)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter valid student ID and amount (positive number)."
            )

    def view_balance(self):
        balance = self.fee_stack.get_balance()
        self.fee_output.config(state="normal")
        self.fee_output.delete(1.0, tk.END)
        self.fee_output.insert(tk.END, f"Current Balance: ${balance:.2f}\n")
        self.fee_output.config(state="disabled")

    def view_payment_history(self):
        self.fee_output.config(state="normal")
        self.fee_output.delete(1.0, tk.END)
        payments = self.fee_stack.get_all_payments()
        output = "Payment History (Newest First):\n"
        for payment in payments:
            output += (
                f"ID: {payment['student_id']}, "
                f"Amount: ${payment['amount']:.2f}, "
                f"Time: {payment['timestamp']}\n"
            )
        self.fee_output.insert(tk.END, output)
        self.fee_output.config(state="disabled")

    # Navigation Methods
    def find_path(self):
        start = self.start_location.get()
        end = self.end_location.get()
        result = find_shortest_path(school_map, start, end)
        self.nav_output.config(state="normal")
        self.nav_output.delete(1.0, tk.END)
        if result["status"] == "success":
            path = " -> ".join(result["path"])
            output = (
                f"Shortest Path: {path}\n"
                f"Distance: {result['distance']} units"
            )
        else:
            output = "No path found or invalid locations."
        self.nav_output.insert(tk.END, output)
        self.nav_output.config(state="disabled")

    # Records Management Methods
    def add_record_student(self):
        try:
            name = self.record_student_name.get().strip()
            id_no = self.record_student_id.get().strip()
            email = self.record_student_email.get().strip()
            if not name or not id_no or not email:
                raise ValueError("Invalid input")
            student = Student(name, id_no, email)
            record_queue.append(student)
            messagebox.showinfo("Success", f"Student {name} added to records.")
            self.record_student_name.delete(0, tk.END)
            self.record_student_id.delete(0, tk.END)
            self.record_student_email.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Enter valid name, ID, and email.")

    def add_record_teacher(self):
        try:
            name = self.record_teacher_name.get().strip()
            emp_id = self.record_teacher_id.get().strip()
            subject = self.record_teacher_subject.get().strip()
            dept = self.record_teacher_dept.get().strip()
            email = self.record_teacher_email.get().strip()
            if not all([name, emp_id, subject, dept, email]):
                raise ValueError("Invalid input")
            teacher = Teacher(name, emp_id, subject, dept, email)
            record_queue.append(teacher)
            messagebox.showinfo("Success", f"Teacher {name} added to records.")
            self.record_teacher_name.delete(0, tk.END)
            self.record_teacher_id.delete(0, tk.END)
            self.record_teacher_subject.delete(0, tk.END)
            self.record_teacher_dept.delete(0, tk.END)
            self.record_teacher_email.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Error", "Enter valid teacher details.")

    def grade_record_student(self):
        try:
            id_no = self.grade_student_id.get().strip()
            subject = self.grade_subject.get().strip()
            grade = float(self.grade_value.get())
            if not id_no or not subject or grade < 0:
                raise ValueError("Invalid input")
            for item in record_queue:
                if isinstance(item, Student) and item.id_no == id_no:
                    item.add_grade(subject, grade)
                    messagebox.showinfo(
                        "Success",
                        f"Grade {grade} added for {item.name} in {subject}."
                    )
                    self.grade_student_id.delete(0, tk.END)
                    self.grade_subject.delete(0, tk.END)
                    self.grade_value.delete(0, tk.END)
                    return
            messagebox.showerror("Error", "Student not found.")
        except ValueError:
            messagebox.showerror(
                "Error",
                "Enter valid ID, subject, and grade (positive number)."
            )

    def view_records(self):
        self.records_output.config(state="normal")
        self.records_output.delete(1.0, tk.END)
        output = "Records:\n"
        for i, item in enumerate(record_queue, start=1):
            data = item.to_dict()
            output += (
                f"{i}. {data['type']}: {data['name']} - "
                f"{data.get('id_no', data.get('emp_id'))} - "
                f"Date: {data['entry_date']}\n"
            )
            if 'grades' in data and data['grades']:
                output += "  Grades:\n"
                for subj, grades in data['grades'].items():
                    for g in grades:
                        output += (
                            f"    {subj}: {g['grade']} (Date: {g['date']})\n"
                        )
        self.records_output.insert(tk.END, output)
        self.records_output.config(state="disabled")

    def save_all_records(self):
        try:
            save_records()
            messagebox.showinfo("Success", "Records saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save records: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = SchoolApp(root)
    root.mainloop()