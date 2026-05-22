from datetime import datetime
import uuid

class KalkulatorDagang:
    def __init__(self):
        pass

    def hitung(self, nama_produk, kategori, modal, jual, qty):
        # Validasi input
        try:
            modal = float(modal)
            jual = float(jual)
            qty = int(qty)
            if modal <= 0 or jual <= 0 or qty <= 0:
                raise ValueError("Nilai harus lebih besar dari 0")
        except (ValueError, TypeError):
            raise ValueError("Input harus berupa angka positif")

        # Kalkulasi
        total_modal = modal * qty
        total_jual = jual * qty
        untung_rugi = total_jual - total_modal
        margin_pct = (untung_rugi / total_modal) * 100 if total_modal != 0 else 0

        # Status
        if untung_rugi > 0:
            status = 'UNTUNG'
        elif untung_rugi < 0:
            status = 'RUGI'
        else:
            status = 'BEP'

        # ID unik
        transaksi_id = str(uuid.uuid4())

        # Tanggal
        tanggal = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        return {
            'id': transaksi_id,
            'nama_produk': nama_produk,
            'kategori': kategori,
            'harga_modal': modal,
            'harga_jual': jual,
            'jumlah': qty,
            'total_modal': total_modal,
            'total_jual': total_jual,
            'untung_rugi': untung_rugi,
            'margin_pct': margin_pct,
            'tanggal': tanggal,
            'status': status
        }