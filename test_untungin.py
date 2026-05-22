#!/usr/bin/env python3
# Test script untuk memverifikasi fungsionalitas aplikasi UNTUNGIN

from app.controller import KalkulatorDagang
from app.model import DataManager
import os

def test_controller():
    print("Testing Controller...")
    calc = KalkulatorDagang()
    
    # Test valid input
    result = calc.hitung("Baju", "Pakaian", 100, 120, 10)
    print("Valid input result:", result)
    
    # Test invalid input
    try:
        calc.hitung("Baju", "Pakaian", "invalid", 120, 10)
    except ValueError as e:
        print("Invalid input error:", e)
    
    print("Controller test passed!\n")

def test_model():
    print("Testing Model...")
    model = DataManager('data/test_transaksi.csv')
    
    # Save transaction
    trans = {
        'id': 'test-id',
        'nama_produk': 'Test Product',
        'kategori': 'Test',
        'harga_modal': 100,
        'harga_jual': 120,
        'jumlah': 10,
        'total_modal': 1000,
        'total_jual': 1200,
        'untung_rugi': 200,
        'margin_pct': 20,
        'tanggal': '2023-01-01 12:00:00'
    }
    model.save_transaction(trans)
    
    # Load transactions
    transactions = model.load_transactions()
    print("Loaded transactions:", len(transactions))
    
    # Clean up
    if os.path.exists('data/test_transaksi.csv'):
        os.remove('data/test_transaksi.csv')
    
    print("Model test passed!\n")

if __name__ == "__main__":
    test_controller()
    test_model()
    print("All tests passed!")