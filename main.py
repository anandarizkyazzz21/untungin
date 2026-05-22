import os
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.graphics import Color, Rectangle

from app.controller import KalkulatorDagang
from app.model import DataManager


class DashboardScreen(Screen):
    pass


class HitungBaruScreen(Screen):
    pass


class RiwayatScreen(Screen):
    pass


class LaporanScreen(Screen):
    pass


class UntunginApp(App):
    kv_file = ''
    sidebar_bg = ListProperty([217 / 255, 230 / 255, 209 / 255, 1])
    nav_color = ListProperty([0.11, 0.34, 0.16, 1])
    active_nav_color = ListProperty([0.18, 0.49, 0.16, 1])
    card_bg = ListProperty([247 / 255, 244 / 255, 238 / 255, 1])
    border_color = ListProperty([219 / 255, 211 / 255, 200 / 255, 1])
    text_color = ListProperty([0.12, 0.14, 0.11, 1])
    danger_text = ListProperty([0.78, 0.22, 0.18, 1])
    success_text = ListProperty([0.15, 0.55, 0.24, 1])

    def build(self):
        self.controller = KalkulatorDagang()
        self.data_manager = DataManager()
        self.current_result = None

        self.root = Builder.load_file(os.path.join(os.path.dirname(__file__), 'untungin.kv'))
        self.switch_screen('dashboard')
        return self.root

    def get_screen_ids(self, screen_name):
        return self.root.ids.screen_manager.get_screen(screen_name).ids

    def switch_screen(self, screen_name):
        self.root.ids.screen_manager.current = screen_name
        mapping = {
            'dashboard': 'dashboard_btn',
            'hitung_baru': 'hitung_btn',
            'riwayat': 'riwayat_btn',
            'laporan': 'laporan_btn'
        }
        for key, btn_id in mapping.items():
            btn = self.root.ids.get(btn_id)
            if btn:
                btn.background_color = self.active_nav_color if key == screen_name else self.nav_color

        if screen_name == 'dashboard':
            self.refresh_dashboard()
        elif screen_name == 'riwayat':
            self.refresh_history()
        elif screen_name == 'laporan':
            self.refresh_report()

    def refresh_dashboard(self):
        transactions = self.data_manager.load_transactions()
        omzet = sum(tx['total_jual'] for tx in transactions)
        pengeluaran = sum(tx['total_modal'] for tx in transactions)
        net_profit = sum(tx['untung_rugi'] for tx in transactions)
        dashboard_ids = self.get_screen_ids('dashboard')

        dashboard_ids.omzet_value.text = f'Rp {omzet:,.2f}'
        dashboard_ids.pengeluaran_value.text = f'Rp {pengeluaran:,.2f}'
        dashboard_ids.net_value.text = f'Rp {net_profit:,.2f}'
        dashboard_ids.quick_value.text = f'{len(transactions)} transaksi'
        dashboard_ids.quick_state_label.text = 'Tekan Untung / Rugi untuk melihat ringkasan cepat'

        self.refresh_dashboard_table(transactions)
        self.refresh_recent_activity(transactions)

    def refresh_dashboard_table(self, transactions):
        body = self.get_screen_ids('dashboard').dashboard_table
        body.clear_widgets()
        if not transactions:
            body.add_widget(Label(text='Tidak ada transaksi', color=(0.4, 0.4, 0.4, 1), halign='center', valign='middle', size_hint_y=None, height=dp(40), text_size=(self.root.width, None)))
            return

        latest = transactions[-8:]
        for index, tx in enumerate(latest):
            row = self._build_table_row([
                str(tx['nama_produk']),
                f"Rp {tx['harga_modal']:,.2f}",
                f"Rp {tx['harga_jual']:,.2f}",
                str(tx['jumlah']),
                f"Rp {tx['untung_rugi']:,.2f}"
            ], stripe=index % 2 == 1, negative_column=4)
            body.add_widget(row)

    def refresh_recent_activity(self, transactions):
        container = self.get_screen_ids('dashboard').activity_container
        container.clear_widgets()
        latest = transactions[-5:][::-1]
        if not latest:
            container.add_widget(Label(text='Belum ada aktivitas terbaru', color=(0.5, 0.5, 0.5, 1), halign='center', valign='middle', size_hint_y=None, height=dp(40), text_size=(self.root.width, None)))
            return
        for tx in latest:
            row = self._build_activity_row(tx)
            container.add_widget(row)

    def refresh_history(self):
        container = self.get_screen_ids('riwayat').history_grid
        container.clear_widgets()
        transactions = self.data_manager.load_transactions()
        if not transactions:
            container.add_widget(Label(text='Tidak ada data transaksi', color=(0.4, 0.4, 0.4, 1), halign='center', valign='middle', size_hint_y=None, height=dp(40), text_size=(self.root.width, None)))
            return
        for index, tx in enumerate(transactions[::-1]):
            row = self._build_table_row([
                str(tx['nama_produk']),
                f"Rp {tx['harga_modal']:,.2f}",
                f"Rp {tx['harga_jual']:,.2f}",
                str(tx['jumlah']),
                f"Rp {tx['untung_rugi']:,.2f}",
                tx['status']
            ], stripe=index % 2 == 1, negative_column=4)
            container.add_widget(row)

    def refresh_report(self):
        container = self.get_screen_ids('laporan').report_grid
        container.clear_widgets()
        summary = self.build_daily_summary()
        if not summary:
            container.add_widget(Label(text='Belum ada laporan', color=(0.4, 0.4, 0.4, 1), halign='center', valign='middle', size_hint_y=None, height=dp(40), text_size=(self.root.width, None)))
            return
        for date, data in summary:
            row = self._build_table_row([
                date,
                str(data['count']),
                f"Rp {data['profit']:,.2f}",
                f"Rp {data['loss']:,.2f}",
                f"Rp {data['net']:,.2f}"
            ], stripe=False)
            container.add_widget(row)

    def build_daily_summary(self):
        transactions = self.data_manager.load_transactions()
        summary = {}
        for tx in transactions:
            date = tx['tanggal'].split(' ')[0]
            row = summary.setdefault(date, {'count': 0, 'profit': 0.0, 'loss': 0.0, 'net': 0.0})
            row['count'] += 1
            amount = tx['untung_rugi']
            if amount > 0:
                row['profit'] += amount
            elif amount < 0:
                row['loss'] += amount
            row['net'] += amount
        return sorted(summary.items())

    def set_quick_status(self, status):
        transactions = self.data_manager.load_transactions()
        filtered = [tx for tx in transactions if tx['status'] == status]
        total = sum(tx['untung_rugi'] for tx in filtered)
        dashboard_ids = self.get_screen_ids('dashboard')
        dashboard_ids.quick_value.text = f'{len(filtered)} transaksi'
        dashboard_ids.quick_state_label.text = f'Total {status.lower()}: Rp {total:,.2f}'

    def on_calculate(self):
        ids = self.get_screen_ids('hitung_baru')
        try:
            result = self.controller.hitung(
                ids.product_input.text,
                ids.category_input.text,
                ids.modal_input.text,
                ids.price_input.text,
                ids.qty_input.text
            )
            self.current_result = result
            ids.status_result.text = f"Status: {result['status']}"
            ids.total_modal_result.text = f"Total Modal: Rp {result['total_modal']:,.2f}"
            ids.total_jual_result.text = f"Total Jual: Rp {result['total_jual']:,.2f}"
            ids.untung_result.text = f"Untung/Rugi: Rp {result['untung_rugi']:,.2f}"
            ids.margin_result.text = f"Margin: {result['margin_pct']:,.2f}%"
            ids.save_btn.disabled = False
            ids.feedback_label.text = 'Hasil siap disimpan.'
        except Exception as err:
            ids.status_result.text = f'Error: {err}'
            ids.save_btn.disabled = True
            ids.feedback_label.text = 'Periksa kembali input angka.'

    def on_save_transaction(self):
        ids = self.get_screen_ids('hitung_baru')
        if not self.current_result:
            return
        self.data_manager.save_transaction(self.current_result)
        ids.save_btn.disabled = True
        ids.feedback_label.text = 'Transaksi berhasil disimpan.'
        self.current_result = None
        self.refresh_all()

    def on_export_csv(self):
        self.data_manager.export_to_csv('data/transaksi_export.csv')

    def on_clear_transactions(self):
        self.data_manager.clear_all_transactions()
        self.refresh_all()

    def refresh_all(self):
        self.refresh_dashboard()
        self.refresh_history()
        self.refresh_report()

    def _build_table_row(self, values, stripe=False, negative_column=None):
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(40), spacing=dp(8))
        with row.canvas.before:
            Color(rgba=self.card_bg if stripe else (1, 1, 1, 1))
            rect = Rectangle(pos=row.pos, size=row.size)
        def _update_rect(instance, *args):
            rect.pos = instance.pos
            rect.size = instance.size
        row.bind(pos=_update_rect, size=_update_rect)

        for index, text in enumerate(values):
            color = self.danger_text if negative_column is not None and index == negative_column and text.startswith('Rp -') else self.text_color
            label = Label(text=text, color=color, halign='center', valign='middle', size_hint_x=1)
            label.text_size = (label.width, label.height)
            label.bind(size=lambda instance, *args: setattr(instance, 'text_size', (instance.width, instance.height)))
            row.add_widget(label)
        return row

    def _build_activity_row(self, transaction):
        row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(72), spacing=dp(12))
        with row.canvas.before:
            Color(rgba=(1, 1, 1, 1))
            rect = Rectangle(pos=row.pos, size=row.size)
        def _update_rect(instance, *args):
            rect.pos = instance.pos
            rect.size = instance.size
        row.bind(pos=_update_rect, size=_update_rect)

        bullet = Label(text='●', color=self.active_nav_color, size_hint_x=None, width=dp(16), halign='center', valign='middle')
        bullet.text_size = (bullet.width, bullet.height)
        row.add_widget(bullet)
        info = BoxLayout(orientation='vertical', spacing=dp(4))
        info.add_widget(Label(text=str(transaction['nama_produk']), color=self.text_color, bold=True, halign='left', valign='middle'))
        info.add_widget(Label(text=f"{transaction['status']} · {transaction['tanggal']}", color=(0.32, 0.38, 0.28, 1), halign='left', valign='middle'))
        row.add_widget(info)
        return row


if __name__ == '__main__':
    UntunginApp().run()
