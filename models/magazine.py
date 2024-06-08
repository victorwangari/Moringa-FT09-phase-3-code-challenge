from connection2 import CONN, CURSOR
from author import Author 

class Magazine:
    def __init__(self, name, category, id=None):
        self._id = id
        self.name = name
        self.category = category

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if not isinstance(value, int):
            raise ValueError("ID must be of type int")
        self._id = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise ValueError("Name must be a string")
        if len(value) < 2 or len(value) > 16:
            raise ValueError("Name must be between 2 and 16 characters, inclusive")
        self._name = value

    @property
    def category(self):
        return self._category
    
    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise ValueError("Category must be a string")
        if len(value) == 0:
            raise ValueError("Category must be longer than 0")
        self._category = value

    def save(self):
        if not self.name or not self.category:
            raise ValueError("Name and category must be set before saving")
        sql = "INSERT INTO magazines(name, category) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.category))
        CONN.commit()
        self.id = CURSOR.lastrowid
    
    def articles(self):
        if not self.id:
            raise ValueError("ID must be set before fetching articles")
        sql = "SELECT * FROM articles WHERE magazine_id = ?"
        CURSOR.execute(sql, (self.id,))
        articles = CURSOR.fetchall()
        return articles

    def contributors(self):
        if not self.id:
            raise ValueError("ID must be set before fetching contributors")
        sql = "SELECT DISTINCT authors.* FROM authors JOIN articles ON authors.id = articles.author_id WHERE articles.magazine_id = ?"
        CURSOR.execute(sql, (self.id,))
        contributors = CURSOR.fetchall()
        return [Author(*contributor) for contributor in contributors]

    def __repr__(self):
        return f'<Magazine {self.name}>'


Magazine2 = Magazine('name', 'category')
Magazine2.name = 'laptop'
Magazine2.category = 'tech'
Magazine2.save()

contributors = Magazine2.contributors()
print (contributors)