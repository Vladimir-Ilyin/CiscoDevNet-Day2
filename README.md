Консольное приложение:

```
usage: app_find_mac.py [-h] [--mac MAC [MAC ...]] [--mode {access,trunk}]

Поиск MAC адресов на оборудовании

optional arguments:
  -h, --help            show this help message and exit
  --mac MAC [MAC ...]   Поиск заданного MAC на устройствах
  --mode {access,trunk}
                        Режим интерфейса при поиске - access или trunk, по умолчанию поиск всех
```

Web приложение:

Написано на Flask, запустить flask_app.py
Перейти в браузере по ссылке http://127.0.0.1:5000/