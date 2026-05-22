# Testpy Python GUI Applications

This workspace contains several Python applications with GUI interfaces:

- `kalkulator_kivy.py`: A daily calorie calculator using Kivy GUI.
- `kalkulator_tkinter.py`: A daily calorie calculator using Tkinter GUI.
- `toko_baju_kivy.py`: A clothing store app using Kivy GUI.
- `toko_baju_tkinter.py`: A clothing store app using Tkinter GUI.
- **`main.py`**: 🆕 **Untungin** - Modern store management app with Glassmorphism design using KivyMD.

## Requirements

- Python 3.8+ (recommended)
- Kivy (for Kivy apps)
- KivyMD (for Untungin app)
- Tkinter (usually included with Python)

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the apps

### Calorie Calculator
- **Kivy version**: `python kalkulator_kivy.py`
- **Tkinter version**: `python kalkulator_tkinter.py`

### Clothing Store
- **Kivy version**: `python toko_baju_kivy.py`
  - Automatically switches to console/text mode in headless environments
  - Full GUI in graphical environments
- **Tkinter version**: `python toko_baju_tkinter.py`

### 🆕 Untungin - Modern Store Management
- **Main app**: `python main.py`
- **Database test**: `python database.py`
- **Usage examples**: `python example_usage.py`

## 🛍️ Untungin Features

- **Dashboard**: Total profit and capital display
- **Inventory**: Product list with stock management
- **Kasir**: Sales recording with auto-profit calculation
- **SQLite Database**: Local data storage
- **Glassmorphism UI**: Modern transparent design
- **Mobile-first**: Optimized for touch interfaces

## Notes

- **Kivy apps**: Automatically detect environment and switch to console/text mode when GUI cannot be displayed
- **Tkinter apps**: Work in most environments including terminals with GUI support
- **Untungin**: Requires graphical environment for full UI experience
- **Console mode**: Full functionality available through text-based menu system
- Order data is saved in JSON files in the same directory
- Untungin data is saved in `untungin.db` SQLite database
