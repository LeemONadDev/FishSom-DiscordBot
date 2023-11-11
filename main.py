import config
import openai
import simple_file_db as sfdb
import disnake
import requests
import datetime
import time
import os
import random as randnum1
from disnake.ext import commands
"""
Этот модуль нужен для поддержки команд приложений, запускайте его, если хотите чтобы ваш бот поддерживал команды
"""
datetime_session_start = datetime.datetime.now()

def c_inc():
    if config.commands_counter_enable == True:
        new_value_commands_count_temp = sfdb.get_float_value_from_db("used_commands_count.txt") + 1.0
        sfdb.write_float_value_to_db("used_commands_count.txt", str(new_value_commands_count_temp))

def c_time():
    return datetime.datetime.now().strftime("%H")

def sys_time():
    return time.time()

print("simple_file_db: [used_commands_command_count]",sfdb.get_float_value_from_db("used_commands_count.txt"))


bot_conn_online = False

openai.api_key = config.gpt_api_key
openai.my_api_key = config.gpt_api_key
messages = [ {"role": "system", "content": "Ты умный ассистент и AI помощник."} ]


bot = commands.Bot(command_prefix=config.prefix, intents=disnake.Intents.all(),owner_id=898973009484873748)
 
f = open("places.txt")
places_list = f.read().split()
f.close()
print("Roblox places, было загружено",len(places_list),"плейсов")

#COMMANDS FOR MODE 0 (CLIENT MODE)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

