class Article:
    def __init__(self, id=None, title=None, content=None, author=None, magazine=None, conn=None, author_id=None, magazine_id=None):
        self.id = id
        self._title = None
        self.content = content
        self.author_id = author_id if author_id else (author.id if author else None)
        self.magazine_id = magazine_id if magazine_id else (magazine.id if magazine else None)
        self.conn = conn
        if title:
            self.title = title  # This uses the title setter

        if conn:
            self.cursor = self.conn.cursor()
            self.add_to_database()

    def __repr__(self):
        return f'<Article {self.title}>'

    def add_to_database(self):
        sql = "INSERT INTO articles (title, content, author_id, magazine_id) VALUES (?, ?, ?, ?)"
        self.cursor.execute(sql, (self.title, self.content, self.author_id, self.magazine_id))
        self.conn.commit()
        self.id = self.cursor.lastrowid

    @property
    def title(self):
        if not self._title and self.id:
            sql = "SELECT title FROM articles WHERE id = ?"
            row = self.cursor.execute(sql, (self.id,)).fetchone()
            if row:
                self._title = row[0]
        return self._title

    @title.setter
    def title(self, title):
        if isinstance(title, str) and 5 <= len(title) <= 50 and self._title is None:
            self._title = title
        else:
            raise ValueError("Title must be a string between 5 and 50 characters long and can only be set once.")

    def author(self):
        from models.author import Author
        sql = "SELECT authors.* FROM articles INNER JOIN authors ON articles.author_id = authors.id WHERE articles.id = ?"
        row = self.cursor.execute(sql, (self.id,)).fetchone()
        return Author(id=row[0], name=row[1], conn=self.conn) if row else None

    def magazine(self):
        from models.magazine import Magazine
        sql = "SELECT magazines.* FROM articles INNER JOIN magazines ON articles.magazine_id = magazines.id WHERE articles.id = ?"
        row = self.cursor.execute(sql, (self.id,)).fetchone()
        return Magazine(id=row[0], name=row[1], category=row[2], conn=self.conn) if row else None

    @classmethod
    def get_all_articles(cls, conn):
        sql = "SELECT * FROM articles"
        cursor = conn.cursor()
        articles = cursor.execute(sql).fetchall()
        return [cls(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4], conn=conn) for row in articles]
