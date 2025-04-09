from csv_chat.question_answerer import QuestionAnswerer
import re



class Analytics:
    """
    Class for running analytics on a predefined set of questions and expected answers.
    """
    questions_data = [
        ("Какой процент фрилансеров, считающих себя экспертами, выполнил менее 100 проектов?", 33.85),
        ("Насколько выше доход у фрилансеров, принимающих оплату в криптовалюте, по сравнению с другими способами оплаты? Выдай разницу со вторым местом.", 119.34),
        ("Как распределяется доход фрилансеров в зависимости от региона проживания? Выдай топ1.", 1479897.0),
        ("Как отличаются оценки клиентов в зависимости от региона или платформы, где работают фрилансеры? Выдай наибольшую среднюю оценку.", 4.176865671641791),
        ("Каким способом оплаты (например, криптовалюта, банковский перевод, мобильные платежи) достигается наибольшее количество выполненных проектов?", 78167),
        ("Как распределяются почасовые ставки фрилансеров по регионам, и отличаются ли они существенно от глобальных показателей? Выдай разницу топ1 от средней.", 1.9294352630186993),
        ("Какая разница в заработке между проектами с фиксированной оплатой и почасовыми проектами?", 30.690429104732935),
        ("Какова доля Австралии в категории графического дизайна? Отвей дай в процентах.", 16.981132075471697),
        ("Какова доля США в категории веб разработки? Отвей дай в процентах.", 15.2),
    ]

    def __init__(self, questioner):
        self.questioner = questioner

    @staticmethod
    def get_numeric_answer(text):
        """
        Extracts and returns the first numeric value found in the text.
        Returns None if no numeric value is found.
        """
        match = re.search(r"(-?\d+(?:\.\d+)?)", text)
        if match:
            return float(match.group(1))
        return None

    def run(self) -> float:
        """
        Run analytics by asking predefined questions and comparing the answers to expected values.
        Returns the overall success rate.
        """
        overall_success = 0
        overall_attempts = 0
        iterations = 10

        for question, expected in self.questions_data:
            q_text = question + " Пожалуйста, ответь одним числом без дополнительных комментариев."
            successes = 0

            for i in range(iterations):
                result = self.questioner.answer(q_text)
                try:
                    result_numeric = float(self.get_numeric_answer(result))
                except (ValueError, TypeError):
                    result_numeric = None

                if result_numeric is not None and abs(result_numeric - expected) < 0.1:
                    successes += 1

                overall_attempts += 1

            question_success_rate = successes / iterations
            overall_success += successes
            print(f"Вопрос: '{question}' – Успех: {question_success_rate*100:.2f}% ({successes}/{iterations})")

        total_success_rate = overall_success / overall_attempts
        print(f"Общий процент успешных ответов: {total_success_rate*100:.2f}% ({overall_success}/{overall_attempts})")

        return total_success_rate
