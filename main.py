import flet as ft
from models import Task, MyMap, SessionManager


class BoxCol(ft.Column):
    def __init__(self, ctrls, align=ft.MainAxisAlignment.START, h_align=ft.CrossAxisAlignment.START, sp=10):
        super().__init__(controls=ctrls, alignment=align, horizontal_alignment=h_align, spacing=sp, expand=True)


class LineRow(ft.Row):
    def __init__(self, ctrls, align=ft.MainAxisAlignment.SPACE_BETWEEN, sp=10):
        super().__init__(controls=ctrls, alignment=align, vertical_alignment=ft.CrossAxisAlignment.CENTER, spacing=sp)


class MainBtn(ft.FilledButton):
    def __init__(self, txt, cb):
        super().__init__(content=txt, on_click=cb)


class SecBtn(ft.OutlinedButton):
    def __init__(self, txt, cb):
        super().__init__(content=txt, on_click=cb)


class InputTxt(ft.TextField):
    def __init__(self, lbl, val=""):
        super().__init__(label=lbl, value=val)


class CardItem(ft.Card):
    def __init__(self, cont):
        super().__init__(content=cont)


class ScrollList(ft.ListView):
    def __init__(self, items):
        super().__init__(controls=items, spacing=5, padding=10, expand=True)


class HeadText(ft.Text):
    def __init__(self, txt, sz=20, col=ft.Colors.BLACK):
        super().__init__(value=txt, size=sz, color=col, weight=ft.FontWeight.BOLD)


class DivLine(ft.Divider):
    def __init__(self):
        super().__init__()


class BadgeBox(ft.Container):
    def __init__(self, txt, bg_col):
        super().__init__(
            content=HeadText(txt, 12, ft.Colors.WHITE),
            bgcolor=bg_col,
            padding=8, 
            border_radius=10,
            alignment=ft.Alignment.CENTER
        )


class AppLogic:
    def __init__(self, page: ft.Page):
        self.pg = page
        self.map_tasks = MyMap()      
        self.list_tasks = []          
        self.session_mgr = SessionManager()
        
        self._init_data()
        self._setup_page()
        self._build_ui()
        
        self.pg.window.prevent_close = True
        self.pg.window.on_event = self._on_window_close

    def _init_data(self):
        names = ["Лаба", "Реферат", "ДЗ", "Тест", 
                 "Практика", "Эссе", "Проект", "Отчет", 
                 "Подготовка", "Чтение"]
        prios = [5, 8, 2, 9, 1, 7, 4, 6, 10, 3]
        
        for i in range(10):
            t = Task(i+1, names[i], prios[i])
            if i % 3 == 0:
                t.done = True
            
            self.map_tasks.set_item(t.get_id(), t)
            self.list_tasks.append(t)
            
        self.list_tasks.sort()

    def _setup_page(self):
        self.pg.title = "UniTrack OOP"
        self.pg.window.width = 600
        self.pg.window.height = 800
        self.pg.alignment = ft.Alignment.CENTER

    def _build_ui(self):
        self.input_login = InputTxt("Введите логин")
        btn_enter = MainBtn("Войти", self.handle_login)
        
        login_view = BoxCol([
            HeadText("UniTrack System", 30, ft.Colors.BLUE),
            DivLine(),
            self.input_login,
            btn_enter
        ], align=ft.MainAxisAlignment.CENTER, h_align=ft.CrossAxisAlignment.CENTER)
        
        self.container_main = ft.Container(content=login_view, expand=True, bgcolor=ft.Colors.GREY_100)
        self.pg.add(self.container_main)

    def handle_login(self, e):
        val = self.input_login.value.strip()
        if not val:
            self.show_snack("Введите имя!")
            return
        
        self.session_mgr.set_user(val)
        self.build_dashboard()

    def build_dashboard(self):
        self.pg.clean()
        
        self.inp_name = InputTxt("Название задачи")
        self.inp_prio = InputTxt("Приоритет (1-10)", "5")
        btn_add = MainBtn("+ Добавить", self.handle_add_task)
        
        form_row = LineRow([self.inp_name, self.inp_prio, btn_add])
        form_cont = ft.Container(content=form_row, padding=10, bgcolor=ft.Colors.WHITE)
        
        self.task_list_ctrl = ScrollList(self.render_cards())
        
        btn_exit = SecBtn("Выход и отчет", self.handle_exit)
        
        dash_col = BoxCol([
            HeadText(f"Привет, {self.session_mgr.user_login}", 24),
            DivLine(),
            form_cont,
            self.task_list_ctrl,
            btn_exit
        ])
        
        self.pg.add(dash_col)
        self.pg.update()

    def render_cards(self):
        cards = []
        for task in self.list_tasks:
            stat_txt = "Сделана" if task.done else "Активна"
            stat_col = ft.Colors.GREEN if task.done else ft.Colors.ORANGE
            badge = BadgeBox(stat_txt, stat_col)
            
            info_col = BoxCol([
                HeadText(task.name, 16),
                ft.Text(f"ID: {task.id} | Prio: {task.priority}", size=12, color=ft.Colors.GREY_600)
            ], sp=2)
            
            btn_toggle = SecBtn("Поменять", lambda ev, tid=task.id: self.toggle_status(tid))
            
            row_content = LineRow([info_col, badge, btn_toggle])
            card = CardItem(row_content)
            cards.append(card)
            
        return cards

    def handle_add_task(self, e):
        name = self.inp_name.value.strip()
        prio_str = self.inp_prio.value.strip()
        
        if not name:
            self.show_snack("Название обязательно")
            return
            
        try:
            prio = int(prio_str)
        except:
            self.show_snack("Приоритет должен быть числом")
            return
            
        new_id = len(self.list_tasks) + 100 
        new_task = Task(new_id, name, prio)
        
        self.map_tasks.set_item(new_id, new_task)
        self.list_tasks.append(new_task)
        self.list_tasks.sort() 
        
        self.task_list_ctrl.controls = self.render_cards()
        self.inp_name.value = ""
        self.inp_prio.value = "5"
        self.pg.update()
        self.show_snack("Задача добавлена")

    def toggle_status(self, task_id):
        task = self.map_tasks.get_item(task_id)
        if task:
            task.done = not task.done
            self.task_list_ctrl.controls = self.render_cards()
            self.pg.update()

    def show_snack(self, msg):
        sb = ft.SnackBar(ft.Text(msg))
        self.pg.overlay.append(sb)
        sb.open = True
        self.pg.update()

    def handle_exit(self, e):
        self.save_report()
        self.pg.window.destroy()

    def _on_window_close(self, e):
        if e.type == ft.WindowEventType.CLOSE:
            self.save_report()
            self.pg.window.destroy()

    def save_report(self):
        self.session_mgr.save_to_file("report.txt")


def main(page: ft.Page):
    app = AppLogic(page)

if __name__ == "__main__":
    ft.run(main)