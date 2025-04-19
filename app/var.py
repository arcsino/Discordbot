import sqlite3


def get_var_list():
    dbname = "./app/global.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute("SELECT * FROM var")
    v_list = cur.fetchall()
    cur.close()
    conn.close()
    return v_list


def execute_db(command: str):
    dbname = "./app/global.db"
    conn = sqlite3.connect(dbname)
    cur = conn.cursor()
    cur.execute(command)
    conn.commit()
    cur.close()
    conn.close()


def new_var_command(name: str, content: str):
    """変数新規作成"""

    for var in get_var_list():
        if var[1] == name:
            raise Exception(
                f"既に`{name}`という名前の変数が存在します。別の名前で新規作成するか、既存の変数を削除してください。"
            )
    execute_db(f'INSERT INTO var(name, content) values("{name}", "{content}")')


def edit_var_command(name: str, content: str):
    """変数編集"""

    does_exist = False
    for var in get_var_list():
        if var[1] == name:
            does_exist = True
            break
    if not does_exist:
        raise Exception(
            f"`{name}`という名前の変数が存在しません。入力ミスがないか確認してください。"
        )
    execute_db(f'UPDATE var SET content = "{content}" WHERE name = "{name}"')


def delete_var_command(name: str):
    """変数削除"""

    does_exist = False
    for var in get_var_list():
        if var[1] == name:
            does_exist = True
            break
    if not does_exist:
        raise Exception(
            f"`{name}`という名前の変数が存在しません。入力ミスがないか確認してください。"
        )
    execute_db(f'DELETE FROM var WHERE name = "{name}"')


def var_list_command():
    """変数リスト"""

    v_list = [(var[1], var[2]) for var in get_var_list()]
    if not v_list:
        raise Exception("変数が存在しません。")
    return v_list
