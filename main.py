from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.core.window import Window

from kivy.uix.floatlayout import FloatLayout

import json

from random import *

from base import *

Window.size = (400, 700)

class GameScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # ← Сначала передаём kwargs
        self.orientation = 'vertical'

        self.current_player_index = 0

        self.padding = 20
        self.spacing = 15

        self.players_name = {}

        # 1. Заголовок (фиксированная высота)
        title = Label(text='БУНКЕР', size_hint_y=None, height=50, font_size='24sp')
        self.add_widget(title)

        # 2. Поле ввода
        self.input = TextInput(
            hint_text='Введите текст...',
            multiline=False,
            size_hint_y=None,
            height=50
        )
        self.add_widget(self.input)

        # 3. Кнопка добавить игроков
        player_button = Button(text='Добавить игрока', size_hint_y=None, height=50)
        player_button.bind(on_press=self.add_player)  # Привязка события
        self.add_widget(player_button)

        # 4. Информационная метка (занимает всё свободное место)
        self.info_label = Label(text='Добавьте игроков', font_size='18sp')
        self.info_label.bind(on_press=self.add_player,size=self.info_label.setter('text_size'))  # Перенос слов
        self.add_widget(self.info_label)

        # 5. Кнопка начала игры
        start_button = Button(text='Начать игру', size_hint_y=None, height=50)
        start_button.bind(on_press=self.start_game)  # Привязка события
        self.add_widget(start_button)

    def random_characteristic(self, name_player):
        self.players_name[name_player] = \
            {
                'Профессия': {'значение': choice(PROFESSION), 'flag': False},
                'Пол': {'значение': choice(SEX), 'flag': False},
                'Возраст': {'значение': randint(10, 120), 'flag': False},
                'Характеристики': {'значение': None, 'flag': False},
                'Ориентация': {'значение': None, 'flag': False},
                'Предмет': {'значение': None, 'flag': False}
             }

        if self.players_name[name_player]['Пол']['значение'] == 'Мужчина':
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY[1:])
        elif self.players_name[name_player]['Пол']['значение'] == 'Женщина':
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY[:-1])
        elif self.players_name[name_player]['Пол']['значение'] == 'Средний (на выбор)':
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY[1:-1])
        else:
            self.players_name[name_player]['Ориентация']['значение'] = choice(SEXUALITY)

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
            self.plot()

    def plot(self, instance=None):
        self.clear_widgets()

        self.plot = Label(text=choice(APOCALYPSE), font_size='15sp')
        self.plot.bind(size=self.plot.setter('text_size'))  # Перенос слов
        self.add_widget(self.plot)

        self.next_button = Button(text='Далее', size_hint_y=None, height=50)
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
            font_size='24sp',
            halign='center',
            valign='middle'
        )
        layout.add_widget(title)

        # BoxLayout для кнопок
        buttons_layout = BoxLayout(
            orientation='vertical',
            spacing=10,
            size_hint=(0.8, 1),  # Ширина 80%, высота 100%
            pos_hint={'top': 1.3, 'center_x': 0.5}  # Центрируем сам layout
        )

        # Создаём кнопки
        for players in self.players_name.keys():
            btn = Button(
                text=f'{players}',
                size_hint_y=None,
                height=50
            )
            btn.bind(on_press=lambda instance, name=players: self.player_turn(name))
            buttons_layout.add_widget(btn)

        layout.add_widget(buttons_layout)

        layout.move_button = Button(
            text='Раскрыть первую характеристику',
            size_hint_y=None,
            height=50,
            pos_hint={'top': 0.1, 'center_x': 0.5})
        layout.move_button.bind(on_press=self.move)
        layout.add_widget(layout.move_button)

        self.add_widget(layout)

    # просмотр характеристик
    def player_turn(self, name):
        self.clear_widgets()

        self.name_label = Label(text=name, font_size='18sp')
        self.add_widget(self.name_label)

        self.char_label = Label(text='', font_size='18sp')
        for param_name, param_data in self.players_name[name].items():
            value = param_data['значение']
            self.char_label.text += f"{param_name}: {value}\n"
        self.char_label.bind(size=self.char_label.setter('text_size'))
        self.add_widget(self.char_label)

        self.back_button = Button(text='Назад', size_hint_y=None, height=50)
        self.back_button.bind(on_press=self.main_game_interface)  # Привязка события
        self.add_widget(self.back_button)

    def move(self, instance):
        self.clear_widgets()

        players_list = list(self.players_name.keys())
        current_player = players_list[self.current_player_index]

        # Заголовок
        title = Label(text=f"Игрок: {current_player}", font_size='24sp')
        self.add_widget(title)

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
            if not self.players_name[current_player][characteristic]['flag']:
                btn = Button(
                    text=characteristic,
                    size_hint_y=None,
                    height=50
                )
                btn.bind(on_press=lambda inst, char=characteristic:
                self.show_characteristic(current_player, char))
                buttons_layout.add_widget(btn)

        self.add_widget(buttons_layout)

        # Кнопка "Далее" (появится когда все раскроют)
        # self.next_btn = Button(text='Далее', size_hint_y=None, height=50)
        # self.next_btn.bind(on_press=self.next_player)
        # self.next_btn.disabled = True  # Отключена пока не все раскрыто
        # self.add_widget(self.next_btn)

        # # Проверяем сколько раскрыто
        # self.check_all_revealed(current_player)

    def next_player(self, instance):
        """Переход к следующему игроку"""
        self.current_player_index += 1
        self.move(None)

    def show_characteristic(self, players, name):
        self.clear_widgets()

        self.characteristic_label = Label(text=str(self.players_name[players][name]['значение']), font_size='18sp')
        self.add_widget(self.characteristic_label)

        self.players_name[players][name]['flag'] = True
        self.current_player_index += 1

        if self.current_player_index >= len(self.players_name):
            self.next_btn = Button(text='Далее', size_hint_y=None, height=50)
            self.next_btn.bind(on_press=self.results)
            self.add_widget(self.next_btn)
        else:
            self.next_btn = Button(text='Далее', size_hint_y=None, height=50)
            self.next_btn.bind(on_press=self.move)
            self.add_widget(self.next_btn)

    def results(self, instance):
        self.clear_widgets()

        for name in self.players_name.keys():
            player_row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=120,  # Уменьшили высоту строки
                spacing=5
            )

            # Левая часть - информация об игроке
            info_layout = BoxLayout(
                orientation='vertical',
                size_hint_x=0.8,
                spacing=2  # Минимальный отступ
            )

            # Имя игрока
            self.name_label = Label(
                text=name,
                font_size='10sp',  # Уменьшили шрифт
                size_hint_y=None,
                height=13,  # Уменьшили высоту
                halign='center',
                valign='middle',
                bold=True
            )
            info_layout.add_widget(self.name_label)

            # Характеристики
            self.char_label = ''
            for param_name, param_data in self.players_name[name].items():
                if param_data['flag']:
                    value = param_data['значение']
                    self.char_label += f"{param_name}: {value}\n"
                else:
                    self.char_label += f"{param_name}: ???\n"

            self.char_l = Label(
                text=self.char_label,
                font_size='8sp',  # Маленький шрифт
                size_hint_y=None,
                height=80,  # Фиксированная высота для характеристик
                halign='left',
                valign='top'
            )

            self.char_l.bind(size=self.char_l.setter('text_size'))
            info_layout.add_widget(self.char_l)

            # Добавляем info_layout в строку
            player_row.add_widget(info_layout)

            # Правая часть - кнопка удаления
            delete_btn = Button(
                text='X',  # Вместо "Удалить" просто крестик
                size_hint_x=0.2,
                size_hint_y=None,
                height=60,
                background_color=(1, 0, 0, 1),
                font_size='14sp'  # Красная кнопка
            )
            delete_btn.bind(on_press=lambda inst, player_name=name: self.delete_player(player_name))
            player_row.add_widget(delete_btn)

            # Добавляем строку с игроком на экран
            self.add_widget(player_row)

        self.next_button = Button(text='Оставить всех', size_hint_y=None, height=30)
        self.next_button.bind(on_press=self.index)
        self.add_widget(self.next_button)

    def delete_player(self, name):

        self.clear_widgets()

        self.name_label = Label(text=name, font_size='18sp')
        self.add_widget(self.name_label)

        self.char_label = Label(text='', font_size='18sp')
        for param_name, param_data in self.players_name[name].items():
            value = param_data['значение']
            self.char_label.text += f"{param_name}: {value}\n"
        self.char_label.bind(size=self.char_label.setter('text_size'))
        self.add_widget(self.char_label)

        del self.players_name[name]

        if len(self.players_name) == 2:
            self.next_button = Button(text='Далее', size_hint_y=None, height=50)
            self.next_button.bind(on_press=self.end_game)
            self.add_widget(self.next_button)
        else:
            self.next_button = Button(text='Далее', size_hint_y=None, height=50)
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
            pos_hint={'top': 1, 'center_x': 0.5},
            font_size='24sp',
            halign='center',
            valign='middle'
        )
        layout.add_widget(title)

        players_list = list(self.players_name.keys())

        # Выводим первых 2 победителей
        text = 'ПОБЕДИЛИ:\n' + players_list[0] + '\n' + players_list[1]

        winners = Label(
            text=text,
            size_hint=(1, 0.1),
            pos_hint={'top': 0.8, 'center_x': 0.5},
            font_size='24sp',
            halign='center',
            valign='middle'
        )
        layout.add_widget(winners)
        self.add_widget(layout)

class BunkerApp(App):
    def build(self):
        return GameScreen()


BunkerApp().run()
