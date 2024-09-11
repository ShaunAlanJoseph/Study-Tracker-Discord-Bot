# Study Tracker Discord Bot

## 1. Project Planning

### Project Title:
Study Tracker Discord Bot

### Define Objectives:
The objective of the Study Tracker Discord Bot is to help users manage their study schedules, tasks, and focus modes through a Discord bot interface. The system should allow users to create and manage tasks, track their study time, and maintain playlists for study sessions.

## 2. Requirement Analysis

### System Specification:
- **Functional Requirements:**
  - Users should be able to create, read, update, and delete tasks.
  - Users should be able to start and stop focus modes.
  - Users should be able to create and manage playlists and songs.
  - The bot should provide reminders and notifications for tasks and focus modes.
  - The bot should maintain a history of completed tasks and focus sessions.

- **Non-Functional Requirements:**
  - **Performance:** The system should handle multiple users and concurrent operations efficiently.
  - **Security:** User data should be securely stored and accessed.

### Data Requirements:
- **Types of Data:**
  - User information (user_id, username, join_date)
  - Tasks (task_id, user_id, name, description, status, due_date, completion_time)
  - Focus modes (user_id, start, duration, status)
  - Playlists (playlist_id, user_id)
  - Songs (song_id, bytes, artist)
  - Card sets and cards for study materials

- **Relationships:**
  - Users have multiple tasks, focus modes, playlists, and card sets.
  - Playlists contain multiple songs.
  - Card sets contain multiple cards.

- **Constraints:**
  - Primary keys and foreign keys to maintain data integrity.
  - Unique constraints on user_id, task_id, playlist_id, and song_id.

## 3. Database Design

### Conceptual Design:
The Entity-Relationship (ER) diagram visualizes the entities, attributes, and relationships. Here is a textual representation based on the provided context:

- **Users** (user_id (PK), username, join_date)
  - (1:N) Tasks (task_id (PK), user_id (FK), name, description, status, due_date, completion_time)
  - (1:N) TimeTableEntry (tt_id (PK), user_id (FK), name, description, days, time, duration, ping)
    - (1:N) TimeTableCompletedEntries (tt_id (FK), time, status)
  - (1:1) FocusMode (user_id (FK), start, duration, status)
  - (1:N) Playlist (playlist_id (PK), user_id (FK))
    - (1:N) SongEntry (playlist_id (FK), song_id)
      - (N:1) Songs (song_id (PK), bytes, artist)
  - (1:N) CardSet (card_set_id (PK), user_id (FK))
    - (1:N) CardEntry (card_set_id (FK), card_id)
      - (N:1) Cards (card_id (PK), question, answer, card_type)
        - (1:1) DropdownCards (card_id (FK), option)
    <br>
### ER Overview:
```plaintext
Users (user_id (PK), username, join_date) // Strong Entity
    |
    |<-- (1:N) -- Tasks (task_id (PK), user_id (FK), name, description, status, due_date, completion_time) // Strong Entity
    |
    |<-- (1:N) -- TimeTableEntry (tt_id (PK), user_id (FK), name, description, days, time, duration, ping) // Strong Entity
    |                |
    |                |<-- (1:N) -- TimeTableCompletedEntries (tt_id (FK), time, status) // Weak Entity
    |
    |<-- (1:N) -- FocusMode (user_id (FK), start, duration) // Weak Entity
    |
    |<-- (1:N) -- Playlist (playlist_id (PK), user_id (FK)) // Strong Entity
    |                |
    |                |<-- (1:N) -- SongEntry (playlist_id (FK), song_id) // Junction table for m:n relations. Represent this as a m:n relation
    |                                |
    |                                |<-- (N:1) -- Songs (song_id (PK), bytes, artist) // Strong Entity
    |
    |   
    | 
    |<-- (1:N) -- CardSet (card_set_id (PK), user_id (FK)) // Strong Entity
    |               |
                    |<-- (1:N) -- CardEntry (card_set_id (FK), card_id) // Junction table for m:n relations. Represent this as a m:n relation
                                    |
                                    |<-- (N:1) -- Cards (card_id (PK), question, answer, card_type) // Strong Entity
                                                    |
                                                    |<-- (1:1) -- DropdownCards (card_id (FK), option) // Weak Entity
                                                    |
                                                    |<-- (1:N) -- CardHistory (card_id (FK), time, status) // Weak Entity
```

 
  
