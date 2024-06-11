class Author:
    def __init__(self, id=None, name=None, conn=None):
        self._id = id
        self._name = name
        self.conn = conn

        if conn:
            self.cursor = conn.cursor()
            self._initialize_author()

    def __repr__(self):
        return f'<Author {self._name}>'

    def __eq__(self, other):
        if isinstance(other, Author):
            return self._id == other._id and self._name == other._name
        return False

    def __hash__(self):
        return hash((self._id, self._name))

    def _initialize_author(self):
        if self._name:
            self._ensure_author_in_db()
        elif self._id:
            self._fetch_name_from_db()

    def _ensure_author_in_db(self):
        sql_check = "SELECT id FROM authors WHERE name = ? LIMIT 1"
        result = self.cursor.execute(sql_check, (self._name,)).fetchone()
        if result:
            self._id = result[0]
        else:
            sql_insert = "INSERT INTO authors(name) VALUES (?)"
            self.cursor.execute(sql_insert, (self._name,))
            self.conn.commit()
            self._id = self.cursor.lastrowid

    def _fetch_name_from_db(self):
        sql = "SELECT name FROM authors WHERE id = ?"
        result = self.cursor.execute(sql, (self._id,)).fetchone()
        if result:
            self._name = result[0]

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if value is None:
            self._id = 0
        elif isinstance(value, int):
            self._id = value
        else:
            raise ValueError("Invalid ID value")

    @property
    def name(self):
        if self._name is None and self._id:
            self._fetch_name_from_db()
        return self._name

    @name.setter
    def name(self, value):
        if isinstance(value, str) and value:
            self._name = value
        else:
            raise ValueError("Invalid name value")

    def articles(self):
        from models.article import Article
        sql = "SELECT * FROM articles WHERE author_id = ?"
        rows = self.cursor.execute(sql, (self._id,)).fetchall()
        return [Article(id=row[0], title=row[1], content=row[2], author_id=row[3], magazine_id=row[4], conn=self.conn) for row in rows]

    def magazines(self):
        from models.magazine import Magazine
        sql = """SELECT DISTINCT magazines.id, magazines.name, magazines.category
                 FROM magazines
                 INNER JOIN articles ON articles.magazine_id = magazines.id
                 WHERE articles.author_id = ?"""
        rows = self.cursor.execute(sql, (self._id,)).fetchall()
        return [Magazine(id=row[0], name=row[1], category=row[2], conn=self.conn) for row in rows]

    @classmethod
    def get_all_authors(cls, conn):
        sql = "SELECT * FROM authors"
        cursor = conn.cursor()
        authors = cursor.execute(sql).fetchall()
        return [cls(id=author[0], name=author[1], conn=conn) for author in authors]
