import flet as ft
import atexit
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Optional



class BaseEntity(ABC):

    @abstractmethod
    def get_id(self) -> int:
        pass

    @abstractmethod
    def to_display_string(self) -> str:
        pass


class KeyValuePair:
    """
    используется внутри CustomMap вместо  dict
    """

    def __init__(self, key: Any, value: Any):
        self._key = key
        self._value = value

    @property
    def key(self) -> Any:
        return self._key

    @key.setter
    def key(self, value: Any):
        self._key = value

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, value: Any):
        self._value = value

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, KeyValuePair):
            return NotImplemented
        return self._key == other._key and self._value == other._value

    def __hash__(self) -> int:
        return hash((self._key, str(self._value)))

    def __str__(self) -> str:
        return f"{self._key}: {self._value}"

    def __repr__(self) -> str:
        return f"KeyValuePair(key={self._key!r}, value={self._value!r})"


class CustomMap:
    """
    хранит данные в списке объектов KeyValuePair
    """

    def __init__(self):
        self._items = []

    @property
    def items(self) -> list:
        return self._items

    @items.setter
    def items(self, value: list):
        if not isinstance(value, list):
            raise ValueError("items must be a list")
        self._items = value

    def put(self, key: Any, value: Any) -> None:
        """добавление или обновляет значение по ключу"""
        for item in self._items:
            if item.key == key:
                item.value = value
                return
        self._items.append(KeyValuePair(key, value))

    def get(self, key: Any) -> Optional[Any]:
        """отдает значение по ключу или None"""
        for item in self._items:
            if item.key == key:
                return item.value
        return None

    def remove(self, key: Any) -> bool:
        """удаляет пару по ключу. True если удалено"""
        for index, item in enumerate(self._items):
            if item.key == key:
                self._items.pop(index)
                return True
        return False

    def get_all_values(self) -> list:
        """отдает список всех значений"""
        result = []
        for item in self._items:
            result.append(item.value)
        return result

    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self):
        return iter(self._items)

    def __contains__(self, key: Any) -> bool:
        for item in self._items:
            if item.key == key:
                return True
        return False

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, CustomMap):
            return NotImplemented
        return self._items == other._items

    def __str__(self) -> str:
        parts = []
        for item in self._items:
            parts.append(str(item))
        return "CustomMap([" + ", ".join(parts) + "])"

    def __repr__(self) -> str:
        return f"CustomMap(items={self._items!r})"



class User(BaseEntity):
    """
    юзер системы
    """

    def __init__(self, user_id: int, login: str):
        self._id = user_id
        self._login = login

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("User id must be a non-negative integer")
        self._id = value

    @property
    def login(self) -> str:
        return self._login

    @login.setter
    def login(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Login must be a non-empty string")
        self._login = value.strip()

    def get_id(self) -> int:
        return self._id

    def to_display_string(self) -> str:
        return f"User: {self._login}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, User):
            return NotImplemented
        return self._id < other._id

    def __add__(self, other: Any) -> str:
        if not isinstance(other, User):
            return NotImplemented
        return f"{self._login} & {other.login}"

    def __str__(self) -> str:
        return f"User({self._login})"

    def __repr__(self) -> str:
        return f"User(id={self._id}, login={self._login!r})"


class Assignment(BaseEntity):
    def __init__(
        self,
        task_id: int,
        title: str,
        priority: int,
        completed: bool = False
    ):
        self._id = task_id
        self._title = title
        self._priority = priority
        self._completed = completed

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Assignment id must be a non-negative integer")
        self._id = value

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Title must be a non-empty string")
        self._title = value.strip()

    @property
    def priority(self) -> int:
        return self._priority

    @priority.setter
    def priority(self, value: int):
        if not isinstance(value, int) or value < 1 or value > 10:
            raise ValueError("Priority must be an integer from 1 to 10")
        self._priority = value

    @property
    def completed(self) -> bool:
        return self._completed

    @completed.setter
    def completed(self, value: bool):
        self._completed = bool(value)

    def get_id(self) -> int:
        return self._id

    def to_display_string(self) -> str:
        status = "done" if self._completed else "active"
        return f"[{self._priority}] {self._title} ({status})"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Assignment):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, Assignment):
            return NotImplemented
        if self._priority == other._priority:
            return self._id < other._id
        return self._priority < other._priority

    def __len__(self) -> int:
        return len(self._title)

    def __bool__(self) -> bool:
        return bool(self._title)

    def __str__(self) -> str:
        return f"Assignment: {self._title}"

    def __repr__(self) -> str:
        return (
            f"Assignment(id={self._id}, title={self._title!r}, "
            f"priority={self._priority}, completed={self._completed})"
        )


