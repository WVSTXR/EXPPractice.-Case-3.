from datetime import datetime


class User:
    """Пользователь системы."""

    def __init__(self, username: str, role: str = "employee"):
        self.username = username
        self.role = role  # admin, manager, employee

    def to_dict(self) -> dict:
        return {"username": self.username, "role": self.role}

    @staticmethod
    def from_dict(data: dict) -> "User":
        return User(data["username"], data["role"])

    def __repr__(self):
        return f"User({self.username}, {self.role})"


class Document:
    """Документ в системе."""

    def __init__(self, doc_id: int, title: str, author: str,
                 content: str = "", status: str = "draft",
                 created_at: str = None, deadline: str = None):
        self.doc_id = doc_id
        self.title = title
        self.author = author
        self.content = content
        self.status = status  # draft, on_review, approved, rejected, archived
        self.created_at = created_at or datetime.now().isoformat(timespec="seconds")
        self.deadline = deadline  # ISO-строка или None

    def to_dict(self) -> dict:
        return {
            "doc_id": self.doc_id,
            "title": self.title,
            "author": self.author,
            "content": self.content,
            "status": self.status,
            "created_at": self.created_at,
            "deadline": self.deadline,
        }

    @staticmethod
    def from_dict(data: dict) -> "Document":
        return Document(
            doc_id=data["doc_id"],
            title=data["title"],
            author=data["author"],
            content=data.get("content", ""),
            status=data.get("status", "draft"),
            created_at=data.get("created_at"),
            deadline=data.get("deadline"),
        )

    def __repr__(self):
        return f"Document(#{self.doc_id}, {self.title}, {self.status})"