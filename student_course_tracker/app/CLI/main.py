# app/main.py

import sys
import time
import subprocess

BANNER = """
=============================================
   🎓 Student Course and Performance Tracker
=============================================
"""

def show_about():
    print("\n📘 ABOUT THE SYSTEM")
    print("---------------------------------------------")
    print("This is a CLI-based Student Course and Performance Tracker system.")
    print("It helps manage student enrollments, track performance, and assign teachers.")
    print("Admins oversee approvals, while teachers monitor their students' progress.\n")
    input("Press Enter to go back to the Home Menu...")

def show_contact():
    print("\n📞 CONTACT INFORMATION")
    print("---------------------------------------------")
    print("Developed by: MCA Team")
    print("Email: support@studenttracker.edu")
    print("Version: 1.0.0")
    print("Last Updated: November 2025\n")
    input("Press Enter to go back to the Home Menu...")

def open_login_menu():
    """
    Calls the login system (from login.py)
    You can use subprocess or import depending on your design preference.
    """
    print("\n🔐 Redirecting to Login/Sign-Up system...\n")
    time.sleep(1)
    subprocess.run(["python3", "-m", "app.CLI.login"])

def show_home():
    while True:
        print(BANNER)
        print("1️⃣  About the System")
        print("2️⃣  Contact")
        print("3️⃣  Login / Sign Up")
        print("4️⃣  Exit\n")

        choice = input("Enter your choice (1–4): ").strip()

        if choice == "1":
            show_about()
        elif choice == "2":
            show_contact()
        elif choice == "3":
            open_login_menu()
        elif choice == "4":
            print("\n👋 Exiting the system. Goodbye!\n")
            sys.exit(0)
        else:
            print("\n❌ Invalid choice. Please try again.\n")
            time.sleep(1)

if __name__ == "__main__":
    show_home()
