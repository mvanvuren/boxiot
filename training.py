import sqlite3
from sqlite3 import Error
from gtts import gTTS
import os
import hashlib
from playsound import playsound
import time


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def get_training(conn, training_id):

    sql = '''
        SELECT
            cns.Id
        ,	cns.Pattern
        ,	cns.Text
        ,	cns.Level
        ,	tcs.Repetition
        ,	cns.MD5
        FROM 
            TrainingCombinations tcs
            INNER JOIN Combinations cns
                ON tcs.CombinationId = cns.Id
        WHERE
            tcs.TrainingId = ?
        ORDER BY
            tcs.SequenceId
    '''
    cur = conn.cursor()
    cur.execute(sql, (training_id,))

    training = cur.fetchall()

    return training


def speak(text):
    print(text)
    md5 = hashlib.md5(text.encode())
    md5hex = md5.hexdigest()
    filename = "./mp3/misc/{}.mp3".format(md5hex)
    if not os.path.isfile(filename):
        tts = gTTS(text)
        tts.save(filename)
    playsound(filename)
    time.sleep(1)


def main():
    database = r"D:\projects\boxiot2\boxiot.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        training = get_training(conn, 1)
        for (id, pattern, text, level, repetition, md5) in training:
            speak('combination {}. {} times.'.format(id, repetition))
            for i in range(repetition):
                print(i + 1, text)
                filename = "./mp3/{}.mp3".format(md5)
                playsound(filename)
                time.sleep(1)


if __name__ == '__main__':
    main()
