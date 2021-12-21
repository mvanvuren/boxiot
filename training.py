#!/usr/bin/python3
import hashlib
import os
import subprocess
import sqlite3
import time
from enum import Enum
from sqlite3 import Error

from gtts import gTTS
from pygame import mixer


class SpeakType(Enum):
    Clause = 1
    Combination = 2
    Test = 3


def create_connection(database_file):
    connection = None
    try:
        connection = sqlite3.connect(database_file)
    except Error as e:
        print(e)

    return connection


def get_training(connection, training_id):

    sql = '''
        SELECT
            cns.Id
        ,   cns.Pattern
        ,   cns.Text
        --,	cns.Level
        ,   tcs.Repetition
        --,	cns.MD5
        FROM 
            TrainingCombinations tcs
            INNER JOIN Combinations cns
                ON tcs.CombinationId = cns.Id
        WHERE
            tcs.TrainingId = ?
        ORDER BY
            tcs.SequenceId
    '''
    cursor = connection.cursor()
    cursor.execute(sql, (training_id,))

    training = cursor.fetchall()

    return training


def display_combination(pattern, text):
    with open("combination.txt","w", encoding="utf-8") as cf:
        cf.write("FillScrren,0x0000\n")
        cf.write("SetFontDirection,3\n")
        cf.write(f"DrawUTF8String,G32,40,4,{pattern},0xf000\n")
        x = 64
        parts = [p.strip() for p in text.split(".") if p != ""]
        for part in parts:
            cf.write(f"DrawUTF8String,G24,{x},4,{part},0xffff\n")
            x += 24
    subprocess.call(["./draw", "combination.txt"])

def wait_while_playing():
    while mixer.music.get_busy() == True:
        pass


def get_audio_file(text, speak_type):

    speak_type_name = speak_type.name.lower()
    md5 = hashlib.md5(text.encode()).hexdigest()
    filename = f'./mp3/{speak_type_name}/{md5}.mp3'

    if not os.path.isfile(filename):
        tts = gTTS(text)
        tts.save(filename)

    return filename


def speak(text, speak_type=SpeakType.Clause, repetition=1, pause=0.5):
    print(text)
    filename = get_audio_file(text, speak_type)
    mixer.init(buffer=2048)
    mixer.music.load(filename)
    #for _ in range(repetition):
    for _ in range(1):
        mixer.music.play()
        wait_while_playing()
        time.sleep(pause)
        mixer.music.rewind()


def main():
    connection = create_connection(r"./boxiot.db")
    with connection:
        training = get_training(connection, 1)
        for (id, pattern, text, repetition) in training:
            #display_combination(pattern, text)
            speak(f'combination {id}. {repetition} times.')
            speak(text, SpeakType.Combination, repetition)


if __name__ == '__main__':
    main()