class SessionRecord(BaseEntity):
    """
    Запись о сессии пользователя
    """

    def __init__(
        self,
        record_id: int,
        login: str,
        time_in: datetime,
        time_out: Optional[datetime] = None
    ):
        self._id = record_id
        self._login = login
        self._time_in = time_in
        self._time_out = time_out

    @property
    def id(self) -> int:
        return self._id

    @id.setter
    def id(self, value: int):
        if not isinstance(value, int) or value < 0:
            raise ValueError("Session id must be a non-negative integer")
        self._id = value

    @property
    def login(self) -> str:
        return self._login

    @login.setter
    def login(self, value: str):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Login must be a non-empty string")
        self._login = value.strip()

    @property
    def time_in(self) -> datetime:
        return self._time_in

    @time_in.setter
    def time_in(self, value: datetime):
        if not isinstance(value, datetime):
            raise ValueError("time_in must be datetime")
        self._time_in = value

    @property
    def time_out(self) -> Optional[datetime]:
        return self._time_out

    @time_out.setter
    def time_out(self, value: Optional[datetime]):
        if value is not None and not isinstance(value, datetime):
            raise ValueError("time_out must be datetime or None")
        self._time_out = value

    def get_id(self) -> int:
        return self._id

    def to_display_string(self) -> str:
        return f"{self._login}: {self._time_in} -> {self._time_out}"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, SessionRecord):
            return NotImplemented
        return self._id == other._id

    def __hash__(self) -> int:
        return hash(self._id)

    def __lt__(self, other: Any) -> bool:
        if not isinstance(other, SessionRecord):
            return NotImplemented
        return self._time_in < other._time_in

    def __str__(self) -> str:
        return f"SessionRecord(login={self._login})"

    def __repr__(self) -> str:
        return (
            f"SessionRecord(id={self._id}, login={self._login!r}, "
            f"time_in={self._time_in!r}, time_out={self._time_out!r})"
        )



class ReportFormatter:
    """
    Класс для формирования отчёта
    """

    TIME_FORMAT = "%d.%m.%Y %H:%M:%S"

    @staticmethod
    def format_datetime(value: Optional[datetime]) -> str:
        if value is None:
            return "N/A"
        return value.strftime(ReportFormatter.TIME_FORMAT)

    @staticmethod
    def build_table(records: list) -> str:
        """
        Строит таблицу
        """
        if not records:
            return ""

        login_values = ["login"]
        time_in_values = ["time_in"]
        time_out_values = ["time_out"]

        for record in records:
            login_values.append(record.login)
            time_in_values.append(ReportFormatter.format_datetime(record.time_in))
            time_out_values.append(ReportFormatter.format_datetime(record.time_out))

        first_width = max(len(value) for value in login_values)
        second_width = max(len(value) for value in time_in_values)
        third_width = max(len(value) for value in time_out_values)

        border = (
            "+"
            + "-" * (first_width + 2)
            + "+"
            + "-" * (second_width + 2)
            + "+"
            + "-" * (third_width + 2)
            + "+"
        )

        header = (
            "| "
            + login_values[0].ljust(first_width)
            + " | "
            + time_in_values[0].ljust(second_width)
            + " | "
            + time_out_values[0].ljust(third_width)
            + " |"
        )

        lines = [border, header, border]

        for index in range(1, len(login_values)):
            row = (
                "| "
                + login_values[index].ljust(first_width)
                + " | "
                + time_in_values[index].ljust(second_width)
                + " | "
                + time_out_values[index].ljust(third_width)
                + " |"
            )
            lines.append(row)

        lines.append(border)
        return "\n".join(lines) + "\n"

    @staticmethod
    def save(records: list, filename: str) -> None:
        report_text = ReportFormatter.build_table(records)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(report_text)


