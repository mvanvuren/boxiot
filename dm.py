#!/usr/bin/python3
import argparse
import csv
import os
import re
import sqlite3
from sqlite3 import Error
#import sys

DB_FOLDER = "boxiot/database"
DB_FILE = "boxiot.db"
DB_SCHEMA = "schema.sql"
CSV_FOLDER = "boxiot/database/csv"
CSV_ACTIONS = "actions.csv"
CSV_COMBINATIONS = "combinations.csv"

# DB_TABLE_ACTION_TYPES = "ActionTypes"
# DB_TABLE_ACTION = "Actions"
# DB_TABLE_COMBINATION = "Combinations"
# DB_TABLE_COMBINATION_ACTIONS = "CombinationActions"

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


def execute_script(connection, sql_script):
    cursor = connection.cursor()
    cursor.executescript(sql_script)
    connection.commit()

def get_action_type(connection, action):
    sql = '''
        SELECT
            *
        FROM
            ActionTypes
        WHERE
            Name = :ActionType
    '''
    cursor = connection.cursor()
    cursor.execute(sql, action)
    
    return next(cursor, None)

def insert_action_type(connection, action):
    
    sql = '''
        INSERT INTO 
            ActionTypes 
            (Name)
        VALUES
            (:ActionType)
    '''
    cursor = connection.cursor()
    cursor.execute(sql, action)

    return cursor.lastrowid


def upsert_action_type(connection, action):

    db_action_type = get_action_type(connection, action)
    if db_action_type == None:
        Id = insert_action_type(connection, action)
    else:
        Id = db_action_type["Id"]
    
    action["ActionTypeId"] = Id


def get_action(connection, action):
    sql = '''
        SELECT
            *
        FROM
            Actions
        WHERE
            Symbol = :Symbol
    '''
    cursor = connection.cursor()
    cursor.execute(sql, action)
    
    return next(cursor, None)

def insert_action(connection, action):

    sql = '''
        INSERT INTO 
            Actions
            (Symbol, Text, ActionTypeId)
        VALUES
            (:Symbol, :Text, :ActionTypeId)
    '''
    cursor = connection.cursor()
    cursor.execute(sql, action)

    return cursor.lastrowid


def update_action(connection, action):
    sql = '''
        UPDATE
            Actions
        SET
            Text = :Text
        ,   ActionTypeId = :ActionTypeId
        WHERE
            Id = :Id
    '''
    cursor = connection.cursor()
    cursor.execute(sql, action)

def upsert_action(connection, action):

    upsert_action_type(connection, action)

    db_action = get_action(connection, action)
    if db_action == None:
        insert_action(connection, action)
    else:
        action['Id'] = db_action['Id']
        update_action(connection, action)


def get_combination(connection, combination_actions):
    sql = '''
        SELECT
            *
        FROM
            Combinations
        WHERE
            Pattern = :Pattern
    '''
    cursor = connection.cursor()
    cursor.execute(sql, combination_actions)
    
    return next(cursor, None)


def insert_combination(connection, combination_actions):

    sql = '''
        INSERT INTO 
            Combinations
            (Pattern, Text, ActionCount)
        VALUES
            (:Pattern, :Text, :ActionCount)
    '''
    cursor = connection.cursor()
    cursor.execute(sql, combination_actions)

    return cursor.lastrowid


def update_combination(connection, combination_actions):
    sql = '''
        UPDATE
            Combinations
        SET
            Text = :Text
        WHERE
            Id = :Id
    '''
    cursor = connection.cursor()
    cursor.execute(sql, combination_actions)


def get_combination_action(connection, combination_action):
    sql = '''
        SELECT
            *
        FROM
            CombinationActions
        WHERE
            CombinationId = :CombinationId
        AND ActionId = :ActionId
        AND Sequence = :Sequence
        AND SubSequence = :SubSequence
    '''
    cursor = connection.cursor()
    cursor.execute(sql, combination_action)
    
    return next(cursor, None)


def insert_combination_action(connection, combination_action):

    sql = '''
        INSERT INTO 
            CombinationActions
            (CombinationId, ActionId, Sequence, SubSequence)
        VALUES
            (:CombinationId, :ActionId, :Sequence, :SubSequence)
    '''
    cursor = connection.cursor()
    cursor.execute(sql, combination_action)

    return cursor.lastrowid

