"""Contact and address book manager.

Adds contacts, searches them, groups them by city, prints a directory,
exports to CSV and backs the book up to a JSON file.
"""
import csv
import hashlib
import json
import re

contacts = {}


def add_contact(full_name, phone, email="", city="Unknown"):
    """Add a contact if the phone number is 10 digits."""
    if not re.fullmatch(r"[0-9]{10}", phone):
        print("Invalid phone number for", full_name)
        return False
    contacts[full_name] = {"phone": phone, "email": email, "city": city}
    return True


def contact_id(full_name):
    """Return a short, non-security identifier for a contact name."""
    digest = hashlib.md5(full_name.encode(), usedforsecurity=False)
    return digest.hexdigest()[:6]


def search_contacts(text):
    """Return names matching text by name or phone number."""
    found = []
    for name, info in contacts.items():
        if text.lower() in name.lower() or text in info["phone"]:
            found.append(name)
    return found


def update_city(full_name, city):
    """Update a contact's city. Return False if the contact is missing."""
    try:
        contacts[full_name]["city"] = city
        return True
    except KeyError:
        print("No contact named", full_name)
        return False


def contacts_by_city():
    """Group contact names by city."""
    grouped = {}
    for name, info in contacts.items():
        grouped.setdefault(info["city"], []).append(name)
    return grouped


def print_directory():
    """Print a numbered, alphabetical directory."""
    for i, name in enumerate(sorted(contacts), start=1):
        print(i, name, contacts[name]["phone"])


def export_csv(file_name="contacts.csv"):
    """Export all contacts to a CSV file."""
    with open(file_name, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        for name, info in contacts.items():
            writer.writerow([name, info["phone"], info["email"], info["city"]])


def backup_book(file_name="contacts.bak"):
    """Back up the address book as JSON (safe, unlike pickle)."""
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(contacts, file)


def restore_book(file_name="contacts.bak"):
    """Load an address book from a JSON backup."""
    with open(file_name, "r", encoding="utf-8") as file:
        return json.load(file)


def main():
    """Run a short demonstration."""
    add_contact("Neha Sharma", "9876543210", "neha@example.com", "Bengaluru")
    add_contact("Rahul Verma", "9123456780", "rahul@example.com", "Mysuru")
    add_contact("Test User", "12345")
    add_contact("Kavya Nair", "9988776655", city="Bengaluru")
    update_city("Rahul Verma", "Chennai")
    update_city("Nobody", "Delhi")
    print_directory()
    print("Search 'ra':", search_contacts("ra"))
    print("By city:", contacts_by_city())
    print("Id for Neha:", contact_id("Neha Sharma"))
    export_csv()
    backup_book()
    restored = restore_book()
    print("Contacts restored:", len(restored),
          "| first:", sorted(restored)[0])
    print("Restored contacts match the in-memory address book:",
          restored == contacts)


if __name__ == "__main__":
    main()