class SessionManager:
    """
    Управляет записями сессий и сохранением отчёта
    """

    def __init__(self):
        self._records = []
        self._current = None
        self.start_session("Guest")

    @property
    def records(self) -> list:
        return self._records

    @records.setter
    def records(self, value: list):
        if not isinstance(value, list):
            raise ValueError("records must be a list")
        self._records = value
        if self._records:
            self._current = self._records[-1]
        else:
            self._current = None

    @property
    def current(self) -> Optional[SessionRecord]:
        return self._current

    @current.setter
    def current(self, value: Optional[SessionRecord]):
        if value is not None and not isinstance(value, SessionRecord):
            raise ValueError("current must be SessionRecord or None")
        self._current = value

    def start_session(self, login: str) -> SessionRecord:
        record = SessionRecord(
            record_id=len(self._records) + 1,
            login=login,
            time_in=datetime.now(),
            time_out=None
        )
        self._records.append(record)
        self._current = record
        return record

    def set_login(self, login: str) -> None:
        if self._current is not None:
            self._current.login = login

    def end_session(self) -> None:
        if self._current is not None and self._current.time_out is None:
            self._current.time_out = datetime.now()

    def save_report(self, filename: str = "report.txt") -> None:
        self.end_session()
        ReportFormatter.save(self._records, filename)


class StyledColumn(ft.Column):
    """компонент 1: колонка с типовыми настройками"""

    def __init__(
        self,
        controls: list,
        alignment: Any = ft.MainAxisAlignment.START,
        horizontal_alignment: Any = ft.CrossAxisAlignment.START,
        spacing: float = 10,
        expand: bool = False
    ):
        super().__init__(
            controls=controls,
            alignment=alignment,
            horizontal_alignment=horizontal_alignment,
            spacing=spacing,
            expand=expand
        )


class StyledRow(ft.Row):
    """компонент 2: строка с типовыми настройками."""

    def __init__(
        self,
        controls: list,
        alignment: Any = ft.MainAxisAlignment.START,
        vertical_alignment: Any = ft.CrossAxisAlignment.CENTER,
        spacing: float = 10,
        expand: bool = False
    ):
        super().__init__(
            controls=controls,
            alignment=alignment,
            vertical_alignment=vertical_alignment,
            spacing=spacing,
            expand=expand
        )


class StyledContainer(ft.Container):
    """компонент 3 контейнер с рамкой и фоном"""

    def __init__(
        self,
        content: Any = None,
        bgcolor: Any = None,
        padding: float = 10,
        border_radius: float = 10,
        alignment: Any = None,
        expand: bool = False,
        visible: bool = True
    ):
        super().__init__(
            content=content,
            bgcolor=bgcolor,
            padding=padding,
            border_radius=border_radius,
            alignment=alignment,
            expand=expand,
            visible=visible
        )


class PrimaryButton(ft.FilledButton):
    """компонент 4: основная кнопка"""

    def __init__(self, label: str, on_click: Any = None):
        super().__init__(
            content=label,
            on_click=on_click
        )


class SecondaryButton(ft.OutlinedButton):
    """компонент 5: не основная кнопка"""

    def __init__(self, label: str, on_click: Any = None):
        super().__init__(
            content=label,
            on_click=on_click
        )


class InputField(ft.TextField):
    """компонент 6 поле ввода"""

    def __init__(
        self,
        label: str,
        value: str = "",
        expand: bool = False
    ):
        super().__init__(
            label=label,
            value=value,
            expand=expand
        )


