DETAILED THE OVERVIEW OF contact management system using C++

This project implements a contact management system using C++ that stores two types of contacts: Family and Work. Each contact is added dynamically to a list and assigned to a group. The system allows for the display of all contacts and grouped contacts using object-oriented principles like inheritance, polymorphism, and dynamic memory allocation.
The Following are main features:
Struct Contact
Stores contact name and phone number.
Abstract Base Class ContactBase
Declares a pure virtual function display() for polymorphic behavior.
Derived Classes:
FamilyContact: Includes an additional relation field.
WorkContact: Includes an additional position field.
Struct Group
Manages a dynamic array of ContactBase* for group members.
Main Features Implemented:
Add family or work contact via user input
Automatically assign contacts to a default group
Display all contacts
Display group members
The followings are explanation of line-by-line of these projects:
class ContactBase {
public:
    virtual void display() = 0;
    virtual const char* getName() = 0;
    virtual ~ContactBase() {}
};
ContactBase is an abstract class (cannot be instantiated).

display(): A pure virtual function for showing contact info.

getName(): Another pure virtual function used to get the contact’s name (useful for search/removal).

~ContactBase(): A virtual destructor to ensure derived class memory is released correctly.
class FamilyContact : public ContactBase {
    Contact* info;
    char relation[20];
public:
    FamilyContact(const char* name, const char* phone, const char* rel) {
        info = new Contact;
        strcpy(info->name, name);
        strcpy(info->phone, phone);
        strcpy(relation, rel);
    }
Inherits from ContactBase.

Has an additional field relation to describe family relation.

Dynamically allocates a Contact object and sets its fields using strcpy().
void display() override {
        cout << "[FAMILY] Name: " << info->name << ", Phone: " << info->phone
             << ", Relation: " << relation << endl;
    }
display() overrides the base class method and prints all family contact info.
const char* getName() override {
        return info->name;
    }
getName() allows access to the name for comparison or display
~FamilyContact() {
        delete info;
    }
};
Destructor frees the dynamically allocated Contact memory.
class WorkContact : public ContactBase {
    Contact* info;
    char position[20];
Inherits from ContactBase.

Adds position to store job title or role.

public:
    WorkContact(const char* name, const char* phone, const char* pos) {
        info = new Contact;
        strcpy(info->name, name);
        strcpy(info->phone, phone);
        strcpy(position, pos);
    }
Initializes contact info and position field using input data.

    void display() override {
        cout << "[WORK] Name: " << info->name << ", Phone: " << info->phone
             << ", Position: " << position << endl;
    }

    const char* getName() override {
        return info->name;
    }

    ~WorkContact() {
        delete info;
    }
};
Same as FamilyContact, but for work-related data.
Group Struct
struct Group {
    char name[20];
    ContactBase** members;
    int memberCount;
Group holds a name, a list of members (pointers to ContactBase), and how many members are in it.

    Group(const char* gname) {
        strcpy(name, gname);
        members = nullptr;
        memberCount = 0;
    }
Constructor initializes the group name and sets member list to empty.
    void addMember(ContactBase* contact) {
        ContactBase** temp = new ContactBase*[memberCount + 1];
        for (int i = 0; i < memberCount; i++) {
            temp[i] = members[i];
        }
        temp[memberCount] = contact;
        delete[] members;
        members = temp;
        memberCount++;
    }
Adds a contact to the group:

Creates a bigger array,

Copies old members,

Adds the new member,

Deletes the old array,

Replaces it with the new one.

    void displayGroup() {
        cout << "Group: " << name << endl;
        for (int i = 0; i < memberCount; i++) {
            members[i]->display();
        }
    }

    ~Group() {
        delete[] members;
    }
};
displayGroup() shows all members in the group.

Destructor deletes the array of pointers.

 Main Function

int main() {
    ContactBase** allContacts = nullptr;
    int contactCount = 0;
    Group* group = nullptr;
allContacts: A dynamic array to hold all contacts.

contactCount: Tracks how many contacts are stored.
group: A pointer to the group (we only use one default group in this version).
    int choice;
    char name[30], phone[15], extra[20], groupName[20];
Input buffers for user data.
    allContacts = new ContactBase*[100]; // max 100 contacts
    group = new Group("DefaultGroup");
Allocates space for 100 contacts.

Creates a default group named "DefaultGroup".
    do {
        cout << "\n1. Add Family Contact\n2. Add Work Contact\n3. Display Contacts\n4. Display Group\n5. Exit\nEnter choice: ";
        cin >> choice;
        cin.ignore();
Shows options to the user.

cin.ignore() clears input buffer for getline().
Add Family Contact
        if (choice == 1) {
            cout << "Enter Name: ";
            cin.getline(name, 30);
            cout << "Enter Phone: ";
            cin.getline(phone, 15);
            cout << "Enter Relation: ";
            cin.getline(extra, 20);

            allContacts[contactCount] = new FamilyContact(name, phone, extra);
            group->addMember(allContacts[contactCount]);
            contactCount++;
        }
Prompts user to input name, phone, and relation.
Creates a FamilyContact object.
Adds it to allContacts and the group.
 Add Work Contact
        else if (choice == 2) {
            cout << "Enter Name: ";
            cin.getline(name, 30);
            cout << "Enter Phone: ";
            cin.getline(phone, 15);
            cout << "Enter Position: ";
            cin.getline(extra, 20);

            allContacts[contactCount] = new WorkContact(name, phone, extra);
            group->addMember(allContacts[contactCount]);
            contactCount++;
        }
Similar to above, but for work contacts.
Display Contact
 else if (choice == 3) {
            cout << "\n--- All Contacts ---\n";
            for (int i = 0; i < contactCount; i++) {
                allContacts[i]->display();
            }
        }
Loops through and calls display() on each contact.
 Display Group
   else if (choice == 4) {
            cout << "\n--- Group Contacts ---\n";
            group->displayGroup();
        }
Shows all group members using displayGroup().
Exit and Clean-Up
    } while (choice != 5);
  for (int i = 0; i < contactCount; i++)
        delete allContacts[i];
    delete[] allContacts;
    delete group;
 return 0;
}
Loop runs until the user selects "5. Exit".
All dynamically allocated memory is deleted to prevent memory leaks.


![Screenshot 2025-06-19 115740](https://github.com/user-attachments/assets/b1b02035-2276-469d-b86d-0eed2ad315eb)


