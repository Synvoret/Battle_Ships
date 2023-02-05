import unittest
from parameterized import parameterized
from game import level_game, game_statistic

class TestLevelGame(unittest.TestCase):
    
    def setUp(self):
        print('Setting up...')
    
    @parameterized.expand([
        ('player', 4),
        ('cpu', 4)
    ])
    def test_level_game(self, who, ships):
        self.assertEqual(level_game(who), ships)


if __name__ == '__main__':
    unittest.main()
