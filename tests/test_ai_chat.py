import json
import unittest

from app.main import lambda_handler


class TestAiChat(unittest.TestCase):
    def test_ai_chat(self):
        simulated_event = {
            "body": json.dumps(
                {
                    # "input_message": "Can you tell me about Alen's background?"
                    # "input_message": "What's your visa status?"
                    "input_message": "Do you like banana?"
                }
            )
        }
        simulated_context = None
        response = lambda_handler(simulated_event, simulated_context)
        print(response)


if __name__ == "__main__":
    unittest.main()
