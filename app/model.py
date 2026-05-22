import csv
import os
import sqlite3


class DataManager:
    FIELDNAMES = [
        'id', 'nama_produk', 'kategori', 'harga_modal', 'harga_jual',
        'jumlah', 'total_modal', 'total_jual', 'untung_rugi', 'margin_pct', 'tanggal', 'status'
    ]

    def __init__(self, db_file='data/transaksi.db'):
        self.db_file = db_file
        os.makedirs(os.path.dirname(self.db_file), exist_ok=True)
        self._create_database()

    def _connect(self):
        connection = sqlite3.connect(self.db_file)
        connection.row_factory = sqlite3.Row
        return connection

    def _create_database(self):
        with self._connect() as conn:
            conn.execute(
                '''CREATE TABLE IF NOT EXISTS transaksi (
                    id TEXT PRIMARY KEY,
                    nama_produk TEXT,
                    kategori TEXT,
                    harga_modal REAL,
                    harga_jual REAL,
                    jumlah INTEGER,
                    total_modal REAL,
                    total_jual REAL,
                    untung_rugi REAL,
                    margin_pct REAL,
                    tanggal TEXT,
                    status TEXT
                )'''
            )
            conn.commit()

    def save_transaction(self, transaction):
        with self._connect() as conn:
            conn.execute(
                '''INSERT OR REPLACE INTO transaksi (
                    id, nama_produk, kategori, harga_modal, harga_jual,
                    jumlah, total_modal, total_jual, untung_rugi, margin_pct, tanggal, status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                [
                    transaction.get('id'),
                    transaction.get('nama_produk'),
                    transaction.get('kategori'),
                    float(transaction.get('harga_modal', 0)),
                    float(transaction.get('harga_jual', 0)),
                    int(transaction.get('jumlah', 0)),
                    float(transaction.get('total_modal', 0)),
                    float(transaction.get('total_jual', 0)),
                    float(transaction.get('untung_rugi', 0)),
                    float(transaction.get('margin_pct', 0)),
                    transaction.get('tanggal'),
                    transaction.get('status')
                ]
            )
            conn.commit()

    def load_transactions(self, limit=None):
        query = 'SELECT * FROM transaksi ORDER BY datetime(tanggal) ASC'
        with self._connect() as conn:
            cursor = conn.cursor()
            if limit:
                cursor.execute(query + ' LIMIT ?', (limit,))
            else:
                cursor.execute(query)
            rows = cursor.fetchall()

        result = []
        for row in rows:
            item = {key: row[key] for key in row.keys()}
            item['harga_modal'] = float(item['harga_modal'])
            item['harga_jual'] = float(item['harga_jual'])
            item['jumlah'] = int(item['jumlah'])
            item['total_modal'] = float(item['total_modal'])
            item['total_jual'] = float(item['total_jual'])
            item['untung_rugi'] = float(item['untung_rugi'])
            item['margin_pct'] = float(item['margin_pct'])
            result.append(item)
        return result

    def clear_all_transactions(self):
        with self._connect() as conn:
            conn.execute('DELETE FROM transaksi')
            conn.commit()

    def export_to_csv(self, export_file):
        transactions = self.load_transactions()
        os.makedirs(os.path.dirname(export_file), exist_ok=True)
        with open(export_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=self.FIELDNAMES)
            writer.writeheader()
            for transaction in transactions:
                writer.writerow({key: transaction.get(key, '') for key in self.FIELDNAMES})