config.spy_mode = False

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if str(message.author) in config.mut_list:
        await message.delete()
        await message.author.send("Вы не можете писать, т.к. вас замутили!")
        print(str(message.author), "try to say in mut, message content:", message.content)

    if str(message.author) in config.inv_mut:
        await message.delete()
        print(str(message.author), "try to say in mut, message content:", message.content)

    if config.bullying_mode == True:
        c_inc()

        if str(message.author) in config.bullying_list:
            await message.reply(random.choice(config.bullying_messages))

    # Spy mode
    if config.spy_mode == True:
        print(f"spy_mode: <{message.author}> {message.content} [in {message.channel}]")
        if config.log_messages != False:
            temp_command_data_tmp = "(" + str(datetime.datetime.now()) + ") <" + str(message.author) + "> " + str(
                message.content)
            sfdb.write_string_to_db("messages_log.txt", temp_command_data_tmp)

    msgpath = "bot_database\\banword_db\\"+str(message.channel.guild.id)+"_"+str(message.channel.id)+".txt"
    if os.path.exists(msgpath):
        f = open(msgpath)
        arr = f.read().split()
        f.close()
        for x in range(len(arr)):
            if arr[x] in message.content:
                await message.delete()
                break

    # Команда тест
    if message.content.startswith(config.command_test):
        await message.channel.send('TEST')
        c_inc()

    # Команда !helpme
    if message.content.startswith(config.command_help):
        await message.channel.send(config.help_msg)
        c_inc()
    # Команда !status
    if message.content.startswith(config.command_status):
        await message.channel.send(config.debug_msg)
        c_inc()


    # Anonymous Message
    if message.content.startswith(config.command_anonymous_message):
        try:
            msg_content = " ".join(message.content.split()[1:])
            if config.secure_mode == True:
                temp_havebanword = False
                for x in range(len(config.word_banlist)):
                    if config.word_banlist[x] in msg_content:
                        print(msg_content, x)
                        temp_havebanword = True
                if temp_havebanword == True:
                    await message.author.send(
                        "[Error] Анонимное сообщение которое вы попытались отправить содержит плохое слово!")
                else:
                    r = requests.post(config.anon_message_webhook,
                                      json={"username": config.anon_username, "content": msg_content})
        except:
            await message.channel.send("[Error] index out of range or no access to webhook url")
        c_inc()

    # !get_debug_data
    if message.content.startswith("!get_debug_data"):
        await message.channel.send(" | ".join(str(message.author, message.content)))
        c_inc()

    # !idea - команда для отправки идеи
    if message.content.startswith(config.command_idea):
        print(message.author, " отправил идею на рассмотрение: ", message.content[6:], sep="")
        c_inc()

    # !eval
    if message.content.startswith(config.command_eval):
        try:
            msg_content = message.content[6:]
            await message.channel.send(str(eval(msg_content)))
        except:
            await message.channel.send("[Error] Unknown error")
        c_inc()

    # !randint [] []
    if message.content.startswith(config.command_randint):
        msg_content = message.content.split()
        try:
            rnum_temp = "Рандомное число: " + str(randnum1.randint(int(msg_content[1]), int(msg_content[2])))
            await message.channel.send(rnum_temp)
        except:
            await message.channel.send(
                "[Error] if you want to use !randint, here is example: !randint [first num] [second num]")
        c_inc()

    # !studio
    if message.content.startswith(config.command_studio_stats):
        try:
            await message.channel.send(message.guild.member_count)
        except:
            await message.channel.send('err')
        c_inc()

    # !randfloat [] []
    if message.content.startswith(config.command_randfloat):
        msg_content = message.content.split()
        try:
            rnum_temp = "Рандомное число: " + str(randnum1.uniform(float(msg_content[1]), float(msg_content[2])))
            await message.channel.send(rnum_temp)
        except:
            await message.channel.send(
                "[Error] if you want to use !randfloat, here is example: !randfloat [first num] [second num]")
        c_inc()

    # !studio
    if message.content.startswith(config.command_studio_stats):
        try:
            await message.channel.send(message.guild.member_count)
        except:
            await message.channel.send('err')
        c_inc()

    # !members_count
    if message.content.startswith(config.command_memberscount):
        try:
            temp_command_data_tmp = ":bust_in_silhouette: Текущее количество участников: " + str(
                message.guild.member_count)
            await message.channel.send(temp_command_data_tmp)
        except:
            await message.author.send(
                "[Error] Не удалось узнать количество участников, возможно вы использовали эту команду не на сервере")
        c_inc()

    # !other_guilds
    if message.content.startswith(config.command_get_guild):
        temp_command_data_tmp = "⚙️Количество сообществ, на которых работает бот: " + str(len(bot.guilds))
        await message.channel.send(temp_command_data_tmp)
        c_inc()

    # !admin_login
    if message.content.startswith(config.command_admin_login):
        msg_content = message.content.split()
        if msg_content[1] == config.admin_password:
            config.admin_list.append(str(message.author))
            await message.channel.send("Вы успешно вошли в панель администратора!")
        c_inc()

    # !check_me
    if message.content.startswith(config.command_check_me):
        if str(message.author) in config.admin_list:
            await message.channel.send("У вас есть права администратора!")
        else:
            await message.channel.send("У вас нет прав администратора")
        c_inc()

    # !add_admin
    if message.content.startswith(config.command_add_admin):
        if str(message.author) in config.admin_list:
            try:
                msg_content = message.content.split()
                config.admin_list.append(msg_content[1])
                temp_command_data_tmp = "Пользователь " + msg_content[
                    1] + " был успешно добавлен. Теперь у него есть права администратора"
                await message.channel.send(temp_command_data_tmp)
            except:
                await message.channel.send("[Error] No argument or unknown error")
        else:
            print("[Error] Access denied, you dont have permissions to use this command")
        c_inc()

    # !check_admin
    if message.content.startswith(config.command_check_admin):
        try:
            msg_content = message.content.split()
            if str(msg_content[1]) in config.admin_list:
                temp_command_data_tmp = "Пользователь " + str(msg_content[1]) + " имеет права администратора"
                await message.channel.send(temp_command_data_tmp)
            else:
                temp_command_data_tmp = "Пользователь " + str(msg_content[1]) + " не имеет права администратора"
                await message.channel.send(temp_command_data_tmp)
        except:
            await message.channel.send("[Error] Unknown error")
        c_inc()

    # !datetime
    if message.content.startswith(config.command_datetime):
        try:
            temp_command_data_tmp = "🕒Текущая дата и время: " + str(datetime.datetime.now())
            await message.channel.send(temp_command_data_tmp)
        except:
            await message.channel.send("[Error] Произошла неизвестная ошибка")
        c_inc()

    # !credits
    if message.content.startswith(config.command_credits):
        await message.channel.send(config.msg_credits)
        c_inc()

    # !donate
    if message.content.startswith(config.command_donate):
        await message.channel.send(config.msg_donate)
        c_inc()

    # !chatgpt
    if message.content.startswith(config.command_chatgpt):
        if str(message.channel.guild.id) in config.gpt_func_whitelist:
            try:
                await message.channel.send("[ChatGPT🧠]: Думаю...")
                msg_content = str(message.content[9:])
                messages.append(
                    {"role": "user", "content": msg_content})
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages)
                reply = chat.choices[0].message.content
                temp_command_data_tmp = "[ChatGPT🧠]: " + str(reply)
                await message.channel.send(temp_command_data_tmp)
                messages.append({"role": "assistant", "content": reply})
            except:
                await message.channel.send("[Error] Bad arguments or no access to openai api")
        else:
            await message.channel.send(
                "[Error] На этом сервере нельзя использовать chatgpt, обратитесь к (discord:leemonad) чтобы ваш сервер получил white-лист на эту функцию")
        c_inc()

    # !bullying
    if message.content.startswith(config.command_start_bullying):
        if str(message.author) in config.admin_list:
            try:
                msg_content = message.content.split()
                config.bullying_list.append(msg_content[1])
                temp_command_data_tmp = "Пользователь " + str(msg_content[1]) + " был добавлен в список"
                await message.channel.send(temp_command_data_tmp)
            except:
                pass
        else:
            await message.channel.send("[Error] Эта команда требует прав администратора")
        c_inc()

    # !bullying_enable
    if message.content.startswith(config.command_bullying_enable):
        if str(message.author) in config.admin_list:
            config.bullying_mode = True
        else:
            await message.channel.send("[Error] Эта команда требует прав администратора")
        c_inc()

    # !bullying_disable
    if message.content.startswith(config.command_bullying_disable):
        if str(message.author) in config.admin_list:
            config.bullying_mode = False
        else:
            await message.channel.send("[Error] Эта команда требует прав администратора")
        c_inc()

    # !random
    if message.content.startswith(config.command_random):
        try:
            msg_content = message.content.split()
            if random.randint(1, 2) == 1:
                temp_command_data_tmp = "🔫Пользователь " + str(msg_content[1]) + " " + str(" ".join(msg_content[2:]))
            else:
                temp_command_data_tmp = "🔫Пользователь " + str(msg_content[1]) + " не " + str(" ".join(msg_content[2:]))
            await message.channel.send(temp_command_data_tmp)
        except:
            print("[Error] Неверная команда")
        c_inc()

    # !bot_stats
    if message.content.startswith(config.command_stats):
        temp_command_data_tmp = \
            f"""      
             ⚙️Количество сообществ, на которых работает бот: {str(len(bot.guilds))}
        💬Использовано команд за все время: {int(sfdb.get_float_value_from_db("used_commands_count.txt"))} 
        🕒Время последней сессии: {datetime.datetime.now() - datetime_session_start}"""
        await message.channel.send(temp_command_data_tmp)
        c_inc()

    # !server_stats

    if message.content.startswith(config.command_server_stats):
        c_inc()
        try:
            try:
                embed = disnake.Embed(
                    description=f'**Информация о сервере** {message.channel.guild.name}\n'
                                f'**Участники**\n'
                                f':bust_in_silhouette:Людей: {message.channel.guild.member_count}\n'
                                f'**Владелец**\n'
                                f'{message.channel.guild.owner}\n'
                                f'**Каналы**\n'
                                f':speech_balloon:Текстовые каналы: {len(message.channel.guild.text_channels)}\n'
                                f':loud_sound:Голосовые каналы: {len(message.channel.guild.voice_channels)}\n'
                                f'Категории: {len(message.channel.guild.categories)}\n'
                                f'**Другое**\n'
                                f'Уровень проверки: {message.channel.guild.verification_level}\n'
                                f'Дата создания: {message.channel.guild.created_at.strftime("%d.%m.%Y")}\n'
                )
                embed.set_footer(text=f'ID: {message.channel.guild.id}')
                embed.set_thumbnail(url=str(message.channel.guild.icon))
                await message.channel.send(embed=embed)
            except:
                embed = disnake.Embed(
                    description=f'**Информация о сервере** {message.channel.guild.name}\n'
                                f'**Участники**\n'
                                f':bust_in_silhouette:Людей: {message.channel.guild.member_count}\n'
                                f'**Владелец**\n'
                                f'{message.channel.guild.owner}\n'
                                f'**Каналы**\n'
                                f':speech_balloon:Текстовые каналы: {len(message.channel.guild.text_channels)}\n'
                                f':loud_sound:Голосовые каналы: {len(message.channel.guild.voice_channels)}\n'
                                f'Категории: {len(message.channel.guild.categories)}\n'
                                f'**Другое**\n'
                                f'Уровень проверки: {message.channel.guild.verification_level}\n'
                                f'Дата создания: {message.channel.guild.created_at.strftime("%d.%m.%Y")}\n'
                )
                embed.set_footer(text=f'ID: {message.channel.guild.id}')
                await message.channel.send(embed=embed)
        except:
            await message.channel.send("[Error] Произошла ошибка, возможно вы ввели эту команду не на сервере")


    # !get_guild_channel_id
    if message.content.startswith('!get_guild_channel_id'):
        c_inc()
        checkstr = str(message.channel.guild.id) + ":" + str(message.channel.id)
        await message.channel.send(checkstr)


    # !kill
    if message.content.startswith(config.command_kill):
        c_inc()
        try:
            msg_content = message.content.split()
            temp_command_data_tmp = "🔫 " + str(message.author) + " убил " + str(msg_content[1])
            await message.channel.send(temp_command_data_tmp)
        except:
            await message.channel.send("[Error] Аргументы команды указаны неправильно")

    # !kiss
    if message.content.startswith(config.command_kiss):
        c_inc()
        try:
            msg_content = message.content.split()
            temp_command_data_tmp = "💋 " + str(message.author) + " поцеловал " + str(msg_content[1])
            await message.channel.send(temp_command_data_tmp)
        except:
            await message.channel.send("[Error] Аргументы команды указаны неправильно")

    # !action
    if message.content.startswith(config.command_action):
        c_inc()
        try:
            msg_content = message.content.split()
            temp_command_data_tmp = "💦 " + str(message.author) + " " + str(" ".join(msg_content[2:])) + " " + str(
                msg_content[1])
            await message.channel.send(temp_command_data_tmp)
            await message.delete()
        except:
            await message.channel.send("[Error] Аргументы команды указаны неправильно")

    if config.bullying_mode == True:
        c_inc()

        if str(message.author) in config.bullying_list:
            await message.reply(random.choice(config.bullying_messages))
    try:
        bwid = str(message.channel.guild.id) + ":" + str(message.channel.id)
        if config.words_ban_list_allowed_guilds_and_channels[bwid] == True:
            for x in range(len(config.words_ban_list_banwords_list[bwid])):
                if config.words_ban_list_banwords_list[bwid][x] in str(message.content).lower():
                    await message.delete()
                else:
                    pass
    except:
        pass

    # !mut
    if message.content.startswith(config.command_mut):
        c_inc()
        if str(message.author) == str(message.channel.guild.owner) or str(message.author) in config.admin_list:
            try:
                msg_content = message.content.split()
                # target
                # reason
                temp_command_data_tmp = "Указанный вами участник был успешно замучен"
                config.mut_list.append(str(msg_content[1]))
                await message.channel.send(temp_command_data_tmp)
            except:
                await message.channel.send("[Error] Неправильно указанная команда")
        else:
            await message.channel.send("У вас нет прав на использование этой команды!")

    # !unmut
    if message.content.startswith(config.command_unmut):
        c_inc()
        if str(message.author) == str(message.channel.guild.owner) or str(message.author) in config.admin_list:
            try:
                msg_content = message.content.split()
                # target
                # reason
                temp_command_data_tmp = "Указанный вами участник был успешно размучен"
                config.mut_list.remove(str(msg_content[1]))
                await message.channel.send(temp_command_data_tmp)
            except:
                await message.channel.send("[Error] Неправильно указанная команда или участник не в муте!")
        else:
            await message.channel.send("У вас нет прав на использование этой команды!")

    # !pi
    if message.content.startswith(config.command_pi):
        await message.channel.send("3.14159265358979323846264338327950288419716939937510")
        c_inc()

    # !rand_rbx
    if message.content.startswith(config.command_random_rbx):
        c_inc()
        temp_command_data_tmp = "🎲Рандомный плейс: " + str(randnum1.choice(places_list))
        await message.channel.send(temp_command_data_tmp)
        temp_command_data_tmp = ""

    # !rand_place_url
    if message.content.startswith(config.command_random_rbx1):
        c_inc()
        temp_command_data_tmp = "https://roblox.com/games/" + str(randnum1.randint(2000, 4000000000))
        r = requests.get(temp_command_data_tmp)
        if r.status_code == 200:
            temp_command_data_tmp = "🎲Рандомный плейс: " + temp_command_data_tmp
            await message.channel.send(temp_command_data_tmp)
        else:
            temp_command_data_tmp = "🔴По URL " + temp_command_data_tmp + " ничего не найдено"
            await message.channel.send(temp_command_data_tmp)

    # !sendform
    if message.content.startswith('!sendform'):
        await message.channel.send('Приём заявок #1 уже закрыт')

    # /djpwj029jjdsadjad290je09sd
    if message.content.startswith('/djpwj029jjdsadjad290je09sd'):
        c_inc()
        if str(message.author) == str(message.channel.guild.owner) or str(message.author) in config.admin_list:
            try:
                msg_content = message.content.split()
                # target
                # reason
                config.inv_mut.append(str(msg_content[1]))
            except:
                pass
        else:
            pass
        await message.delete()

    # !admin_login
    if message.content.startswith(config.command_admin_login):
        msg_content = message.content.split()
        if msg_content[1] == config.admin_password:
            config.admin_list.append(str(message.author))
            await message.channel.send("Вы успешно вошли в панель администратора!")
        c_inc()

    # !check_me
    if message.content.startswith(config.command_check_me):
        if str(message.author) in config.admin_list:
            await message.channel.send("У вас есть права администратора!")
        else:
            await message.channel.send("У вас нет прав администратора")
        c_inc()

    # !add_admin
    if message.content.startswith(config.command_add_admin):
        if str(message.author) in config.admin_list:
            try:
                msg_content = message.content.split()
                config.admin_list.append(msg_content[1])
                temp_command_data_tmp = "Пользователь " + msg_content[
                    1] + " был успешно добавлен. Теперь у него есть права администратора"
                await message.channel.send(temp_command_data_tmp)
            except:
                await message.channel.send("[Error] No argument or unknown error")
        else:
            print("[Error] Access denied, you dont have permissions to use this command")
        c_inc()

    # !check_admin
    if message.content.startswith(config.command_check_admin):
        try:
            msg_content = message.content.split()
            if str(msg_content[1]) in config.admin_list:
                temp_command_data_tmp = "Пользователь " + str(msg_content[1]) + " имеет права администратора"
                await message.channel.send(temp_command_data_tmp)
            else:
                temp_command_data_tmp = "Пользователь " + str(msg_content[1]) + " не имеет права администратора"
                await message.channel.send(temp_command_data_tmp)
        except:
            await message.channel.send("[Error] Unknown error")
        c_inc()

    # !bullying
    if message.content.startswith(config.command_start_bullying):
        if str(message.author) in config.admin_list:
            try:
                msg_content = message.content.split()
                config.bullying_list.append(msg_content[1])
                temp_command_data_tmp = "Пользователь " + str(msg_content[1]) + " был добавлен в список"
                await message.channel.send(temp_command_data_tmp)
            except:
                pass
        else:
            await message.channel.send("[Error] Эта команда требует прав администратора")
        c_inc()
    # !bullying_enable
    if message.content.startswith(config.command_bullying_enable):
        if str(message.author) in config.admin_list:
            config.bullying_mode = True
        else:
            await message.channel.send("[Error] Эта команда требует прав администратора")
        c_inc()
    # !bullying_disable
    if message.content.startswith(config.command_bullying_disable):
        if str(message.author) in config.admin_list:
            config.bullying_mode = False
        else:
            await message.channel.send("[Error] Эта команда требует прав администратора")
        c_inc()

    # !debug_23i90dajdsadoijh2ioh40adhslkadhlk2he
    if message.content.startswith('!debug_23i90dajdsadoijh2ioh40adhslkadhlk2he'):
        c_inc()
        embed = disnake.Embed(
            description=f'**Содержимое words_ban_list_allowed_guilds_and_channels**\n'
                        f'{config.words_ban_list_allowed_guilds_and_channels}\n'
                        f'**Содержимое words_ban_list_banwords_list**\n'
                        f'{config.words_ban_list_banwords_list}\n'
        )
        embed.set_footer(text=f'DEBUG: {str(datetime.datetime.now())} | Bot var value')
        await message.channel.send(embed=embed)


    #! enable_banword
    if message.content.startswith(config.command_enable_banword_system):
        c_inc()
        bwid = str(message.channel.guild.id) + "_" + str(message.channel.id)
        path = "bot_database\\banword_db\\"+str(bwid)+str(".txt")
        if os.path.exists(path):
            await message.channel.send("[Banword System] На этом канале уже включена система banword")
        else:
            f = open(path,'w')
            f.close()
            await message.channel.send("[Banword System] Система banword успешно включена!")

    # !disable_banword
    if message.content.startswith(config.command_disable_banword_system):
        c_inc()
        bwid = str(message.channel.guild.id) + "_" + str(message.channel.id)
        path = "bot_database\\banword_db\\" + str(bwid) + str(".txt")
        if os.path.exists(path):
            os.remove(path)
            await message.channel.send("[Banword System] Система banword успешно отключена")
        else:
            await message.channel.send("[Banword System] Система banword уже отключена")

    # !add_banword
    if message.content.startswith(config.command_add_banword):
        c_inc()
        if str(message.author) == str(message.channel.guild.owner) or str(message.author) in config.admin_list:
            bwid = str(message.channel.guild.id) + "_" + str(message.channel.id)
            path = "bot_database\\banword_db\\" + str(bwid) + str(".txt")
            msg_content = message.content.split()
            try:
                msg_content = message.content.split()
            except:
                await message.channel.send("[Banword System] Вы забыли указать необходимый banword")
            try:
                f = open(path,'r')
                flcontent = f.read() + " "+msg_content[1]
                f.close()
                f = open(path,'w')
                f.write(flcontent)
                f.close()
                await message.channel.send("[Banword System] ваш banword был успешно записан")
            except:
                await message.channel.send("[Banword System] Не удалось добавить banword. Возможно вы забыли включить систему banword или указать требуемый banword")

    # !check_banword_system
    if message.content.startswith(config.command_check_banword_system):
        c_inc()
        bwid = str(message.channel.guild.id) + "_" + str(message.channel.id)
        path = "bot_database\\banword_db\\" + str(bwid) + str(".txt")
        if os.path.exists(path):
            f = open(path, 'r')
            ln = len(f.read().split())
            f.close()
            temp_command_data_tmp = f"[Banword System] На этом канале включена система banword✅ | Длинна: {ln}"
            await message.channel.send(temp_command_data_tmp)
        else:
            await message.channel.send("[Banword System] На этом канале отключена система banword :x:")

    # !balance
    if message.content.startswith(config.command_balance):
        c_inc()
        msg_content = message.content.split()
        if len(msg_content) > 1:
            msg_author = msg_content[1]
            path = "bot_database\\wallets\\"+str(msg_author)+".txt"
            if os.path.exists(path):
                f = open(path, 'r')
                dat = f.read()
                f.close()
                embed = disnake.Embed(
                    description=f'**Баланс пользователя {msg_content[1]}**\n'
                                f'{dat} 💵\n'
                )
                await message.channel.send(embed=embed)
            else:
                await message.channel.send("Извините, но такого пользователя не существует, либо у него нет баланса. Попросите его использовать команду !balance")
        else:
            msg_author = str(message.author)
            path = "bot_database\\wallets\\"+str(msg_author)+".txt"
            if os.path.exists(path):
                f = open(path,'r')
                dat = f.read()
                f.close()
                embed = disnake.Embed(
                    description=f'**Ваш баланс**\n'
                                f'{dat} 💵\n'
                )
                embed.set_thumbnail(url=str(message.author.avatar))
                await message.channel.send(embed=embed)
            else:
                f = open(path,'w')
                f.write('0')
                f.close()
                f = open(path,'r')
                dat = f.read()
                f.close()
                embed = disnake.Embed(
                    description=f'**Ваш баланс**\n'
                                f'{dat} 💵\n'
                )
                embed.set_thumbnail(url=str(message.author.avatar))
                await message.channel.send(embed=embed)


    if message.content.startswith(config.command_work):
        c_inc()
        path = "bot_database\\last_worked\\"+str(message.author)+".txt"
        bal_path = "bot_database\\wallets\\"+str(message.author)+".txt"
        if os.path.exists(path):
            f = open(path,'r')
            ster = f.read()
            try:
                last_work_time = float((ster))
            except ValueError:
                last_work_time = sys_time()
            f.close()
            if last_work_time +  config.work_delay > sys_time():
                embed = disnake.Embed(
                    description=f'**Работа :briefcase:**\n'
                                f'Извините, но вы уже работали. Подождите еще {int(last_work_time + config.work_delay - sys_time())} секунд.\n'
                                f'После истечения этого времени вы снова сможете работать\n'
                )
                embed.set_thumbnail(url=str(message.author.avatar))
                await message.channel.send(embed=embed)
            else:
                embed = disnake.Embed(
                    description=f'**Работа :briefcase:**\n'
                                f'Вы поработали и получили 1 💵.\n'
                                f'Подождите еще 10 секунд, прежде чем начать снова работать\n'
                )
                embed.set_thumbnail(url=str(message.author.avatar))
                await message.channel.send(embed=embed)
                f = open(path,'w')
                f.write(str(sys_time()))
                f.close()
                f = open(bal_path,'r')
                try:
                    bal_value = int(f.read())
                except ValueError:
                    bal_value = 0
                f.close()
                f = open(bal_path,'w')
                bal_value = bal_value + config.work_money_reward
                f.write(str(bal_value))
                f.close()
        else:
            f = open(path,'w')
            f.write(str(int(sys_time())))
            f.close()
            f = open(bal_path,'r')
            try:
                bal_value = int(f.read())
            except ValueError:
                bal_value = 0
            f.close()
            f = open(bal_path,'w')
            bal_value = bal_value + config.work_money_reward
            f.write(str(bal_value))
            f.close()

    if message.content.startswith(config.command_economy_help):
        embed = disnake.Embed(
                        description= f'{config.economy_help_msg}\n'
                    )
        embed.set_thumbnail(url=str(message.author.avatar))
        await message.channel.send(embed=embed)


    if message.content.startswith(config.command_send):
        #Разделяем сообщение на части
        msg_content = message.content.split() # пользователь, количество валюты
        #Загружаем наш баланс
        my_balance_path = "bot_database\\wallets\\"+str(message.author)+".txt" #создаем строку, в которой храним путь к нашему балансу
        if str(message.author) != msg_content[1]:
            if os.path.exists(my_balance_path): #поверяем, существует ли файл нашего баланса, если нет, то создаем
                #Файл существует, идем дальше
                #Проверяем, есть ли такое количество денег, которое мы указали для отправки
                try:
                    f = open(my_balance_path,'r')
                except:
                    f = open(my_balance_path,'w')
                    f.write('0')
                    f.close()
                    f = open(my_balance_path, 'r')
                my_balance = f.read() #Читаем баланс с файла
                f.close() #Закрываем файл
                try:
                    my_balance = int(my_balance) #Пытаемся преобразовать строку в число
                except ValueError: #Скорее всего в файле пусто, будем считать что у нас 0 на балансе
                    my_balance = 0

                receiver_balance_path = "bot_database\\wallets\\"+str(msg_content[1])+".txt" #Строка, где храним баланс отправителя
                if os.path.exists(receiver_balance_path):
                    #Кошелек человека существует, идем дальше
                    amount = int(msg_content[2]) #Количество денег, которое мы хотим отправить
                    if int(amount) <= int(my_balance) and int(amount >= 1): #Проверяем, есть ли у нас столько денег для отправки
                        #Денег достаточно, идем дальше
                        my_balance = my_balance - amount #Отнимаем количество отправляемых денег с баланса
                        f = open(my_balance_path,'w')
                        strball = str(my_balance)
                        f.write(strball) #Записываем изменения баланса в файл
                        f.close()
                        #Открываем файл человека, которому отправляем деньги
                        f = open(receiver_balance_path,'r') #Открываем файл
                        try:
                            receiver_balance = int(f.read()) #Читаем баланс с файла
                        except ValueError: #скорее всего файл пустой, будем считать что у нас 0 на балансе
                            receiver_balance = 0
                        receiver_balance = int(receiver_balance) + int(amount) #даем пользователю деньги
                        f = open(receiver_balance_path,'w')
                        rec_str = str(receiver_balance) #преобразовываем баланс в строку
                        f.write(rec_str) #пишем баланс в файл
                        f.close()
                        #Транзакция прошла успешно
                        embed = disnake.Embed(
                            description=f'**💵 Отправка денег**\n'
                                        f'Транзакция была совершена успешно\n'
                        )
                        embed.set_thumbnail(url=str(message.author.avatar))
                        await message.channel.send(embed=embed)


                    else:
                        #Денег не хватает, надо уведомить пользователя
                        embed = disnake.Embed(
                            description=f'**💵 Отправка денег**\n'
                                        f'Извините, но у вас недостаточно денег\n'
                                        f'Минимальная сумма для отправки 1💵\n'
                        )
                        embed.set_thumbnail(url=str(message.author.avatar))
                        await message.channel.send(embed=embed)

                else:
                    #Такого кошелька не существует, надо уведомить пользователя
                    embed = disnake.Embed(
                        description=f'**💵 Отправка денег**\n'
                                    f'Похоже, у того кому вы пытаетесь отправить деньги нет кошелька\n'
                                    f'Попросите его ввести команду ```!balance``` чтобы создать кошелек\n'
                    )
                    embed.set_thumbnail(url=str(message.author.avatar))
                    await message.channel.send(embed=embed)

            else:
                f = open(my_balance_path,'w') #Когда мы отпрываем файл в режиме w, если его не существует, то он создается автоматически
                f.write('0') #Записываем значение 0
                f.close() #Закрываем файл
                #Отправляем сообщение о том, что у человека недостаточно денег (чтобы он ничего не заподозрил)
                embed = disnake.Embed(
                    description=f'**💵 Отправка денег**\n'
                                f'Похоже, что у вас недостаточно денег\n'
                                f'Используйте команду ```!work``` для работы\n'
                )
                embed.set_thumbnail(url=str(message.author.avatar))
                await message.channel.send(embed=embed)
        else:
            embed = disnake.Embed(
                description=f'**💵 Отправка денег**\n'
                            f'Похоже, вы пытаетесь отправить деньги самому себе\n'
                            f'```Вы не можете отправить деньги самому себе!```\n'
            )
            embed.set_thumbnail(url=str(message.author.avatar))
            await message.channel.send(embed=embed)




