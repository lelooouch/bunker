from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.scrollview import ScrollView
from kivy.core.text import LabelBase
from kivy.graphics import Rectangle
from kivy.clock import Clock
from kivy.uix.image import Image

img_path = '/data/data/org.test.myapp/files/app/'

LabelBase.register(name='Big', fn_regular='fonts/DreiFraktur.ttf')
LabelBase.register(name='Small', fn_regular='fonts/Mason Sans.ttf')
LabelBase.register(name='Btn', fn_regular='fonts/Monomakh-Regular.ttf')
LabelBase.register(name='X', fn_regular='fonts/Blaka-Regular.ttf')

from random import *

from base import *

Window.size = (400, 700)

class GameScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # ← Сначала передаём kwargs
        self.orientation = 'vertical'

        with self.canvas.before:
            self.bg = Rectangle(source='pic/bg_dark.jpg', pos=self.pos, size=self.size)

        #  Обновляем фон при изменении позиции и размера
        self.bind(pos=self.update_bg, size=self.update_bg)

        #  Обновляем фон после загрузки (через 0.1 сек)
        Clock.schedule_once(self.update_bg, 0.1)

        self.current_player_index = 0

        self.padding = 20
        self.spacing = 15

        self.players_name = {}

        # 1. Заголовок (фиксированная высота)
        title = Label(text='БУНКЕР', size_hint_y=None, height=50, font_size='30sp', font_name='Big')
        self.add_widget(title)

        # 2. Поле ввода
        self.input = TextInput(
            hint_text='Введите текст...',
            font_name='Small',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.input)

        self.background_color = [0, 0, 0, 0]

        # 3. Кнопка добавить игроков
        player_button = Button(
            text='ДОБАВИТЬ ИГРОКА',
            font_name='Btn',
            font_size='20sp',
            size_hint_y=None,
            height=50,
            size_hint_x=None,  # ← Важно: не растягивать по ширине
            width=350,  # ← Важно: задать явную ширину
            background_normal='pic/btn.png',
            #background_down=img_path,
            background_color=[1, 1, 1, 1],  # Не закрашивать картинку
            color=[1, 1, 1, 1],  # Цвет текста
            border=(0, 0, 0, 0)  # Убрать стандартную рамку
        )
        player_button.bind(on_press=self.add_player)  # Привязка события
        self.add_widget(player_button)

        # 4. Информационная метка (занимает всё свободное место)
        self.info_label = Label(text='Добавьте игроков', font_name='Small', font_size='24sp')
        self.info_label.bind(on_press=self.add_player,size=self.info_label.setter('text_size'))  # Перенос слов
        self.add_widget(self.info_label)

        # 5. Кнопка начала игры
        start_button = Button(
            text='НАЧАТЬ ИГРУ',
            font_name='Btn',
            font_size='24sp',
            size_hint_y=None,
            border=(0, 0, 0, 0),
            height=50,
            background_color=[0.2, 0.4, 0.8, 1])
        start_button.bind(on_press=self.start_game)  # Привязка события
        self.add_widget(start_button)

    def update_bg(self, *args):
        """Обновление фона при изменении размера"""
        self.bg.pos = self.pos
        self.bg.size = self.size

    def random_characteristic(self, name_player):
        self.players_name[name_player] = \
            {
                'Профессия': {'значение': choice(PROFESSION), 'flag': False},
                'Пол': {'значение': choice(SEX), 'flag': False},
                'Возраст': {'значение': min(randint(10, 120), randint(10, 120),), 'flag': False},
                'Характеристики': {'значение': None, 'flag': False},
                'Ориентация': {'значение': None, 'flag': False},
                'Предмет': {'значение': None, 'flag': False},
                'img': None
             }

        if self.players_name[name_player]['Пол']['значение'] == 'Мужчина':
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY[1:])
            self.players_name[name_player]['img'] = f'pic/man/{randint(1, 13)}.png'
        elif self.players_name[name_player]['Пол']['значение'] == 'Женщина':
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY[:-1])
            self.players_name[name_player]['img'] = f'pic/woman/{randint(1, 9)}.png'
        elif self.players_name[name_player]['Пол']['значение'] == 'Средний (на выбор)':
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY[1:-1])
            self.players_name[name_player]['img'] = f'pic/{choice(["woman", "man"])}/{randint(1, 9)}.png'
        else:
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY)

        if self.players_name[name_player]['Пол']['значение'] == 'Транс (из мужика в женщину)':
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY[1:])
            self.players_name[name_player]['img'] = f'pic/woman/{randint(1, 9)}.png'
        elif self.players_name[name_player]['Пол']['значение'] == 'Транс (из женщины в мужика)':
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY[1:])
            self.players_name[name_player]['img'] = f'pic/man/{randint(1, 13)}.png'


        return self.players_name

    def add_player(self, instance):
        if self.input.text:
            self.random_characteristic(self.input.text)
            l = [str(gamers) for gamers in self.players_name.keys()]
            self.info_label.text = 'Игроки:\n' + '\n'.join(l)

    def start_game(self, instance):
        if len(self.players_name) < 3:
            self.info_label.text = 'Для начала добавте минимум 3-х игроков.'
        else:
            self.start_plot()

    def start_plot(self, instance=None):
        self.clear_widgets()

        self.plot = Label(
            text=choice(APOCALYPSE),
            font_name='Small',
            font_size='28sp',
            halign='center',  # Горизонтальное выравнивание
            valign='middle',  # Вертикальное выравнивание
            size_hint=(1, 1),  # Занимает всю доступную область
            pos_hint={'center_x': 0.5, 'center_y': 0.5}  # Позиционирование по центру
        )
        self.plot.bind(size=self.plot.setter('text_size'))  # Перенос слов
        self.plot.bind(texture_size=self.plot.setter('size'))  # Адаптация размера
        self.add_widget(self.plot)

        self.next_button = Button(
            text='Далее',
            font_name='Btn',
            font_size='24sp',
            size_hint_y=None,
            border=(0, 0, 0, 0),
            height=50,
            background_color=[0.2, 0.4, 0.8, 1])
        self.next_button.bind(on_press=self.main_game_interface)
        self.add_widget(self.next_button)

    # характеристики
    def main_game_interface(self, instance=None):

        # Очищаем все виджеты
        self.clear_widgets()

        # Создаём все виджеты
        layout = FloatLayout()

        # Надпись в самом верху
        title = Label(
            text='ИГРА НАЧАЛАСЬ',
            size_hint=(1, 0.1),
            pos_hint={'top': 1, 'center_x': 0.5},
            font_size='30sp',
            halign='center',
            valign='middle',
            font_name='Big'
        )
        layout.add_widget(title)

        poisn = Label(
            text='Посмотрите свои роли',
            size_hint=(1, 0.1),
            pos_hint={'top': 0.85, 'center_x': 0.5},
            font_size='24sp',
            halign='center',
            valign='middle',
            font_name='Small'
        )
        layout.add_widget(poisn)

        # BoxLayout для кнопок
        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(0.8, 1),  # Ширина 80%, высота 100%
            pos_hint={'top': 1.2, 'center_x': 0.5}  # Центрируем сам layout
        )

        # Создаём кнопки
        for players in self.players_name.keys():
            btn = Button(
                text=f'{players}',
                size_hint_y=None,
                height=50,
                font_name='Small',
                background_color = [0.5, 0.25, 0.25, 0.9],
                border=(10, 10, 10, 10)
            )
            btn.bind(on_press=lambda instance, name=players: self.player_turn(name))
            buttons_layout.add_widget(btn)

        layout.add_widget(buttons_layout)

        layout.move_button = Button(
            text='Раскрыть первую характеристику',
            size_hint_y=None,
            height=50,
            font_name='Small',
            pos_hint={'top': 0.1, 'center_x': 0.5},
            background_color=[0.2, 0.4, 0.8, 1],
            border=(0, 0, 0, 0)
        )
        layout.move_button.bind(on_press=self.move)
        layout.add_widget(layout.move_button)

        self.add_widget(layout)

    # просмотр характеристик
    def player_turn(self, name):
        self.clear_widgets()

        self.name_label = Label(
            text=name,
            font_size='24sp',
            font_name='Big',
            size_hint = (1, 0.1),
            pos_hint = {'top': 1.2, 'center_x': 0.5},
            halign = 'center',
            valign = 'middle'
        )
        self.add_widget(self.name_label)

        img = Image(
            source=self.players_name[name]['img'],
            size_hint=(None, None),  # Фиксированный размер
            size=(200, 300),  # Ширина и высота в пикселях
            pos_hint={'center_x': 0.5, 'y': 0.15}  # По центру, на 15% от низа
        )
        self.add_widget(img)

        self.char_label = Label(
            text='',
            font_size='18sp',
            font_name='Small',
            pos_hint={'top': 0.7,'center_x': 0.5},
            halign='center',
            valign='middle')
        for param_name, param_data in self.players_name[name].items():
            if param_name != 'img':
                value = param_data['значение']
                self.char_label.text += f"{param_name}: {value}\n"
        self.char_label.bind(size=self.char_label.setter('text_size'))
        self.add_widget(self.char_label)

        self.back_button = Button(
            text='Назад',
            size_hint_y=None,
            height=50,
            font_name='Btn',
            font_size='24sp',
            border=(0, 0, 0, 0),
            background_color=[0.2, 0.4, 0.8, 1]
        )
        self.back_button.bind(on_press=self.main_game_interface)
        self.add_widget(self.back_button)

    def move(self, instance):
        self.clear_widgets()

        players_list = list(self.players_name.keys())
        current_player = players_list[self.current_player_index]

        # Заголовок
        title = Label(
            text=f"Игрок:\n{current_player}",
            font_size='28sp',
            font_name='Big',
            color=[0.039, 0.063, 0.118, 1],
            halign='center',  # ← По горизонтали
            valign='middle'
        )
        self.add_widget(title)

        layout = FloatLayout()

        # Картинка с точными координатами
        img = Image(
            source=self.players_name[current_player]['img'],
            size_hint=(None, None),
            size=(150, 250),
            pos_hint={'center_x': 0.5, 'center_y': 0.7}  # 70% высоты экрана
        )
        layout.add_widget(img)
        self.add_widget(layout)

        # Метка для показа раскрытых характеристик
        self.char_label = Label(text='', font_size='18sp')
        self.add_widget(self.char_label)

        # Контейнер для кнопок
        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(0.8, 1),
            pos_hint={'center_x': 0.5}
        )

        for characteristic in self.players_name[current_player].keys():
            if characteristic != 'img':
                if not self.players_name[current_player][characteristic]['flag']:
                    btn = Button(
                        text=characteristic,
                        size_hint_y=None,
                        height=50,
                        font_name = 'Small',
                        background_color = [0.5, 0.25, 0.25, 0.9],
                        border = (10, 10, 10, 10)
                    )
                    btn.bind(on_press=lambda inst, char=characteristic:
                    self.show_characteristic(current_player, char))
                    buttons_layout.add_widget(btn)

        self.add_widget(buttons_layout)

    def next_player(self, instance):
        """Переход к следующему игроку"""
        self.current_player_index += 1
        self.move(None)

    def show_characteristic(self, players, name):
        self.clear_widgets()

        self.characteristic_label = Label(
            text=str(self.players_name[players][name]['значение']),
            font_size='24sp',
            font_name='Small')
        self.add_widget(self.characteristic_label)

        self.players_name[players][name]['flag'] = True
        self.current_player_index += 1

        self.next_btn = Button(
            text='Далее',
            size_hint_y=None,
            height=50,
            font_name='Btn',
            font_size='24sp',
            border=(0, 0, 0, 0),
            background_color=[0.2, 0.4, 0.8, 1]
        )

        if self.current_player_index >= len(self.players_name):
            self.next_btn.bind(on_press=self.results)
            self.add_widget(self.next_btn)
        else:
            self.next_btn.bind(on_press=self.move)
            self.add_widget(self.next_btn)

    def results(self, instance):
        self.clear_widgets()

        # Создаём ScrollView
        scroll = ScrollView(size_hint=(1, 1))

        # Главный контейнер для всех игроков
        main_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=10,
            padding=10  # Увеличили padding
        )
        main_layout.bind(minimum_height=main_layout.setter('height'))

        for name in self.players_name.keys():
            player_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=180,  # Увеличили высоту
                spacing=10
            )

            # Левая часть - информация об игроке
            info_layout = BoxLayout(
                orientation='vertical',
                size_hint_x=0.9,  # 90% ширины (было 1)
                spacing=5,
                padding=10  # Добавили отступы внутри
            )

            # Имя игрока - БОЛЬШЕ
            name_label = Label(
                text=name,
                font_size='24sp',  # Увеличили (было 14sp)
                size_hint_y=None,
                height=35,  # Увеличили
                halign='left',  # Выравнивание по левому краю
                valign='middle',
                bold=True,
                font_name='Big'
            )
            info_layout.add_widget(name_label)

            # Характеристики - БОЛЬШЕ
            char_text = ''
            for param_name, param_data in self.players_name[name].items():
                if param_name != 'img':
                    if param_data['flag']:
                        value = param_data['значение']
                    else:
                        value = '???'
                    char_text += f"{param_name}: {value}\n"

            char_label = Label(
                text=char_text,
                font_size='16sp',  # Увеличили (было 12sp)
                size_hint_y=None,
                halign='left',
                valign='top',
                font_name='Small'
            )
            char_label.bind(texture_size=char_label.setter('size'))
            info_layout.add_widget(char_label)

            player_row.add_widget(info_layout)

            # Кнопка удаления - МЕНЬШЕ
            delete_btn = Button(
                text='X',
                size_hint_x=0.15,  # Уменьшили (было 0.15)
                size_hint_y=None,
                height=180,
                background_color=[0, 0, 0, 0],
                font_size='30sp',
                color = [1,0,0,1],
                font_name='X'
            )
            delete_btn.bind(on_press=lambda inst, player_name=name: self.delete_player(player_name))
            player_row.add_widget(delete_btn)

            main_layout.add_widget(player_row)

        # Кнопка "Оставить всех"
        next_button = Button(
            text='Оставить всех',
            size_hint_y=None,
            height=50,
            border=(0, 0, 0, 0),
            background_color=[0.2, 0.4, 0.8, 1],
            font_name='Btn',
            font_size='24sp'
        )
        next_button.bind(on_press=self.index)
        main_layout.add_widget(next_button)

        # Добавляем layout в ScrollView
        scroll.add_widget(main_layout)
        self.add_widget(scroll)

    def delete_player(self, name):

        self.clear_widgets()

        self.name_label = Label(text=name, font_size='28sp', font_name='Big')
        self.add_widget(self.name_label)

        self.char_label = Label(
            text='',
            font_size='18sp',
            font_name='Small',
            halign='center',  # ← По горизонтали
            valign='middle'
        )
        for param_name, param_data in self.players_name[name].items():
            if param_name != 'img':
                value = param_data['значение']
                self.char_label.text += f"{param_name}: {value}\n"
        self.char_label.bind(size=self.char_label.setter('text_size'))
        self.add_widget(self.char_label)

        del self.players_name[name]
        self.next_button = Button(
            text='Далее',
            size_hint_y=None,
            height=50,
            border=(0, 0, 0, 0),
            background_color=[0.2, 0.4, 0.8, 1],
            font_name='Btn')

        if len(self.players_name) == 2:
            self.next_button.bind(on_press=self.end_game)
            self.add_widget(self.next_button)
        else:
            self.next_button.bind(on_press=self.index)
            self.add_widget(self.next_button)

    def index(self, instance):
        self.current_player_index = 0
        self.move(None)

    def end_game(self, instance):
        self.clear_widgets()

        layout = FloatLayout()

        # Надпись в самом верху
        title = Label(
            text='КОНЕЦ ИГРЫ',
            size_hint=(1, 0.1),
            pos_hint={'top': 0.8, 'center_x': 0.5},
            font_size='30sp',
            halign='center',
            valign='middle',
            font_name='Big'
        )
        layout.add_widget(title)

        players_list = list(self.players_name.keys())

        # Выводим первых 2 победителей
        text = '\nПОБЕДИЛИ:\n' + '\n' + players_list[0] + '\n' + '\n' + players_list[1]

        winners = Label(
            text=text,
            size_hint=(1, 0.1),
            pos_hint={'top': 0.6, 'center_x': 0.5},
            font_size='28sp',
            halign='center',
            valign='middle',
            font_name='Big'
        )
        layout.add_widget(winners)
        self.add_widget(layout)


class BunkerApp(App):
    def build(self):
        return GameScreen()


BunkerApp().run()