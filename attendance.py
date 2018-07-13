# coding: utf-8

import discord
import asyncio
import pandas as pd
import datetime

client = discord.Client()

filename = 'data.csv'
csv_data = pd.read_csv(filename, encoding="shift-jis")
#csv_data = pd.DataFrame(columns = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'attend', 'absent', 'late'])

master = ''

def read_csv(filename):
    f = open(filename, "r")
    csv_data = csv.reader(f)
    list = [ e for e in csv_data]
    f.close()
    return list

def update(index, name, column, new):
    csv_data.loc[index, [column]] = new
    """
    for index in (0, range(len(csv_data))):
        if name == csv_data.loc[index, ["name"]]:
           csv_data.loc[index, [column]] = new

           break
    """
    csv_data.to_csv('data.csv', index = False, encoding="shift-jis")

    print(csv_data.loc[0, ['name']])

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content.startswith('attend'): #出席連絡
        for index in range(len(csv_data)):
            if csv_data.loc[index, ['name']]['name'] == str(message.author):
            #csv_data[csv_data.name == message.author][['absent']] = 1
                update(index, message.author, 'attend', 1)

        await client.send_message(message.channel, 'OK')

    elif message.content.startswith('absent'):  #欠席連絡
        for index in range(len(csv_data)):
            if csv_data.loc[index, ['name']]['name'] == str(message.author):
            #csv_data[csv_data.name == message.author][['absent']] = 1
                update(index, message.author, 'absent', 1)

        await client.send_message(message.channel, 'OK')

    elif message.content.startswith('late'):  #遅刻連絡
        late_data = message.content.split()
        for index in range(len(csv_data)):
            if csv_data.loc[index, ['name']]['name'] == str(message.author):
            #csv_data[csv_data.name == message.author][['absent']] = 1
                update(index, message.author, 'late', late_data[1])

        await client.send_message(message.channel, 'OK')


    elif message.content.startswith('regist'):  #登録
        regist_weekdays = message.content.split()
        if regist_weekdays[1] == "new":
            for index in range(len(csv_data)):
                if csv_data[csv_data.name == message.author] is not None:
                    await client.send_message(message.channel, 'すでに登録されています')
                    break
                """
                if str(message.author) == str(csv_data.loc[index, ['name']]):
                    await client.send_message(message.channel, 'すでに登録されています')
                    break
                """
            else:
                num = len(csv_data)
                csv_data.loc[num, ["name"]] = message.author

                for column1 in ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]:
                    update(num, message.author, column1, 1)
                for column2 in ['attend', 'absent', 'late']:
                    update(num, message.author, column2, 0)
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
                    update(str(message.author), column1, 1)
                for column2 in ['attend', 'absent', 'late']:
                    update(str(message.author), column2, 0)

        await client.send_message(message.channel, 'OK')


    elif message.content.startswith('output'):  #出席者確認
        global master
        message_text = "[本日の出席者]\n"
        if str(message.author) == master:
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

            for index in range(len(csv_data)):
                if csv_data.loc[index, ['attend']]['attend'] == 1: #出席連絡がある場合
                    message_text = message_text + str(csv_data.loc[index, ["name"]]["name"]) + "\n"
                    #await client.send_message(message.channel, name)
                    #update(index, message.author, 'attend', 0)
                elif csv_data.loc[index, ['absent']]['absent'] == 0: #欠席連絡がない場合
                    if  csv_data.loc[index, ['late']]['late'] != 0:  #遅刻連絡があった場合
                        message_text = message_text + str(csv_data.loc[index, ["name"]]["name"]) + ' (' + str(csv_data.loc[index, 'late']) + ')\n'
                        #await client.send_message(message.channel, str(name) + ' (' + str(csv_data.at[name, 'late']) + ')')
                        #update(index, message.author, 'late', 0)
                    else:   #遅刻連絡がない場合
                        if csv_data.loc[index, [day]][day] == 1:
                            message_text = message_text + str(csv_data.loc[index, ["name"]]["name"]) + "\n"
                            #await client.send_message(message.channel, name)
                            #update(index, message.author, 'late', 0)
                else:   #欠席連絡がある場合
                    update(index, message.author, 'absent', 0)
                for column in ['attend', 'absent', 'late']:
                    update(index, message.author, column, 0)
            await client.send_message(message.channel, message_text)
        else:
            await client.send_message(message.channel, 'あなたにはその権限はありません。')

    #elif message.content.startswith('exit'):  #プログラム終了
    #    exit()

    elif message.content.startswith('master'):
        master = str(message.author)


client.run('NDY2MTk3NDI2OTExMzEzOTMw.DiYm7g.2nWing3Y1vCc1s-w33FHsuvkIyU') #実行
