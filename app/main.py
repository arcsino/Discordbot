import os, discord
from discord import app_commands
from dotenv import load_dotenv
from logging import getLogger, FileHandler, INFO, Formatter
from embed import (
    new_embed_command,
    edit_embed_command,
    delete_embed_command,
    embed_list_command,
    send_embed_command,
)
from var import new_var_command, edit_var_command, delete_var_command, var_list_command
from server import server_thread  # 開発環境でコメント


# 環境変数の読み込み
load_dotenv()


# ロガー設定
logger = getLogger(__name__)
logger.setLevel(INFO)
f_handler = FileHandler("./app/app.log")
f_handler.setLevel(INFO)
formatter = Formatter("%(asctime)s - %(levelname)s in %(funcName)s : %(message)s")
f_handler.setFormatter(formatter)
logger.addHandler(f_handler)


# ボットの各設定
TOKEN = os.environ["TOKEN"]
MY_GUILD = discord.Object(id=os.environ["GUILD_ID"])


class MyClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)

    async def setup_hook(self):
        # self.tree.copy_global_to(guild=MY_GUILD)  # 開発環境ではコメント解除
        # await self.tree.sync(guild=MY_GUILD)  # 開発環境ではコメント解除
        await self.tree.sync()  # 開発環境ではコメント


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
async def newembed(interaction: discord.Interaction, name: str, content: str):
    """埋め込みメッセージを新規作成します。"""
    try:
        new_embed_command(name, content)
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
async def editembed(interaction: discord.Interaction, name: str, content: str):
    """既存の埋め込みメッセージを編集します。"""
    try:
        edit_embed_command(name, content)
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
async def deleteembed(interaction: discord.Interaction, name: str):
    """既存の埋め込みメッセージを削除します。"""
    try:
        delete_embed_command(name)
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
async def embedlist(interaction: discord.Interaction):
    """既存の埋め込みメッセージのリストを表示します。"""
    try:
        e_list = embed_list_command()
        text_to_send = "\n".join([f"・{embed}" for embed in e_list])
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
async def sendembed(interaction: discord.Interaction, name: str):
    """既存の埋め込みメッセージを送信します。"""
    try:
        text_to_send = send_embed_command(name)
        embed = discord.Embed(
            title="",
            color=0xFF6347,
            description=text_to_send,
        )
        await interaction.channel.send(embed=embed)
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
async def presendembed(interaction: discord.Interaction, name: str):
    """既存の埋め込みメッセージをプレ送信します。"""
    try:
        text_to_send = send_embed_command(name)
        embed = discord.Embed(
            title="",
            color=0xFF6347,
            description=text_to_send,
        )

        await interaction.response.send_message(
            f"埋め込みメッセージ`{name}`をプレ送信しました。",
            embed=embed,
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
async def newvar(interaction: discord.Interaction, name: str, content: str):
    """変数を新規作成します。"""
    try:
        new_var_command(name, content)
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
async def editvar(interaction: discord.Interaction, name: str, content: str):
    """既存の変数を編集します。"""
    try:
        edit_var_command(name, content)
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
async def deletevar(interaction: discord.Interaction, name: str):
    """既存の変数を削除します。"""
    try:
        delete_var_command(name)
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
async def varlist(interaction: discord.Interaction):
    """既存の変数のリストを表示します。"""
    try:
        v_list = var_list_command()
        text_to_send = "\n".join([f"・{var[0]}" for var in v_list])
        await interaction.response.send_message(
            f"変数のリストは以下の通りです。\n```{text_to_send}```",
            ephemeral=True,
        )
    except Exception as e:
        await interaction.response.send_message(f"[Error]:{e}", ephemeral=True)
        logger.error("Failed to send Var list")


# Koyeb用 サーバー立ち上げ
server_thread()  # 開発環境ではコメント
client.run(TOKEN)
