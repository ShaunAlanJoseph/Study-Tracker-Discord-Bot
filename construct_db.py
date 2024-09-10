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


    Database().terminate_connection()


if __name__ == '__main__':
    main()