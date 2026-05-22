import os
from kivy.core.window import Window
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
    # Simulate a typical Android phone portrait size when running on PC
    Window.size = (360, 640)
    primary_color = ListProperty([0.11, 0.34, 0.16, 1])
    accent_color = ListProperty([0.18, 0.49, 0.16, 1])
    background_color = ListProperty([0.96, 0.95, 0.92, 1])
    card_color = ListProperty([1, 1, 1, 1])
    text_color = ListProperty([0.12, 0.14, 0.11, 1])
    success_text = ListProperty([0.15, 0.55, 0.24, 1])
    danger_text = ListProperty([0.78, 0.22, 0.18, 1])
    muted_text = ListProperty([0.44, 0.46, 0.44, 1])
    divider_color = ListProperty([0.84, 0.84, 0.84, 1])

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
            'laporan': 'laporan_btn',
        }
        for key, btn_id in mapping.items():
            button = self.root.ids.get(btn_id)
            if button:
                active = key == screen_name
                button.background_color = self.accent_color if active else (1, 1, 1, 1)
                button.color = (1, 1, 1, 1) if active else self.text_color
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

        self.refresh_transaction_cards(transactions)
        self.refresh_recent_activity(transactions)

    def refresh_transaction_cards(self, transactions):
        dashboard_ids = self.get_screen_ids('dashboard')
        container = dashboard_ids.dashboard_transactions_list
        container.clear_widgets()
        if not transactions:
            container.add_widget(Label(text='Belum ada transaksi', color=self.muted_text, halign='center', valign='middle', size_hint_y=None, height=dp(100), text_size=(self.root.width, None)))
            return
        latest = transactions[-6:][::-1]
        for transaction in latest:
            card = self._build_transaction_card(transaction)
            container.add_widget(card)

    def refresh_recent_activity(self, transactions):
        container = self.get_screen_ids('dashboard').activity_container
        container.clear_widgets()
        recent = transactions[-4:][::-1]
        if not recent:
            container.add_widget(Label(text='Belum ada aktivitas terbaru', color=self.muted_text, halign='center', valign='middle', size_hint_y=None, height=dp(80), text_size=(self.root.width, None)))
            return
        for transaction in recent:
            container.add_widget(self._build_activity_card(transaction))

    def refresh_history(self):
        container = self.get_screen_ids('riwayat').history_grid
        container.clear_widgets()
        transactions = self.data_manager.load_transactions()[::-1]
        if not transactions:
            container.add_widget(Label(text='Riwayat kosong', color=self.muted_text, halign='center', valign='middle', size_hint_y=None, height=dp(100), text_size=(self.root.width, None)))
            return
        for transaction in transactions:
            container.add_widget(self._build_history_card(transaction))

    def refresh_report(self):
        container = self.get_screen_ids('laporan').report_grid
        container.clear_widgets()
        summary = self.build_daily_summary()
        if not summary:
            container.add_widget(Label(text='Belum ada laporan harian', color=self.muted_text, halign='center', valign='middle', size_hint_y=None, height=dp(100), text_size=(self.root.width, None)))
            return
        for date, values in summary:
            container.add_widget(self._build_report_card(date, values))

    def build_daily_summary(self):
        transactions = self.data_manager.load_transactions()
        summary = {}
        for tx in transactions:
            date = tx['tanggal'].split(' ')[0]
            entry = summary.setdefault(date, {'count': 0, 'profit': 0.0, 'loss': 0.0, 'net': 0.0})
            entry['count'] += 1
            if tx['untung_rugi'] > 0:
                entry['profit'] += tx['untung_rugi']
            elif tx['untung_rugi'] < 0:
                entry['loss'] += abs(tx['untung_rugi'])
            entry['net'] += tx['untung_rugi']
        return sorted(summary.items(), reverse=True)

    def set_quick_status(self, status):
        transactions = self.data_manager.load_transactions()
        filtered = [tx for tx in transactions if tx['status'] == status]
        total = sum(tx['untung_rugi'] for tx in filtered)
        dashboard_ids = self.get_screen_ids('dashboard')
        dashboard_ids.quick_value.text = f'{len(filtered)} transaksi'
        dashboard_ids.quick_state_label.text = f'Total {status.title()}: Rp {total:,.2f}'

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
            ids.feedback_label.text = 'Periksa input dan coba lagi.'

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

    def _create_label(self, text, color=None, bold=False, size='14sp', halign='left'):
        label = Label(
            text=text,
            color=color or self.text_color,
            bold=bold,
            font_size=size,
            halign=halign,
            valign='middle'
        )
        label.bind(size=lambda instance, *args: setattr(instance, 'text_size', (instance.width, instance.height)))
        return label

    def _build_transaction_card(self, transaction):
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(120), padding=dp(14), spacing=dp(8))
        with card.canvas.before:
            Color(rgba=self.card_color)
            rect = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=lambda instance, *args: setattr(rect, 'pos', card.pos), size=lambda instance, *args: setattr(rect, 'size', card.size))

        header = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(24))
        header.add_widget(self._create_label(transaction['nama_produk'], bold=True, size='16sp'))
        status_color = self.success_text if transaction['untung_rugi'] >= 0 else self.danger_text
        header.add_widget(self._create_label(transaction['status'], color=status_color, bold=True, size='14sp', halign='right'))
        card.add_widget(header)

        card.add_widget(self._create_label(f"Qty: {transaction['jumlah']}", color=self.muted_text, size='14sp'))
        card.add_widget(self._create_label(f"Modal: Rp {transaction['total_modal']:,.2f}", color=self.muted_text, size='14sp'))
        amount_color = self.success_text if transaction['untung_rugi'] >= 0 else self.danger_text
        card.add_widget(self._create_label(f"Untung/Rugi: Rp {transaction['untung_rugi']:,.2f}", color=amount_color, bold=True, size='15sp'))
        return card

    def _build_activity_card(self, transaction):
        card = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(72), padding=dp(12), spacing=dp(10))
        with card.canvas.before:
            Color(rgba=self.card_color)
            rect = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=lambda instance, *args: setattr(rect, 'pos', card.pos), size=lambda instance, *args: setattr(rect, 'size', card.size))

        side = BoxLayout(size_hint_x=None, width=dp(8))
        side.canvas.before.clear()
        with side.canvas.before:
            Color(rgba=self.accent_color)
            rect_side = Rectangle(pos=side.pos, size=side.size)
        side.bind(pos=lambda instance, *args: setattr(rect_side, 'pos', side.pos), size=lambda instance, *args: setattr(rect_side, 'size', side.size))
        card.add_widget(side)

        content = BoxLayout(orientation='vertical', spacing=dp(4))
        content.add_widget(self._create_label(transaction['nama_produk'], bold=True, size='15sp'))
        content.add_widget(self._create_label(f"{transaction['status']} · {transaction['tanggal']}", color=self.muted_text, size='13sp'))
        card.add_widget(content)
        return card

    def _build_history_card(self, transaction):
        card = self._build_transaction_card(transaction)
        return card

    def _build_report_card(self, date, values):
        card = BoxLayout(orientation='vertical', size_hint_y=None, height=dp(110), padding=dp(14), spacing=dp(8))
        with card.canvas.before:
            Color(rgba=self.card_color)
            rect = Rectangle(pos=card.pos, size=card.size)
        card.bind(pos=lambda instance, *args: setattr(rect, 'pos', card.pos), size=lambda instance, *args: setattr(rect, 'size', card.size))

        card.add_widget(self._create_label(date, bold=True, size='16sp'))
        card.add_widget(self._create_label(f"Transaksi: {values['count']}", color=self.muted_text, size='14sp'))
        card.add_widget(self._create_label(f"Total Untung: Rp {values['profit']:,.2f}", color=self.success_text, size='14sp'))
        card.add_widget(self._create_label(f"Total Rugi: Rp {values['loss']:,.2f}", color=self.danger_text, size='14sp'))
        card.add_widget(self._create_label(f"Net Profit: Rp {values['net']:,.2f}", bold=True, size='15sp'))
        return card


if __name__ == '__main__':
    UntunginApp().run()
