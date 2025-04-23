from setting import session
from models import Var


def get_var_list():
    """変数一覧取得"""
    with session as s:
        v_list = s.query(Var).all()
        return v_list


def new_var_command(name: str, content: str):
    """変数新規作成"""
    with session as s:
        if s.query(Var).filter(Var.name == name).all():
            raise Exception(
                f"既に`{name}`という名前の変数が存在します。別の名前で新規作成するか、既存の変数を削除してください。"
            )
        var = Var(name=name, content=content)
        s.add(var)
        s.commit()


def edit_var_command(name: str, content: str):
    """変数編集"""
    with session as s:
        var = s.query(Var).filter(Var.name == name).all()
        if not var:
            raise Exception(
                f"`{name}`という名前の変数が存在しません。入力ミスがないか確認してください。"
            )
        var[0].content = content
        s.commit()


def delete_var_command(name: str):
    """変数削除"""
    with session as s:
        var = s.query(Var).filter(Var.name == name).all()
        if not var:
            raise Exception(
                f"`{name}`という名前の変数が存在しません。入力ミスがないか確認してください。"
            )
        s.delete(var[0])
        s.commit()


def var_list_command():
    """変数リスト"""
    v_list = get_var_list()
    if not v_list:
        raise Exception("変数が存在しません。")
    return v_list
