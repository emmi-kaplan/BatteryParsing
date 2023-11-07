import pandas as pd
from matplotlib import pyplot as plt


def plot_battery_data(charge_plotpoints, discharge_plotpoints):
    """ Parses data from a tab separated text file and plots the result """
    charge_x, charge_y = zip(*charge_plotpoints)
    discharge_x, discharge_y = zip(*discharge_plotpoints)
    # create figure
    fig, ax = plt.subplots()
    ax.plot(charge_x, charge_y, label='Charge Capacity')
    ax.plot(discharge_x, discharge_y, label='Discharge Capacity')
    ax.set_xlabel('Cycle #')
    ax.set_title('Battery Capacity')
    ax.legend()
    # save plot to file
    plt.savefig('CapacityPlots/Fig1')
    plt.show()


def extract_half_cycles(cycle_data):
    """ Find each new half cycle and record capacity data at the end of the previous cycle"""
    final_charge_capacities = []
    final_discharge_capacities = []
    current_half_cycle = 0
    current_capacity = 0
    for datapoint in cycle_data:
        # only collect a new datapoint if the half-cycle increases. Data starts at half-cycle = 0
        if datapoint['half cycle'] > current_half_cycle:
            # if half cycle num is even, add previous half cycle datapoint to the charge list
            if current_half_cycle % 2 == 0:
                final_charge_capacities.append((current_cycle_num, current_capacity))
            # if half cycle num is odd, add previous half cycle datapoint to the discharge list
            else:
                final_discharge_capacities.append((current_cycle_num, current_capacity))
            current_half_cycle = datapoint['half cycle']
        # re-assign capacity and cycle number after previous datapoint has been recorded
        current_capacity = datapoint['Capacity/mA.h']
        current_cycle_num = datapoint['cycle number']
    return final_charge_capacities, final_discharge_capacities


def create_dict_from_file(filename):
    """ Creates a dictionary of relevant data columns from a tab separated text file """
    use_cols = ['half cycle', 'cycle number', 'Capacity/mA.h']
    my_data = pd.read_csv(filename, sep='\t', index_col=False, usecols=use_cols, skiprows=67,)
    # transform the DataFrame to list of datapoints in dictionary form
    list_of_dicts = [item for item in my_data.T.to_dict().values()]
    return list_of_dicts


# Press the green button to run the script.
if __name__ == '__main__':
    cycle_data = create_dict_from_file('BatteryData/battery_parsing.txt')
    charge_plotpoints, discharge_plotpoints = extract_half_cycles(cycle_data)
    plot_battery_data(charge_plotpoints, discharge_plotpoints)

