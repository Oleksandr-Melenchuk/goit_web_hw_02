from collections import UserDict
from datetime import datetime, timedelta

class Field:
    def __init__(self, value):
        self.value = value
        
    def __str__(self):
        return str(self.value)
    

class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not self.number_check(value):
            raise ValueError("Not correct form of number")
        super().__init__(value)
    
    @staticmethod
    def number_check(value):
        return value.isdigit() and len(value) == 10


class Birthday(Field):
    def __init__(self, value: str):
        try:
            datetime.strptime(value, "%d.%m.%Y")
            self.value = value
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
    
    def add_phone(self, phone):
        self.phones.append(Phone(phone))
        
    def remove_phone(self, phone):
        if not self.phones:
            raise ValueError("No phones to remove")
        
        phone_obj = self.find_phone(phone)
        if phone_obj:
            self.phones.remove(phone_obj)
            return  
        raise ValueError(f"{phone} Number not in AddressBook")
    
    def edit_phone(self, phone, new_phone):
        if not self.find_phone(phone):
            raise ValueError(f"{phone} Number not found")
        self.add_phone(new_phone)
        self.remove_phone(phone)
    
    def find_phone(self, phone):
        for ph in self.phones:
            if ph.value == phone: 
                return ph
        return None
    
    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)
    
    def __str__(self):
        phones_str = '; '.join(p.value for p in self.phones)
        birthday_str = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones_str}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record
    
    def find(self, name):
        return self.data.get(name)
    
    def delete(self, name):
        if name in self.data:
            del self.data[name]
    
    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        
        for record in self.data.values():
            if record.birthday:
                converted_record = datetime.strptime(record.birthday.value, "%d.%m.%Y").date()
                birthday_this_year = converted_record.replace(year=today.year)
                if birthday_this_year < today:
                    birthday_this_year = birthday_this_year.replace(year=today.year + 1)
                
                days_ahead = (birthday_this_year - today).days
                if days_ahead <= 7:
                    congrats_date = birthday_this_year
                    if congrats_date.weekday() in (5, 6):
                        congrats_date += timedelta(days=(7 - congrats_date.weekday()))
                    
                    upcoming_birthdays.append({
                        "name": record.name.value,
                        "birthday": congrats_date.strftime("%d.%m.%Y")
                    })
        
        return upcoming_birthdays

