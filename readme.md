## Запуск проекта
```bash
poetry shell
poetry install
python create_db.py # Создать локальную базу данных
python executor.py # Запустить цикл, который будет мониторить tasks
```
## Использование проекта
Флаги
1) `-u` `--User` - пользователь, от имени которого совершается комманда
2) `-a` `--Action` - вид действия для совершения
   1) `create` - создать скрипт на исполнение
      1) `-c` `--Command` - скрипт за исполнение
      2) `-s` `--Schedule` - дата исполнения в формате "YYYY-MM-DD HH:MM:SS"
   2) `completed` - посмотреть завершенные задачи
      1) `-l` `--Limit` - сколько последних завершенных задач вывести
   3) `scheduled` - посмотреть pending задачи
      1) `-l` `--Limit` - сколько pending задач вывести
   4) `cancled` - TODO
      1) `-t` `--Task` - id таска на удаление. TODO

Примеры:

- В одном терминале запущен executor.py
- Во втором терминале использовать main.py
```bash
 python main.py -u user_1 -a create -c dir -s '2022-12-01 12:00:00'
 python main.py -u user_1 -a completed -l 5
```

```bash
 python main.py -u user_1 -a create -c dir -s '2022-12-30 12:00:00'
 python main.py -u user_1 -a scheduled -l 5
```

## TODO:
1) Добавить удаление tasks
2) Добавить отсылку по почте
3) В executor используется while True с паузой в 1 сек. на мониторинг тасков и последовательное исполнение.
Можно придумать что-нибудь более гибкое
4) Добавить больше валидаций в schemas
5) Поменять формат печати в терминал