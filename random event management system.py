from abc import ABC, abstractmethod
from datetime import date
import json

class BaseObject(ABC):
    def __init__(self, entity_no):
        self.entity_no = entity_no

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def edit(self):
        pass

    @abstractmethod
    def delete(self):
        pass

class Event(BaseObject):
    def __init__(self, event_no, event_name, date, event_venue):
        super().__init__(event_no)
        self.event_no = event_no
        self.event_name = event_name
        self.date = date
        self.event_venue = event_venue
        self.attendees = []

    def create(self):
        while True:
            try:
                event_no = int(input("\nEnter Event No. : "))
                event_name = input("Enter Event name: ")
                date_str = input("Enter Event date (yyyy-mm-dd): ")
                year, month, day = map(int, date_str.split('-'))
                event_date = date(year, month, day)
                event_venue = Venue.create(Venue)
                event = Event(event_no, event_name, event_date, event_venue)
                events[event_no] = event
                print(f"\nEvent {event_no} created: {event_name}")
                break
            except ValueError:
                print("Invalid input. Please enter valid values.")

    def edit(self):
        print(f"\nEditing Event No.: {self.event_no}, Event Name: {self.event_name}, Event Date: {self.date}, Event Venue: {self.event_venue[0]}, Venue Capacity: {self.event_venue[1]}, Venue Location: {self.event_venue[2]}")
        edit_choice = input("What would you like to edit? (Name, Date, Venue, All?)").lower()
        if edit_choice == 'venue':
            # Editing venue details
            new_venue_name = input(f"Enter updated venue name ({self.event_venue[0]}): ")
            self.event_venue = (new_venue_name, self.event_venue[1], self.event_venue[2])
            print("\nEvent venue updated.")
        elif edit_choice in {'name', 'date', 'venue', 'all'}:
            # Editing name, date, venue, or all details
            if edit_choice == 'all':
                self.event_name = input(f"Updating event name from ({self.event_name}) to: ")
                self.event_date = input(f"Updating event date from ({self.event_date}) to: ")
                self.event_venue = input(f"Updating event venue from ({self.event_venue}) to: ")
            else:
                new_value = input(f"Enter updated {edit_choice} ({getattr(self, edit_choice)}): ")
                setattr(self, edit_choice, new_value)
            print("\nEvent details updated.")
        else:
            print("Invalid option.")
        
    def delete(self):
        print(f"\nEvent {self.event_no}: {self.event_name} deleted.")
        global events, attendees
        if self.event_no in events:
            del events[self.event_no]
            attendees_to_delete = [attendee_no for attendee_no, attendee in attendees.items() if attendee.event_no == self.event_no]
            for attendee_no in attendees_to_delete:
                del attendees[attendee_no]
        else:
            print("Event not found.")
             # add file handling / error handling

    @classmethod
    def from_dict(cls, event_dict):
        event_no = event_dict['event_no']
        event_name = event_dict['event_name']
        year, month, day = map(int, event_dict['date'].split('-'))
        event_date = date(year, month, day)
        event_venue = event_dict['event_venue']
        event = cls(event_no, event_name, event_date, event_venue)
        return event

class Venue(BaseObject):
    def __init__(self, venue_no, venue_name, venue_capacity, venue_location):
        super().__init__(venue_no)
        self.venue_name = venue_name
        self.venue_capacity = venue_capacity
        self.venue_location = venue_location
 
    def create(self):
        try:
            venue_name = input("Enter Venue name: ")
            while True:
                try:
                    venue_capacity = int(input("Enter Capacity of Venue: "))
                    break
                except ValueError:
                    print("Invalid input. Please enter a valid integer for capacity.")
            venue_location = input("Enter Venue location: ")
            return venue_name, venue_capacity, venue_location
        except ValueError:
            print("Invalid input. Please enter valid values.")

