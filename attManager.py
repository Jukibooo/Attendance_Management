# coding: utf-8

import discord
import asyncio
import pandas as pd
import datetime
import os

client = discord.Client()

historyname = 'history.csv'
dbname = 'members.csv'

today_att = []
today_abs = []

hist = pd.read_csv(historyname)
if os.path.isfile(dbname):
    db = pd.read_csv(dbname)
else:
    db = pd.DataFrame(columns = ['Mon_s', 'Mon_e', 'Tue_s', 'Tue_e', 'Wed_s', 'Wed_e', 'Thu_s', 'Thu_e', 'Fri_s', 'Fri_e', 'Sat_s', 'Sat_e', 'Sun_s', 'Sun_e'])

master = ''

def read_csv(filename):
    f = open(filename, "r")
    csv_data = csv.reader(f)
    list = [ e for e in csv_data]
    f.close()
    return list

def update(df, name, column, value, fname):
    df.at[name, column] = value
    df.to_csv(fname) #index = True説

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    msg = ''
    if message.content.startswith('attend'): #出席連絡
        today_att.append(message.author)
        
        msg = message.author + 'は本日出席します。'
        await client.send_message(message.channel, msg)

    elif message.content.startswith('absent'):  #欠席連絡
        today_abs.append(message.author)
        msg = message.author + 'は本日欠席します。'
        await client.send_message(message.channel, msg)

    elif message.content.startswith('late'):  #遅刻連絡
        late_data = message.content.split()
        update(message.author, 'late', late_data[1])
        msg = message.author + 'は本日遅刻で、' + late_data[1] + 'から参加します。'
        await client.send_message(message.channel, msg)


    elif message.content.startswith('regist'):  #登録
        mode = message.content.split()
        if mode[1] == "new":
            for c in db.columns:
                update(db, message.author, c, 'any', dbname)
            msg = message.author + 'が登録されました。'
        else:
            day_time = mode[2].split(",")
            if mode[1] == "play":
                for day in day_time:
                    weekday = day.split()[0]
                    start = day.split()[1].split('-')[0]
                    end = day.split()[1].split('-')[1]
                    update(db, message.author, weekday+'_s', start, dbname)
                    update(db, message.author, weekday+'_e', end, dbname)
                
                msg = message.author + 'が参加時間帯を変更しました。'
            elif mode[1] == "delete":
                for day in day_time:
                    weekday = day.split()[0]
                    update(db, message.author, weekday+'_s', 'none', dbname)
                    update(db, message.author, weekday+'_e', 'none', dbname)

                msg = message.author + 'が参加時間帯を変更しました。'
        await client.send_message(message.channel, msg)


    elif message.content.startswith('output'):  #出席者確認
        global master
        if str(message.author) == master:
            await client.send_message(message.channel, '[本日の出席者]')
            aDate = datetime.date.today()
            weekday = aDate.weekday()   #曜日取得
            if (weekday == 0):
                day = "Mon"
            elif (weekday == 1):
                day = "Tue"
            elif (weekday == 2):
                day = "Wed"
            elif (weekday == 3):
                day = "Thu"
            elif (weekday == 4):
                day = "Fri"
            elif (weekday == 5):
                day = "Sat"
            elif (weekday == 6):
                day = "Sun"
            print (csv_data)

            for name in csv_data.index.values:
                if csv_data.at[name, 'attend'] == 1: #出席連絡がある場合
                    await client.send_message(message.channel, name)
                    update(message.author, 'attend', 0)
                elif csv_data.at[name, 'absent'] == 0: #欠席連絡がない場合
                    if  csv_data.at[name, 'late'] != 0:  #遅刻連絡があった場合
                        await client.send_message(message.channel, str(name) + ' (' + str(csv_data.at[name, 'late']) + ')から参加')
                        update(message.author, 'late', 0)
                    else:   #遅刻連絡がない場合
                        if csv_data.at[name, day] == 1:
                            await client.send_message(message.channel, name)
                            update(message.author, 'late', 0)
                else:   #欠席連絡がある場合
                    update(message.author, 'absent', 0)
                for column in ['attend', 'absent', 'late']:
                        update(message.author, column, 0)
        else:
            await client.send_message(message.channel, 'あなたにはその権限はありません。')

    #elif message.content.startswith('exit'):  #プログラム終了
    #    exit()

    elif message.content.startswith('master'):
        master = str(message.author)


client.run('NDY2MTk3NDI2OTExMzEzOTMw.DiYm7g.2nWing3Y1vCc1s-w33FHsuvkIyU') #実行
