from setting import session
from models import Embed
from vars import get_var_list


def get_embed_list():
    """埋め込みメッセージ一覧取得"""
    with session as s:
        e_list = s.query(Embed).all()
        return e_list


def new_embed_command(name: str, content: str):
    """埋め込みメッセージ新規作成"""
    with session as s:
        if s.query(Embed).filter(Embed.name == name).all():
            raise Exception(
                f"既に`{name}`という名前の埋め込みメッセージが存在します。別の名前で新規作成するか、既存の埋め込みメッセージを削除してください。"
            )
        content_to_save = "\n".join(content.split("\\n"))
        embed = Embed(name=name, content=content_to_save)
        s.add(embed)
        s.commit()


def edit_embed_command(name: str, content: str):
    """埋め込みメッセージ編集"""
    with session as s:
        embed = s.query(Embed).filter(Embed.name == name).all()
        if not embed:
            raise Exception(
                f"`{name}`という名前の埋め込みメッセージが存在しません。入力ミスがないか確認してください。"
            )
        content_to_save = "\n".join(content.split("\\n"))
        embed[0].content = content_to_save
        s.commit()


def delete_embed_command(name: str):
    """埋め込みメッセージ削除"""
    with session as s:
        embed = s.query(Embed).filter(Embed.name == name).all()
        if not embed:
            raise Exception(
                f"`{name}`という名前の埋め込みメッセージが存在しません。入力ミスがないか確認してください。"
            )
        s.delete(embed[0])
        s.commit()


def embed_list_command():
    """埋め込みメッセージリスト"""
    e_list = get_embed_list()
    if not e_list:
        raise Exception("埋め込みメッセージが存在しません。")
    return e_list


def send_embed_command(name: str):
    """埋め込みメッセージ送信"""
    with session as s:
        embed = s.query(Embed).filter(Embed.name == name).all()
        if not embed:
            raise Exception(
                f"`{name}`という名前の埋め込みメッセージが存在しません。入力ミスがないか確認してください。"
            )
        v_list = get_var_list()
        for v in v_list:
            content_to_send = embed[0].content.replace(f"%({v.name})s", f"{v.content}")
        return content_to_send
