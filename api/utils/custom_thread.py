from django.db import connection
from threading import Thread

class CustomThread(Thread):
    def run(self):
        super().run()
        connection.close()
