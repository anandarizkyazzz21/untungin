import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import StringProperty, ObjectProperty, NumericProperty, ListProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget

from app.controller import KalkulatorDagang
from app.model import DataManager


PRIMARY_GREEN = '#1B5E20'
ACTIVE_GREEN = '#2E7D32'
WHITE = '#FFFFFF'
SUCCESS = '#27AE60'
DANGER = '#E74C3C'


class BGBox(BoxLayout):
    bg_color = ListProperty([1, 1, 1, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            Color(*self.bg_color)
            self._rect = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self._update_rect, size=self._update_rect)

    def _update_rect(self, *args):
        self._rect.pos = self.pos
        self._rect.size = self.size


class Sidebar(Button):
    pass


class DashboardScreen(Screen):
    pass


class HitungBaruScreen(Screen):
    pass


class RiwayatScreen(Screen):
    pass


class LaporanScreen(Screen):
    pass


class UntunginApp(App):
    controller = None
    model = None
    current_result = ObjectProperty(None)

    def build(self):
        Window.size = (1200, 700)
        Window.clearcolor = (1, 1, 1, 1)
        self.controller = KalkulatorDagang()
        self.model = DataManager()

        root = BoxLayout(orientation='horizontal')

        # Sidebar (fixed width) - use canvas before with binding so it resizes
        self.sidebar = BoxLayout(orientation='vertical', size_hint_x=None, width=200, padding=12, spacing=8)
        with self.sidebar.canvas.before:
            Color(*self._hex_to_rgba(PRIMARY_GREEN))
            self._srect = Rectangle(pos=self.sidebar.pos, size=self.sidebar.size)
        self.sidebar.bind(pos=self._update_sidebar_rect, size=self._update_sidebar_rect)

        title = Label(text='UNTUNGIN', size_hint_y=None, height=40, color=self._hex_to_rgba(WHITE), bold=True)
        self.sidebar.add_widget(title)

        # nav buttons
        self.nav_buttons = {}
        for name, screen in [('Dashboard', 'dashboard'), ('Hitung Baru', 'hitung_baru'), ('Riwayat', 'riwayat'), ('Laporan', 'laporan')]:
            btn = Button(text=name, size_hint_y=None, height=42, background_normal='', background_color=self._hex_to_rgba(PRIMARY_GREEN), color=self._hex_to_rgba(WHITE), bold=True)
            btn.bind(on_release=lambda inst, s=screen: self.switch_screen(s))
            self.nav_buttons[screen] = btn
            self.sidebar.add_widget(btn)

        root.add_widget(self.sidebar)

        # Screen Manager area
        self.sm = ScreenManager(size_hint_x=1)
        self.dashboard = DashboardScreen(name='dashboard')
        self.hitung_baru = HitungBaruScreen(name='hitung_baru')
        self.riwayat = RiwayatScreen(name='riwayat')
        self.laporan = LaporanScreen(name='laporan')

        self.sm.add_widget(self.dashboard)
        self.sm.add_widget(self.hitung_baru)
        self.sm.add_widget(self.riwayat)
        self.sm.add_widget(self.laporan)

        root.add_widget(self.sm)

        # Build screens
        self._build_dashboard()
        self._build_hitung_baru()
        self._build_riwayat()
        self._build_laporan()

        # start
        self.switch_screen('dashboard')
        return root

    def _update_sidebar_rect(self, *a):
        self._srect.pos = self.sidebar.pos
        self._srect.size = self.sidebar.size

    def switch_screen(self, screen_name):
        self.sm.current = screen_name
        # active button color
        for k, btn in self.nav_buttons.items():
            if k == screen_name:
                btn.background_color = self._hex_to_rgba(ACTIVE_GREEN)
            else:
                btn.background_color = self._hex_to_rgba(PRIMARY_GREEN)
        # refresh content if needed
        if screen_name == 'dashboard':
            self._refresh_dashboard()
        elif screen_name == 'riwayat':
            self._refresh_riwayat()
        elif screen_name == 'laporan':
            self._refresh_laporan()

    def _build_dashboard(self):
        layout = BGBox(orientation='vertical', padding=16, spacing=12, bg_color=self._hex_to_rgba('#F7F7F7'))
        header = Label(text='[b]Dashboard UNTUNGIN[/b]', size_hint_y=None, height=36, markup=True, color=self._hex_to_rgba('#212121'))
        layout.add_widget(header)

        # summary cards
        cards = BoxLayout(size_hint_y=None, height=100, spacing=10)
        self.card_omzet = self._make_card('Total Omzet', 'Rp 0')
        self.card_modal = self._make_card('Total Modal', 'Rp 0')
        self.card_net = self._make_card('Net Profit', 'Rp 0')
        self.card_count = self._make_card('Transaksi', '0')
        cards.add_widget(self.card_omzet)
        cards.add_widget(self.card_modal)
        cards.add_widget(self.card_net)
        cards.add_widget(self.card_count)
        layout.add_widget(cards)

        # quick calculate (wrapped in soft-contrast container)
        quick = BGBox(orientation='vertical', size_hint_y=None, height=220, padding=10, spacing=8, bg_color=self._hex_to_rgba('#EFEFEF'))
        qlabel = Label(text='[b]Quick Calculate[/b]', size_hint_y=None, height=28, markup=True, color=self._hex_to_rgba('#212121'))
        quick.add_widget(qlabel)
        row = BoxLayout(size_hint_y=None, height=90, spacing=8)
        self.q_modal = TextInput(hint_text='Modal', multiline=False)
        self.q_jual = TextInput(hint_text='Jual', multiline=False)
        self.q_qty = TextInput(hint_text='Qty', multiline=False)
        for w in [self.q_modal, self.q_jual, self.q_qty]:
            w.background_normal = ''
            w.background_color = self._hex_to_rgba(WHITE)
            row.add_widget(w)
        quick.add_widget(row)
        calc_btn = Button(text='Hitung Cepat', size_hint_y=None, height=40, background_color=self._hex_to_rgba(SUCCESS), color=self._hex_to_rgba(WHITE))
        calc_btn.bind(on_release=lambda inst: self._on_quick_calc())
        quick.add_widget(calc_btn)
        self.q_result = Label(text='', halign='left', color=self._hex_to_rgba('#212121'))
        quick.add_widget(self.q_result)
        layout.add_widget(quick)

        self.dashboard.add_widget(layout)

    def _build_hitung_baru(self):
        root = BGBox(orientation='horizontal', padding=16, spacing=12, bg_color=self._hex_to_rgba('#F7F7F7'))

        # Left: Form inputs
        form = BGBox(orientation='vertical', size_hint_x=0.5, padding=12, spacing=8, bg_color=self._hex_to_rgba(WHITE))
        form.add_widget(Label(text='[b]Hitung Baru[/b]', size_hint_y=None, height=34, markup=True, color=self._hex_to_rgba('#212121')))
        self.i_nama = TextInput(hint_text='Nama Produk', multiline=False)
        self.i_kategori = TextInput(hint_text='Kategori', multiline=False)
        self.i_modal = TextInput(hint_text='Harga Modal', multiline=False)
        self.i_jual = TextInput(hint_text='Harga Jual', multiline=False)
        self.i_qty = TextInput(hint_text='Jumlah Unit', multiline=False)
        for w in [self.i_nama, self.i_kategori, self.i_modal, self.i_jual, self.i_qty]:
            w.background_normal = ''
            w.background_color = self._hex_to_rgba(WHITE)
            form.add_widget(w)

        hbtn = Button(text='HITUNG SEKARANG', size_hint_y=None, height=44, background_color=self._hex_to_rgba(SUCCESS), color=self._hex_to_rgba(WHITE))
        hbtn.bind(on_release=lambda inst: self._on_hitung())
        form.add_widget(hbtn)

        # Right: Result panel (white card)
        result_panel = BGBox(orientation='vertical', size_hint_x=0.5, padding=12, spacing=8, bg_color=self._hex_to_rgba(WHITE))
        result_panel.add_widget(Label(text='[b]Hasil Perhitungan[/b]', size_hint_y=None, height=30, markup=True, color=self._hex_to_rgba('#212121')))
        self.r_status = Label(text='--', size_hint_y=None, height=28, markup=True, color=self._hex_to_rgba('#212121'))
        self.r_total_modal = Label(text='Total Modal: Rp 0', size_hint_y=None, height=24, color=self._hex_to_rgba('#212121'))
        self.r_total_jual = Label(text='Total Jual: Rp 0', size_hint_y=None, height=24, color=self._hex_to_rgba('#212121'))
        self.r_untung = Label(text='Untung/Rugi: Rp 0', size_hint_y=None, height=28, color=self._hex_to_rgba('#212121'))
        self.r_margin = Label(text='Margin: 0%', size_hint_y=None, height=24, color=self._hex_to_rgba('#212121'))
        for lbl in [self.r_status, self.r_total_modal, self.r_total_jual, self.r_untung, self.r_margin]:
            result_panel.add_widget(lbl)

        self.save_btn = Button(text='Simpan Transaksi', size_hint_y=None, height=44, background_color=self._hex_to_rgba(SUCCESS), disabled=True, color=self._hex_to_rgba(WHITE))
        self.save_btn.bind(on_release=lambda inst: self._on_save())
        result_panel.add_widget(self.save_btn)

        root.add_widget(form)
        root.add_widget(result_panel)
        self.hitung_baru.add_widget(root)

    def _build_riwayat(self):
        layout = BGBox(orientation='vertical', padding=12, spacing=8, bg_color=self._hex_to_rgba('#F7F7F7'))
        layout.add_widget(Label(text='[b]Riwayat Transaksi[/b]', size_hint_y=None, height=36, markup=True, color=self._hex_to_rgba('#212121')))

        actions = BoxLayout(size_hint_y=None, height=44, spacing=8)
        exp = Button(text='Ekspor CSV', background_color=(0.2, 0.55, 0.91, 1), color=self._hex_to_rgba(WHITE))
        exp.bind(on_release=lambda inst: self.model.export_to_csv('data/transaksi_export.csv'))
        clr = Button(text='Hapus Semua', background_color=self._hex_to_rgba(DANGER), color=self._hex_to_rgba(WHITE))
        clr.bind(on_release=lambda inst: (self.model.clear_all_transactions(), self._refresh_riwayat()))
        actions.add_widget(exp)
        actions.add_widget(clr)
        layout.add_widget(actions)

        # header
        header = GridLayout(cols=6, size_hint_y=None, height=32)
        for t in ['Produk', 'Modal', 'Jual', 'Qty', 'Untung/Rugi', 'Status']:
            header.add_widget(Label(text=f'[b]{t}[/b]', markup=True, color=self._hex_to_rgba('#212121')))
        layout.add_widget(header)

        # rows in ScrollView
        self.history_scroll = ScrollView()
        self.history_grid = GridLayout(cols=6, size_hint_y=None, spacing=4)
        self.history_grid.bind(minimum_height=self.history_grid.setter('height'))
        self.history_scroll.add_widget(self.history_grid)
        layout.add_widget(self.history_scroll)

        self.riwayat.add_widget(layout)
        self._refresh_riwayat()

    def _build_laporan(self):
        layout = BGBox(orientation='vertical', padding=12, spacing=8, bg_color=self._hex_to_rgba('#F7F7F7'))
        layout.add_widget(Label(text='[b]Laporan Harian[/b]', size_hint_y=None, height=36, markup=True, color=self._hex_to_rgba('#212121')))

        self.report_header = GridLayout(cols=5, size_hint_y=None, height=32)
        for t in ['Tanggal', 'Total Transaksi', 'Total Untung', 'Total Rugi', 'Net Profit']:
            self.report_header.add_widget(Label(text=f'[b]{t}[/b]', markup=True, color=self._hex_to_rgba('#212121')))
        layout.add_widget(self.report_header)

        self.report_scroll = ScrollView()
        self.report_grid = GridLayout(cols=5, size_hint_y=None, spacing=4)
        self.report_grid.bind(minimum_height=self.report_grid.setter('height'))
        self.report_scroll.add_widget(self.report_grid)
        layout.add_widget(self.report_scroll)

        self.laporan.add_widget(layout)
        self._refresh_laporan()

    def _on_quick_calc(self):
        modal = self.q_modal.text
        jual = self.q_jual.text
        qty = self.q_qty.text
        try:
            res = self.controller.hitung('', '', modal, jual, qty)
            self.q_result.text = f"Status: {res['status']} | Untung/Rugi: Rp {res['untung_rugi']:.2f} | Margin: {res['margin_pct']:.2f}%"
        except Exception as e:
            self.q_result.text = f"Error: {e}"

    def _on_hitung(self):
        nama = self.i_nama.text
        kategori = self.i_kategori.text
        modal = self.i_modal.text
        jual = self.i_jual.text
        qty = self.i_qty.text
        try:
            res = self.controller.hitung(nama, kategori, modal, jual, qty)
            self.current_result = res
            # update panel
            self.r_total_modal.text = f"Total Modal: Rp {res['total_modal']:.2f}"
            self.r_total_jual.text = f"Total Jual: Rp {res['total_jual']:.2f}"
            self.r_untung.text = f"Untung/Rugi: Rp {res['untung_rugi']:.2f}"
            self.r_margin.text = f"Margin: {res['margin_pct']:.2f}%"
            if res['status'] == 'UNTUNG':
                self.r_status.text = '[b]Status: UNTUNG[/b]'
                self.r_status.color = self._hex_to_rgba(SUCCESS)
            elif res['status'] == 'RUGI':
                self.r_status.text = '[b]Status: RUGI[/b]'
                self.r_status.color = self._hex_to_rgba(DANGER)
            else:
                self.r_status.text = '[b]Status: BEP[/b]'
                self.r_status.color = self._hex_to_rgba('#212121')
            self.save_btn.disabled = False
        except Exception as e:
            self.r_status.text = f"Error: {e}"
            self.save_btn.disabled = True

    def _on_save(self):
        if not self.current_result:
            return
        self.model.save_transaction(self.current_result)
        self.save_btn.disabled = True
        self.r_status.text = '[b]Transaksi disimpan.[/b]'
        self.r_status.color = self._hex_to_rgba('#212121')

    def _refresh_riwayat(self):
        self.history_grid.clear_widgets()
        txs = self.model.load_transactions()
        for idx, tr in enumerate(txs):
            # each cell is a white BGBox with dark text
            for key in ['nama_produk', 'harga_modal', 'harga_jual', 'jumlah', 'untung_rugi']:
                cell = BGBox(size_hint_y=None, height=32, bg_color=self._hex_to_rgba(WHITE))
                cell.add_widget(Label(text=str(tr.get(key, '')), color=self._hex_to_rgba('#212121')))
                self.history_grid.add_widget(cell)
            status = self._status_from_tr(tr)
            cell = BGBox(size_hint_y=None, height=32, bg_color=self._hex_to_rgba(WHITE))
            lbl = Label(text=status, color=self._hex_to_rgba('#212121'))
            cell.add_widget(lbl)
            self.history_grid.add_widget(cell)

    def _refresh_laporan(self):
        self.report_grid.clear_widgets()
        summary = self.build_daily_summary()
        for date, data in summary:
            for val in [str(date), str(data['count']), f"Rp {data['profit']:.2f}", f"Rp {data['loss']:.2f}", f"Rp {data['net']:.2f}"]:
                cell = BGBox(size_hint_y=None, height=32, bg_color=self._hex_to_rgba(WHITE))
                cell.add_widget(Label(text=val, color=self._hex_to_rgba('#212121')))
                self.report_grid.add_widget(cell)

    def _refresh_dashboard(self):
        omzet, modal, net, count = self.calculate_overall_summary()
        self.card_omzet.children[0].text = f'Rp {omzet:.2f}'
        self.card_modal.children[0].text = f'Rp {modal:.2f}'
        self.card_net.children[0].text = f'Rp {net:.2f}'
        self.card_count.children[0].text = str(count)

    def _make_card(self, title, value):
        box = BoxLayout(orientation='vertical', padding=8, spacing=4)
        with box.canvas.before:
            Color(*self._hex_to_rgba(WHITE))
            Rectangle(pos=box.pos, size=box.size)
        title_lbl = Label(text=title, size_hint_y=None, height=20, color=self._hex_to_rgba('#424242'))
        value_lbl = Label(text=f'[b]{value}[/b]', size_hint_y=None, height=28, markup=True, font_size='18sp', color=self._hex_to_rgba('#212121'))
        box.add_widget(title_lbl)
        box.add_widget(value_lbl)
        return box

    def calculate_overall_summary(self):
        txs = self.model.load_transactions()
        omzet = sum(float(t.get('total_jual', 0) or 0) for t in txs)
        modal = sum(float(t.get('total_modal', 0) or 0) for t in txs)
        net = sum(float(t.get('untung_rugi', 0) or 0) for t in txs)
        return omzet, modal, net, len(txs)

    def build_daily_summary(self):
        txs = self.model.load_transactions()
        summary = {}
        for tr in txs:
            date = tr.get('tanggal', '').split(' ')[0] if tr.get('tanggal') else 'Unknown'
            data = summary.setdefault(date, {'count': 0, 'profit': 0.0, 'loss': 0.0, 'net': 0.0})
            unt = float(tr.get('untung_rugi', 0) or 0)
            data['count'] += 1
            if unt > 0:
                data['profit'] += unt
            elif unt < 0:
                data['loss'] += unt
            data['net'] += unt
        return sorted(summary.items())

    def build_overall_totals(self, summary):
        totals = {'total_transactions': 0, 'total_untung': 0.0, 'total_rugi': 0.0, 'net_profit': 0.0}
        for _, v in summary:
            totals['total_transactions'] += v['count']
            totals['total_untung'] += v['profit']
            totals['total_rugi'] += v['loss']
            totals['net_profit'] += v['net']
        return totals

    def _status_from_tr(self, tr):
        try:
            val = float(tr.get('untung_rugi', 0) or 0)
        except Exception:
            return 'BEP'
        if val > 0:
            return 'UNTUNG'
        if val < 0:
            return 'RUGI'
        return 'BEP'

    def _hex_to_rgba(self, hx):
        hx = hx.lstrip('#')
        lv = len(hx)
        return tuple(int(hx[i:i+lv//3], 16)/255.0 for i in range(0, lv, lv//3)) + (1,)


def main():
    UntunginApp().run()


if __name__ == '__main__':
    main()
