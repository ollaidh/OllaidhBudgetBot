import unittest
from commands.command_chart import *
from unittest.mock import MagicMock
from unittest.mock import patch


class TestChart(unittest.TestCase):
    @patch('commands.command_chart.piechart_maker')
    def test_command_execute(self, path_mock):
        command = ChartCommandExecutor()

        class TestAdapter:
            pass
        adapter = TestAdapter()

        adapter.calculate_spent = MagicMock(return_value={'TOTAL': 100, 'meat': 70, 'takeaway': 30})

        path_mock.return_value = r"C:\Users\razer\PycharmProjects\budget_bot\spent.png"
        self.assertEqual(
            {'chart_path': r"C:\Users\razer\PycharmProjects\budget_bot\spent.png"},
            command.execute(adapter, ['2022-12', '2023-02', '$each'])
        )

        adapter.calculate_spent = MagicMock(return_value={'MEAT': 100, 'steak': 50, 'chicken': 50})

        self.assertEqual(
            {'chart_path': r"C:\Users\razer\PycharmProjects\budget_bot\spent.png"},
            command.execute(adapter, ['2022-12', '2023-02', 'meat'])
        )


if __name__ == '__main__':
    unittest.main()

