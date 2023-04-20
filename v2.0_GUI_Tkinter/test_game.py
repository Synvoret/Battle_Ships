import unittest
from game import level_game

from parameterized import parameterized

class TestLevelGame(unittest.TestCase):
    
    def setUp(self):
        print('Setting up...')
    
    @parameterized.expand([('player', 4), ('cpu', 4)])
    def test_level_game(self, who, max_ships):
        self.assertEqual(level_game(who), max_ships)


if __name__ == '__main__':
    unittest.main(verbosity=2)
