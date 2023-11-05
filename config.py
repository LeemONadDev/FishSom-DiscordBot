token = 'insert your token here'
fish_som_token = 'no matter'
gpt_api_key = "insert your openai api key here"
prefix = "!"

anon_message_webhook = "insert your discord webhook here"
anon_username = "insert webhook username here"

spy_mode = False
log_messages = False
log_errors = False
secure_mode = True
switch_mode = 0 #0 is client mode, 1 - is bot mode
commands_counter_enable = True

words_ban_list = []
words_ban_list_guilds_global = []
words_ban_list_allowed_guilds_and_channels = {}
words_ban_list_banwords_list = {}

bullying_mode = False
bullying_messages = ["insert your messages here"]
bullying_list = []

help_msg = """insert your help msg here"""

msg_credits = """insert your credits msg here"""

msg_donate = """
insert your donate message here"""

word_banlist = ["discord.gg"]

admin_list = ["insert your nickname here"]
admin_password = "insert your password here"

gpt_func_whitelist = ["insert server id here"]

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
command_admin_login = prefix + "admin_login"
command_check_admin = prefix + "check_admin"
command_check_me = prefix + "check_me"
command_add_admin = prefix + "add_admin"
command_datetime = prefix + "datetime"
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

#this commands requires bot admin access or owner access
command_start_bullying = prefix + "bullying"
command_bullying_disable = prefix + "bullying_disable"
command_bullying_enable = prefix + "bullying_enable"