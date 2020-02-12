import sqlite3 as lite
import datetime
import json
from time import *


class Database:
    con = None
    cur = None

    def __init__(self, dbname="h9k"):
        self.con = lite.connect(dbname + ".db")
        self.cur = self.con.cursor()

    def createIfNotExists(self):
        self.cur.execute("CREATE TABLE if not exists DrinksLog(ID Integer primary key, drink TEXT, date timestamp)")
        self.cur.execute("CREATE TABLE if not exists IngredientsLog(ID Integer primary key, ingredient TEXT,"
                         "ml integer, date timestamp)")

        self.cur.execute(
            """CREATE TABLE if not exists Ingredients ( Code varchar(50) not null primary key ,Name varchar(100) not 
            null, IsAlcoholic integer default 0 not null);""")
        self.cur.execute("""create unique index if not exists Ingredients_Code_uindex on Ingredients (Code);""")

        self.cur.execute(
            """CREATE TABLE if not exists Servos ( ServoNr integer not null constraint Servos_pk primary key, 
            Code varchar(50) not null, Volume integer not null default 0);""")
        self.cur.execute("""create unique index if not exists Servos_ID_uindex on Servos (ServoNr);""")

        self.cur.execute("""CREATE TABLE if not exists Drinks (`ID` INTEGER UNIQUE, `Name` TEXT, PRIMARY KEY(`ID`));""")

        self.cur.execute(
            """CREATE TABLE if not exists Actions (`code` TEXT UNIQUE, `Text` TEXT, `is_automatic`	INTEGER, 
            PRIMARY KEY(`code`));""")

        self.con.commit()

    def setDefaultValues(self):
        self._import_Ingredients()
        self._import_servos()
        self._import_Actions()

    def _import_Actions(self):
        if not self._check_Table_is_Filled("Actions"):
            self.cur.execute("""INSERT INTO "Actions" ("Code", "Text", "is_automatic") VALUES ('ingr', 'Add Ingredient', 1);""")
            self.cur.execute("""INSERT INTO "Actions" ("Code", "Text", "is_automatic") VALUES ('ping', 'Ring Bell', 1);""")
            self.cur.execute("""INSERT INTO "Actions" ("Code", "Text", "is_automatic") VALUES ('shake', 'Shake', 0);""")
            self.cur.execute("""INSERT INTO "Actions" ("Code", "Text", "is_automatic") VALUES ('stir', 'Stir', 0);""")
            self.cur.execute("""INSERT INTO "Actions" ("Code", "Text", "is_automatic") VALUES ('ice', 'Add Ice', 0);""")
            self.cur.execute("""INSERT INTO "Actions" ("Code", "Text", "is_automatic") VALUES ('umb', 'Add Umbrella', 0);""")
            self.con.commit()

    def _import_Ingredients(self):
        if not self._check_Table_is_Filled("Ingredients"):
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name", "IsAlcoholic") VALUES ('gin', 'Gin', 1);""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name", "IsAlcoholic") VALUES ('rum', 'Rum', 1);""")
            self.cur.execute(
                """INSERT INTO "Ingredients" ("Code", "Name", "IsAlcoholic") VALUES ('vodka', 'Vodka', 1);""")
            self.cur.execute(
                """INSERT INTO "Ingredients" ("Code", "Name", "IsAlcoholic") VALUES ('tequila', 'Tequila', 1);""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('tonic', 'Tonic Water');""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('coke', 'Cola');""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('oj', 'Orange Juice');""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('gren', 'Grenadine');""")
            self.cur.execute(
                """INSERT INTO "Ingredients" ("Code", "Name", "IsAlcoholic") VALUES ('mmix', 'Margarita Mix', 1);""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('mate', 'Mate');""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('pine', 'Pineapple Juice');""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('raspberry', 'Raspberry');""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('gga', 'Ginger Ale');""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('cocos', 'Cocos');""")
            self.cur.execute("""INSERT INTO "Ingredients" ("Code", "Name") VALUES ('mango', 'Mango Juice');""")
            self.con.commit()

    def _import_servos(self):
        table = 'servos'
        if not self._check_Table_is_Filled(table):
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (1, 'gren');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (2, 'rum');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (3, 'vodka');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (4, 'gin');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (5, 'tequila');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (6, 'gibe');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (7, 'lime');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (8, 'tonic');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (9, 'mate');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (10, 'gga');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (11, 'pine');""")
            self.cur.execute("""INSERT INTO "Servos" ("ServoNr", "Code") VALUES (12, 'oj');""")
            self.con.commit()

    def _check_Table_is_Filled(self, table):
        self.cur.execute("SELECT * FROM " + table)
        items = self.cur.fetchall()
        return len(items) > 0

    def get_Servos(self):
        self.cur.execute("SELECT ServoNr, Code, Volume FROM Servos ORDER BY ServoNr")
        items = self.cur.fetchall()
        return items

    def get_Servos_asList(self):
        array = []
        for item in self.get_Servos():
            array.append(item[1])

        return array

    def get_Servos_asJson(self):
        return json.dumps(self.get_Servos())

    def get_AllIngredients(self):
        self.cur.execute("SELECT Code, Name FROM Ingredients")
        items = self.cur.fetchall()
        return items

    def get_AllIngredients_asJson(self):
        return json.dumps(self.get_AllIngredients())

    def countUpDrink(self, drink):
        self.cur.execute("INSERT INTO DrinksLog (drink, date) VALUES (?, ?)", (drink, datetime.datetime.now()))
        self.con.commit()

    def countUpIngredient(self, ingredient, ml):
        self.cur.execute("INSERT INTO IngredientsLog (ingredient, ml, date) VALUES (?, ?, ?)",
                         (ingredient, ml, datetime.datetime.now()))
        self.con.commit()

    def get_Ingredients_Log(self):
        self.cur.execute("SELECT ID, ingredient, ml, date FROM IngredientsLog")
        return self.cur.fetchall()

    def get_Drinks_Log(self):
        self.cur.execute("SELECT ID, drink, date FROM DrinksLog")
        return self.cur.fetchall()

    def __del__(self):
        self.con.commit()
        self.con.close()


# when called directly, read out database and generate a log
if __name__ == "__main__":
    db = Database("h9k")
    db.cur.execute("SELECT * FROM DrinksLog WHERE date > '2018-12-11' ORDER BY date ASC")
    # db.cur.execute("SELECT * FROM DrinksLog ORDER BY date ASC")
    res = db.cur.fetchall()
    # print("%d entries" % len(res))
    for l in res:
        number, name, tstampstr = l
        tstamp = mktime(strptime(tstampstr.split(".")[0], "%Y-%m-%d %H:%M:%S"))
        tstamp += (14 * 24 * 3600 + 10 * 3600 + 8 * 60 + 28)
        print("%30s:  %s" % (strftime("%a %Y-%m-%d %H:%M:%S", localtime(tstamp)), name))
