import unittest
from Graph import *


class MyTestCase(unittest.TestCase):
    def test_createGraph(self):
        g1 = Graph("graph_json.txt")
        g2 = Graph("json.txt")
        self.assertTrue(g1.getNumActors() == g2.getNumActors())

    def test_saveGraph(self):
        g1 = Graph("json.txt")
        g1.saveToJson()

    def test_aNodeToJson(self):
        aNode = ActorNode("Sanchit Dhiman", 1, 22)
        json = aNode.toJson()
        self.assertTrue(json["Name"] == "Sanchit Dhiman")
        self.assertTrue(json["Order Scraped"] == 1)
        self.assertTrue(json["Age"] == 22)

    def test_mNodeToJson(self):
        mNode = MovieNode("DeadPool", 1, "someURL", 1997, 100000, "Me")
        json = mNode.toJson()
        self.assertTrue(json["Name"] == "DeadPool")
        self.assertTrue(json["Order Scraped"] == 1)
        self.assertTrue(json["URL"] == "someURL")
        self.assertTrue(json["Year Released"] == 1997)
        self.assertTrue(json["Grossed"] == 100000)
        self.assertTrue(json["Starring"] == "Me")

    def test_getMovieGross(self):
        graph = Graph("json.txt")
        val = graph.getMovieGross("Lucy")
        self.assertTrue(val > 0)

    def test_getMovieGross(self):
        graph = Graph("json.txt")
        val = graph.getMoviesForActor("Morgan Freeman")
        self.assertTrue(len(val) > 10)

    def test_highestWeighted(self):
        graph = Graph("json.txt")
        val = graph.getHighestWeightedActors()
        self.assertTrue(len(val) == 10)


if __name__ == "__main__":
    unittest.main()
