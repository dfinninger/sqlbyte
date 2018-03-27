"""
table.py

Representation of a Table
"""

import struct


class User:
    """
    hardcoded user instance, this would ideally be generated
    """

    USERNAME_LENGTH = 32
    EMAIL_LENGTH = 255

    STRUCT_REP = f'Q{USERNAME_LENGTH}s{EMAIL_LENGTH}s'

    def __init__(self, userid: int = 0, username: str = '', email: str = ''):
        self.id = userid
        self.username = username
        self.email = email

    def struct(self) -> bytes:
        """return a struct representation of a user"""
        return struct.pack(self.STRUCT_REP, self.id, self.username, self.email)

    @classmethod
    def from_struct(cls, data):
        return cls(*struct.unpack(cls.STRUCT_REP, data))


class TableFullError(Exception):
    pass


class UserTable:
    """
    the users table
    """

    PAGE_SIZE = 4096  # Bytes in a page
    MAX_PAGES = 128   # Limit for the number of pages we can have

    ROWS_PER_PAGE = PAGE_SIZE // struct.calcsize(User.STRUCT_REP)
    TABLE_MAX_ROWS = ROWS_PER_PAGE * MAX_PAGES

    def __init__(self, pages: list = None, row_count: int = 0):
        if pages:
            self.pages = pages
        else:
            self.pages = [bytearray()] * self.MAX_PAGES

        self.row_count = row_count

    def insert(self, user: User):
        if self.row_count >= self.TABLE_MAX_ROWS:
            raise TableFullError(f'No space left in table (max rows: {self.TABLE_MAX_ROWS})')

        serialized_user = user.struct()
        page = self._get_page(self.row_count)
        page += serialized_user

        self.row_count += 1

    def _get_page(self, row_number: int) -> bytearray:
        page_number = row_number // self.ROWS_PER_PAGE
        return self.pages[page_number]
