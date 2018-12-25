from peewee import *
from collections import OrderedDict
import datetime
import sys

# Agregando base de datos
db = SqliteDatabase('diary.db')


# Creando tabla en DB llamada Entry
class Entry(Model):
    content = TextField()
    timestamp = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = db


def create_and_connect():
    db.connect()
    db.create_tables([Entry], safe=True)


def menu_loop():
    """ Mostrar Menu """
    choice = None
    while choice != 'q':
        print("Presione 'q' para salir")
        for key, value in menu.items():
            print("{}) {} ".format(key, value.__doc__))
        choice = input("Opción: ").lower().strip()

        if choice in menu:
            menu[choice]()


def add_entry():
    """ Agredar entrada """
    print("Escribe lo que estas pensando. Presiona Ctrl + D para terminar.")
    data = sys.stdin.read().strip()
    if data and input("Quieres guardar lo que has escito: [Yn] ").lower().strip() != 'n':
        Entry.create(content=data)
        print("Has guardado correctamente.")


def view_entries(search_query=None):
    """ Ver todas las entradas """
    entries = Entry.select().order_by(Entry.timestamp.desc())

    if search_query:
        entries = entries.where(Entry.content.contains(search_query))

    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        print(timestamp)
        print('*' * len(timestamp))
        print("\n",entry.content,"\n")
        print('n) Siguiente entrada ')
        print('d) Borrar entrada    ')
        print('s) Volver al menu')

        next_action = input("Opcion: ".lower().strip())

        if next_action == 's':
            break
        elif next_action == 'd':
            delete_entries(entry)


def search_entries():
    """ Buscar entradas """
    search_query = input("Que deseas buscar: ").strip()
    view_entries(search_query)


def delete_entries(entry):
    """ Borrar entradas """
    action = input("Estas seguro? [Yn]").lower().strip()

    if action == 'y':
        entry.delete_instance()


menu = OrderedDict([
    ('a', add_entry),
    ('v', view_entries),
    ('s', search_entries),
    ('d', delete_entries)
])


if __name__ == '__main__':
    create_and_connect()
    menu_loop()
