import json
import re
import csv
from datetime import datetime
import os

DATA_FILE = "contacts_data.json"

# ---------------- VALIDATION FUNCTIONS ---------------- #

def validate_phone(phone):
    digits = re.sub(r'\D', '', phone)
    if 10 <= len(digits) <= 15:
        return True, digits
    return False, None

def validate_email(email):
    if email == "":
        return True
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

# ---------------- FILE OPERATIONS ---------------- #

def load_contacts():
    try:
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r") as f:
                content = f.read().strip()
                if not content:
                    return {}
                return json.loads(content)
    except json.JSONDecodeError:
        print("⚠️ Invalid JSON file detected. Resetting contacts.")
        return {}
    return {}


def save_contacts(contacts):
    with open(DATA_FILE, 'w') as f:
        json.dump(contacts, f, indent=4)

# ---------------- CRUD OPERATIONS ---------------- #

def add_contact(contacts):
    name = input("Enter contact name: ").strip()
    if not name:
        print("❌ Name cannot be empty")
        return

    if name in contacts:
        print("⚠️ Contact already exists!")
        return

    while True:
        phone = input("Enter phone number: ")
        valid, phone = validate_phone(phone)
        if valid:
            break
        print("❌ Invalid phone number")

    while True:
        email = input("Enter email (optional): ")
        if validate_email(email):
            break
        print("❌ Invalid email")

    group = input("Group (Friends/Work/Family/Other): ") or "Other"

    contacts[name] = {
        "phone": phone,
        "email": email or None,
        "group": group,
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }

    save_contacts(contacts)
    print(f"✅ Contact '{name}' added successfully")

def search_contact(contacts):
    term = input("Enter name to search: ").lower()
    results = {k:v for k,v in contacts.items() if term in k.lower()}

    if not results:
        print("❌ No contacts found")
        return

    for name, info in results.items():
        print(f"\n👤 {name}")
        print(f"📞 {info['phone']}")
        print(f"📧 {info['email']}")
        print(f"👥 {info['group']}")

def update_contact(contacts):
    name = input("Enter contact name to update: ")
    if name not in contacts:
        print("❌ Contact not found")
        return

    phone = input("New phone (press Enter to skip): ")
    if phone:
        valid, phone = validate_phone(phone)
        if valid:
            contacts[name]["phone"] = phone

    email = input("New email (press Enter to skip): ")
    if email and validate_email(email):
        contacts[name]["email"] = email

    contacts[name]["updated_at"] = datetime.now().isoformat()
    save_contacts(contacts)
    print("✅ Contact updated")

def delete_contact(contacts):
    name = input("Enter contact name to delete: ")
    if name in contacts:
        confirm = input("Are you sure? (y/n): ")
        if confirm.lower() == 'y':
            del contacts[name]
            save_contacts(contacts)
            print("✅ Contact deleted")
    else:
        print("❌ Contact not found")

def display_all(contacts):
    if not contacts:
        print("No contacts available")
        return
    for name, info in contacts.items():
        print(f"\n👤 {name}")
        print(f"📞 {info['phone']}")
        print(f"📧 {info['email']}")
        print(f"👥 {info['group']}")

def export_csv(contacts):
    with open("contacts_export.csv", "w", newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Name", "Phone", "Email", "Group"])
        for name, info in contacts.items():
            writer.writerow([name, info['phone'], info['email'], info['group']])
    print("✅ Contacts exported to CSV")

def statistics(contacts):
    print(f"Total Contacts: {len(contacts)}")
    groups = {}
    for c in contacts.values():
        groups[c["group"]] = groups.get(c["group"], 0) + 1
    for g, count in groups.items():
        print(f"{g}: {count}")

# ---------------- MENU ---------------- #

def main_menu():
    contacts = load_contacts()

    while True:
        print("\n========= CONTACT MANAGEMENT SYSTEM =========")
        print("1. Add Contact")
        print("2. Search Contact")
        print("3. Update Contact")
        print("4. Delete Contact")
        print("5. View All Contacts")
        print("6. Export to CSV")
        print("7. View Statistics")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == '1': add_contact(contacts)
        elif choice == '2': search_contact(contacts)
        elif choice == '3': update_contact(contacts)
        elif choice == '4': delete_contact(contacts)
        elif choice == '5': display_all(contacts)
        elif choice == '6': export_csv(contacts)
        elif choice == '7': statistics(contacts)
        elif choice == '8':
            save_contacts(contacts)
            print("👋 Exiting... Contacts Saved.")
            break
        else:
            print("❌ Invalid choice")

if __name__ == "__main__":
    main_menu()
