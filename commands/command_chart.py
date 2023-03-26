import matplotlib.pyplot as plt
import numpy as np
import pathlib
from commands import command_spent
from commands.exceptions import *


def piechart_maker(spent: dict, start_date: str, end_date: str) -> str:
    # formatting function to get value and percentage at the same time on pie chart:
    def autopct_format(numbers):
        def my_format(pct):
            total = sum(numbers)
            val = int(round(pct * total / 100.0))
            return f'{format(pct, ".1f")}%\n{val} {chr(8364)}'

        return my_format

    # make data for pie chart:
    values = [value for key, value in spent.items()]
    labels = list(spent.keys())

    total_title = f"TOTAL: {sum(values)} {chr(8364)}  |  Period: {start_date} - {end_date}"

    colors = plt.get_cmap('viridis')(np.linspace(0.5, 1.0, len(values)))

    # plot
    fig, ax = plt.subplots()
    ax.set_aspect('equal', adjustable='box')
    ax.set_title(total_title, loc='left', fontweight="bold")
    ax.set_frame_on(False)
    ax.pie(values, colors=colors, labels=labels, autopct=autopct_format(values), radius=2,
           wedgeprops={"linewidth": 1, "edgecolor": "white"}, frame=True, rotatelabels=False)

    ax.set(xticks=(), yticks=())

    piechart_path = pathlib.Path(__file__).parent.resolve() / 'spent.png'
    plt.savefig(piechart_path, bbox_inches='tight', format='png')

    return str(piechart_path)


class ChartCommandExecutor:
    def execute(self, database_adapter, user_input: list[str]) -> dict:
        spent_items = command_spent.SpentCommandExecutor()
        parameters = spent_items.validate(user_input)
        if parameters:
            spent = database_adapter.calculate_spent(
                parameters['start_date'],
                parameters['end_date'],
                parameters['category']
            )
            if spent:
                spent.pop('TOTAL', None)
                spent.pop(parameters['category'].upper(), None)
                return {'chart_path': piechart_maker(spent, parameters['start_date'], parameters['end_date'])}
            elif spent == {}:
                raise NoPurchacesThisParametersException
            raise FailedAccessDatabaseException('calculate spent')
        raise InvalidParametersException
