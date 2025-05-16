class SearchUser:
    def __init__(self, id, felhasznalonev, profil_kep):
        self.id = id
        self.felhasznalonev = felhasznalonev
        self.profil_kep = profil_kep


class Page:
    def __init__(self, current, size, total_pages, has_next, has_previous):
        self.current = current
        self.size = size
        self.total_pages = total_pages
        self.has_next = has_next
        self.has_previous = has_previous
        self.previous = max(self.current - 1, 1)
        self.next = min(self.current + 1, self.total_pages)
        self.page_range = range(1, self.total_pages + 1)


    def __str__(self):
        return f"current: {self.current}, size: {self.size}, total_pages: {self.total_pages}, has_next: {self.has_next}, has_previous: {self.has_previous} previous: {self.previous}, next: {self.next}, page_range: {self.page_range}"