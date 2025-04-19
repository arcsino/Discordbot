import sqlite3
from var import get_var_list


def get_embed_list():
    dbname = "./app/global.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM embed")
    e_list = cur.fetchall()
    cur.close()
    conn.close()
    return e_list


def execute_db(command: str):
    dbname = "./app/global.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    cur.close()
    conn.close()


def new_embed_command(name: str, content: str):
    """埋め込みメッセージ新規作成"""

    for embed in get_embed_list():
        if embed[1] == name:
            raise Exception(
                f"既に`{name}`という名前の埋め込みメッセージが存在します。別の名前で新規作成するか、既存の埋め込みメッセージを削除してください。"
            )
    content_to_save = "\n".join(content.split("\\n"))
    execute_db(
        f'INSERT INTO embed(name, content) values("{name}", "{content_to_save}")'
    )


def edit_embed_command(name: str, content: str):
    """埋め込みメッセージ編集"""

    does_exist = False
    for embed in get_embed_list():
        if embed[1] == name:
            does_exist = True
            break
    if not does_exist:
        raise Exception(
            f"`{name}`という名前の埋め込みメッセージが存在しません。入力ミスがないか確認してください。"
        )
    content_to_save = "\n".join(content.split("\\n"))
    execute_db(f'UPDATE embed SET content = "{content_to_save}" WHERE name = "{name}"')


def delete_embed_command(name: str):
    """埋め込みメッセージ削除"""

    does_exist = False
    for embed in get_embed_list():
        if embed[1] == name:
            does_exist = True
            break
    if not does_exist:
        raise Exception(
            f"`{name}`という名前の埋め込みメッセージが存在しません。入力ミスがないか確認してください。"
        )
    execute_db(f'DELETE FROM embed WHERE name = "{name}"')


def embed_list_command():
    """埋め込みメッセージリスト"""

    e_list = [embed[1] for embed in get_embed_list()]
    if not e_list:
        raise Exception("埋め込みメッセージが存在しません。")
    return e_list


def send_embed_command(name: str):
    """埋め込みメッセージ送信"""

    e_list = get_embed_list()
    v_list = get_var_list()

    does_exist = False
    for embed in e_list:
        if embed[1] == name:
            does_exist = True
            content_to_send = str(embed[2])
            break
    if not does_exist:
        raise Exception(
            f"`{name}`という名前の埋め込みメッセージが存在しません。入力ミスがないか確認してください。"
        )

    for var in v_list:
        content_to_send = content_to_send.replace(f"%({var[1]})s", f"{var[2]}")
    return content_to_send
