import os, discord
from pathlib import Path
from discord import app_commands
from dotenv import load_dotenv
from logging import getLogger, FileHandler, INFO, Formatter

import embeds, vars
from keep import keep_alive


# 環境変数の読み込み
load_dotenv()


# ロガー設定
logger = getLogger(__name__)
logger.setLevel(INFO)
f_handler = FileHandler("./bot.log")
f_handler.setLevel(INFO)
formatter = Formatter("%(asctime)s - %(levelname)s in %(funcName)s : %(message)s")
f_handler.setFormatter(formatter)
logger.addHandler(f_handler)


# ボットの各設定
TOKEN = os.environ["TOKEN"]
MY_GUILD = os.environ["GUILD_ID"]


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # self.tree.copy_global_to(guild=discord.Object(id=MY_GUILD))  # 開発環境
        await self.tree.sync(guild=discord.Object(id=MY_GUILD))


intents = discord.Intents.default()
client = MyClient(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")


# 埋め込みメッセージ新規作成コマンド
@client.tree.command()
@app_commands.rename(name="名前", content="内容")
@app_commands.describe(
    name="新規作成する埋め込みメッセージの名前を入力してください。",
    content="新規作成する埋め込みメッセージの内容を入力してください。",
)
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def newembed(interaction: discord.Interaction, name: str, content: str):
    """埋め込みメッセージを新規作成します。"""
    try:
        embeds.new_embed_command(name, content)
        await interaction.response.send_message(
            f"埋め込みメッセージを`{name}`として新規作成しました。", ephemeral=True
        )
        logger.info(f'Created new Embed as "{name}"')
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error(f'Failed to create new Embed "{name}"')


# 埋め込みメッセージ編集コマンド
@client.tree.command()
@app_commands.rename(name="名前", content="内容")
@app_commands.describe(
    name="既存の埋め込みメッセージの名前を入力してください。",
    content="編集後の埋め込みメッセージの内容を入力してください。",
)
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def editembed(interaction: discord.Interaction, name: str, content: str):
    """既存の埋め込みメッセージを編集します。"""
    try:
        embeds.edit_embed_command(name, content)
        await interaction.response.send_message(
            f"埋め込みメッセージ`{name}`を編集しました。", ephemeral=True
        )
        logger.info(f'Edited Embed "{name}"')
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error(f'Failed to edit Embed "{name}"')


# 埋め込みメッセージ削除コマンド
@client.tree.command()
@app_commands.rename(name="名前")
@app_commands.describe(name="削除する埋め込みメッセージの名前を入力してください。")
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def deleteembed(interaction: discord.Interaction, name: str):
    """既存の埋め込みメッセージを削除します。"""
    try:
        embeds.delete_embed_command(name)
        await interaction.response.send_message(
            f"埋め込みメッセージ`{name}`を削除しました。", ephemeral=True
        )
        logger.info(f'Deleted Embed "{name}"')
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error(f'Failed to delete Embed "{name}"')


# 埋め込みメッセージリストコマンド
@client.tree.command()
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def embedlist(interaction: discord.Interaction):
    """既存の埋め込みメッセージのリストを表示します。"""
    try:
        e_list = embeds.embed_list_command()
        text_to_send = "\n".join([f"・{embed.name}" for embed in e_list])
        await interaction.response.send_message(
            f"埋め込みメッセージのリストは以下の通りです。\n```{text_to_send}```",
            ephemeral=True,
        )
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error("Failed to send Embed list")


# 埋め込みメッセージ送信コマンド
@client.tree.command()
@app_commands.rename(name="名前")
@app_commands.describe(name="送信する埋め込みメッセージの名前を入力してください。")
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def sendembed(interaction: discord.Interaction, name: str):
    """既存の埋め込みメッセージを送信します。"""
    try:
        content_to_send = embeds.send_embed_command(name)
        embed_to_send = discord.Embed(
            title="",
            color=0xFF6347,
            description=content_to_send,
        )
        await interaction.channel.send(embed=embed_to_send)
        await interaction.response.send_message(
            f"埋め込みメッセージ`{name}`を送信しました。", ephemeral=True
        )
        logger.info(f'Sent Embed "{name}"')
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error(f'Failed to send Embed "{name}"')


# 埋め込みメッセージプレ送信コマンド
@client.tree.command()
@app_commands.rename(name="名前")
@app_commands.describe(name="プレ送信する埋め込みメッセージの名前を入力してください。")
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def presendembed(interaction: discord.Interaction, name: str):
    """既存の埋め込みメッセージをプレ送信します。"""
    try:
        content_to_send = embeds.send_embed_command(name)
        embed_to_send = discord.Embed(
            title="",
            color=0xFF6347,
            description=content_to_send,
        )

        await interaction.response.send_message(
            f"埋め込みメッセージ`{name}`をプレ送信しました。",
            embed=embed_to_send,
            ephemeral=True,
        )
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error(f'Failed to pre-send Embed "{name}"')


# 変数新規作成コマンド
@client.tree.command()
@app_commands.rename(name="名前", content="内容")
@app_commands.describe(
    name="新規作成する変数の名前を入力してください。",
    content="新規作成する変数の内容を入力してください。",
)
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def newvar(interaction: discord.Interaction, name: str, content: str):
    """変数を新規作成します。"""
    try:
        vars.new_var_command(name, content)
        await interaction.response.send_message(
            f"変数を`{name}`として新規作成しました。", ephemeral=True
        )
        logger.info(f'Created new Var as "{name}"')
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error(f'Failed to create new Var "{name}"')


# 変数編集コマンド
@client.tree.command()
@app_commands.rename(name="名前", content="内容")
@app_commands.describe(
    name="既存の変数の名前を入力してください。",
    content="編集後の変数の内容を入力してください。",
)
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def editvar(interaction: discord.Interaction, name: str, content: str):
    """既存の変数を編集します。"""
    try:
        vars.edit_var_command(name, content)
        await interaction.response.send_message(
            f"変数`{name}`を編集しました。", ephemeral=True
        )
        logger.info(f'Edited Var "{name}"')
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error(f'Failed to edit Var "{name}"')


# 変数削除コマンド
@client.tree.command()
@app_commands.rename(name="名前")
@app_commands.describe(name="削除する変数の名前を入力してください。")
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def deletevar(interaction: discord.Interaction, name: str):
    """既存の変数を削除します。"""
    try:
        vars.delete_var_command(name)
        await interaction.response.send_message(
            f"変数`{name}`を削除しました。", ephemeral=True
        )
        logger.info(f'Deleted Var "{name}"')
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error(f'Failed to delete Var "{name}"')


# 変数リストコマンド
@client.tree.command()
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def varlist(interaction: discord.Interaction):
    """既存の変数のリストを表示します。"""
    try:
        v_list = vars.var_list_command()
        text_to_send = "\n".join([f"・{var.name}" for var in v_list])
        await interaction.response.send_message(
            f"変数のリストは以下の通りです。\n```{text_to_send}```",
            ephemeral=True,
        )
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error("Failed to send Var list")


# ログファイル送信
@client.tree.command()
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def attachlog(interaction: discord.Interaction):
    """ボットのログファイルを送信します。"""
    try:
        await interaction.response.send_message(
            f"ログファイルです。",
            file=discord.File(Path("./bot.log")),
            ephemeral=True,
        )
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error("Failed to send logfile")


# データベースファイル送信
@client.tree.command()
@app_commands.default_permissions(administrator=True)
@discord.app_commands.guilds(int(MY_GUILD))
async def attachdb(interaction: discord.Interaction):
    """データベースファイルを送信します。"""
    try:
        await interaction.response.send_message(
            f"データベースファイルです。",
            file=discord.File(Path("./db.sqlite3")),
            ephemeral=True,
        )
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error("Failed to send dbfile")


# ボットの起動
keep_alive()
try:
    client.run(TOKEN)
except:
    os.system("kill")
