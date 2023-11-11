token = 'Токен вашего бота'

gpt_api_key = "OpenAI API ключ"
prefix = "!"

anon_message_webhook = "Ссылка на вебхук, куда отправляются анонимные сообщения"
anon_username = "Annonymous Message"

spy_mode = False
log_messages = False
log_errors = False
secure_mode = True
switch_mode = 0 #0 is client mode, 1 - is bot mode
commands_counter_enable = True



mut_list = []
inv_mut = []

#economy
work_delay = 10 #time in seconds
work_money_reward = 1

bullying_mode = False
bullying_messages = []
bullying_list = []

help_msg = """Введите свое help-message здесь
"""

economy_help_msg = """    **💵Валюта**
```
!balance - просмотреть баланс
!balance [ник] - баланс другого человека
!work - каждые 10 секунд вы сможете поработать и получить 1 💵
!send (send_money для слэш команд) [пользователь], [количество валюты] - отправить деньги указанному пользователю```\n"""

help_msg2 = """Nothing to see here..."""

msg_credits = """
Ваши кредиты"""

msg_donate = """
Ссылки на донат"""

word_banlist = ["введите ваш список запрещенных слов здесь (нужен для анонимных сообщений)"]

admin_list = []
admin_password = "пароль для входа в панель администратора бота (нужно для отладки)"

gpt_func_whitelist = ["1154784913044807760","1171497670339203102"]

debug_msg = """
⚙️Bot Status
Node#1 - Online 🟢"""

command_test = prefix + "test"
command_help = prefix + "helpme"
command_status = prefix + "status"
command_anonymous_message = prefix + "anonmessage"
command_idea = prefix + "idea"
command_eval = prefix + "eval"
command_randint = prefix + "randint"
command_randfloat = prefix + "randfloat"
command_memberscount = prefix + "members_count"
command_studio_stats = prefix + "studio"
command_get_guild = prefix + "other_guilds"
command_economy_help = prefix + "economy_help"
command_admin_login = prefix + "admin_login"
command_check_admin = prefix + "check_admin"
command_check_me = prefix + "check_me"
command_add_admin = prefix + "add_admin"
command_datetime = prefix + "datetime"
command_send = prefix +"send"
command_credits = prefix + "credits"
command_donate = prefix + "donate"
command_chatgpt = prefix + "chatgpt"
command_random = prefix + "random"
command_stats = prefix + "bot_stats"
command_server_stats = prefix + "server_stats"
command_bump_register = prefix +"bump_register"
command_bump = prefix + "bump"
command_check_banword_system = prefix + "check_banword_system"
command_enable_banword_system = prefix + "enable_banword"
command_disable_banword_system = prefix + "disable_banword"
command_add_banword = prefix + "add_banword"
command_remove_banword = prefix + "remove_banword"
command_kill = prefix + "kill"
command_kiss = prefix + "kiss"
command_mut = prefix + "mut"
command_work = prefix + "work"
command_unmut = prefix + "unmut"
command_pi = prefix + "pi"
command_random_rbx = prefix + "rand_rbx"
command_random_rbx1 = prefix + "rand_place_url"
command_promo = prefix + "promo"
command_action = prefix + "action"
command_helpm2 = prefix +"helpm2"
command_balance = prefix + "balance"

#this commands requires bot admin access or owner access
command_start_bullying = prefix + "bullying"
command_bullying_disable = prefix + "bullying_disable"
command_bullying_enable = prefix + "bullying_enable"