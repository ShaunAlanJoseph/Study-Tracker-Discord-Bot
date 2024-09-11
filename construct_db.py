from database import Database


def main():
    Database().establish_connection()

    # Create Relations

    query = ("CREATE TABLE USERS("
             "user_id BIGINT PRIMARY KEY,"
             "username VARCHAR(64) NOT NULL,"
             "join_date BIGINT NOT NULL"
             ")")
    Database.execute_query(query)
    
    query = ("CREATE TABLE Tasks("
         "task_id BIGINT PRIMARY KEY,"
         "user_id BIGINT NOT NULL,"
         "name VARCHAR(128) NOT NULL,"
         "description TEXT,"
         "status VARCHAR(32),"
         "due_date BIGINT,"
         "completion_time BIGINT,"
         "FOREIGN KEY (user_id) REFERENCES Users(user_id)"
         ")")
    
    Database.execute_query(query)
    
    query = ("CREATE TABLE Time_Table_Entry("
         "tt_id BIGINT PRIMARY KEY,"
         "user_id BIGINT NOT NULL,"
         "name VARCHAR(128) NOT NULL,"
         "description TEXT,"
         "days VARCHAR(64),"
         "time BIGINT,"
         "duration BIGINT,"
         "ping BOOLEAN,"
         "FOREIGN KEY (user_id) REFERENCES Users(user_id)"
         ")")
    
    Database.execute_query(query)
    
    query = ("CREATE TABLE Time_Table_Completed_Entries("
         "tt_id BIGINT,"
         "time BIGINT NOT NULL,"
         "status VARCHAR(32),"
         "PRIMARY KEY (tt_id, time),"
         "FOREIGN KEY (tt_id) REFERENCES Time_Table_Entry(tt_id)"
         ")")
    
    Database.execute_query(query)
    
    
    query = ("CREATE TABLE Focus_Mode("
         "user_id BIGINT,"
         "start BIGINT NOT NULL,"
         "duration BIGINT,"
         "PRIMARY KEY (user_id, start),"
         "FOREIGN KEY (user_id) REFERENCES Users(user_id)"
         ")")
    
    Database.execute_query(query)
    
    
    query = ("CREATE TABLE Songs("
      "song_id BIGINT PRIMARY KEY,"
      "bytes bytea NOT NULL,"
      "artist VARCHAR(128)"
      ")")
    
    Database.execute_query(query)
    
    query = ("CREATE TABLE Playlist("
         "playlist_id BIGINT PRIMARY KEY,"
         "user_id BIGINT NOT NULL,"
         "FOREIGN KEY (user_id) REFERENCES Users(user_id)"
         ")")
    
    Database.execute_query(query)
    
    query = ("CREATE TABLE SongEntry("
         "playlist_id BIGINT,"
         "song_id BIGINT,"
         "PRIMARY KEY (playlist_id, song_id),"
         "FOREIGN KEY (playlist_id) REFERENCES Playlist(playlist_id),"
         "FOREIGN KEY (song_id) REFERENCES Songs(song_id)"
         ")")
    
    Database.execute_query(query)
    
    query = ("CREATE TABLE Cards("
         "card_id BIGINT PRIMARY KEY,"
         "user_id BIGINT NOT NULL,"
         "question TEXT,"
         "answer TEXT,"
         "card_type VARCHAR(64),"
         "FOREIGN KEY (user_id) REFERENCES Users(user_id)"
         ")")
    
    Database.execute_query(query)
    
    query = ("CREATE TABLE Dropdown_Cards("
         "card_id BIGINT PRIMARY KEY,"
         "option VARCHAR(256),"
         "FOREIGN KEY (card_id) REFERENCES Cards(card_id)"
         ")")
    
    Database.execute_query(query)
    
    query = ("CREATE TABLE Card_Set("
         "card_set_id BIGINT PRIMARY KEY,"
         "user_id BIGINT NOT NULL,"
         "FOREIGN KEY (user_id) REFERENCES Users(user_id)"
         ")")
    
    Database.execute_query(query)
    
    query = ("CREATE TABLE CardEntry("
         "card_set_id BIGINT,"
         "card_id BIGINT,"
         "PRIMARY KEY (card_set_id, card_id),"
         "FOREIGN KEY (card_set_id) REFERENCES Card_Set(card_set_id),"
         "FOREIGN KEY (card_id) REFERENCES Cards(card_id)"
         ")")
    
    Database.execute_query(query)
    
    query = ("CREATE TABLE Card_History("
         "card_id BIGINT,"
         "time BIGINT,"
         "status VARCHAR(32),"
         "PRIMARY KEY (card_id, user_id, time),"
         "FOREIGN KEY (card_id) REFERENCES Cards(card_id)"
         ")")
    
    Database.execute_query(query)

    Database().terminate_connection()


if __name__ == '__main__':
    main()