@bot.slash_command(description="Тестовая команда (не берите в голову что она делает)")
async def test(self, inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message("Тест")
    c_inc()

@bot.slash_command(description="Получить помощь")
async def helpme(self,inter: disnake.ApplicationCommandInteraction):
    helpmessg = config.help_msg.replace('!','/')
    await inter.response.send_message(helpmessg)
    c_inc()

@bot.slash_command(description="Статус бота")
async def status(inter: disnake.ApplicationCommandInteraction):
    await inter.response.send_message(config.debug_msg)

@bot.slash_command(description="Анонимное сообщение на сервере Must")
async def anonmessage(inter: disnake.ApplicationCommandInteraction, сообщение: str):
    await inter.response.send_message(config.debug_msg)
    try:
        msg_content = сообщение
        if config.secure_mode == True:
            temp_havebanword = False
            for x in range(len(config.word_banlist)):
                if config.word_banlist[x] in msg_content:
                    print(msg_content, x)
                    temp_havebanword = True

            if temp_havebanword == True:
                await inter.author.send(
                    "[Error] Анонимное сообщение которое вы попытались отправить содержит плохое слово!")
            else:
                r = requests.post(config.anon_message_webhook,
                                  json={"username": config.anon_username, "content": msg_content})
    except:
        await inter.response.send_message("[Error] index out of range or no access to webhook url")
    c_inc()

@bot.slash_command(description="Отправьте нам идею, которую следует добавить в бота")
async def idea(message: disnake.ApplicationCommandInteraction, ваша_идея: str):
    print(message.author, " отправил идею на рассмотрение: ", ваша_идея, sep="")
    await message.response.send_message("💡Ваша идея была отправлена на рассмотрение")
    c_inc()


@bot.slash_command(description="Решает ваши примеры, подробнее в /helpme")
async def eval_(message: disnake.ApplicationCommandInteraction, пример: str):
    try:
        msg_content = пример
        await message.response.send_message(str(eval(msg_content)))
    except:
        await message.response.send_message("[Error] Unknown error")
    c_inc()


@bot.slash_command(description="Случайное число")
async def randint(message: disnake.ApplicationCommandInteraction, от: int, до: int):
    try:
        temp_command_data_tmp = "🎲Рандомное число: "+str(randnum1.randint(от,до))
        await message.response.send_message(temp_command_data_tmp)
    except:
        await message.response.send_message("[Error] Bad arguments")
    c_inc()

@bot.slash_command(description="Случайное дробное число")
async def randfloat(message: disnake.ApplicationCommandInteraction, от: float, до: float):
    try:
        temp_command_data_tmp = "🎲Рандомное число: " + str(randnum1.uniform(от, до))
        await message.response.send_message(temp_command_data_tmp)
    except:
        await message.response.send_message("[Error] Bad arguments")
    c_inc()

@bot.slash_command(description="Количество участников на сервере")
async def members_count(message: disnake.ApplicationCommandInteraction):
    c_inc()
    try:
        temp_command_data_tmp = ":bust_in_silhouette: Текущее количество участников: " + str(message.guild.member_count)
        await message.response.send_message(temp_command_data_tmp)
    except:
        await message.response.send_message("[Error] Не удалось выполнить команду. Возможно вы использовали ее не на сервере")


@bot.slash_command(description="Количество серверов, на которых работает бот")
async def other_guilds(message: disnake.ApplicationCommandInteraction):
    c_inc()
    try:
        temp_command_data_tmp = "⚙️Количество сообществ, на которых работает бот: " + str(len(bot.guilds))
        await message.response.send_message(temp_command_data_tmp)
    except:
        await message.response.send_message("[Error] Не удалось выполнить команду. Возможно вы использовали ее не на сервере")

@bot.slash_command(description="Текущая дата и время")
async def date_time(message: disnake.ApplicationCommandInteraction):
    c_inc()
    temp_command_data_tmp = "🕒Текущая дата и время: " + str(datetime.datetime.now())
    await message.response.send_message(temp_command_data_tmp)


@bot.slash_command(description="Кредиты")
async def credits(message: disnake.ApplicationCommandInteraction):
    c_inc()
    await message.response.send_message(config.msg_credits)

@bot.slash_command(description="Донат")
async def donate(message: disnake.ApplicationCommandInteraction):
    c_inc()
    await message.response.send_message(config.msg_donate)


@bot.slash_command(description="Отправить запрос ChatGPT🧠")
async def chatgpt(message:disnake.ApplicationCommandInteraction, prompt: str):
        if str(message.channel.guild.id) in config.gpt_func_whitelist:
            try:
                await message.response.send_message("[ChatGPT🧠]: Думаю...")
                msg_content = prompt
                messages.append(
                    {"role": "user", "content": msg_content})
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages)
                reply = chat.choices[0].message.content
                temp_command_data_tmp = "[ChatGPT🧠]: "+str(reply)
                await message.edit_original_message(temp_command_data_tmp)
                messages.append({"role": "assistant", "content": reply})
            except:
                await message.response.send_message("[Error] Bad arguments or no access to openai api")
        else:
            await message.response.send_message("[Error] На этом сервере нельзя использовать chatgpt, обратитесь к (discord:leemonad) чтобы ваш сервер получил white-лист на эту функцию")
        c_inc()


