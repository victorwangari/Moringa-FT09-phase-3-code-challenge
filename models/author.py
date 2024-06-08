from connection2 import CONN, CURSOR

class Author:
    def __init__(self, name, id=None): 
        self._id = id
        self._name = None  # Initialize name as None

        # Set name property using setter
        self.name = name  

    @property
    def id(self):
        return self._id
    
    @id.setter
    def id(self, value):
        if value is not None and not isinstance(value, int):
            raise TypeError("Author ID must be an integer")
        self._id = value

    @property
    def name(self):
        if self._name is None:
            if self.id is not None:
                sql = "SELECT name FROM authors WHERE id = ?"
                CURSOR.execute(sql, (self.id,))
                result = CURSOR.fetchone()
                if result:
                    self._name = result[0]
        return self._name
    
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Author name must be a string")
        if len(value) == 0:
            raise ValueError("Author name must be longer than 0 characters")
        if hasattr(self, '_name') and self._name is not None:
            raise AttributeError("Author name cannot be changed after instantiation")
        self._name = value
    

    @classmethod 
    def create(cls, name):
        author = cls(name)
        author.save()
        return author
    
    def save(self):
        if not self.name:
            raise ValueError("Author name must not be empty")
        sql = "INSERT INTO authors (name) VALUES (?)"
        CURSOR.execute(sql, (self.name,))
        CONN.commit()
        self.id = CURSOR.lastrowid
        
    def __repr__(self):
        return f'<Author {self.name}>'
    

Author1 = Author.create("Angel")

