import kivy
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.properties import NumericProperty, StringProperty, ObjectProperty, ListProperty
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.core.audio import SoundLoader
from kivy.lang import Builder
import random
import numpy as np
import tempfile
import wave 

# --- Se Carga el Diseño de la Interfaz (.kv) como un string ---
KV_STRING = """
#:kivy 2.1.0

<MenuScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 10

        Label:
            id: menu_title
            text: 'Configura tu Juego'
            font_size: '24sp'
            size_hint_y: 0.15

        GridLayout:
            cols: 2
            rows: 2
            size_hint_y: None
            height: '90dp'
            spacing: 10
            
            Label:
                text: 'Nº de Preguntas:'
                font_size: '18sp'
            TextInput:
                id: questions_input
                text: '20'  # CAMBIO: Valor por defecto a 20
                font_size: '18sp'
                multiline: False
                input_filter: 'int'

            Label:
                text: 'Tiempo por Respuesta (s):'
                font_size: '18sp'
            TextInput:
                id: time_input
                text: '12'  # CAMBIO: Valor por defecto a 12
                font_size: '18sp'
                multiline: False
                input_filter: 'float'

        Label:
            text: 'Elige las tablas que quieres practicar'
            font_size: '20sp'
            size_hint_y: 0.15

        GridLayout:
            id: grid_tablas
            cols: 4
            rows: 2
            spacing: 10
            
            ToggleButton:
                text: 'Tabla del 2'
            ToggleButton:
                text: 'Tabla del 3'
            ToggleButton:
                text: 'Tabla del 4'
            ToggleButton:
                text: 'Tabla del 5'
            ToggleButton:
                text: 'Tabla del 6'
            ToggleButton:
                text: 'Tabla del 7'
            ToggleButton:
                text: 'Tabla del 8'
            ToggleButton:
                text: 'Tabla del 9'
        
        Button:
            text: '¡A Jugar!'
            font_size: '20sp'
            size_hint_y: 0.2
            background_color: (0.2, 0.8, 0.4, 1)
            on_press: root.start_game_with_selection()


<GameScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10

        BoxLayout:
            size_hint_y: 0.1
            Label:
                text: f"Correctas: {root.correct_answers}"
                color: (0, 1, 0, 1)
            Label:
                text: f"Incorrectas: {root.incorrect_answers}"
                color: (1, 0, 0, 1)

        Label:
            text: root.question_text
            font_size: '40sp'
            size_hint_y: 0.35
        
        Label:
            text: root.user_answer_text
            font_size: '30sp'
            size_hint_y: 0.25
            
        ProgressBar:
            max: root.time_per_question
            value: root.time_left
            size_hint_y: None
            height: '10dp'

        GridLayout:
            cols: 3
            spacing: 5
            
            Button:
                text: '7'
                on_press: root.handle_button_press('7')
            Button:
                text: '8'
                on_press: root.handle_button_press('8')
            Button:
                text: '9'
                on_press: root.handle_button_press('9')
            Button:
                text: '4'
                on_press: root.handle_button_press('4')
            Button:
                text: '5'
                on_press: root.handle_button_press('5')
            Button:
                text: '6'
                on_press: root.handle_button_press('6')
            Button:
                text: '1'
                on_press: root.handle_button_press('1')
            Button:
                text: '2'
                on_press: root.handle_button_press('2')
            Button:
                text: '3'
                on_press: root.handle_button_press('3')
            Button:
                text: 'Borrar'
                on_press: root.handle_button_press('Borrar')
            Button:
                text: '0'
                on_press: root.handle_button_press('0')
            Button:
                text: 'Enter'
                on_press: root.handle_button_press('Enter')
                background_color: (0.2, 0.6, 1, 1)


<ScoreScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        
        Label:
            text: root.final_score_text
            font_size: '28sp'
            halign: 'center'

        Button:
            text: 'Jugar de Nuevo'
            size_hint_y: 0.2
            on_press: root.play_again()
"""
Builder.load_string(KV_STRING)

