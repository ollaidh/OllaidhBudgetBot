import matplotlib.pyplot as plt
import numpy as np
import pathlib


def piechart_maker(spent: dict, start_date: str, end_date: str):
    # formatting function to get value and percentage at the same time on pie chart:
    def autopct_format(numbers):
        def my_format(pct):
            total = sum(numbers)
            val = int(round(pct*total/100.0))
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


if __name__ == '__main__':
    piechart_maker({'takeaway': 15, 'grocery': 10, 'meat': 35, 'dairy': 15, 'training': 10, 'gasoline': 45}, '2023-01', '2023-03')