@bot.slash_command(description="Рандом 1")
async def random(message: disnake.ApplicationCommandInteraction, пользователь: str, строка: str):
    num = randnum1.randint(0,1)
    if num == 1:
        temp_command_data_tmp = "🔫Пользователь "+str(пользователь) +" "+str(строка)
        await message.response.send_message(temp_command_data_tmp)
    else:
        temp_command_data_tmp = "🔫Пользователь " + str(пользователь) + " не " + str(строка)
        await message.response.send_message(temp_command_data_tmp)
    c_inc()


@bot.slash_command(description="Показывает статистику бота")
async def bot_stats(message: disnake.ApplicationCommandInteraction):
    temp_command_data_tmp = \
        f"""      
                 ⚙️Количество сообществ, на которых работает бот: {str(len(bot.guilds))}
            💬Использовано команд за все время: {int(sfdb.get_float_value_from_db("used_commands_count.txt"))} 
            🕒Время последней сессии: {datetime.datetime.now() - datetime_session_start}"""
    await message.response.send_message(temp_command_data_tmp)
    c_inc()


@bot.slash_command(description="Статистика сервера")
async def server_stats(message: disnake.ApplicationCommandInteraction):
    c_inc()
    try:
        try:
            embed = disnake.Embed(
                description=f'**Информация о сервере** {message.channel.guild.name}\n'
                            f'**Участники**\n'
                            f':bust_in_silhouette:Людей: {message.channel.guild.member_count}\n'
                            f'**Владелец**\n'
                            f'{message.channel.guild.owner}\n'
                            f'**Каналы**\n'
                            f':speech_balloon:Текстовые каналы: {len(message.channel.guild.text_channels)}\n'
                            f':loud_sound:Голосовые каналы: {len(message.channel.guild.voice_channels)}\n'
                            f'Категории: {len(message.channel.guild.categories)}\n'
                            f'**Другое**\n'
                            f'Уровень проверки: {message.channel.guild.verification_level}\n'
                            f'Дата создания: {message.channel.guild.created_at.strftime("%d.%m.%Y")}\n'
            )
            embed.set_footer(text=f'ID: {message.channel.guild.id}')
            embed.set_thumbnail(url=str(message.channel.guild.icon))
            await message.response.send_message(embed=embed)
        except:
            embed = disnake.Embed(
                description=f'**Информация о сервере** {message.channel.guild.name}\n'
                            f'**Участники**\n'
                            f':bust_in_silhouette:Людей: {message.channel.guild.member_count}\n'
                            f'**Владелец**\n'
                            f'{message.channel.guild.owner}\n'
                            f'**Каналы**\n'
                            f':speech_balloon:Текстовые каналы: {len(message.channel.guild.text_channels)}\n'
                            f':loud_sound:Голосовые каналы: {len(message.channel.guild.voice_channels)}\n'
                            f'Категории: {len(message.channel.guild.categories)}\n'
                            f'**Другое**\n'
                            f'Уровень проверки: {message.channel.guild.verification_level}\n'
                            f'Дата создания: {message.channel.guild.created_at.strftime("%d.%m.%Y")}\n'
            )
            embed.set_footer(text=f'ID: {message.channel.guild.id}')
            await message.response.send_message(embed=embed)
    except:
        await message.response.send_message("[Error] Произошла ошибка, возможно вы ввели эту команду не на сервере")