# --- Funciones para generar sonidos ---
def generate_sound(frequency=440, duration=0.2, sample_rate=22050):
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    amplitude = int(0.5 * np.iinfo(np.int16).max)
    wav_data = (amplitude * np.sin(2 * np.pi * frequency * t)).astype(np.int16)

    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            fname = tmp.name
        with wave.open(fname, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(wav_data.tobytes())

        return SoundLoader.load(fname)
    except Exception as e:
        print(f"Error al generar o cargar el sonido: {e}")
        return None

# --- Pantalla del Menú Principal ---
class MenuScreen(Screen):
    def start_game_with_selection(self):
        selected_tables = []
        for button in self.ids.grid_tablas.children:
            if isinstance(button, ToggleButton) and button.state == 'down':
                table_number = int(button.text.split()[-1])
                selected_tables.append(table_number)

        try:
            num_questions = int(self.ids.questions_input.text)
            time_per_q = float(self.ids.time_input.text)
            if num_questions <= 0 or time_per_q <= 0:
                self.ids.menu_title.text = "Los valores deben ser mayores a 0"
                return
            self.manager.app.total_questions_config = num_questions
            self.manager.app.time_per_question_config = time_per_q
        except (ValueError, TypeError):
            self.ids.menu_title.text = "Valores de configuración inválidos"
            return

        if selected_tables:
            self.manager.app.selected_tables = selected_tables
            self.manager.current = 'game'
            self.ids.menu_title.text = 'Configura tu Juego'
        else:
            self.ids.menu_title.text = "¡Debes elegir al menos una tabla!"

# --- Pantalla del Juego ---
class GameScreen(Screen):
    total_questions = NumericProperty(0)
    time_per_question = NumericProperty(0)
    correct_answers = NumericProperty(0)
    incorrect_answers = NumericProperty(0)
    question_text = StringProperty('')
    user_answer_text = StringProperty('')
    current_question_number = 0
    timer_event = None
    time_left = NumericProperty(0)
    last_question = None
    question_counts = {}
    failed_questions = []

    def on_enter(self, *args):
        self.total_questions = self.manager.app.total_questions_config
        self.time_per_question = self.manager.app.time_per_question_config
        self.start_game()
        Window.bind(on_key_down=self._on_keyboard_down)

    def on_leave(self, *args):
        Window.unbind(on_key_down=self._on_keyboard_down)
        self.stop_timer()

    def start_game(self):
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.current_question_number = 0
        self.last_question = None
        self.question_counts = {}
        self.failed_questions = []
        self.next_question()

    def next_question(self):
        self.stop_timer()
        self.user_answer_text = ''
        
        if self.current_question_number >= self.total_questions:
            self.end_game()
            return

        self.current_question_number += 1
        
        question_to_ask = None
        ask_failed_one = self.failed_questions and random.random() < 0.4

        if ask_failed_one:
            question_to_ask = self.failed_questions.pop(0)
        else:
            attempts = 0
            while attempts < 50:
                factor1 = random.choice(self.manager.app.selected_tables)
                # CAMBIO: El rango ahora es de 2 a 9
                factor2 = random.randint(2, 9)
                new_question = (factor1, factor2)
                is_last = (new_question == self.last_question)
                count = self.question_counts.get(new_question, 0)
                is_over_limit = (count >= 2)
                if not is_last and not is_over_limit:
                    question_to_ask = new_question
                    break
                attempts += 1
            
            if not question_to_ask:
                factor1 = random.choice(self.manager.app.selected_tables)
                factor2 = random.randint(2, 9)
                question_to_ask = (factor1, factor2)
                if question_to_ask == self.last_question:
                    # CAMBIO: Lógica de fallback ajustada al nuevo rango
                    factor2 = (factor2 % 8) + 2 
                    question_to_ask = (factor1, factor2)
        
        self.factor1, self.factor2 = question_to_ask
        self.correct_result = self.factor1 * self.factor2
        self.question_text = f"{self.factor1} x {self.factor2} = ?"
        self.last_question = question_to_ask
        self.question_counts[question_to_ask] = self.question_counts.get(question_to_ask, 0) + 1
        self.time_left = self.time_per_question
        self.timer_event = Clock.schedule_interval(self.update_timer, 1/60.0)

    def update_timer(self, dt):
        self.time_left -= dt
        if self.time_left <= 0:
            self.time_left = 0
            self.handle_incorrect_answer()
    
    def handle_button_press(self, button_text):
        if button_text == 'Borrar':
            self.user_answer_text = self.user_answer_text[:-1]
        elif button_text == 'Enter':
            self.check_answer()
        else:
            self.user_answer_text += button_text

    def check_answer(self):
        if not self.user_answer_text:
            return
        self.stop_timer()
        current_q = (self.factor1, self.factor2)
        try:
            user_num = int(self.user_answer_text)
        except ValueError:
            user_num = -1
        if user_num == self.correct_result:
            self.correct_answers += 1
            if self.manager.app.correct_sound: self.manager.app.correct_sound.play()
            while current_q in self.failed_questions:
                self.failed_questions.remove(current_q)
            Clock.schedule_once(lambda dt: self.next_question(), 0.5)
        else:
            self.incorrect_answers += 1
            if self.manager.app.incorrect_sound: self.manager.app.incorrect_sound.play()
            self.show_solution_popup(f"Respuesta: {self.correct_result}")
            if current_q not in self.failed_questions:
                self.failed_questions.append(current_q)
            Clock.schedule_once(lambda dt: self.next_question(), 1.6)

    def handle_incorrect_answer(self):
        self.stop_timer()
        self.incorrect_answers += 1
        if self.manager.app.incorrect_sound: self.manager.app.incorrect_sound.play()
        self.show_solution_popup(f"Respuesta: {self.correct_result}")
        current_q = (self.factor1, self.factor2)
        if current_q not in self.failed_questions:
            self.failed_questions.append(current_q)
        Clock.schedule_once(lambda dt: self.next_question(), 1.6)
        
    def show_solution_popup(self, solution_text):
        popup_content = Label(
            text=solution_text,
            font_size='28sp',
            bold=True,
            color=(1, 0.2, 0.2, 1)
        )
        popup = Popup(
            title='¡Ups!',
            content=popup_content,
            size_hint=(0.6, 0.4),
            auto_dismiss=False
        )
        popup.open()
        Clock.schedule_once(popup.dismiss, 1.5)

    def stop_timer(self):
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None
            
    def _on_keyboard_down(self, instance, keyboard, keycode, text, modifiers):
        if keycode == 40: self.check_answer()
        elif keycode == 42: self.user_answer_text = self.user_answer_text[:-1]
        elif text and text.isdigit():
            self.user_answer_text += text
        return True

    def end_game(self):
        self.manager.app.final_correct = self.correct_answers
        self.manager.app.final_incorrect = self.incorrect_answers
        self.manager.current = 'score'

# --- Pantalla de Puntuación Final ---
class ScoreScreen(Screen):
    final_score_text = StringProperty('')
    def on_enter(self, *args):
        app = self.manager.app
        self.final_score_text = (f"¡Juego Terminado!\n\nCorrectas: {app.final_correct}\nIncorrectas: {app.final_incorrect}")
    def play_again(self):
        self.manager.current = 'menu'

# --- Clase Principal de la App ---
class TablasApp(App):
    selected_tables = ListProperty([])
    # CAMBIO: Valores por defecto actualizados
    total_questions_config = NumericProperty(20)
    time_per_question_config = NumericProperty(12.0)
    final_correct = NumericProperty(0)
    final_incorrect = NumericProperty(0)
    correct_sound = ObjectProperty(None, allownone=True)
    incorrect_sound = ObjectProperty(None, allownone=True)

    def build(self):
        self.correct_sound = generate_sound(frequency=880, duration=0.15)
        self.incorrect_sound = generate_sound(frequency=220, duration=0.3)
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name='menu'))
        sm.add_widget(GameScreen(name='game'))
        sm.add_widget(ScoreScreen(name='score'))
        sm.app = self
        return sm

if __name__ == '__main__':
    TablasApp().run()
