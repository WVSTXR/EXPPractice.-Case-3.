import json
from datetime import datetime
from models import User, Document


class DocumentManagementSystem:
    """Ядро системы документооборота."""

    def __init__(self):
        self.users: dict[str, User] = {}
        self.documents: dict[int, Document] = {}
        self.next_id: int = 1

    # ---------- Пользователи ----------

    def register_user(self, username: str, role: str = "employee") -> User:
        if username in self.users:
            raise ValueError(f"Пользователь {username} уже существует")
        user = User(username, role)
        self.users[username] = user
        return user

    def get_user(self, username: str) -> User:
        if username not in self.users:
            raise ValueError(f"Пользователь {username} не найден")
        return self.users[username]

    # ---------- Документы ----------

    def create_document(self, username: str, title: str,
                        content: str = "", deadline: str = None) -> Document:
        user = self.get_user(username)
        doc = Document(
            doc_id=self.next_id,
            title=title,
            author=user.username,
            content=content,
            deadline=deadline,
        )
        self.documents[self.next_id] = doc
        self.next_id += 1
        return doc

    def submit_for_review(self, doc_id: int) -> Document:
        doc = self._get_doc(doc_id)
        if doc.status != "draft":
            raise ValueError("На согласование можно отправить только черновик")
        doc.status = "on_review"
        return doc

    def approve_document(self, doc_id: int, username: str) -> Document:
        user = self.get_user(username)
        if user.role not in ("admin", "manager"):
            raise PermissionError("Недостаточно прав для согласования")
        doc = self._get_doc(doc_id)
        if doc.status != "on_review":
            raise ValueError("Документ не находится на согласовании")
        doc.status = "approved"
        return doc

    def reject_document(self, doc_id: int, username: str) -> Document:
        user = self.get_user(username)
        if user.role not in ("admin", "manager"):
            raise PermissionError("Недостаточно прав для отклонения")
        doc = self._get_doc(doc_id)
        if doc.status != "on_review":
            raise ValueError("Документ не находится на согласовании")
        doc.status = "rejected"
        return doc

    def archive_document(self, doc_id: int, username: str) -> Document:
        user = self.get_user(username)
        if user.role != "admin":
            raise PermissionError("Только администратор может архивировать")
        doc = self._get_doc(doc_id)
        if doc.status != "approved":
            raise ValueError("В архив можно передать только согласованный документ")
        doc.status = "archived"
        return doc

    # ---------- Поиск и контроль ----------

    def find_by_id(self, doc_id: int) -> Document:
        return self._get_doc(doc_id)

    def find_by_author(self, username: str) -> list[Document]:
        return [d for d in self.documents.values() if d.author == username]

    def overdue_documents(self) -> list[Document]:
        now = datetime.now()
        result = []
        for doc in self.documents.values():
            if doc.deadline and doc.status in ("draft", "on_review"):
                deadline = datetime.fromisoformat(doc.deadline)
                if deadline < now:
                    result.append(doc)
        return result

    # ---------- Сохранение / загрузка ----------

    def save_to_file(self, path: str = "data.json"):
        data = {
            "users": [u.to_dict() for u in self.users.values()],
            "documents": [d.to_dict() for d in self.documents.values()],
            "next_id": self.next_id,
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def load_from_file(self, path: str = "data.json"):
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except FileNotFoundError:
            return

        self.users = {u["username"]: User.from_dict(u) for u in data["users"]}
        self.documents = {
            d["doc_id"]: Document.from_dict(d) for d in data["documents"]
        }
        self.next_id = data.get("next_id", 1)

    # ---------- Приватное ----------

    def _get_doc(self, doc_id: int) -> Document:
        if doc_id not in self.documents:
            raise ValueError(f"Документ #{doc_id} не найден")
        return self.documents[doc_id]