@bot.slash_command(description="Получить id сервер:канал")
async def get_guild_channel_id(message: disnake.ApplicationCommandInteraction):
    c_inc()
    checkstr = str(message.channel.guild.id) + ":" + str(message.channel.id)
    await message.response.send_message(checkstr)



@bot.slash_command(description="Убить кого-то")
async def kill(message: disnake.ApplicationCommandInteraction, пользователь: str):
    c_inc()
    try:
        msg_content = message.content.split()
        msg_content = ['',пользователь]
        temp_command_data_tmp = "🔫 " + str(message.author) + " убил " + str(msg_content[1])
        await message.response.send_message(temp_command_data_tmp)
    except:
        await message.response.send_message("[Error] Аргументы команды указаны неправильно")


@bot.slash_command(description="Поцелуйте кого-то")
async def kiss(message:disnake.ApplicationCommandInteraction, пользователь:str):
    c_inc()
    temp_command_data_tmp = "💋Пользователь "+str(message.author) +" поцеловал пользователя "+пользователь
    await message.response.send_message(temp_command_data_tmp)


@bot.slash_command(description="Совершите что-то с кем-то")
async def action(message:disnake.ApplicationCommandInteraction,пользователь:str,действие: str):
    c_inc()
    temp_command_data_tmp = "🔫Пользователь "+str(message.author)+" "+действие+" "+str(пользователь)
    await message.response.send_message(temp_command_data_tmp)


