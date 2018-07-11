# coding: utf-8

import discord
import asyncio
import pandas as pd
import datetime

client = discord.Client()

filename = 'data.csv'
#csv_data = pd.read_csv(filename, encoding="shift-jis")
csv_data = pd.DataFrame(columns = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'attend', 'absent', 'late'])

master = ''

def read_csv(filename):
    f = open(filename, "r")
    csv_data = csv.reader(f)
    list = [ e for e in csv_data]
    f.close()
    return list

def update(name, column, new):
    csv_data.at[name, column] = new
    csv_data.to_csv('data.csv', index=False)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('attend'): #出席連絡
        update(message.author, 'attend', 1)

        await client.send_message(message.channel, 'OK')

    elif message.content.startswith('absent'):  #欠席連絡
        update(message.author, 'absent', 1)

        await client.send_message(message.channel, 'OK')

    elif message.content.startswith('late'):  #遅刻連絡
        late_data = message.content.split()
        update(message.author, 'late', late_data[1])

        await client.send_message(message.channel, 'OK')


    elif message.content.startswith('regist'):  #登録
        regist_weekdays = message.content.split()
        if regist_weekdays[1] == "new":
            for column1 in csv_data.columns.values:
                update(message.author, column1, 1)
            for column2 in ['attend', 'absent', 'late']:
                update(message.author, column2, 0)
            print (csv_data)
        else:
            
            regist_weekday = regist_weekdays[2].split(",")
            if regist_weekdays[1] == "play":
                for day in regist_weekday:
                    update(message.author, day, 1)
            elif regist_weekdays[1] == "delete":
                for day in regist_weekday:
                    update(message.author, day, 0)

            elif regist_weekdays[1] == "new":
                for column1 in df.columns.values:
                    update(message.author, column1, 1)
                for column2 in ['attend', 'absent', 'late']:
                    update(message.author, column2, 0)

        await client.send_message(message.channel, 'OK')


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
                        await client.send_message(message.channel, str(name) + ' (' + str(csv_data.at[name, 'late']) + ')')
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
