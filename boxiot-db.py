import sqlite3
from sqlite3 import Error
from gtts import gTTS
import os
import hashlib
import re


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def get_combinations(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM Combinations ORDER BY Id")

    combinations = cur.fetchall()

    return combinations


def get_actions(conn, combination_id):

    sql = '''
        SELECT 
            *
        FROM 
            CombinationActions
            INNER JOIN Actions
                ON CombinationActions.ActionId = Actions.Id
        WHERE
            CombinationId = ?
        ORDER BY 
            SequenceId, SubSequenceId    
    '''
    cur = conn.cursor()
    cur.execute(sql, (combination_id,))

    actions = cur.fetchall()

    return actions


def update_combination(conn, combination_id, md5hex, text):
    sql = '''
        UPDATE
            Combinations
        SET 
            MD5 = ?
        ,   [Text] = ?
        WHERE
            Id = ?
    '''
    cur = conn.cursor()
    cur.execute(sql, (md5hex, text, combination_id))
    conn.commit()


def main():
    database = r"D:\projects\boxiot2\boxiot.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        combinations = get_combinations(conn)
        for combination in combinations:
            combination_id = combination[0]
            actions = get_actions(conn, combination_id)
            text = ''
            sequence_id = 1
            for action in actions:
                if action[3] != sequence_id:
                    text += '. '
                    sequence_id = action[3]
                text += ' ' + action[7]

            text = re.sub(' +', ' ', text.lstrip()) + '.'
            md5 = hashlib.md5(text.encode())
            md5hex = md5.hexdigest()
            filename = "./mp3/{}.mp3".format(md5hex)
            if not os.path.isfile(filename):
                tts = gTTS(text)
                tts.save(filename)
                update_combination(conn, combination_id, md5hex, text)
                print(filename)


if __name__ == '__main__':
    main()