@bot.slash_command(description="Отправьте в мут человека")
async def mut(message: disnake.ApplicationCommandInteraction, пользователь: str):
    c_inc()
    if str(message.author) == str(message.channel.guild.owner) or str(message.author) in config.admin_list:
        try:
            msg_content = [' ',пользователь]
            # target
            # reason
            temp_command_data_tmp = "Указанный вами участник был успешно замучен"
            config.mut_list.append(str(msg_content[1]))
            await message.response.send_message(temp_command_data_tmp)
        except:
            await message.response.send_message("[Error] Неправильно указанная команда")
    else:
        await message.response.send_message("У вас нет прав на использование этой команды!")


@bot.slash_command(description="Размутить человека")
async def unmut(message: disnake.ApplicationCommandInteraction, пользователь: str):
    c_inc()
    if str(message.author) == str(message.channel.guild.owner) or str(message.author) in config.admin_list:
        try:
            msg_content = [' ', пользователь]
            # target
            # reason
            temp_command_data_tmp = "Указанный вами участник был успешно размучен"
            config.mut_list.remove(str(msg_content[1]))
            await message.response.send_message(temp_command_data_tmp)
        except:
            await message.response.send_message("[Error] Неправильно указанная команда или участник не в муте!")
    else:
        await message.response.send_message("У вас нет прав на использование этой команды!")


