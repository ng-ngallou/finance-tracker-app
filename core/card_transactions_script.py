import numpy as np
import pandas as pd
from pprint import pprint

class Transactions:
    EXP_CATEGORIES: dict = {
        'Rent': [],
        'Supermarket': [],
        'Food at work': [],
        'Food out': [],
        'Car': [],
        'Transportation': [],
        'Shopping': [],
        'Services': [],
        'Spanish': [],
        'Entertainment': [],
        'Hotels': [],
        'Health / Pharmacy': [],
        'Gifts': [],
        'Stocks': [],
        'Other Investments': [],
        'Unclassified': []
    }

    def __init__(self, filename: str, exchange_rate: float) -> None:
        self.exchange_rate = exchange_rate
        self.reimbursements = 0

        # Load the data
        df = pd.read_csv(filename, sep=";", skiprows=1)
        self.df = df.dropna(subset=['Card number'])

    def analyze(self):
        for _, row in self.df.iterrows():
            self.check_pending_transactions(row)
            self.check_for_reimbursements(row)
            self.convert_chf_to_eur(row)

            store = row['Booking text'].split('  ')[0]
            if store in ['NOVAE RESTAURATION', 'NYA*Novae Restauration', 'CERN Restaurant no 2', 'CERN Restaurant no 1',
                             'SELECTA SAS']:
                self.EXP_CATEGORIES['Food at work'].append(row['Debit'])
                continue

            if 'amazon' in store.lower() or 'mueller' in store.lower():
                self.EXP_CATEGORIES['Shopping'].append(row['Debit'])
                continue

            sector = row['Sector']
            if sector in ['Bakeries', 'Restaurants', 'Fast-Food Restaurants', 'Candy and nut stores']:
                self.EXP_CATEGORIES['Food out'].append(row['Debit'])

            elif sector in ['Parking & Garages', 'Gasoline service stations', 'Car component', 'Toll and bridge fees']:
                self.EXP_CATEGORIES['Car'].append(row['Debit'])

            elif sector in ['Grocery stores']:
                self.EXP_CATEGORIES['Supermarket'].append(row['Debit'])

            elif sector in ['Commuter transportation', 'Airlines']:
                self.EXP_CATEGORIES['Transportation'].append(row['Debit'])

            elif sector in ['Clothing store', 'Department stores', 'Clothing - sports', 'Shoe stores',
                                'Pet shops pet foods and supplies stores', 'Leather goods', 'Furniture',
                                'Home supply warehouse stores', 'Cosmetic stores']:
                self.EXP_CATEGORIES['Shopping'].append(row['Debit'])

            elif sector in ['Pharmacies', 'Medical Services Health Practitioners - No Elsewhere Classified']:
                self.EXP_CATEGORIES['Health / Pharmacy'].append(row['Debit'])

            elif sector in ['Barber or beauty shops']:
                self.EXP_CATEGORIES['Services'].append(row['Debit'])

            elif sector in ['Club Membership']:
                self.EXP_CATEGORIES['Entertainment'].append(row['Debit'])

            elif sector in ['Hotels']:
                if row['Debit'] < 120:
                    self.EXP_CATEGORIES['Food out'].append(row['Debit'])
                else:
                    self.EXP_CATEGORIES['Hotels'].append(row['Debit'])

            else:
                self.EXP_CATEGORIES['Unclassified'].append(row)

        self.calculate_expenses()

    def calculate_expenses(self):
        for key in self.EXP_CATEGORIES:
            self.EXP_CATEGORIES[key] = round(float(sum(self.EXP_CATEGORIES[key])), 2)

    def convert_chf_to_eur(self, row):
        if row['Currency'] == 'CHF':
            row['Debit'] = row['Debit'] * self.exchange_rate

    def check_for_reimbursements(self, row):
        if pd.isna(row['Debit']):
            if row['Credit'] is not np.nan:
                self.reimbursements += row['Credit']
                row['Debit'] = -row['Credit']

    def check_pending_transactions(self, row):
        if pd.isna(row['Debit']) and pd.isna(row['Credit']):
            row['Debit'] = row['Amount']

