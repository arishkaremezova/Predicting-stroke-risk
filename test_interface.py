import unittest
from unittest.mock import patch, MagicMock
import joblib


import interface_new  # Имя файла с ботом

try:
    interface_new.model1 = joblib.load("model.pkl")
except FileNotFoundError:

    interface_new.model1 = MagicMock()
    print("model.pkl не найден. Используется фиктивная модель для тестирования.")


class TestBot(unittest.TestCase):

    def setUp(self):

        self.bot_patcher = patch('interface_new.bot', new_callable=MagicMock)
        self.mock_bot = self.bot_patcher.start()
        self.mock_bot.return_value = MagicMock()

        self.cursor_patcher = patch('interface_new.cursor', new_callable=MagicMock)
        self.mock_cursor = self.cursor_patcher.start()
        self.conn_patcher = patch('interface_new.conn', new_callable=MagicMock)
        self.mock_conn = self.conn_patcher.start()


        interface_new.user_data = {}


    def tearDown(self):

        self.bot_patcher.stop()
        self.cursor_patcher.stop()
        self.conn_patcher.stop()

    def setup_user_data(self, user_id):
        interface_new.user_data[user_id] = {}

    @patch('interface_new.ask_gender')
    def test_start_command(self, mock_ask_gender):  # Add mock_ask_gender as argument

        message = MagicMock()
        message.from_user.id = 123
        message.chat.id = 456

        interface_new.start(message)

        mock_ask_gender.assert_called_once_with(456)

        self.assertIn(123, interface_new.user_data)
        self.assertEqual(interface_new.user_data[123], {})


    @patch('interface_new.ask_age')
    def test_process_gender(self, mock_ask_age):

        self.setup_user_data(123)
        call = MagicMock()
        call.data = 'gender_1'
        call.from_user.id = 123
        call.message.chat.id = 456

        interface_new.process_gender(call)

        self.assertEqual(interface_new.user_data[123]['gender'], 1)
        mock_ask_age.assert_called_once_with(456)


    @patch('interface_new.ask_hypertension')
    def test_process_age_step_valid_age(self, mock_ask_hypertension):

        self.setup_user_data(123)
        message = MagicMock()
        message.text = '30'
        message.from_user.id = 123
        message.chat.id = 456

        interface_new.process_age_step(message)

        self.assertEqual(interface_new.user_data[123]['age'], 30)
        mock_ask_hypertension.assert_called_once_with(456)


    def test_process_age_step_invalid_age(self):

        self.setup_user_data(123)
        message = MagicMock()
        message.text = 'invalid'
        message.from_user.id = 123
        message.chat.id = 456

        interface_new.process_age_step(message)

        self.mock_bot.send_message.assert_called_once()
        self.mock_bot.register_next_step_handler.assert_called_once()

    @patch('interface_new.ask_heart_disease')
    def test_process_hypertension(self, mock_ask_heart_disease):
        self.setup_user_data(123)
        call = MagicMock()
        call.data = 'hypertension_0'
        call.from_user.id = 123
        call.message.chat.id = 456

        interface_new.process_hypertension(call)

        self.assertEqual(interface_new.user_data[123]['hypertension'], 0)
        mock_ask_heart_disease.assert_called_once_with(456)

    @patch('interface_new.ask_marital_status')
    def test_process_heart_disease(self, mock_ask_marital_status):
        self.setup_user_data(123)  # Инициализируем user_data
        call = MagicMock()
        call.data = 'heart_1'
        call.from_user.id = 123
        call.message.chat.id = 456

        interface_new.process_heart_disease(call)

        self.assertEqual(interface_new.user_data[123]['heart_disease'], 1)
        mock_ask_marital_status.assert_called_once_with(456)

    @patch('interface_new.ask_work_type')
    def test_process_marital_status(self, mock_ask_work_type):

        self.setup_user_data(123)
        call = MagicMock()
        call.data = 'married_0'
        call.from_user.id = 123
        call.message.chat.id = 456

        interface_new.process_marital_status(call)

        self.assertEqual(interface_new.user_data[123]['ever_married'], 0)
        mock_ask_work_type.assert_called_once_with(456)

    @patch('interface_new.ask_residence_type')
    def test_process_work_type(self, mock_ask_residence_type):

        self.setup_user_data(123)
        call = MagicMock()
        call.data = 'work_1'
        call.from_user.id = 123
        call.message.chat.id = 456

        interface_new.process_work_type(call)

        self.assertEqual(interface_new.user_data[123]['work_type'], 1)
        mock_ask_residence_type.assert_called_once_with(456)

    @patch('interface_new.ask_glucose')
    def test_process_residence_type(self, mock_ask_glucose):

        self.setup_user_data(123)
        call = MagicMock()
        call.data = 'residence_0'
        call.from_user.id = 123
        call.message.chat.id = 456

        interface_new.process_residence_type(call)

        self.assertEqual(interface_new.user_data[123]['residence_type'], 0)
        mock_ask_glucose.assert_called_once_with(456)

    @patch('interface_new.ask_bmi')
    def test_process_glucose_step_valid_glucose(self, mock_ask_bmi):

        self.setup_user_data(123)
        message = MagicMock()
        message.text = '7.5'
        message.from_user.id = 123
        message.chat.id = 456

        interface_new.process_glucose_step(message)

        self.assertEqual(interface_new.user_data[123]['avg_glucose_level'], 7.5)
        mock_ask_bmi.assert_called_once_with(456)

    def test_process_glucose_step_invalid_glucose(self):

        self.setup_user_data(123)  # Инициализируем user_data
        message = MagicMock()
        message.text = 'abc'
        message.from_user.id = 123
        message.chat.id = 456

        interface_new.process_glucose_step(message)

        self.mock_bot.send_message.assert_called_once()
        self.mock_bot.register_next_step_handler.assert_called_once()

    @patch('interface_new.ask_smoking_status')
    def test_process_bmi_step_valid_bmi(self, mock_ask_smoking_status):

        self.setup_user_data(123)  # Инициализируем user_data
        message = MagicMock()
        message.text = '25.0'
        message.from_user.id = 123
        message.chat.id = 456

        interface_new.process_bmi_step(message)

        self.assertEqual(interface_new.user_data[123]['bmi'], 25.0)
        mock_ask_smoking_status.assert_called_once_with(456)

    def test_process_bmi_step_invalid_bmi(self):

        self.setup_user_data(123)
        message = MagicMock()
        message.text = 'invalid_bmi'
        message.from_user.id = 123
        message.chat.id = 456

        interface_new.process_bmi_step(message)

        self.mock_bot.send_message.assert_called_once()
        self.mock_bot.register_next_step_handler.assert_called_once()

    @patch('interface_new.make_prediction')
    def test_process_smoking_status(self, mock_make_prediction):

        self.setup_user_data(123)
        call = MagicMock()
        call.data = 'smoking_1'
        call.from_user.id = 123
        call.message.chat.id = 456

        interface_new.process_smoking_status(call)

        self.assertEqual(interface_new.user_data[123]['smoking_status'], 1)
        mock_make_prediction.assert_called_once_with(456, 123)


if __name__ == '__main__':
    unittest.main()
