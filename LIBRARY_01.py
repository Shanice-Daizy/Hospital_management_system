class Student:
    def _init_(self, name, reg_no, contact):
        self.name = name
        self.reg_no = reg_no
        self.contact = contact
        self.loans = []


    def _str_(self):
        status = "available" if self.is_available else "borrowed"
        return f"{self.name}({self.reg_no})" 


class Book:
    catalogue = []

    def _init_(self, title,author):
        self.title = title
        self.author = author
        self. copies = None
        Book.catalogue.append(self)  

    @classmethod
    def all_titles(cls):
        return [b.title for b in cls.catalogue]

    @staticmethod
    def is_valid_isbn(isbn):
        return len(isbn.replace("-","")) in (10, 13)

    
class BookCopy:
    def _init_(self, copy_id, book):
        self.copy_id = copy_id
        self.book = book
        self.is_available = True

    def _str_(self):
        status = "available" if self.is_available else "borrowed"
        return f"{self.copy_id}: {self.book.title} ({status})"

    def _repr_(self):
        return f"BookCopy{self.copy_id!r}, {self.book.title!r})"

    
    def mark_borrowed(self):
        if not self.is_available:
            raise ValueError("Already out") 
        self.is_available = False


    def mark_returned(self):
        self.is_available = True       








class loan:
    FINE_PER_DAY = 1000 #clasS attribute(shared, UGX)

    def _init_(self, student, copy, borrow_date, due_date):
        self.student = student #Instance attribute
        self.copy = copy
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None

    def calculate_fine(self, today):
        if today <= self.due_date:
            return 0

        days = (today - self.due_date).days
        return days * loan. FINE_PER_DAY    



    