def upsert_combination(connection, combination_actions):

    # upsert_combination_type(connection, combination_actions)

    db_combination = get_combination(connection, combination_actions)
    if db_combination == None:
        combination_actions["Id"] = insert_combination(connection, combination_actions)
    else:
        combination_actions['Id'] = db_combination['Id']
        update_combination(connection, combination_actions)

#endregion database

#region import

regex = re.compile(r"([\[\(\{\/\<]){0,1}([0-9]{0,1})([a-z]{0,5})([\]\)\}\/\>]{0,1})")

def add_action(combination_actions, action, sequence, sub_sequence):
    
    combination_actions["Actions"].append({ "ActionId": action["Id"], "Sequence": sequence, "SubSequence": sub_sequence })

    if sub_sequence == 1:
        combination_actions["Text"].append(action["Text"])
    else:
        combination_actions["Text"][-1] += " " + action["Text"]

def convert_combination(combination, actions):
    
    pattern = combination["Combination"]
    type = combination["CombinationType"]

    combination_actions = { "Pattern": pattern, "CombinationType": type, "Actions": [], "Text": [] }

    sequence = 1
    for action in pattern.split("-"):

        match = regex.match(action)

        if match == None:
            continue

        sub_sequence = 1

        if match.group(1):
            symbol = match.group(1) + match.group(4)
            add_action(combination_actions, actions[symbol], sequence, sub_sequence)  
            sub_sequence += 1

        if match.group(2):
            symbol = match.group(2)
            add_action(combination_actions, actions[symbol], sequence, sub_sequence)
            sub_sequence += 1

        if match.group(3):
            symbol = match.group(3)
            add_action(combination_actions, actions[symbol], sequence, sub_sequence)

        sequence += 1

    combination_actions["ActionCount"] = len(combination_actions["Text"])
    combination_actions["Text"] = ", ".join(combination_actions["Text"])

    return combination_actions

def upsert_combination_actions(connection, combination_actions):

    upsert_combination(connection, combination_actions)

    for combination_action in combination_actions["Actions"]:
        combination_action["CombinationId"] = combination_actions["Id"]
        db_combination_action = get_combination_action(connection, combination_action)
        if db_combination_action == None:
            insert_combination_action(connection, combination_action)



#endregion

#region general
def get_file_content(file):
    with open(file, "r", encoding="UTF-8") as f:
        return f.read()
#endregion

parser = argparse.ArgumentParser()

parser.add_argument("-d", "--database", default=DB_FILE)
parser.add_argument("--create", action="store_true")
parser.add_argument("--import-csv", action="store_true")
parser.add_argument("-f", "--force", action="store_true")

args = parser.parse_args()
args.database = os.path.join(DB_FOLDER, args.database)

if args.create: # TODO: replace with --script [array]
    if os.path.isfile(args.database):
        if not args.force:
            print(f"database {args.database} already exists")
            quit()
        os.remove(args.database)

    connection = create_connection(args.database)
    with connection:
        # TODO: simply run all numbered files in init folder
        for sql_script_file in [DB_SCHEMA]: #, "actiontypes.sql", "actions.sql", "combinations.sql", "combinationactions.sql"]:
            sql_script = get_file_content(os.path.join(DB_FOLDER, sql_script_file))
            execute_script(connection, sql_script)

if args.import_csv:

    actions = {}

    with open(os.path.join(CSV_FOLDER, CSV_ACTIONS), encoding="UTF-8") as csv_file:
        actions_reader = csv.DictReader(csv_file, delimiter=",", quotechar="\"")
        connection = create_connection(args.database)
        with connection:
            for action in actions_reader:
                upsert_action(connection, action)
                actions[action["Symbol"]] = action

            connection.commit()


    with open(os.path.join(CSV_FOLDER, CSV_COMBINATIONS), encoding="UTF-8") as csv_file:
        combinations_reader = csv.DictReader(csv_file, delimiter=",", quotechar="\"")
        connection = create_connection(args.database)
        with connection:
            for combination in combinations_reader:
                combination_actions = convert_combination(combination, actions)
                upsert_combination_actions(connection, combination_actions)

            connection.commit()