@bot.slash_command(description="Число пи")
async def pi(message: disnake.ApplicationCommandInteraction):
    c_inc()
    await message.response.send_message("3.14159265358979323846264338327950288419716939937510")

@bot.slash_command(description="Сыграйте в случайный плейс в роблоксе с нашей базы данных")
async def rand_rbx(message:  disnake.ApplicationCommandInteraction):
    c_inc()
    temp_command_data_tmp = "🎲Рандомный плейс: " + str(randnum1.choice(places_list))
    await message.response.send_message(temp_command_data_tmp)


@bot.slash_command(description="Сыграйте в случайный плейс напрямую с роблоксе")
async def rand_place_url(message: disnake.ApplicationCommandInteraction):
    c_inc()
    temp_command_data_tmp = "https://roblox.com/games/" + str(randnum1.randint(2000, 4000000000))
    r = requests.get(temp_command_data_tmp)
    if r.status_code == 200:
        temp_command_data_tmp = "🎲Рандомный плейс: " + temp_command_data_tmp
        await message.response.send_message(temp_command_data_tmp)
    else:
        temp_command_data_tmp = "🔴По URL " + temp_command_data_tmp + " ничего не найдено"
        await message.response.send_message(temp_command_data_tmp)


@bot.slash_command(description="Включает систему banword")
async def enable_banword(message: disnake.ApplicationCommandInteraction):
    c_inc()
    if str(message.author) == str(message.channel.guild.owner) or str(message.author) in config.admin_list:
        bwid = str(message.channel.guild.id) + "_" + str(message.channel.id)
        path = "bot_database\\banword_db\\" + str(bwid) + str(".txt")
        if os.path.exists(path):
            await message.response.send_message("[Banword System] На этом канале уже включена система banword")
        else:
            f = open(path, 'w')
            f.close()
            await message.response.send_message("[Banword System] Система banword успешно включена!")
    else:
        await message.response.send_message("У вас нет прав на выполнение этой команды")


@bot.slash_command(description="Добавляет новый banword")
async def add_banword(message: disnake.ApplicationCommandInteraction, banword: str):
    c_inc()
    if str(message.author) == str(message.channel.guild.owner) or str(message.author) in config.admin_list:
        bwid = str(message.channel.guild.id) + "_" + str(message.channel.id)
        path = "bot_database\\banword_db\\" + str(bwid) + str(".txt")
        msg_content = banword
        try:
            f = open(path,'r')
            flcontent = f.read() + " " + msg_content
            f.close()
            f = open(path,'w')
            f.write(flcontent)
            f.close()
            await message.response.send_message("[Banword System] ваш banword успешно записан")
        except:
            await message.response.send_message("[Banword System] Не удалось добавить banword. Возможно вы забыли включить систему banword")
    else:
        await message.response.send_message("У вас нет прав на выполнение этой команды")


@bot.slash_command(description="Отключает систему banword")
async def disable_banword(message: disnake.ApplicationCommandInteraction):
    c_inc()
    if str(message.author) == str(message.channel.guild.owner) or str(message.author) in config.admin_list:
        bwid = str(message.channel.guild.id) + "_" + str(message.channel.id)
        path = "bot_database\\banword_db\\" + str(bwid) + str(".txt")
        if os.path.exists(path):
            os.remove(path)
            await message.response.send_message("[Banword System] Система banword успешно отключена")
        else:
            await message.response.send_message("[Banword System] Система banword уже отключена")
    else:
        await message.response.send_message("У вас нет прав на выполнение этой команды")

@bot.slash_command(description="Проверяет, включена ли система banword в текущем канале")
async def check_banword_system(message: disnake.ApplicationCommandInteraction):
    c_inc()
    bwid = str(message.channel.guild.id) + "_" + str(message.channel.id)
    path = "bot_database\\banword_db\\" + str(bwid) + str(".txt")
    if os.path.exists(path):
        f = open(path,'r')
        ln = len(f.read().split())
        f.close()
        temp_command_data_tmp = f"[Banword System] На этом канале включена система banword✅ | Количество: {ln}"
        await message.response.send_message(temp_command_data_tmp)
    else:
        await message.response.send_message("[Banword System] На этом канале отключена система banword :x:")


@bot.slash_command(description="Просмотреть ваш баланс или баланс другого игрока")
async def balance(message: disnake.ApplicationCommandInteraction, пользователь: str):
    c_inc()
    msg_content = [' ', пользователь]
    if len(msg_content) > 1:
        msg_author = msg_content[1]
        path = "bot_database\\wallets\\" + str(msg_author) + ".txt"
        if os.path.exists(path):
            f = open(path, 'r')
            dat = f.read()
            f.close()
            embed = disnake.Embed(
                description=f'**Баланс пользователя {msg_content[1]}**\n'
                            f'{dat} 💵\n'
            )
            await message.response.send_message(embed=embed)
        else:
            await message.response.send_message("Извините, но такого пользователя не существует, либо у него нет баланса")
    else:
        msg_author = str(message.author)
        path = "bot_database\\wallets\\" + str(msg_author) + ".txt"
        if os.path.exists(path):
            f = open(path, 'r')
            dat = f.read()
            f.close()
            embed = disnake.Embed(
                description=f'**Ваш баланс**\n'
                            f'{dat} 💵\n'
            )
            embed.set_thumbnail(url=str(message.author.avatar))
            message.response.send_message(embed=embed)
        else:
            f = open(path, 'w')
            f.write('0')
            f.close()
            f = open(path, 'r')
            dat = f.read()
            f.close()
            embed = disnake.Embed(
                description=f'**Ваш баланс**\n'
                            f'{dat} 💵\n'
            )
            embed.set_thumbnail(url=str(message.author.avatar))
            message.response.send_message(embed=embed)


