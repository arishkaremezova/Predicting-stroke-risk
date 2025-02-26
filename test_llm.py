import unittest
from unittest.mock import patch, MagicMock
from gigachat import GigaChat

import llm_part

class TestGigaChat(unittest.TestCase):

    def test_connect_gigachat_success(self):
        model = llm_part.connect_gigachat()
        self.assertIsInstance(model, GigaChat)

    @patch('llm_part.GigaChat')
    def test_connect_gigachat_credentials(self, mock_gigachat):

        llm_part.connect_gigachat()

        mock_gigachat.assert_called_once_with(
            credentials=llm_part.TOKEN,
            model="GigaChat-Pro",
            verify_ssl_certs=False
        )


    @patch('llm_part.GigaChat')
    def test_ask_gigachat_success(self, mock_gigachat_class):

        mock_gigachat_instance = MagicMock()
        mock_gigachat_class.return_value = mock_gigachat_instance

        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "Mocked response from GigaChat"

        mock_gigachat_instance.chat.return_value = mock_response


        model = llm_part.connect_gigachat()
        prompt = "What is the meaning of life?"
        response = llm_part.ask_gigachat(model, prompt)


        mock_gigachat_instance.chat.assert_called_once()
        call_args = mock_gigachat_instance.chat.call_args[0][0]
        expected_message = [{'role': 'user', 'content': 'What is the meaning of life?'}]

        self.assertEqual(call_args['messages'], expected_message)
        self.assertEqual(call_args['temperature'], 0.1)
        self.assertEqual(call_args['top_p'], 0.9)



        self.assertEqual(response, "Mocked response from GigaChat")


if __name__ == '__main__':
    unittest.main()