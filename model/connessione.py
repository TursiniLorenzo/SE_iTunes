from dataclasses import dataclass
from model.album import Album


@dataclass
class Connessione :
    album1 : int
    album2 : int

    def __str__ (self) :
        return f"{self.album1} - {self.album2}"

    def __hash__ (self) :
        return hash((self.album1, self.album2))