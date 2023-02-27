import os
import disnake

default_prefix = ["/.", "r.", "R."] #обычный префикс бота

error_color = disnake.Colour.from_rgb(255, 0, 0)
success_color = disnake.Colour.from_rgb(0, 255, 64)
warning_color = disnake.Colour.from_rgb(255, 238, 0)
main_color = disnake.Colour.from_rgb(55, 0, 255)

#цвета ембедов

developers = [942347441016021012] #айдишники разрабов

betatestbottoken = "MTA3NzI5MjEwNzIyOTgzOTQ2Mw.GEglzJ.OqI9prA-_ZrFEyjqzxlI8Q_6a6f5YHFT0wzRNw" #токен тестового бота
maintoken = "MTA3NzI5MjEwNzIyOTgzOTQ2Mw.GEglzJ.OqI9prA-_ZrFEyjqzxlI8Q_6a6f5YHFT0wzRNw" #токен основного бота

betatests = True #режим бета тестирования бота
logsram = True #логи о потраченой памяти

logs_webhook = "https://discordapp.com/api/webhooks/1031614039698190376/lpqZ0C85u_nDxCQj1wqnF4hWwYCKKd6HPYwdqVMtVkzQpwkCDnnYBVhxM91RupazOOCt" #хук с логами заходов

default_wl = [942347441016021012] #белый список по умолчанию, айди своего бота добавлять не надо, т.к он не реагирует на свои же действия

support_server = "https://discord.gg/KjJzsCskpq" #тут код приглашения на сервер поддержки бота

version = "1.3 Beta, slash commands" #версия бота

ramlogssleep = 60 #задержка на логи о потраченой памяти
