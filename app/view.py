import kivy
kivy.require('2.0.0')

from kivy.app import App
from kivy.core.window import Window
from kivy.graphics import Color, Ellipse, Line, Rectangle, RoundedRectangle
from kivy.properties import ObjectProperty, ListProperty
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

PRIMARY_GREEN = '#1E5628'
ACTIVE_GREEN = '#2E7D32'
SAGE = '#A5B89A'
SIDEBAR_BG = '#D9E6D1'
WHITE = '#FFFFFF'
BROKEN_WHITE = '#F7F4EE'
SUCCESS = '#27AE60'
DANGER = '#E74C3C'
LIGHT_GREY = '#F3F5F7'
CARD_BORDER = '#DBD3C8'
TEXT_COLOR = (0.12, 0.14, 0.11, 1)


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


class SidebarButton(Button):
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

        self.sidebar = BoxLayout(orientation='vertical', size_hint_x=None, width=220, spacing=14, padding=(20, 24, 20, 24))
        with self.sidebar.canvas.before:
            Color(*self._hex_to_rgba(SIDEBAR_BG))
            self._sidebar_rect = Rectangle(pos=self.sidebar.pos, size=self.sidebar.size)
        self.sidebar.bind(pos=self._update_sidebar_rect, size=self._update_sidebar_rect)

        self.sidebar.add_widget(Label(text='UNTUNGIN', size_hint_y=None, height=48, bold=True, color=self._hex_to_rgba(PRIMARY_GREEN), font_size='22sp'))

        self.nav_buttons = {}
        for label, screen in [('🏠 Dashboard', 'dashboard'), ('🧾 Hitung Baru', 'hitung_baru'), ('📜 Riwayat', 'riwayat'), ('📊 Laporan', 'laporan')]:
            btn = SidebarButton(text=label, size_hint_y=None, height=44, background_normal='', background_color=self._hex_to_rgba(PRIMARY_GREEN), color=self._hex_to_rgba(WHITE), bold=True)
            btn.bind(on_release=lambda inst, s=screen: self.switch_screen(s))
            self.nav_buttons[screen] = btn
            self.sidebar.add_widget(btn)

        self.sm = ScreenManager()
        self.dashboard = DashboardScreen(name='dashboard')
        self.hitung_baru = HitungBaruScreen(name='hitung_baru')
        self.riwayat = RiwayatScreen(name='riwayat')
        self.laporan = LaporanScreen(name='laporan')

        self.sm.add_widget(self.dashboard)
        self.sm.add_widget(self.hitung_baru)
        self.sm.add_widget(self.riwayat)
        self.sm.add_widget(self.laporan)

        root.add_widget(self.sidebar)
        root.add_widget(self.sm)

        self._build_dashboard()
        self._build_hitung_baru()
        self._build_riwayat()
        self._build_laporan()

        self.switch_screen('dashboard')
        return root

    def _update_sidebar_rect(self, *args):
        self._sidebar_rect.pos = self.sidebar.pos
        self._sidebar_rect.size = self.sidebar.size

    def switch_screen(self, screen_name):
        self.sm.current = screen_name
        for key, btn in self.nav_buttons.items():
            btn.background_color = self._hex_to_rgba(ACTIVE_GREEN if key == screen_name else PRIMARY_GREEN)

        if screen_name == 'dashboard':
            self._refresh_dashboard()
        elif screen_name == 'riwayat':
            self._refresh_riwayat()
        elif screen_name == 'laporan':
            self._refresh_laporan()

    def _build_dashboard(self):
        layout = BoxLayout(orientation='vertical', spacing=16, padding=20)

        banner = BGBox(orientation='vertical', size_hint_y=None, height=170, padding=20, spacing=10, bg_color=self._hex_to_rgba(PRIMARY_GREEN))
        with banner.canvas.before:
            Color(*self._hex_to_rgba(PRIMARY_GREEN))
            self._banner_rect = RoundedRectangle(pos=banner.pos, size=banner.size, radius=[20])
        banner.bind(pos=self._update_banner_graphics, size=self._update_banner_graphics)

        title = Label(text='UNTUNGIN', font_size='32sp', bold=True, color=self._hex_to_rgba(WHITE), halign='left', valign='middle', size_hint_y=None, height=40)
        title.bind(size=title.setter('text_size'))
        subtitle = Label(text='Aplikasi Perhitungan Untung & Rugi Pedagang', font_size='16sp', color=self._hex_to_rgba(WHITE), halign='left', valign='middle', size_hint_y=None, height=24)
        subtitle.bind(size=subtitle.setter('text_size'))

        bottom_row = BoxLayout(size_hint_y=None, height=44, spacing=10)
        badge = BGBox(size_hint=(None, None), size=(160, 40), bg_color=self._hex_to_rgba(ACTIVE_GREEN))
        badge_label = Label(text='Rp UNTUNGIN', bold=True, font_size='14sp', color=self._hex_to_rgba(WHITE), halign='center', valign='middle')
        badge_label.bind(size=badge_label.setter('text_size'))
        badge.add_widget(badge_label)
        bottom_row.add_widget(badge)
        bottom_row.add_widget(Widget())

        banner.add_widget(title)
        banner.add_widget(subtitle)
        banner.add_widget(Widget())
        banner.add_widget(bottom_row)

        cards = BoxLayout(orientation='horizontal', spacing=12, size_hint_y=None, height=140)
        self.card_omzet = self._make_dashboard_card('Total Omzet', 'Rp 0', '💰', self._hex_to_rgba(PRIMARY_GREEN))
        self.card_pengeluaran = self._make_dashboard_card('Total Pengeluaran', 'Rp 0', '👛', self._hex_to_rgba(DANGER))
        self.card_net = self._make_dashboard_card('Net Profit', 'Rp 0', '📈', self._hex_to_rgba(SUCCESS))
        self.card_state = self._make_dashboard_card('Quick Calculate', '', '⚡', self._hex_to_rgba('#212121'), state_badges=True)
        cards.add_widget(self.card_omzet)
        cards.add_widget(self.card_pengeluaran)
        cards.add_widget(self.card_net)
        cards.add_widget(self.card_state)

        bottom = BoxLayout(orientation='horizontal', spacing=16)

        left_panel = BGBox(orientation='vertical', padding=18, spacing=14, bg_color=self._hex_to_rgba(BROKEN_WHITE), size_hint_x=0.68)
        left_panel.add_widget(Label(text='Tabel Ringkasan Transaksi', size_hint_y=None, height=34, bold=True, color=TEXT_COLOR, halign='left', valign='middle'))

        header = GridLayout(cols=5, size_hint_y=None, height=36, spacing=8)
        for label in ['Produk', 'Modal', 'Jual', 'Qty', 'Untung/Rugi']:
            lbl = Label(text=f'[b]{label}[/b]', markup=True, color=TEXT_COLOR, halign='center', valign='middle', size_hint_y=None, height=36, shorten=True)
            lbl.bind(size=lbl.setter('text_size'))
            header.add_widget(lbl)
        left_panel.add_widget(header)

        self.dashboard_table_scroll = ScrollView(size_hint=(1, 1), bar_width=10, do_scroll_x=False)
        self.dashboard_table = BoxLayout(orientation='vertical', size_hint_y=None, spacing=2)
        self.dashboard_table.bind(minimum_height=self.dashboard_table.setter('height'))
        self.dashboard_table_scroll.add_widget(self.dashboard_table)
        left_panel.add_widget(self.dashboard_table_scroll)

        action_row = BoxLayout(size_hint_y=None, height=78, spacing=12)
        view_details = Button(text='View Details', size_hint_x=0.6, background_normal='', background_color=self._hex_to_rgba(PRIMARY_GREEN), color=self._hex_to_rgba(WHITE), bold=True)
        view_details.bind(on_release=lambda inst: self.switch_screen('riwayat'))

        quick_calc_panel = BGBox(orientation='vertical', padding=12, spacing=10, bg_color=self._hex_to_rgba(WHITE))
        quick_calc_panel.add_widget(Label(text='Quick Calculate', size_hint_y=None, height=26, bold=True, color=TEXT_COLOR, halign='left', valign='middle'))
        btn_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=36)
        untung_btn = Button(text='Untung', background_normal='', background_color=self._hex_to_rgba(PRIMARY_GREEN), color=self._hex_to_rgba(WHITE), bold=True)
        rugi_btn = Button(text='Rugi', background_normal='', background_color=self._hex_to_rgba(DANGER), color=self._hex_to_rgba(WHITE), bold=True)
        untung_btn.bind(on_release=lambda inst: self._set_profit_state('UNTUNG'))
        rugi_btn.bind(on_release=lambda inst: self._set_profit_state('RUGI'))
        btn_row.add_widget(untung_btn)
        btn_row.add_widget(rugi_btn)
        quick_calc_panel.add_widget(btn_row)
        self.q_status_label = Label(text='Pilih status untuk melihat ringkasan', size_hint_y=None, height=24, color=TEXT_COLOR, halign='left', valign='middle')
        self.q_status_label.bind(size=self.q_status_label.setter('text_size'))
        quick_calc_panel.add_widget(self.q_status_label)

        action_row.add_widget(view_details)
        action_row.add_widget(quick_calc_panel)
        left_panel.add_widget(action_row)

        right_panel = BGBox(orientation='vertical', padding=18, spacing=14, bg_color=self._hex_to_rgba(WHITE), size_hint_x=0.32)
        right_panel.add_widget(Label(text='Recent Activity', size_hint_y=None, height=34, bold=True, color=TEXT_COLOR, halign='left', valign='middle'))
        self.recent_activity_scroll = ScrollView(size_hint=(1, 1), bar_width=10)
        self.recent_activity_container = BoxLayout(orientation='vertical', size_hint_y=None, spacing=12)
        self.recent_activity_container.bind(minimum_height=self.recent_activity_container.setter('height'))
        self.recent_activity_scroll.add_widget(self.recent_activity_container)
        right_panel.add_widget(self.recent_activity_scroll)

        bottom.add_widget(left_panel)
        bottom.add_widget(right_panel)

        layout.add_widget(banner)
        layout.add_widget(cards)
        layout.add_widget(bottom)
        self.dashboard.add_widget(layout)

        self._refresh_dashboard()

    def _build_hitung_baru(self):
        root = BGBox(orientation='horizontal', padding=20, spacing=20, bg_color=self._hex_to_rgba(LIGHT_GREY))

        form_panel = BGBox(orientation='vertical', size_hint_x=0.55, padding=20, spacing=14, bg_color=self._hex_to_rgba(WHITE))
        form_panel.add_widget(Label(text='Hitung Baru', size_hint_y=None, height=34, bold=True, color=TEXT_COLOR))

        nama_field, self.i_nama = self._make_form_input('Nama Produk')
        kategori_field, self.i_kategori = self._make_form_input('Kategori')
        modal_field, self.i_modal = self._make_form_input('Harga Modal')
        jual_field, self.i_jual = self._make_form_input('Harga Jual')
        qty_field, self.i_qty = self._make_form_input('Jumlah Unit')
        for field in [nama_field, kategori_field, modal_field, jual_field, qty_field]:
            form_panel.add_widget(field)

        submit_btn = Button(text='HITUNG SEKARANG', size_hint_y=None, height=36, background_normal='', background_color=self._hex_to_rgba(PRIMARY_GREEN), color=self._hex_to_rgba(WHITE), bold=True)
        submit_btn.bind(on_release=lambda inst: self._on_hitung())
        form_panel.add_widget(submit_btn)

        result_panel = BGBox(orientation='vertical', size_hint_x=0.45, padding=20, spacing=10, bg_color=self._hex_to_rgba(WHITE))
        result_panel.add_widget(Label(text='Hasil Perhitungan', size_hint_y=None, height=34, bold=True, color=TEXT_COLOR))
        self.r_status = Label(text='Status: -', size_hint_y=None, height=28, color=TEXT_COLOR, halign='left', valign='middle', shorten=True)
        self.r_total_modal = Label(text='Total Modal: Rp 0', size_hint_y=None, height=28, color=TEXT_COLOR, halign='left', valign='middle', shorten=True)
        self.r_total_jual = Label(text='Total Jual: Rp 0', size_hint_y=None, height=28, color=TEXT_COLOR, halign='left', valign='middle', shorten=True)
        self.r_untung = Label(text='Untung/Rugi: Rp 0', size_hint_y=None, height=28, color=TEXT_COLOR, halign='left', valign='middle', shorten=True)
        self.r_margin = Label(text='Margin: 0%', size_hint_y=None, height=28, color=TEXT_COLOR, halign='left', valign='middle', shorten=True)
        for label in [self.r_status, self.r_total_modal, self.r_total_jual, self.r_untung, self.r_margin]:
            label.bind(size=label.setter('text_size'))
            result_panel.add_widget(label)

        self.save_btn = Button(text='Simpan Transaksi', size_hint_y=None, height=36, background_normal='', background_color=self._hex_to_rgba(ACTIVE_GREEN), color=self._hex_to_rgba(WHITE), disabled=True, bold=True)
        self.save_btn.bind(on_release=lambda inst: self._on_save())
        result_panel.add_widget(self.save_btn)

        root.add_widget(form_panel)
        root.add_widget(result_panel)
        self.hitung_baru.add_widget(root)

    def _build_riwayat(self):
        layout = BGBox(orientation='vertical', padding=20, spacing=14, bg_color=self._hex_to_rgba(LIGHT_GREY))
        layout.add_widget(Label(text='Riwayat Transaksi', size_hint_y=None, height=36, bold=True, color=TEXT_COLOR))

        action_row = BoxLayout(size_hint_y=None, height=44, spacing=12)
        export_btn = Button(text='Ekspor CSV', size_hint_y=None, height=36, background_normal='', background_color=self._hex_to_rgba(PRIMARY_GREEN), color=self._hex_to_rgba(WHITE), bold=True)
        export_btn.bind(on_release=lambda inst: self.model.export_to_csv('data/transaksi_export.csv'))
        clear_btn = Button(text='Hapus Semua', size_hint_y=None, height=36, background_normal='', background_color=self._hex_to_rgba(DANGER), color=self._hex_to_rgba(WHITE), bold=True)
        clear_btn.bind(on_release=lambda inst: (self.model.clear_all_transactions(), self._refresh_riwayat()))
        action_row.add_widget(export_btn)
        action_row.add_widget(clear_btn)
        layout.add_widget(action_row)

        header = GridLayout(cols=6, size_hint_y=None, height=35, spacing=6)
        for title in ['Produk', 'Modal', 'Jual', 'Qty', 'Untung/Rugi', 'Status']:
            label = Label(text=f'[b]{title}[/b]', markup=True, color=TEXT_COLOR, halign='center', valign='middle', size_hint_y=None, height=35, shorten=True)
            label.bind(size=label.setter('text_size'))
            header.add_widget(label)
        layout.add_widget(header)

        self.history_scroll = ScrollView(size_hint=(1, 1))
        self.history_grid = GridLayout(cols=6, size_hint_y=None, spacing=6)
        self.history_grid.bind(minimum_height=self.history_grid.setter('height'))
        self.history_scroll.add_widget(self.history_grid)
        layout.add_widget(self.history_scroll)

        self.riwayat.add_widget(layout)
        self._refresh_riwayat()

    def _build_laporan(self):
        layout = BGBox(orientation='vertical', padding=20, spacing=14, bg_color=self._hex_to_rgba(LIGHT_GREY))
        layout.add_widget(Label(text='Laporan Harian', size_hint_y=None, height=36, bold=True, color=TEXT_COLOR))

        self.report_header = GridLayout(cols=5, size_hint_y=None, height=35, spacing=6)
        for title in ['Tanggal', 'Total Transaksi', 'Total Untung', 'Total Rugi', 'Net Profit']:
            label = Label(text=f'[b]{title}[/b]', markup=True, color=TEXT_COLOR, halign='center', valign='middle', size_hint_y=None, height=35, shorten=True)
            label.bind(size=label.setter('text_size'))
            self.report_header.add_widget(label)
        layout.add_widget(self.report_header)

        self.report_scroll = ScrollView(size_hint=(1, 1))
        self.report_grid = GridLayout(cols=5, size_hint_y=None, spacing=6)
        self.report_grid.bind(minimum_height=self.report_grid.setter('height'))
        self.report_scroll.add_widget(self.report_grid)
        layout.add_widget(self.report_scroll)

        self.laporan.add_widget(layout)
        self._refresh_laporan()

    def _make_dashboard_card(self, title, value, icon, value_color, state_badges=False):
        card = BGBox(orientation='vertical', padding=16, spacing=10, bg_color=self._hex_to_rgba(WHITE), size_hint_y=None, height=120)
        with card.canvas.after:
            Color(*self._hex_to_rgba(CARD_BORDER))
            card._border = Line(rectangle=(card.x, card.y, card.width, card.height), width=1)
        card.bind(pos=lambda instance, *args: self._update_shape(instance._border, instance), size=lambda instance, *args: self._update_shape(instance._border, instance))

        title_row = BoxLayout(orientation='horizontal', size_hint_y=None, height=26, spacing=8)
        title_row.add_widget(Label(text=icon, font_size='20sp', color=self._hex_to_rgba(PRIMARY_GREEN), size_hint_x=None, width=28, halign='center', valign='middle'))
        title_label = Label(text=title, color=TEXT_COLOR, halign='left', valign='middle')
        title_label.bind(size=title_label.setter('text_size'))
        title_row.add_widget(title_label)
        card.add_widget(title_row)

        if state_badges:
            badge_row = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=38)
            badge_row.add_widget(self._make_badge('Untung', self._hex_to_rgba(SUCCESS), self._hex_to_rgba(WHITE)))
            badge_row.add_widget(self._make_badge('Rugi', self._hex_to_rgba(DANGER), self._hex_to_rgba(WHITE)))
            card.add_widget(badge_row)
            card.value_label = None
        else:
            value_label = Label(text=value, font_size='22sp', bold=True, color=value_color, halign='left', valign='middle', size_hint_y=None, height=36)
            value_label.bind(size=value_label.setter('text_size'))
            card.add_widget(value_label)
            card.value_label = value_label
        return card

    def _make_badge(self, text, bg_color, text_color):
        badge = BGBox(size_hint=(None, None), size=(100, 34), padding=8, bg_color=bg_color)
        label = Label(text=text, bold=True, color=text_color, halign='center', valign='middle', size_hint_y=None, height=18)
        label.bind(size=label.setter('text_size'))
        badge.add_widget(label)
        return badge

    def _set_profit_state(self, state):
        if state == 'UNTUNG':
            self.q_status_label.text = 'Menampilkan status UNTUNG. Semua ringkasan positif.'
        else:
            self.q_status_label.text = 'Menampilkan status RUGI. Semua ringkasan negatif.'

    def _make_recent_activity_item(self, name, status, timestamp):
        row = BGBox(orientation='horizontal', padding=10, spacing=10, size_hint_y=None, height=72, bg_color=self._hex_to_rgba(WHITE))
        indicator = BGBox(size_hint=(None, None), size=(12, 12), bg_color=self._hex_to_rgba(PRIMARY_GREEN))
        row.add_widget(indicator)
        info = BoxLayout(orientation='vertical', spacing=4)
        info.add_widget(Label(text=name, color=TEXT_COLOR, bold=True, halign='left', valign='middle', size_hint_y=None, height=24))
        info.add_widget(Label(text=f'{status} · {timestamp}', color=(0.32, 0.38, 0.28, 1), halign='left', valign='middle', size_hint_y=None, height=20))
        row.add_widget(info)
        return row

    def _refresh_recent_activity(self):
        self.recent_activity_container.clear_widgets()
        transactions = self.model.load_transactions()
        if not transactions:
            self.recent_activity_container.add_widget(Label(text='Belum ada aktivitas terbaru', color=(0.5, 0.5, 0.5, 1), halign='center', valign='middle', size_hint_y=None, height=40))
            return
        latest = transactions[-5:][::-1]
        for tx in latest:
            name = str(tx.get('nama_produk', 'Produk'))
            status = self._status_from_tr(tx)
            timestamp = tx.get('tanggal', 'beberapa saat lalu')
            self.recent_activity_container.add_widget(self._make_recent_activity_item(name, status, timestamp))

    def _make_form_input(self, label_text):
        container = BoxLayout(orientation='vertical', size_hint_y=None, height=72, spacing=4)
        label = Label(text=label_text, size_hint_y=None, height=18, color=TEXT_COLOR, halign='left', valign='middle', shorten=True)
        label.bind(size=label.setter('text_size'))
        input_widget = TextInput(multiline=False, size_hint_y=None, height=36, background_normal='', background_color=self._hex_to_rgba(WHITE), foreground_color=TEXT_COLOR, padding=[10, 8, 10, 8])
        container.add_widget(label)
        container.add_widget(input_widget)
        return container, input_widget

    def _make_table_label(self, text):
        label = Label(text=text, color=TEXT_COLOR, halign='center', valign='middle', size_hint_y=None, height=30, shorten=True)
        label.bind(size=label.setter('text_size'))
        return label

    def _update_shape(self, shape, widget):
        shape.rectangle = (widget.x, widget.y, widget.width, widget.height)

    def _update_banner_graphics(self, instance, *args):
        self._banner_rect.pos = instance.pos
        self._banner_rect.size = instance.size

    def _refresh_dashboard(self):
        omzet, modal, net, _ = self.calculate_overall_summary()
        if self.card_omzet.value_label:
            self.card_omzet.value_label.text = f'Rp {omzet:,.2f}'
        if self.card_pengeluaran.value_label:
            self.card_pengeluaran.value_label.text = f'Rp {modal:,.2f}'
        if self.card_net.value_label:
            self.card_net.value_label.text = f'Rp {net:,.2f}'
        self._refresh_dashboard_table()
        self._refresh_recent_activity()

    def _refresh_dashboard_table(self):
        self.dashboard_table.clear_widgets()
        transactions = self.model.load_transactions()
        if not transactions:
            placeholder = Label(text='Tidak ada transaksi', color=(0.4, 0.4, 0.4, 1), halign='center', valign='middle', size_hint_y=None, height=40, shorten=True)
            placeholder.bind(size=placeholder.setter('text_size'))
            self.dashboard_table.add_widget(placeholder)
            return

        latest = transactions[-8:]
        for index, tx in enumerate(latest):
            row_bg = BGBox(orientation='horizontal', size_hint_y=None, height=40, spacing=8,
                           bg_color=self._hex_to_rgba(BROKEN_WHITE) if index % 2 else self._hex_to_rgba(WHITE))
            row_bg.add_widget(self._make_table_label(str(tx.get('nama_produk', ''))))
            row_bg.add_widget(self._make_table_label(f"Rp {float(tx.get('harga_modal', 0)):,.2f}"))
            row_bg.add_widget(self._make_table_label(f"Rp {float(tx.get('harga_jual', 0)):,.2f}"))
            row_bg.add_widget(self._make_table_label(str(tx.get('jumlah', ''))))
            untung_label = self._make_table_label(f"Rp {float(tx.get('untung_rugi', 0)):,.2f}")
            if float(tx.get('untung_rugi', 0) or 0) < 0:
                untung_label.color = (0.78, 0.22, 0.18, 1)
            row_bg.add_widget(untung_label)
            self.dashboard_table.add_widget(row_bg)

    def _on_quick_calc(self):
        modal = self.q_modal_input.text
        jual = self.q_jual_input.text
        qty = self.q_qty_input.text
        try:
            res = self.controller.hitung('', '', modal, jual, qty)
            self.q_result_status.text = f"Status: {res['status']}"
            self.q_result_bayar.text = f"Untung/Rugi: Rp {res['untung_rugi']:.2f}"
            self.q_result_margin.text = f"Margin: {res['margin_pct']:.2f}%"
        except Exception as exc:
            self.q_result_status.text = f"Error: {exc}"
            self.q_result_bayar.text = ''
            self.q_result_margin.text = ''

    def _on_hitung(self):
        nama = self.i_nama.text
        kategori = self.i_kategori.text
        modal = self.i_modal.text
        jual = self.i_jual.text
        qty = self.i_qty.text
        try:
            res = self.controller.hitung(nama, kategori, modal, jual, qty)
            self.current_result = res
            self.r_status.text = f"Status: {res['status']}"
            self.r_total_modal.text = f"Total Modal: Rp {res['total_modal']:.2f}"
            self.r_total_jual.text = f"Total Jual: Rp {res['total_jual']:.2f}"
            self.r_untung.text = f"Untung/Rugi: Rp {res['untung_rugi']:.2f}"
            self.r_margin.text = f"Margin: {res['margin_pct']:.2f}%"
            self.save_btn.disabled = False
        except Exception as exc:
            self.r_status.text = f"Error: {exc}"
            self.save_btn.disabled = True

    def _on_save(self):
        if not self.current_result:
            return
        self.model.save_transaction(self.current_result)
        self.save_btn.disabled = True
        self.r_status.text = 'Transaksi disimpan.'
        self._refresh_dashboard()

    def _refresh_riwayat(self):
        self.history_grid.clear_widgets()
        txs = self.model.load_transactions()
        if not txs:
            for _ in range(6):
                self.history_grid.add_widget(Widget(size_hint_y=None, height=35))
            return
        for tr in txs:
            self.history_grid.add_widget(self._make_table_label(str(tr.get('nama_produk', ''))))
            self.history_grid.add_widget(self._make_table_label(f"Rp {float(tr.get('harga_modal', 0)):,.2f}"))
            self.history_grid.add_widget(self._make_table_label(f"Rp {float(tr.get('harga_jual', 0)):,.2f}"))
            self.history_grid.add_widget(self._make_table_label(str(tr.get('jumlah', ''))))
            self.history_grid.add_widget(self._make_table_label(f"Rp {float(tr.get('untung_rugi', 0)):,.2f}"))
            self.history_grid.add_widget(self._make_table_label(self._status_from_tr(tr)))

    def _refresh_laporan(self):
        self.report_grid.clear_widgets()
        summary = self.build_daily_summary()
        if not summary:
            for _ in range(5):
                self.report_grid.add_widget(Widget(size_hint_y=None, height=35))
            return
        for date, data in summary:
            self.report_grid.add_widget(self._make_table_label(str(date)))
            self.report_grid.add_widget(self._make_table_label(str(data['count'])))
            self.report_grid.add_widget(self._make_table_label(f"Rp {data['profit']:.2f}"))
            self.report_grid.add_widget(self._make_table_label(f"Rp {data['loss']:.2f}"))
            self.report_grid.add_widget(self._make_table_label(f"Rp {data['net']:.2f}"))

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
        return tuple(int(hx[i:i+lv // 3], 16) / 255.0 for i in range(0, lv, lv // 3)) + (1,)


def main():
    UntunginApp().run()


if __name__ == '__main__':
    main()
