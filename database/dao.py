from database.DB_connect import DBConnect
from model.album import Album
from model.connessione import Connessione

class DAO:

    @staticmethod
    def read_album (threshold):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ select a.id, a.title, a.artist_id, sum(t.milliseconds / 60000) as durata
                    from album a, track t
                    where a.id = t.album_id
                    group by a.id, a.title, a.artist_id 
                    having durata > %s 
                """

        cursor.execute(query, (threshold, ))

        for row in cursor:
            result.append(Album (**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def read_connessione (threshold) :
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """ 
                select distinct
                t1.album_id as album1,
                t2.album_id as album2
                from playlist_track pt1
                join playlist_track pt2
                on pt1.playlist_id = pt2.playlist_id
                join track t1 on pt1.track_id = t1.id
                join track t2 on pt2.track_id = t2.id
            
                join (
                    select a.id
                    from album a
                    join track t on a.id = t.album_id
                    group by a.id
                    having sum(t.milliseconds) / 60000 > %s
                ) a1 on a1.id = t1.album_id
                
                join (
                    select a.id
                    from album a
                    join track t on a.id = t.album_id
                    group by a.id
                    having sum(t.milliseconds) / 60000 > %s
                ) a2 on a2.id = t2.album_id
                
                where t1.album_id < t2.album_id
        """

        cursor.execute(query, (threshold, threshold, ))

        for row in cursor :
            result.append(Connessione (**row))

        cursor.close()
        conn.close()
        return result
