import telebot
import sqlite3
import datetime as dt

import logging
FORMAT = "%(asctime)-15s %(clientip)s %(user)-8s %(message)s"
logging.basicConfig(format=FORMAT)


class Tweetbot(object):

    bot = None
    def __init__(self, token):
        self.bot = telebot.TeleBot(token)
        self.conn = sqlite3.connect('stalker.db', check_same_thread=False)
        self.initDatabases()
        self.initActions()


    def poll(self):
        self.bot.polling()

    def initActions(self):
        self.start()
        self.stop()
        self.follow_handler()
        self.unfollow_handler()
        self.list_users_handler()

    def initDatabases(self):
        try:
            self.conn.execute('''CREATE TABLE  if not exists stalkers
                (datec text, dateu text, user varchar primary key, enabled integer)''')
        except:
            print("Error al crear la tabla STALKERS")
            raise
        else:
            print("Exito al crear la tabla STALKERS")

    def start(self):
        @self.bot.message_handler(commands=['start'])
        def send_welcome(message):
            self.bot.reply_to(message, "INICIANDO SERVICIO WEB")
            #TODO: Iniciar el ws

    def stop(self):
        @self.bot.message_handler(commands=['stop'])
        def send_welcome(message):
            self.bot.reply_to(message, "PARANDO SERVICIO WEB")
            #TODO: parar el ws

    def follow(self, nombre):
        try:
            now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.conn.execute(
                "insert into stalkers(datec, dateu, user, enabled) values (\"{0}\", \"{0}\", ?, 1)".format(now), (nombre,))
            return True
        except sqlite3.IntegrityError:
            return False
        except:
            raise

    def unfollow(self, nombre):
        try:
            now = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self.conn.execute(
                "update stalkers set dateu = ?, enabled = 0 where user = ?", (now, nombre,))
            return True
        except sqlite3.IntegrityError:
            return False
        except:
            raise


    def follow_handler(self):
        @self.bot.message_handler(commands=['follow'])
        def send_welcome(message):
            arguments = message.text.split(' ')
            name = arguments[1]
            if self.follow(name):
                self.bot.reply_to(message, "SIGUIENDO USUARIO %s" % name)
            else:
                self.bot.reply_to(message, "ERROR AL SEGUIR USUARIO %s: YA EXISTE" % name)


    def unfollow_handler(self):
        @self.bot.message_handler(commands=['unfollow'])
        def send_welcome(message):
            arguments = message.text.split(' ')
            name = arguments[1]
            if self.unfollow(name):
                self.bot.reply_to(message, "DEJANDO DE SEGUIR A USUARIO %s" % name)
            else:
                self.bot.reply_to(
                    message, "ERROR AL DEJAR DE SEGUIR USUARIO %s" % name)


    def list_users(self):
        curs = self.conn.cursor()
        curs.execute("select user from stalkers where enabled = 1")
        results = curs.fetchall()
        results = [str(elem[0]) for elem in results]
        return results


    def list_users_handler(self):
        @self.bot.message_handler(commands=['list_users'])
        def send_welcome(message):
            results = self.list_users()
            self.bot.reply_to(message, "\n".join(results))


# Ponemos nuestro Token generado con el @BotFather
TOKEN = '511354357:AAEOEGk47uDZ4zvxW8vAlFJmcvIxlNOFHtw'

bot = Tweetbot(TOKEN)
bot.poll()


"""
/assign google.com
/ping
/map

AWS
"""