class Attendee(BaseObject):

    def __init__(self, attendee_no, event_no, name, phone, email):
        super().__init__(attendee_no)
        self.attendee_no = attendee_no
        self.event_no = event_no
        self.name = name
        self.phone = phone
        self.email = email

    def create(event_no):
        while True:
            event = events.get(event_no)
            try:
                if event:
                    attendee_no = int(input("\nEnter Attendee No.: "))
                    name = input("Enter Attendee name: ")
                    phone = input("Enter phone number: ")
                    email = input("Enter email: ")
                    attendee = Attendee(attendee_no, event_no, name, phone, email)
                    attendees[attendee_no] = attendee
                    event.attendees.append(attendee_no)
                    print(f"\nAttendee {attendee_no} added to Event {event_no}: {event.event_name}")
                    break
                else:
                    print("Event not found")
                    break
            except ValueError:
                print("Invalid input. Please enter valid values.")

    def edit(self):
        print(f"Editing Attendee {self.attendee_no}:")
        edit_choice = input("What would you like to edit? (Name, Phone, Email, Event, All?)").lower()
        if edit_choice in {'name', 'phone', 'email', 'event', 'all'}:
            if edit_choice == 'event':
                new_event_no = int(input(f"Updating event no from ({self.event_no}) to: "))
                if new_event_no in events:
                    old_event = events[self.event_no]
                    new_event = events[new_event_no]
                    if self.attendee_no in old_event.attendees:
                        old_event.attendees.remove(self.attendee_no)
                        new_event.attendees.append(self.attendee_no)
                        self.event_no = new_event_no
                        print(f"Attendee moved to Event {new_event_no}: {new_event.event_name}")
                    else:
                        print("Attendee not found in the current event.")
                else:
                    print("Event not found.")
            elif edit_choice == 'all':  
                self.name = input(f"\nUpdating attendee name from ({self.name}) to: ")
                self.phone = input(f"Updating phone from ({self.phone}) to: ")
                self.email = input(f"Updating email from ({self.email}) to: ")
                self.event_no = input(f"Updating event no from ({self.event_no}) to: ")
                print("\nAttendee details updated.")
            else:
                new_value = input(f"Enter updated {edit_choice} ({getattr(self, edit_choice)}): ")
                setattr(self, edit_choice, new_value)
                print("\nAttendee details updated.")
        else:
            print("Invalid option.")

    def delete(self):
        print(f"Deleting Attendee {self.attendee_no}: {self.name}")
        global attendees
        if self.attendee_no in attendees:
            del attendees[self.attendee_no]
            print("Attendee deleted.")
        else:
            print("Attendee not found.")


    @classmethod
    def from_dict(cls, attendee_dict):
        attendee_no = attendee_dict['attendee_no']
        event_no = attendee_dict['event_no']
        name = attendee_dict['name']
        phone = attendee_dict['phone']
        email = attendee_dict['email']
        attendee = cls(attendee_no, event_no, name, phone, email)
        return attendee

events = {
    1: {"event_no": 1, "event_name": "Party", "date": "2023-08-01", "event_venue": ("Park", 100, "Downtown"), "attendees": []},
    2: {"event_no": 2, "event_name": "Wedding", "date": "2023-08-15", "event_venue": ("Random Church", 150, "Downtown"), "attendees": []},
    3: {"event_no": 3, "event_name": "Halloween Party", "date": "2023-10-31", "event_venue": ("Warehouse", 150, "Downtown"), "attendees": []},
}

attendees = {
    1: {"attendee_no": 1, "event_no": 1, "name": "John Doe", "phone": "1234567890", "email": "john@example.com"},
    2: {"attendee_no": 2, "event_no": 1, "name": "Jane Smith", "phone": "9876543210", "email": "jane@example.com"},
    3: {"attendee_no": 3, "event_no": 2, "name": "Alice Johnson", "phone": "5555555555", "email": "alice@example.com"},
}

def list_attendees(event_no):
    print(f"Attendees for Event {event_no}:")
    event = events.get(event_no)
    if event:
        for attendee_no, attendee in attendees.items():
            if attendee.event_no == event_no:
                print(f"Attendee {attendee_no}: {attendee.name}")
    else:
        print("\nEvent not found.")

def list_all_events():
    for event_no, event in events.items():
        print("-------------------------------------------------------------------------------------------------")
        print(f"Event {event_no}: {event.event_name}, Venue Name: {event.event_venue[0]}, Capacity: {event.event_venue[1]}, Location: {event.event_venue[2]},  Date: {event.date}")

def list_event():
    while True:
        user_input = input("\nEnter Event No. to list: ")
        try:
            event_no = int(user_input)
            load_data_from_files()  # Load data from the files
            event = events.get(event_no)
            if event:
                print(f"Event {event.event_no}: {event.event_name}")
            else:
                print("Event not found.")
            break  # Exit the loop if everything is successful
        except ValueError:
            print("Invalid input. Please enter a valid integer for Event No.")

def load_data_from_files():
    try:
        with open("events_data.json", "r") as events_file:
            events_data = json.load(events_file)
            global events
            events = {event_no: Event.from_dict(event_data) for event_no, event_data in events_data.items()}
    except FileNotFoundError:
        print("Events data file not found. Starting with empty events dictionary.")
        events = {event_no: Event.from_dict(event_data) for event_no, event_data in events.items()}

    try:
        with open("attendees_data.json", "r") as attendees_file:
            attendees_data = json.load(attendees_file)
            global attendees
            attendees = {attendee_no: Attendee.from_dict(attendee_data) for attendee_no, attendee_data in attendees_data.items()}
    except FileNotFoundError:
        print("Attendees data file not found. Starting with empty attendees dictionary.")
        attendees = {attendee_no: Attendee.from_dict(attendee_data) for attendee_no, attendee_data in attendees.items()}

