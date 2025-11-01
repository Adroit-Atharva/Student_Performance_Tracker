# app/controllers/student_controller.py

def student_menu(student_id):
    print(f"\n=== Student Dashboard ===")
    print(f"Logged in as Student ID: {student_id}")

    while True:
        print("\nSelect an option:")
        print("1. View Profile")
        print("2. View Courses")
        print("3. View Performance")
        print("4. Logout")

        choice = input("Enter choice: ").strip()

        if choice == "1":
            print(f"📘 Showing profile for Student ID {student_id}...")
            # Later: fetch from DB
        elif choice == "2":
            print(f"📚 Showing enrolled courses for Student ID {student_id}...")
        elif choice == "3":
            print(f"📊 Showing performance report for Student ID {student_id}...")
        elif choice == "4":
            print("👋 Logging out...\n")
            break
        else:
            print("❌ Invalid choice. Try again.")
