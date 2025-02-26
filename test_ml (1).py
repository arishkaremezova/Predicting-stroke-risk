import unittest
import numpy as np
import joblib


class TestModelLoading(unittest.TestCase):

    def setUp(self):
        """Загружаем модель перед каждым тестом."""
        try:
            self.model = joblib.load("model.pkl")
        except FileNotFoundError:
            self.fail("model.pkl не найден. Убедитесь, что он существует в правильном месте.")
        except Exception as e:
            self.fail(f"Ошибка при загрузке model.pkl: {e}")

    def test_model_loading_success(self):
        """Проверяем, что модель успешно загружена."""
        self.assertIsNotNone(self.model, "Модель не должна быть None после загрузки.")

    def test_model_prediction_valid_input(self):
        """Проверяем, что модель делает предсказания."""
        sample_data = np.array([[1, 25, 0, 0, 1, 3, 1, 80, 24, 1]])
        try:
            prediction = self.model.predict(sample_data)
            self.assertIsNotNone(prediction, "Предсказание не должно быть None")
        except Exception as e:
            self.fail(f"Prediction failed with valid input: {e}")



if __name__ == '__main__':
    unittest.main()