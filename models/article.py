from connection2 import CONN, CURSOR

class Article:
    def __init__(self, id=None, title=None, content=None, author_id=None, magazine_id=None):
        self._id = id
        self._title = title
        self._content = content
        self._author_id = author_id
        self._magazine_id = magazine_id
        self._title_loaded = False

    @property
    def title(self):
        if self._title is None and self._id is not None and not self._title_loaded:
            CURSOR.execute("SELECT title FROM articles WHERE id = ?", (self._id,))
            row = CURSOR.fetchone()
            if row:
                self._title = row[0]
            self._title_loaded = True
        return self._title

    @title.setter
    def title(self, value):
        if self._title is not None:
            raise AttributeError("Cannot change the title of an article once it is set")
        if not isinstance(value, str):
            raise TypeError("Title must be a string")
        if not (5 <= len(value) <= 50):
            raise ValueError("Title must be between 5 and 50 characters long")
        self._title = value

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if not isinstance(value, str):
            raise TypeError("Content must be a string")
        self._content = value

    @property
    def author_id(self):
        return self._author_id

    @author_id.setter
    def author_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Author ID must be an integer")
        self._author_id = value

    @property
    def magazine_id(self):
        return self._magazine_id

    @magazine_id.setter
    def magazine_id(self, value):
        if not isinstance(value, int):
            raise TypeError("Magazine ID must be an integer")
        self._magazine_id = value


    def save(self):
        if not self.title or not self.content:
            raise Exception("Title and content are required")
        CURSOR.execute("INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)", 
                       (self.title, self.content, self.author_id, self.magazine_id))
        CONN.commit()
        self._id = CURSOR.lastrowid
    
    def get_author(self):
        if self._author_id is None:
            return None
        CURSOR.execute("SELECT authors.id, authors.name FROM authors JOIN articles ON articles.author_id = authors.id WHERE articles.id = ?", (self._id,))
        row = CURSOR.fetchone()

        if row:
            return {'id': row[0], 'name': row[1]}
        return None
    
    def get_magazine(self):
        if self._magazine_id is None:
            return None
        CURSOR.execute("SELECT magazines.id, magazines.name FROM magazines JOIN articles ON articles.magazine_id = magazines.id WHERE articles.id = ? " , (self._id,))
        row = CURSOR.fetchone()

        if row:
            return {'id': row[0], 'name': row[1]}
        return None
                       
    

    def __repr__(self):
        return f'<Article {self.title}>'
# EXAMPLE USAGE 
article = Article()
article.title = 'coding techniques'
article.content = 'Always debug your code '
article.author_id = 41
article.magazine_id = 18
article.save()

author = article.get_author()
magazine = article.get_magazine()
print(author)
print(magazine)

 
