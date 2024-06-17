import numpy as np
import matplotlib.pyplot as plt
from database_connection import db_connection


def graph_view(sys_name):
    database, cursor = db_connection(sys_name)
    month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
                  'November', 'December']
    # Fetching data from database
    petrol_list = []
    diesel_list = []
    for single_month in month_list:
        petrol_total, diesel_total = 0, 0
        cursor.execute(F"SELECT fuel_l, month, fuel_type FROM oil_records INNER JOIN vehicle_register on vehicle_reg = reg_num WHERE month='{single_month}'")
        result = cursor.fetchall()
        for record in result:
            print(record)
            if record[2] == 'Petrol':
                petrol_total += record[0]
            elif record[2] == 'Diesel':
                diesel_total += record[0]
        petrol_list.append(petrol_total)
        diesel_list.append(diesel_total)

    print(petrol_list)
    print(diesel_list)
    # Graph plot
    plt.figure(figsize=(13, 5))
    X_axis = np.arange(len(month_list))

    plt.bar(X_axis - 0.2, petrol_list, 0.4, label='Petrol')
    plt.bar(X_axis + 0.2, diesel_list, 0.4, label='Diesel')

    plt.xticks(X_axis, month_list)
    plt.xlabel("Months")
    plt.ylabel("Liters used")
    plt.title(f"Fuel Usage - {sys_name.replace('_', ' ')}")
    plt.xticks(rotation=20)
    plt.legend()
    plt.show()


if __name__ == '__main__':
    graph_view("OR_SYSTEM_2022")