class TaskCard(ft.Card):
    """Компонент 7 карточка задачи"""

    def __init__(self, content: Any):
        super().__init__(content=content)


class TaskList(ft.ListView):
    """компонент 8 прокручиваемый список задач"""

    def __init__(
        self,
        controls: list,
        spacing: float = 10,
        padding: float = 10,
        expand: bool = True
    ):
        super().__init__(
            controls=controls,
            spacing=spacing,
            padding=padding,
            expand=expand
        )


class TitleText(ft.Text):
    """компонент 9: текстовый заголовок"""

    def __init__(
        self,
        value: str,
        size: float = 16,
        color: Any = ft.Colors.BLACK
    ):
        super().__init__(
            value=value,
            size=size,
            color=color
        )


class SeparatorLine(ft.Divider):
    """компонент 10: разделитель"""

    def __init__(self):
        super().__init__()


class Application:
    """
    Главный класс приложения.
    Хранит состояние, строит UI и обрабатывает события.
    """

    def __init__(self, page: ft.Page):
        self._page = page
        self._session_manager = SessionManager()

        self._users_map = CustomMap()
        self._tasks_map = CustomMap()

        self._tasks = []
        self._users_set = set()

        self._report_saved = False

        self._login_input = None
        self._login_status_text = None
        self._login_section = None

        self._welcome_text = None
        self._title_input = None
        self._priority_input = None
        self._status_text = None
        self._task_list = None
        self._dashboard_section = None

        self._initialize_data()
        self._configure_page()
        self._build_ui()

        atexit.register(self._save_on_exit)

        self._page.update()


    @property
    def page(self) -> ft.Page:
        return self._page

    @page.setter
    def page(self, value: ft.Page):
        if not isinstance(value, ft.Page):
            raise ValueError("page must be ft.Page")
        self._page = value

    @property
    def session_manager(self) -> SessionManager:
        return self._session_manager

    @session_manager.setter
    def session_manager(self, value: SessionManager):
        if not isinstance(value, SessionManager):
            raise ValueError("session_manager must be SessionManager")
        self._session_manager = value

    @property
    def users_map(self) -> CustomMap:
        return self._users_map

    @users_map.setter
    def users_map(self, value: CustomMap):
        if not isinstance(value, CustomMap):
            raise ValueError("users_map must be CustomMap")
        self._users_map = value

    @property
    def tasks_map(self) -> CustomMap:
        return self._tasks_map

    @tasks_map.setter
    def tasks_map(self, value: CustomMap):
        if not isinstance(value, CustomMap):
            raise ValueError("tasks_map must be CustomMap")
        self._tasks_map = value

    @property
    def tasks(self) -> list:
        return self._tasks

    @tasks.setter
    def tasks(self, value: list):
        if not isinstance(value, list):
            raise ValueError("tasks must be a list")
        self._tasks = value


    def _initialize_data(self) -> None:
        """
        создает стартовые объекты
        """

        user_a = User(1, "StudentA")
        user_b = User(2, "StudentB")
        user_c = User(3, "TeacherC")

        self._users_map.put(user_a.get_id(), user_a)
        self._users_map.put(user_b.get_id(), user_b)
        self._users_map.put(user_c.get_id(), user_c)

        self._users_set.add(user_a)
        self._users_set.add(user_b)
        self._users_set.add(user_c)

        priorities = (5, 2, 8, 1, 9, 3, 7, 4, 10, 6)

        for index in range(10):
            task = Assignment(
                task_id=index + 1,
                title=f"Лабораторная работа №{index + 1}",
                priority=priorities[index],
                completed=(index % 3 == 0)
            )

            self._tasks.append(task)
            self._tasks_map.put(task.get_id(), task)

        self._tasks.sort(reverse=True)


    def _configure_page(self) -> None:
        self._page.title = "UniTrack OOP Project"
        self._page.window.width = 860
        self._page.window.height = 920

        self._page.on_close = self._on_page_close

    # построение интерфейса

    def _build_ui(self) -> None:
        self._build_login_section()
        self._build_dashboard_section()

        root = StyledColumn(
            controls=[
                self._login_section,
                self._dashboard_section
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=0,
            expand=True
        )

        self._page.add(root)

    def _build_login_section(self) -> None:
        self._login_input = InputField(
            label="Введите логин",
            value="",
            expand=True
        )

        self._login_status_text = TitleText(
            value="",
            size=14,
            color=ft.Colors.RED
        )

        login_button = PrimaryButton(
            label="Войти в систему",
            on_click=self._handle_login
        )

        login_column = StyledColumn(
            controls=[
                TitleText(
                    value="UniTrack",
                    size=36,
                    color=ft.Colors.BLUE
                ),
                TitleText(
                    value="Трекер учебных задач",
                    size=18,
                    color=ft.Colors.GREY_700
                ),
                SeparatorLine(),
                self._login_input,
                self._login_status_text,
                login_button
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=20,
            expand=False
        )

        self._login_section = StyledContainer(
            content=login_column,
            bgcolor=ft.Colors.GREY_100,
            padding=40,
            border_radius=14,
            alignment=ft.Alignment.CENTER,
            expand=True,
            visible=True
        )

    def _build_dashboard_section(self) -> None:
        self._welcome_text = TitleText(
            value="Дашборд",
            size=30,
            color=ft.Colors.BLACK
        )

        self._title_input = InputField(
            label="Название задачи",
            value="",
            expand=True
        )

        self._priority_input = InputField(
            label="Приоритет 1-10",
            value="5",
            expand=False
        )

        add_button = PrimaryButton(
            label="Добавить задачу",
            on_click=self._handle_add_task
        )

        add_row = StyledRow(
            controls=[
                self._title_input,
                self._priority_input,
                add_button
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            expand=True
        )

        add_container = StyledContainer(
            content=add_row,
            bgcolor=ft.Colors.GREY_200,
            padding=15,
            border_radius=10,
            expand=True
        )

        self._status_text = TitleText(
            value="",
            size=14,
            color=ft.Colors.BLUE
        )

        self._task_list = TaskList(
            controls=self._create_task_cards(),
            spacing=10,
            padding=10,
            expand=True
        )

        exit_button = SecondaryButton(
            label="Выйти и сохранить отчет",
            on_click=self._handle_exit
        )

        exit_row = StyledRow(
            controls=[exit_button],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=10,
            expand=False
        )

        dashboard_column = StyledColumn(
            controls=[
                self._welcome_text,
                SeparatorLine(),
                TitleText(
                    value="Добавить новую задачу",
                    size=20,
                    color=ft.Colors.BLACK
                ),
                add_container,
                self._status_text,
                TitleText(
                    value="Список задач",
                    size=20,
                    color=ft.Colors.BLACK
                ),
                self._task_list,
                exit_row
            ],
            alignment=ft.MainAxisAlignment.START,
            horizontal_alignment=ft.CrossAxisAlignment.STRETCH,
            spacing=15,
            expand=True
        )

        self._dashboard_section = StyledContainer(
            content=dashboard_column,
            bgcolor=ft.Colors.WHITE,
            padding=20,
            border_radius=14,
            expand=True,
            visible=False
        )


    def _handle_login(self, e: Any) -> None:
        login = ""

        if self._login_input.value is not None:
            login = self._login_input.value.strip()

        if not login:
            self._show_message("Введите логин!")
            return

        self._session_manager.set_login(login)
        self._welcome_text.value = f"Привет, {login}!"

        self._login_section.visible = False
        self._dashboard_section.visible = True

        self._show_message("Вход выполнен успешно.")
        self._page.update()

    def _handle_add_task(self, e: Any) -> None:
        title = ""
        priority_raw = ""

        if self._title_input.value is not None:
            title = self._title_input.value.strip()

        if self._priority_input.value is not None:
            priority_raw = self._priority_input.value.strip()

        if not title:
            self._show_message("Название задачи не может быть пустым.")
            return

        try:
            priority = int(priority_raw)
        except ValueError:
            self._show_message("Приоритет должен быть целым числом от 1 до 10.")
            return

        if priority < 1 or priority > 10:
            self._show_message("Приоритет должен быть от 1 до 10.")
            return

        task_id = self._next_task_id()

        task = Assignment(
            task_id=task_id,
            title=title,
            priority=priority,
            completed=False
        )

        self._tasks.append(task)
        self._tasks_map.put(task.get_id(), task)

        self._tasks.sort(reverse=True)

        self._title_input.value = ""
        self._priority_input.value = "5"

        self._refresh_task_list()
        self._show_message(f"Задача добавлена: {task.title}")

    def _handle_toggle_task(self, task_id: int, e: Any = None) -> None:
        task = self._tasks_map.get(task_id)

        if task is None:
            self._show_message("Задача не найдена.")
            return

        task.completed = not task.completed

        self._refresh_task_list()

        if task.completed:
            self._show_message(f"Задача отмечена выполненной: {task.title}")
        else:
            self._show_message(f"Задача возвращена в работу: {task.title}")

    async def _handle_exit(self, e: Any) -> None:
        self._finish_and_save()

        try:
            await self._page.window.destroy()
        except Exception:
            raise SystemExit

    def _on_page_close(self, e: Any = None) -> None:
        self._finish_and_save()

    def _save_on_exit(self) -> None:
        self._finish_and_save()


    def _next_task_id(self) -> int:
        last_id = 0

        for task in self._tasks:
            current_id = task.get_id()
            if current_id > last_id:
                last_id = current_id

        return last_id + 1

    def _refresh_task_list(self) -> None:
        if self._task_list is not None:
            self._task_list.controls = self._create_task_cards()
            self._page.update()

    def _create_task_cards(self) -> list:
        cards = []

        for task in self._tasks:
            status_text = "выполнено" if task.completed else "в работе"
            status_color = ft.Colors.GREEN if task.completed else ft.Colors.ORANGE

            info_column = StyledColumn(
                controls=[
                    TitleText(
                        value=task.title,
                        size=17,
                        color=ft.Colors.BLACK
                    ),
                    TitleText(
                        value=(
                            f"ID: {task.get_id()} | "
                            f"Приоритет: {task.priority} | "
                            f"Статус: {status_text}"
                        ),
                        size=12,
                        color=ft.Colors.GREY_700
                    )
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=4,
                expand=True
            )

            status_badge = StyledContainer(
                content=TitleText(
                    value=status_text,
                    size=12,
                    color=ft.Colors.WHITE
                ),
                bgcolor=status_color,
                padding=8,
                border_radius=20,
                alignment=ft.Alignment.CENTER,
                expand=False
            )

            toggle_label = (
                "Отметить выполненной"
                if not task.completed
                else "Вернуть в работу"
            )

            toggle_button = SecondaryButton(
                label=toggle_label,
                on_click=lambda event, tid=task.get_id(): self._handle_toggle_task(tid, event)
            )

            card_row = StyledRow(
                controls=[
                    info_column,
                    status_badge,
                    toggle_button
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
                expand=True
            )

            cards.append(TaskCard(content=card_row))

        return cards

    def _show_message(self, message: str) -> None:
        if self._login_section is not None and self._login_section.visible:
            if self._login_status_text is not None:
                self._login_status_text.value = message

        if self._status_text is not None:
            self._status_text.value = message

        self._page.update()

    def _finish_and_save(self) -> None:
        if not self._report_saved:
            self._session_manager.save_report("report.txt")
            self._report_saved = True



class AppRunner:
    @staticmethod
    def main(page: ft.Page) -> None:
        Application(page)


if __name__ == "__main__":
    ft.run(AppRunner.main)