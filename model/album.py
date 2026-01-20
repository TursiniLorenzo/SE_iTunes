from dataclasses import dataclass

@dataclass
class Album :
    id : int
    title : str
    artist_id : int
    durata : float

    def __str__ (self) :
        return f"Album {self.title} - {self.id} - {self.durata}"

    def __hash__ (self) :
        return hash (self.id)