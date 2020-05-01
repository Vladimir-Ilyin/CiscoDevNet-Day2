Cisco DevNet Марафон День 2
=======================

В репозитарии два приложения: консольное и web

Консольное приложение:
-----------------------

Для запуска необходимо использовать ключи командной строки.

При запуске без ключей отобразит полную таблицу MAC адресов всех устройств

```
usage: app_find_mac.py [-h] [--mac MAC [MAC ...]] [--mode {access,trunk}]

Поиск MAC адресов на оборудовании

optional arguments:
  -h, --help            show this help message and exit
  --mac MAC [MAC ...]   Поиск заданного MAC на устройствах
  --mode {access,trunk}
                        Режим интерфейса при поиске - access или trunk, по умолчанию поиск всех
```

Пример вывода:

```
#./app_find_mac.py --mac 5475.d07c.890a --mode access
+-----------------+----------+---------------+------+----------------+
|    SwitchName   |   Port   |      Mode     | Vlan |      MAC       |
+-----------------+----------+---------------+------+----------------+
| SW-SEG-LAB-CORE | Gi1/0/11 | static access | 204  | 5475.d07c.890a |
+-----------------+----------+---------------+------+----------------+
```


Web приложение:
-----------------------

Состоит из приложения API и front-end

API написано на Flask, front-end написан с использованием библиотеки knockout и datatables

Для запуска установить `pip install -r requirements.txt` и запустить `flask_app.py`

Перейти в браузере по ссылке `http://127.0.0.1:5000/`

![Экран приложения](/img/screen.PNG?raw=true)

Возможные проблемы Web приложения:
-----------------------

При обращении по адресу отличному от `127.0.0.1` в консоли браузера может отобразится ошибка CORS

В этом случае необходимо либо открыть приложение по адресу `127.0.0.1`, либо сменить в `static/index.html` переменную `BaseURI` (в двух функциях)