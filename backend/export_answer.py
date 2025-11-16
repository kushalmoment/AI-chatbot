# export_answers.py
"""
回答データを CSV にエクスポートするワンファイルスクリプト。
- Firestore を使う場合: 環境変数 USE_FIREBASE=true を設定
    - 本番: FIREBASE_CRED_PATH=<service-account.json のパス>
    - エミュレータ: FIRESTORE_EMULATOR_HOST=localhost:8081 / FIREBASE_PROJECT_ID=demo-project
- SQL を使う場合: USE_FIREBASE=false（既定） + DATABASE_URL=sqlite:///app.db など

出力: backend/answers_export.csv
期待スキーマ:
  質問テンプレート (question_templates)
    - question_id (str/int)
    - attribute (str)
    - question_text (str)
  ユーザー回答 (user_answers)
    - user_id (str)
    - session_id (str)
    - question_id (str/int)
    - answer_text (str)
※ フィールド名が違う場合は、下の MAPPERS を調整してください。
"""

from __future__ import annotations
import os
from pathlib import Path
import csv
from typing import Dict, Any, Iterable, Tuple

BASE_DIR = Path(__file__).resolve().parent

# ===== 切替え設定（環境変数） =====
USE_FIREBASE = os.getenv("USE_FIREBASE", "false").lower() == "true"
FIREBASE_CRED_PATH = os.getenv("FIREBASE_CRED_PATH")  # 例: backend/credentials/firebase-service-account.json
FIRESTORE_EMULATOR_HOST = os.getenv("FIRESTORE_EMULATOR_HOST")  # 例: localhost:8081
FIREBASE_PROJECT_ID = os.getenv("FIREBASE_PROJECT_ID", "demo-project")

DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{(BASE_DIR / 'app.db').as_posix()}")

# ====== フィールド名のマッピング（必要に応じて修正） ======
MAPPERS = {
    "templates": {
        "collection": "question_templates",   # Firestore collection / SQL table
        "id_field": "question_id",
        "attr_field": "attribute",
        "text_field": "question_text",
    },
    "answers": {
        "collection": "user_answers",         # Firestore collection / SQL table
        "user_field": "user_id",
        "session_field": "session_id",
        "qid_field": "question_id",
        "answer_field": "answer_text",
    }
}


def resolve_path(p: str | None) -> Path | None:
    if not p:
        return None
    pp = Path(p)
    return pp if pp.is_absolute() else (BASE_DIR / pp).resolve()


# =========================
# Firestore 版
# =========================
def export_from_firestore(out_csv: Path) -> None:
    # 依存を遅延 import（未使用環境での ImportError を避ける）
    import firebase_admin
    from firebase_admin import credentials, firestore

    # 初期化
    if FIRESTORE_EMULATOR_HOST:
        # エミュレータ: サービスアカウント不要
        if not firebase_admin._apps:
            firebase_admin.initialize_app(options={"projectId": FIREBASE_PROJECT_ID})
    else:
        cred_path = resolve_path(FIREBASE_CRED_PATH)
        if not cred_path or not cred_path.exists():
            raise FileNotFoundError(
                "FIREBASE_CRED_PATH が未設定またはファイルが見つかりません。\n"
                "本番 Firestore に接続する場合はサービスアカウント JSON を用意してください。"
            )
        if not firebase_admin._apps:
            cred = credentials.Certificate(str(cred_path))
            firebase_admin.initialize_app(cred)

    db = firestore.client()

    T = MAPPERS["templates"]
    A = MAPPERS["answers"]

    # テンプレートを取得 → 辞書化
    t_docs = db.collection(T["collection"]).stream()
    qmap: Dict[str, Tuple[str, str]] = {}
    for doc in t_docs:
        d = doc.to_dict() or {}
        q_id = str(d.get(T["id_field"], "")).strip()
        if not q_id:
            continue
        attr = (d.get(T["attr_field"], "") or "")
        qtext = (d.get(T["text_field"], "") or "")
        qmap[q_id] = (str(attr), str(qtext))

    # 回答を取得
    a_docs = db.collection(A["collection"]).stream()

    # CSV 出力
    with out_csv.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["user_id", "session_id", "question_id", "attribute", "question_text", "answer_text"])
        count = 0
        for doc in a_docs:
            d = doc.to_dict() or {}
            user = str(d.get(A["user_field"], "") or "")
            sess = str(d.get(A["session_field"], "") or "")
            qid = str(d.get(A["qid_field"], "") or "")
            ans = str(d.get(A["answer_field"], "") or "")
            attr, qtext = qmap.get(qid, ("", ""))
            w.writerow([user, sess, qid, attr, qtext, ans])
            count += 1

    print(f"✅ Firestore から {count} 件をエクスポート: {out_csv.name}")


