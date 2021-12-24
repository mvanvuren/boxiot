#!/usr/bin/python3
import hashlib
import datetime
import eyed3
import os
import subprocess
import sqlite3
import time
from enum import Enum
from sqlite3 import Error

from gtts import gTTS
from pygame import mixer

DB_FOLDER = "boxiot/database"
DB_FILE = "boxiot.db"

class SpeakType(Enum):
    Introduction = 1
    Combination = 2
    Repetition = 3

#region database
def dict_factory(cursor, row):
    dict = {}
    for idx, col in enumerate(cursor.description):
        dict[col[0]] = row[idx]
    return dict


def create_connection(database_file):
    connection = None
    try:
        connection = sqlite3.connect(database_file)
        connection.row_factory = dict_factory
    except Error as e:
        print(e)

    return connection


def get_training(connection, training_id):

    sql = '''
        SELECT
            cns.Id
        ,   cns.Pattern
        ,   cns.Text
        ,   tcs.Repetition
		,	cts.Name AS CombinationType
        FROM 
            TrainingCombinations tcs
        INNER JOIN 
			Combinations cns
			ON 
				tcs.CombinationId = cns.Id
		INNER JOIN
			CombinationTypes cts
			ON
				cns.CombinationTypeId = cts.Id
        WHERE
            tcs.TrainingId = ?
        ORDER BY
            tcs.Sequence
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
        parts = text.split(", ")
        for part in parts:
            cf.write(f"DrawUTF8String,G24,{x},4,{part},0xffff\n")
            x += 24
    subprocess.call(["./draw", "combination.txt"])


def wait_while_playing():
    while mixer.music.get_busy() == True:
        pass


def get_audio_file(combination):

    speak_type_name = combination["SpeakType"].name[0:1].lower()
    id = combination["Id"]
    speak = combination["Speak"]
    md5 = hashlib.md5(speak.encode()).hexdigest()
    if combination["SpeakType"] == SpeakType.Repetition:
        filename = f"boxiot/mp3/{speak_type_name}-{md5}.mp3"
    else:
        filename = f"boxiot/mp3/{speak_type_name}-{id}-{md5}.mp3"

    if not os.path.isfile(filename):
        
        tts = gTTS(speak)
        tts.save(filename)

        mp3 = eyed3.load(filename)
        if not mp3.tag:
            mp3.initTag()

        if combination["SpeakType"] != SpeakType.Repetition:
            mp3.tag.track_num = id
        mp3.tag.title = speak
        mp3.tag.save()

    return filename


def speak(combination):
          
    filename = get_audio_file(combination)

    if "__Generate" in combination:
        return
    
    repetition = 1
    if combination["SpeakType"] == SpeakType.Combination:
        repetition = combination["Repetition"]

    print(combination["Speak"])
    
    start_time = datetime.datetime.now()

    mixer.init(buffer=2048)
    mixer.music.load(filename)
    for _ in range(repetition):
        time.sleep(0.5)
        mixer.music.play()
        wait_while_playing()
        mixer.music.rewind()

    end_time = datetime.datetime.now()
    duration = end_time - start_time

    return 1000 * duration.total_seconds()

def speak_combination(combination):

    # intro
    combination["SpeakType"] = SpeakType.Introduction
    combination["Speak"] = f'{combination["CombinationType"]} combination {combination["Id"]}'
    speak(combination)
    
    # repetition
    combination["SpeakType"] = SpeakType.Repetition
    combination["Speak"] = f'{combination["Repetition"]} times'
    speak(combination)

    # combination
    combination["SpeakType"] = SpeakType.Combination
    combination["Speak"] = combination["Text"]
    speak(combination)

def train(training_id):
    connection = create_connection(os.path.join(DB_FOLDER, DB_FILE))
    with connection:
        training = get_training(connection, training_id)
        for combination in training:
            #combination["__Generate"] = True
            speak_combination(combination)

def main():
    # train(1)
    # train(2)
    # train(3)
    # train(4)
    # train(5)
    # train(6)
    train(7)

if __name__ == '__main__':
    main()