### ER Diagram:

https://cdn.discordapp.com/attachments/1273219520860913679/1283350650717077567/Drawing_2024-08-30_10.32.29.excalidraw.png?ex=66e2acee&is=66e15b6e&hm=88ac4e2f0ca14870ba2cd94cf0034239f3ed948880c867c4dd8c011fddbc7616&


### Logical Design:
Convert the ER diagram into a relational schema:

- **Users**:
  ```sql
  CREATE TABLE Users (
      user_id BIGINT PRIMARY KEY,
      username VARCHAR(64) NOT NULL,
      join_date BIGINT NOT NULL
  );
  ```

- **Tasks**:
  ```sql
  CREATE TABLE Tasks (
      task_id BIGINT PRIMARY KEY,
      user_id BIGINT NOT NULL,
      name VARCHAR(128) NOT NULL,
      description TEXT,
      status VARCHAR(32),
      due_date BIGINT,
      completion_time BIGINT,
      FOREIGN KEY (user_id) REFERENCES Users(user_id)
  );
  ```

- **FocusMode**:
  ```sql
  CREATE TABLE FocusMode (
      user_id BIGINT,
      start BIGINT NOT NULL,
      duration BIGINT,
      status BOOLEAN,
      PRIMARY KEY (user_id, start),
      FOREIGN KEY (user_id) REFERENCES Users(user_id)
  );
  ```

- **Playlist**:
  ```sql
  CREATE TABLE Playlist (
      playlist_id BIGINT PRIMARY KEY,
      user_id BIGINT NOT NULL,
      FOREIGN KEY (user_id) REFERENCES Users(user_id)
  );
  ```

- **Songs**:
  ```sql
  CREATE TABLE Songs (
      song_id BIGINT PRIMARY KEY,
      bytes BLOB NOT NULL,
      artist VARCHAR(128)
  );
  ```

- **CardSet**:
  ```sql
  CREATE TABLE CardSet (
      card_set_id BIGINT PRIMARY KEY,
      user_id BIGINT NOT NULL,
      FOREIGN KEY (user_id) REFERENCES Users(user_id)
  );
  ```

- **Cards**:
  ```sql
  CREATE TABLE Cards (
      card_id BIGINT PRIMARY KEY,
      question TEXT,
      answer TEXT,
      card_type VARCHAR(64)
  );
  ```

- **DropdownCards**:
  ```sql
  CREATE TABLE DropdownCards (
      card_id BIGINT PRIMARY KEY,
      option VARCHAR(256),
      FOREIGN KEY (card_id) REFERENCES Cards(card_id)
  );
  ```

### Normalization:
The database is normalized up to the third normal form (3NF) to reduce redundancy and improve integrity.

## 4. Implementation

### Database Creation:
The database and tables are created using SQL queries as shown in the logical design section.

### Coding:
 SQL queries for CRUD operations. Example for tasks:
```sql
-- Create
INSERT INTO Tasks (task_id, user_id, name, description, status, due_date, completion_time) VALUES (?, ?, ?, ?, ?, ?, ?);

-- Read
SELECT * FROM Tasks WHERE user_id = ?;

-- Update
UPDATE Tasks SET name = ?, description = ?, status = ?, due_date = ?, completion_time = ? WHERE task_id = ?;

-- Delete
DELETE FROM Tasks WHERE task_id = ?;
```
However in this project these operations are performed internally by discord through the python functions we have written

### Stored Procedures and Triggers:
Implemented stored procedures, functions, and triggers 
```sql
CREATE OR REPLACE FUNCTION update_task_status()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status = 'completed' THEN
        NEW.completion_time = EXTRACT(EPOCH FROM NOW());
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER task_status_update
BEFORE UPDATE ON Tasks
FOR EACH ROW
EXECUTE FUNCTION update_task_status();
```

### User Interface (UI) Design:
  For this project, the UI is implemented as a Discord bot using the `discord.py` library.

---


