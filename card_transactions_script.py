import numpy as np
import pandas as pd
from pprint import pprint

def analyze_transactions():

    CHF_TO_EUR_COEFFICIENT = 1.07
    CHECK_TOTAL = 0
    REIMBURSEMENTS = 0

    # Load the data
    df = pd.read_csv('July_card_transactions.csv', sep=";", skiprows=1)
    df = df.dropna(subset=['Card number'])

    # Check total expenses
    curr_eur = df['Currency'] == 'EUR'
    eur_expenses = df[curr_eur]
    curr_chf = df['Currency'] == 'CHF'
    chf_expenses = df[curr_chf]
    print(f'Total expenses in EUR: {eur_expenses["Debit"].sum().round(2)} EUR\n'
          f'Total expenses in CHF: {chf_expenses["Debit"].sum().round(2)} CHF\n'
          f'------------------------------------------------------------------\n'
          f'CARD TOTAL WITHOUT REIMBURSEMENTS: {(eur_expenses["Debit"].sum() + chf_expenses["Debit"].sum() * CHF_TO_EUR_COEFFICIENT).round(2)} EUR\n')

    # Check transactions
    my_categories = {'Rent': [], 'Supermarket': [], 'Food at work': [], 'Food out': [], 'Car': [], 'Transportation': [],
                     'Shopping': [], 'Services': [], 'Spanish': [], 'Entertainment': [], 'Hotels': [],
                     'Health / Pharmacy': [], 'Gifts / Loans': [], 'Stocks': [], 'Other Investments': [],
                     }
    non_classified = []

    for index, row in df.iterrows():
        row_store = row['Booking text'].split('  ')[0]

        if pd.isna(row['Debit']) and pd.isna(row['Credit']):
            print(f'-------------Transactions is NOT completed yet!: \n{row}\n')
            row['Debit'] = row['Amount']

        if pd.isna(row['Debit']):
            if row['Credit'] is not np.nan:
                REIMBURSEMENTS += row['Credit']
                row['Debit'] = -row['Credit']
                print(f'---------------Reimbursement: \n{row}\n')

        if row['Currency'] == 'CHF':
            row['Debit'] = row['Debit'] * CHF_TO_EUR_COEFFICIENT

        if row_store in ['NOVAE RESTAURATION', 'NYA*Novae Restauration', 'CERN Restaurant no 2', 'CERN Restaurant no 1',
                         'SELECTA SAS']:
            my_categories['Food at work'].append(row['Debit'])
            continue

        if 'amazon' in row_store.lower() or 'mueller' in row_store.lower():
            my_categories['Shopping'].append(row['Debit'])
            # print(f'Shopping: {row}')
            continue

        row_sector = row['Sector']
        if row_sector in ['Bakeries', 'Restaurants', 'Fast-Food Restaurants', 'Candy and nut stores']:
            my_categories['Food out'].append(row['Debit'])

        elif row_sector in ['Parking & Garages', 'Gasoline service stations', 'Car component', 'Toll and bridge fees']:
            my_categories['Car'].append(row['Debit'])

        elif row_sector in ['Grocery stores']:
            my_categories['Supermarket'].append(row['Debit'])

        elif row_sector in ['Commuter transportation', 'Airlines']:
            my_categories['Transportation'].append(row['Debit'])

        elif row_sector in ['Clothing store', 'Department stores', 'Clothing - sports', 'Shoe stores',
                            'Pet shops pet foods and supplies stores', 'Leather goods', 'Furniture',
                            'Home supply warehouse stores', 'Cosmetic stores']:
            my_categories['Shopping'].append(row['Debit'])
            # print(f'Shopping: {row}')

        elif row_sector in ['Pharmacies', 'Medical Services Health Practitioners - No Elsewhere Classified']:
            my_categories['Health / Pharmacy'].append(row['Debit'])

        elif row_sector in ['Barber or beauty shops']:
            my_categories['Services'].append(row['Debit'])

        elif row_sector in ['Club Membership']:
            my_categories['Entertainment'].append(row['Debit'])

        elif row_sector in ['Hotels']:
            if row['Debit'] < 120:
                my_categories['Food out'].append(row['Debit'])
            else:
                my_categories['Hotels'].append(row['Debit'])

        else:
            non_classified.append(row)
            CHECK_TOTAL += row['Debit']

    for key in my_categories:
        my_categories[key] = round(float(sum(my_categories[key])), 2)
        CHECK_TOTAL += my_categories[key]
    CHECK_TOTAL = round(CHECK_TOTAL, 2)


    print(f'\nCARD TOTAL EXPENSES COUNTED: {CHECK_TOTAL} EUR\n'
          f'REIMBURSEMENTS: {REIMBURSEMENTS} EUR\n'
          f'Sanity Check: {CHECK_TOTAL + REIMBURSEMENTS} EUR\n')
    pprint(my_categories)
    print(f'\nNon classified: \n'
          f'------------------------------------------------------------------'
          f'\n{non_classified}')

#     pie_plot(list(my_categories.values()), list(my_categories.keys()))
#
#
# def pie_plot(data, labels):
#     fig, ax = plt.subplots()
#     title('January 2025')
#     ax.pie(data, labels=labels, autopct='%1.1f%%')
#     plt.show()


if __name__ == '__main__':
    card_transactions()