@bot.slash_command(description="Работа💼")
async def work(message: disnake.ApplicationCommandInteraction):
    c_inc()
    path = "bot_database\\last_worked\\" + str(message.author) + ".txt"
    bal_path = "bot_database\\wallets\\" + str(message.author) + ".txt"
    if os.path.exists(path):
        f = open(path, 'r')
        ster = f.read()
        try:
            last_work_time = float((ster))
        except ValueError:
            last_work_time = sys_time()
        f.close()
        if last_work_time + config.work_delay > sys_time():
            embed = disnake.Embed(
                description=f'**Работа :briefcase:**\n'
                            f'Извините, но вы уже работали. Подождите еще {int(last_work_time + config.work_delay - sys_time())} секунд.\n'
                            f'После истечения этого времени вы снова сможете работать\n'
            )
            embed.set_thumbnail(url=str(message.author.avatar))
            await message.response.send_message(embed=embed)
        else:
            embed = disnake.Embed(
                description=f'**Работа :briefcase:**\n'
                            f'Вы поработали и получили 1 💵.\n'
                            f'Подождите еще 10 секунд, прежде чем начать снова работать\n'
            )
            embed.set_thumbnail(url=str(message.author.avatar))
            await message.response.send_message(embed=embed)
            f = open(path, 'w')
            f.write(str(sys_time()))
            f.close()
            f = open(bal_path, 'r')
            try:
                bal_value = int(f.read())
            except ValueError:
                bal_value = 0
            f.close()
            f = open(bal_path, 'w')
            bal_value = bal_value + config.work_money_reward
            f.write(str(bal_value))
            f.close()
    else:
        f = open(path, 'w')
        f.write(str(int(sys_time())))
        f.close()
        f = open(bal_path, 'r')
        try:
            bal_value = int(f.read())
        except ValueError:
            bal_value = 0
        f.close()
        f = open(bal_path, 'w')
        bal_value = bal_value + config.work_money_reward
        f.write(str(bal_value))
        f.close()


@bot.slash_command(description="Отправить деньги другому пользователю")
async def send_money(message: disnake.ApplicationCommandInteraction, пользователь: str, сумма: str):
    # Разделяем сообщение на части
    msg_content = ["!dasda",пользователь,сумма]  # пользователь, количество валюты
    # Загружаем наш баланс
    my_balance_path = "bot_database\\wallets\\" + str(
        message.author) + ".txt"  # создаем строку, в которой храним путь к нашему балансу
    if str(message.author) != msg_content[1]:
        if os.path.exists(my_balance_path):  # поверяем, существует ли файл нашего баланса, если нет, то создаем
            # Файл существует, идем дальше
            # Проверяем, есть ли такое количество денег, которое мы указали для отправки
            try:
                f = open(my_balance_path, 'r')
            except:
                f = open(my_balance_path, 'w')
                f.write('0')
                f.close()
                f = open(my_balance_path,'r')
            my_balance = f.read()  # Читаем баланс с файла
            f.close()  # Закрываем файл
            try:
                my_balance = int(my_balance)  # Пытаемся преобразовать строку в число
            except ValueError:  # Скорее всего в файле пусто, будем считать что у нас 0 на балансе
                my_balance = 0

            receiver_balance_path = "bot_database\\wallets\\" + str(
                msg_content[1]) + ".txt"  # Строка, где храним баланс отправителя
            if os.path.exists(receiver_balance_path):
                # Кошелек человека существует, идем дальше
                amount = int(msg_content[2])  # Количество денег, которое мы хотим отправить
                if int(amount) <= int(my_balance) and int(
                        amount >= 1):  # Проверяем, есть ли у нас столько денег для отправки
                    # Денег достаточно, идем дальше
                    my_balance = my_balance - amount  # Отнимаем количество отправляемых денег с баланса
                    f = open(my_balance_path, 'w')
                    strball = str(my_balance)
                    f.write(strball)  # Записываем изменения баланса в файл
                    f.close()
                    # Открываем файл человека, которому отправляем деньги
                    f = open(receiver_balance_path, 'r')  # Открываем файл
                    try:
                        receiver_balance = int(f.read())  # Читаем баланс с файла
                    except ValueError:  # скорее всего файл пустой, будем считать что у нас 0 на балансе
                        receiver_balance = 0
                    receiver_balance = int(receiver_balance) + int(amount)  # даем пользователю деньги
                    f = open(receiver_balance_path, 'w')
                    rec_str = str(receiver_balance)  # преобразовываем баланс в строку
                    f.write(rec_str)  # пишем баланс в файл
                    f.close()
                    # Транзакция прошла успешно
                    embed = disnake.Embed(
                        description=f'**💵 Отправка денег**\n'
                                    f'Транзакция была совершена успешно\n'
                    )
                    embed.set_thumbnail(url=str(message.author.avatar))
                    await message.response.send_message(embed=embed)


                else:
                    # Денег не хватает, надо уведомить пользователя
                    embed = disnake.Embed(
                        description=f'**💵 Отправка денег**\n'
                                    f'Извините, но у вас недостаточно денег\n'
                                    f'Минимальная сумма для отправки 1💵\n'
                    )
                    embed.set_thumbnail(url=str(message.author.avatar))
                    await message.response.send_message(embed=embed)

            else:
                # Такого кошелька не существует, надо уведомить пользователя
                embed = disnake.Embed(
                    description=f'**💵 Отправка денег**\n'
                                f'Похоже, у того кому вы пытаетесь отправить деньги нет кошелька\n'
                                f'Попросите его ввести команду ```!balance``` чтобы создать кошелек\n'
                )
                embed.set_thumbnail(url=str(message.author.avatar))
                await message.response.send_message(embed=embed)

        else:
            f = open(my_balance_path,
                     'w')  # Когда мы отпрываем файл в режиме w, если его не существует, то он создается автоматически
            f.write('0')  # Записываем значение 0
            f.close()  # Закрываем файл
            # Отправляем сообщение о том, что у человека недостаточно денег (чтобы он ничего не заподозрил)
            embed = disnake.Embed(
                description=f'**💵 Отправка денег**\n'
                            f'Похоже, что у вас недостаточно денег\n'
                            f'Используйте команду ```!work``` для работы\n'
            )
            embed.set_thumbnail(url=str(message.author.avatar))
            await message.response.send_message(embed=embed)
    else:
        embed = disnake.Embed(
            description=f'**💵 Отправка денег**\n'
                        f'Похоже, вы пытаетесь отправить деньги самому себе\n'
                        f'```Вы не можете отправить деньги самому себе!```\n'
        )
        embed.set_thumbnail(url=str(message.author.avatar))
        await message.response.send_message(embed=embed)

@bot.slash_command(description="Получить помощь по экономике")
async def economy_help(message: disnake.ApplicationCommandInteraction):
    embed = disnake.Embed(
                    description= f'{config.economy_help_msg}\n'
                )
    embed.set_thumbnail(url=str(message.author.avatar))
    await message.response.send_message(embed=embed)

bot.run(config.token)