def save_data_to_files():
    with open("events_data.json", "w") as events_file:
        json.dump(events, events_file, indent=4, default=serialize_event)
    
    with open("attendees_data.json", "w") as attendees_file:
        json.dump(attendees, attendees_file, indent=4, default=serialize_attendee)

def serialize_attendee(obj):
    if isinstance(obj, Attendee):
        return {
            "attendee_no": obj.attendee_no,
            "event_no": obj.event_no,
            "name": obj.name,
            "phone": obj.phone,
            "email": obj.email
        }
    raise TypeError("Object of type Attendee is not JSON serializable")

def serialize_event(obj):
    if isinstance(obj, Event):
        return {
            "event_no": obj.event_no,
            "event_name": obj.event_name,
            "date": obj.date.strftime("%Y-%m-%d") if isinstance(obj.date, date) else obj.date, 
            "event_venue": obj.event_venue,
            "attendees": obj.attendees
        }
    raise TypeError("Object of type Event is not JSON serializable")

def main():
    load_data_from_files()
    while True:
        print("\n---------------------------")
        print("| Event Management System |")
        print("---------------------------")
        print("\n[1] List event(s)")
        print("[2] Create/Edit/Delete an event")
        print("[3] List attendees of an event")
        print("[4] Add/Delete/Edit an attendee from an event")  
        print("[E]xit")
        user_input = input("\nPlease select one of the options:\n ")

        if user_input.lower() == 'e' or user_input.lower() == 'exit':
            print("Goodbye!")
            save_data_to_files()
            break

        elif user_input == '1':
            while True:
                event_listing = input("\nDo you wish to view [E]vent or [A]ll events?\n ")
                if event_listing.lower() == 'a' or event_listing.lower() == 'all':
                    list_all_events()
                    break
                elif event_listing.lower() == 'e' or event_listing.lower() == 'event':
                    list_event()
                    break
                else:
                    print("Invalid choice.")    
                                           
        elif user_input == '2':
            user_choice = input("\nDo you wish to [C]reate, [E]dit, or [D]elete an event?\n")
            while True:
                if user_choice.lower() == 'e' or user_choice.lower() == 'edit':
                        try:
                            event_no = int(input("\nEnter Event No. to edit: "))
                            event = events.get(event_no)
                            if event:
                                event.edit()
                                break
                            else:
                                print("Event not found.")
                        except ValueError:
                            print("Invalid input. Please enter a valid integer for Event No.")
                elif user_choice.lower() == 'c' or user_choice.lower() == 'create':
                    try:
                        Event.create(Event)
                        break
                    except ValueError:
                        print("Invalid input. Please provide valid inputs for event creation.")
                elif user_choice.lower() == 'd' or user_choice.lower() == 'delete':
                    try:
                        event_no = int(input("\nEnter Event No. to delete: "))
                        event = events.get(event_no)
                        if event:
                            event.delete()
                            break  # Call the delete method on the event instance
                        else:
                            print("Event not found.")
                    except ValueError:
                        print("Invalid input. Please enter a valid integer for Event No.")
                else:
                    print("Invalid choice.")   

        elif user_input == '3':
            while True:
                event_no = int(input("\nEnter Event no. to list attendees: "))
                if event_no in events:
                    list_attendees(event_no)
                    break  # Exit the loop and go back to the main menu
                else:
                    print("Event not found. Please enter a valid event number.")

        elif user_input == '4':
            user_edit = input("Do you wish to [A]dd, [D]elete, or [E]dit an attendee from an event?\n")
            if user_edit.lower() == 'add' or user_edit.lower() == 'a':
                event_no = int(input("Enter Event No. to add attendee: "))
                Attendee.create(event_no)  # Pass the event_no as an argument
            elif user_edit.lower() == 'edit' or user_edit.lower() == 'e':
                attendee_no = int(input("Enter Attendee No. you wish to edit: "))
                attendee = attendees.get(attendee_no)
                if attendee:
                    attendee.edit()
                else:
                    print("Attendee not found.")
            elif user_edit.lower() == 'delete' or user_edit.lower() == 'd':
                attendee_no = int(input("Enter Attendee No. you wish to delete from event: "))
                attendee = attendees.get(attendee_no)
                if attendee:
                    attendee.delete()
                else:
                    print("Attendee not found.")
        else:
            print("\nInvalid choice.")

main()