import csv
import os
from datetime import datetime

class DataManager:
    FIELDNAMES = [
        'id', 'nama_produk', 'kategori', 'harga_modal', 'harga_jual',
        'jumlah', 'total_modal', 'total_jual', 'untung_rugi', 'margin_pct', 'tanggal'
    ]

    def __init__(self, csv_file='data/transaksi.csv'):
        self.csv_file = csv_file
        self.ensure_csv_exists()

    def ensure_csv_exists(self):
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
                writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
                writer.writeheader()

    def save_transaction(self, transaction):
        with open(self.csv_file, 'a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            sanitized = {key: transaction[key] for key in self.FIELDNAMES if key in transaction}
            writer.writerow(sanitized)

    def load_transactions(self):
        transactions = []
        if os.path.exists(self.csv_file):
            with open(self.csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    transactions.append(row)
        return transactions

    def clear_all_transactions(self):
        with open(self.csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()

    def export_to_csv(self, export_file):
        transactions = self.load_transactions()
        with open(export_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            if transactions:
                writer.writerows(transactions)
