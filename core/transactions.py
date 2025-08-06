import numpy as np
import pandas as pd
import calendar

class Transactions:

    def __init__(self, filename: str, exchange_rate: float) -> None:
        self.exchange_rate = exchange_rate
        self.reimbursements = 0
        self.EXP_CATEGORIES: dict = {
            'Rent': [1050],
            'Hotels': [],
            'Supermarket': [],
            'Services': [],
            'Food at work': [],
            'Food out': [],
            'Health / Pharmacy': [],
            'Car': [],
            'Transportation': [],
            'Shopping': [],
            # 'Spanish': [],
            'Entertainment': [],
            # 'Gifts': [],
            # 'Stocks': [],
            # 'Other Investments': [],
        }
        self.UNCLASSIFIED_EXPENSES: list = []

        # Load the data
        df = pd.read_csv(filename, sep=";", skiprows=1)
        self.df = df.dropna(subset=['Card number'])

        # Expose month and year for plot title
        last_date = self.df['Purchase date'][0]
        self.year = last_date.split('.')[-1]
        int_month = int(last_date.split('.')[1])
        self.month = calendar.month_name[int_month]

        # Check total expenses approximately
        self.total_expenses = self.calculate_total_expenses(df, exchange_rate)

    def calculate_total_expenses(self, df, exchange_rate):
        curr_eur = df['Currency'] == 'EUR'
        eur_expenses = df[curr_eur]
        curr_chf = df['Currency'] == 'CHF'
        chf_expenses = df[curr_chf]

        return (eur_expenses["Debit"].sum() + chf_expenses["Debit"].sum() * exchange_rate).round(2)

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

            if 'amazon' in store.lower() or 'mueller' in store.lower() or 'AMZN' in store:
                self.EXP_CATEGORIES['Shopping'].append(row['Debit'])
                continue

            if 'CHF SURCHARGE ABROAD'in store:
                self.EXP_CATEGORIES['Services'].append(row['Debit'])
                continue

            sector = row['Sector']
            if sector in ['Bakeries', 'Restaurants', 'Fast-Food Restaurants', 'Candy and nut stores', 'Fast Food Restaurant']:
                self.EXP_CATEGORIES['Food out'].append(row['Debit'])

            elif sector in ['Parking & Garages', 'Gasoline service stations', 'Car component', 'Toll and bridge fees',
                            'Government Services']:
                self.EXP_CATEGORIES['Car'].append(row['Debit'])

            elif sector in ['Grocery stores']:
                self.EXP_CATEGORIES['Supermarket'].append(row['Debit'])

            elif sector in ['Commuter transportation', 'Airlines', 'Passenger railways', 'Swiss International Air Lines']:
                self.EXP_CATEGORIES['Transportation'].append(row['Debit'])

            elif sector in ['Clothing store', 'Department stores', 'Clothing - sports', 'Shoe stores',
                                'Pet shops pet foods and supplies stores', 'Leather goods', 'Furniture',
                                'Home supply warehouse stores', 'Cosmetic stores', 'Electronics Stores',
                            'Card or gift or novelty or souvenir shop', 'Combination Catalog & Retail']:
                self.EXP_CATEGORIES['Shopping'].append(row['Debit'])

            elif sector in ['Pharmacies', 'Medical Services Health Practitioners - No Elsewhere Classified']:
                self.EXP_CATEGORIES['Health / Pharmacy'].append(row['Debit'])

            elif sector in ['Barber or beauty shops', 'Postal Services',
                            'Commercial Sports, Professional Sports Clubs, Athletic Fields, and Sports Promoters']:
                self.EXP_CATEGORIES['Services'].append(row['Debit'])

            elif sector in ['Club Membership', 'Tourist Attractions and Exhibits']:
                self.EXP_CATEGORIES['Entertainment'].append(row['Debit'])

            elif sector in ['Hotels']:
                if row['Debit'] < 120:
                    self.EXP_CATEGORIES['Food out'].append(row['Debit'])
                else:
                    self.EXP_CATEGORIES['Hotels'].append(row['Debit'])

            else:
                self.UNCLASSIFIED_EXPENSES.append(str(row))

        self.calculate_expenses()

    def calculate_expenses(self):
        for key in self.EXP_CATEGORIES:
            self.EXP_CATEGORIES[key] = round(float(sum(self.EXP_CATEGORIES[key])), 2)

    def convert_chf_to_eur(self, row):
        if row['Currency'] == 'CHF':
            row['Debit'] = round(row['Debit'] * self.exchange_rate, 2)

    def check_for_reimbursements(self, row):
        if pd.isna(row['Debit']):
            if row['Credit'] is not np.nan:
                self.reimbursements += row['Credit']
                row['Debit'] = -row['Credit']
                self.total_expenses += row['Debit']

    def check_pending_transactions(self, row):
        if pd.isna(row['Debit']) and pd.isna(row['Credit']):
            row['Debit'] = row['Amount']
            self.total_expenses += row['Debit']