# =========================
# SQLAlchemy（RDB）版
# =========================
def export_from_sql(out_csv: Path) -> None:
    from sqlalchemy import create_engine, Column, Integer, String, Text
    from sqlalchemy.orm import declarative_base, sessionmaker

    T = MAPPERS["templates"]
    A = MAPPERS["answers"]

    # 簡易モデル（最低限の列のみ定義）
    Base = declarative_base()

    class QuestionTemplate(Base):
        __tablename__ = T["collection"]
        id = Column(Integer, primary_key=True, autoincrement=True)
        # 期待カラム名に合わせる（異なる場合はテーブル側を修正 or ここを変更）
        question_id = Column(String, nullable=False, unique=True)
        attribute = Column(String, default="")
        question_text = Column(Text, default="")

    class UserAnswer(Base):
        __tablename__ = A["collection"]
        id = Column(Integer, primary_key=True, autoincrement=True)
        user_id = Column(String, default="")
        session_id = Column(String, default="")
        question_id = Column(String, default="")
        answer_text = Column(Text, default="")

    engine = create_engine(DATABASE_URL, future=True)
    # 既存DBを前提。必要なら下行で作成（未作成時のみ）
    # Base.metadata.create_all(engine)

    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    with SessionLocal() as session:
        # テンプレート辞書
        qmap = {
            str(q.question_id): (q.attribute or "", q.question_text or "")
            for q in session.query(QuestionTemplate).all()
        }
        rows: Iterable[UserAnswer] = session.query(UserAnswer).all()

        with out_csv.open("w", newline="", encoding="utf-8-sig") as f:
            w = csv.writer(f)
            w.writerow(["user_id", "session_id", "question_id", "attribute", "question_text", "answer_text"])
            count = 0
            for r in rows:
                qid = str(r.question_id or "")
                attr, qtext = qmap.get(qid, ("", ""))
                w.writerow([r.user_id or "", r.session_id or "", qid, attr, qtext, r.answer_text or ""])
                count += 1

    print(f"✅ SQL（{DATABASE_URL}）から {count} 件をエクスポート: {out_csv.name}")


# =========================
# メイン
# =========================
def main() -> None:
    out_csv = BASE_DIR / "answers_export.csv"
    if USE_FIREBASE:
        export_from_firestore(out_csv)
    else:
        export_from_sql(out_csv)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
            # 失敗時にヒントを追加
            if USE_FIREBASE:
                hint = (
                    "\n対処ヒント:\n"
                    "- FIRESTORE_EMULATOR_HOST=host:port を設定してエミュレータ接続\n"
                    "- または FIREBASE_CRED_PATH でサービスアカウントJSONへのパスを設定\n"
                    "- コレクション/フィールド名が違う場合は MAPPERS を修正\n"
                )
            else:
                hint = (
                    "\n対処ヒント:\n"
                    f"- DATABASE_URL（現在: {DATABASE_URL}）が正しいか\n"
                    "- テーブル名/カラム名が既存DBと一致しているか（MAPPERSかモデルを調整）\n"
                )
            raise SystemExit(f"❌ エクスポート中にエラー: {e}{hint}")
