#!/usr/bin/python3
import sqlite3
from sqlite3 import Error
from gtts import gTTS
from pygame import mixer
import os
import hashlib
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


def speak(text, type='clause', repetition=1, pause=0.5):
    print(text)
    filename = './mp3/{}/{}.mp3'.format(type,
                                        hashlib.md5(text.encode()).hexdigest())
    if not os.path.isfile(filename):
        tts = gTTS(text)
        tts.save(filename)
    mixer.init()
    mixer.music.load(filename)
    for i in range(repetition):
        mixer.music.play()
        while mixer.music.get_busy() == True:
            pass
        time.sleep(pause)
        mixer.music.rewind()


def main():
    database = r"./boxiot.db"

    conn = create_connection(database)
    with conn:
        training = get_training(conn, 1)
        for (id, pattern, text, level, repetition, md5) in training:
            speak('combination {}. {} times.'.format(id, repetition))
            speak(text, 'combination', repetition)


if __name__ == '__main__':
    main()
