from system import DocumentManagementSystem


def main():
    system = DocumentManagementSystem()
    system.load_from_file()

    # Демонстрационные пользователи
    if not system.users:
        system.register_user("admin", "admin")
        system.register_user("ivanov", "employee")
        system.register_user("petrov", "manager")

    while True:
        print("\n===== СЭД ХМГМА =====")
        print("1. Создать документ")
        print("2. Отправить на согласование")
        print("3. Согласовать")
        print("4. Отклонить")
        print("5. Архивировать")
        print("6. Найти документ по ID")
        print("7. Мои документы")
        print("8. Просроченные документы")
        print("9. Сохранить")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        try:
            if choice == "1":
                user = input("Логин автора: ")
                title = input("Заголовок: ")
                content = input("Содержание: ")
                deadline = input("Срок (YYYY-MM-DD) или пусто: ") or None
                doc = system.create_document(user, title, content, deadline)
                print(f"Создан документ #{doc.doc_id}")

            elif choice == "2":
                doc_id = int(input("ID документа: "))
                doc = system.submit_for_review(doc_id)
                print(f"Документ #{doc.doc_id} отправлен на согласование")

            elif choice == "3":
                user = input("Логин согласующего: ")
                doc_id = int(input("ID документа: "))
                doc = system.approve_document(doc_id, user)
                print(f"Документ #{doc.doc_id} согласован")

            elif choice == "4":
                user = input("Логин согласующего: ")
                doc_id = int(input("ID документа: "))
                doc = system.reject_document(doc_id, user)
                print(f"Документ #{doc.doc_id} отклонён")

            elif choice == "5":
                user = input("Логин администратора: ")
                doc_id = int(input("ID документа: "))
                doc = system.archive_document(doc_id, user)
                print(f"Документ #{doc.doc_id} передан в архив")

            elif choice == "6":
                doc_id = int(input("ID документа: "))
                doc = system.find_by_id(doc_id)
                print(doc.to_dict())

            elif choice == "7":
                user = input("Логин автора: ")
                for d in system.find_by_author(user):
                    print(d)

            elif choice == "8":
                overdue = system.overdue_documents()
                if not overdue:
                    print("Просроченных документов нет")
                for d in overdue:
                    print(d)

            elif choice == "9":
                system.save_to_file()
                print("Данные сохранены")

            elif choice == "0":
                system.save_to_file()
                print("Выход")
                break

            else:
                print("Неверный выбор")

        except (ValueError, PermissionError) as e:
            print(f"Ошибка: {e}")


if __name__ == "__main__":
    main()