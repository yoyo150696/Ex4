import unittest
from client_python.Pokemon import Pokemon
from client_python.Agent import Agent


class MyTestCase(unittest.TestCase):

    def test_pok(self):
        pok = Pokemon(3, 4, 5, 6)
        self.assertEqual(pok.value,3)
        self.assertEqual(pok.type,4)
        self.assertEqual(pok.x,5)
        self.assertEqual(pok.y,6)



    def test_agent(self):
        agent = Agent(1,2,3,4,5,6,7)
        self.assertEqual(agent.id, 1)
        self.assertEqual(agent.value, 2)
        self.assertEqual(agent.src, 3)
        self.assertEqual(agent.dest, 4)
        self.assertEqual(agent.speed, 5)
        self.assertEqual(agent.x, 6)
        self.assertEqual(agent.y, 7)




if __name__ == '__main__':
    unittest.main()
