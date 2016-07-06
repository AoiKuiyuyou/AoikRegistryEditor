[:var_set('', """
# Compile command
aoikdyndocdsl -s README.src.md -n aoikdyndocdsl.ext.all::nto -g README.md
""")
]\
[:HDLR('heading', 'heading')]\
# AoikRegistryEditor
A customizable registry editor.

Tested working with:
- Windows 8.1
- Python 3.5

![Image](https://raw.githubusercontent.com/AoiKuiyuyou/AoikRegistryEditor/0.1.0/screenshot/screenshot.gif)

## Table of Contents
[:hd_to_key('toc')]\
[:toc(beg='next', indent=-1)]

## Setup
[:tod()]

### Setup via pip
Run:
```
pip install git+https://github.com/AoiKuiyuyou/AoikRegistryEditor
```

### Setup via git
Run:
```
git clone https://github.com/AoiKuiyuyou/AoikRegistryEditor

cd AoikRegistryEditor

python setup.py install
```

### Run program
Run:
```
aoikregistryeditor
```
Or:
```
python -m aoikregistryeditor
```
Or:
```
python src/aoikregistryeditor/aoikregistryeditor.py
```

## Usage
[:tod()]

### Show help
Run:
```
aoikregistryeditor --help
```

### Run
Run:
```
aoikregistryeditor
```

### Run with custom menu config
Run:
```
aoikregistryeditor --menu-conf-default > menu_config.py

aoikregistryeditor --menu-conf "menu_config.py::MENU_CONFIG"
```

### Run with custom UI config
Run:
```
aoikregistryeditor --ui-conf-default > ui_config.py

aoikregistryeditor --ui-conf "ui_config.py::configure_ui"
```

### Run with custom field editor factory
Run:
```
aoikregistryeditor --field-editor-default > field_editor_config.py

aoikregistryeditor --field-editor "field_editor_config.py::field_editor_factory"
```

# Acknowledgements
Images used by this program are made by other designers with licenses applied.
See the [acknowledgements](/ACKS.md) file for details.
