import Hector.conf.database
import os

from .helper import h9kTestHelper


class Test_database:
    dbhelper = h9kTestHelper.dbHelper()

    def test_GetServos(self):
        self.dbhelper.prepareDB()
        servos = self.dbhelper.database.get_Servos()

        assert len(servos) == 12

    def test_GetServosAsList(self):
        self.dbhelper.prepareDB()
        servos = self.dbhelper.database.get_Servos_asList()
        assert "['gren', 'rum', 'vodka', 'gin', 'tequila', 'gibe', 'lime', 'tonic', 'mate', " \
               "'gga', 'pine', 'oj']" == str(servos)

    def test_GetIngredients(self):
        self.dbhelper.prepareDB()

        ing = self.dbhelper.database.get_AllIngredients()

        assert ing[0][1] == "Gin"

    def test_count_up_ingredient(self):
        self.dbhelper.prepareDB()
        self.dbhelper.database.countUpIngredient("Gin", 200)

        ingrcount = self.dbhelper.database.get_Ingredients_Log()
        assert len(ingrcount) == 1

    def test_count_up_Drinks(self):
        self.dbhelper.prepareDB()
        self.dbhelper.database.countUpDrink("Mate")

        drinkCount = self.dbhelper.database.get_Drinks_Log()
        assert len(drinkCount) == 1

    # ---------------------------------------------------------------------

    def __exit__(self):
        self.dbhelper.removeDB()
