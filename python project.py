import os
import random
import json

def str2bool(v):
    """Convert string input to boolean (for True/False answers)."""
    return v.lower() in ("yes", "true", "t", "1", "y")

class Quiz:
    def __init__(self):
        """Initialize the quiz."""
        self.correct_score = 0
        self.incorrect_score = 0
        self.questions = self.load_questions()

        if not self.questions:
            print("No questions found! Please check your questions.json file.")
            return

        category = self.show_catalogs()
        if category == -1:
            self.__init__()  # Restart quiz
            return
        elif category == 0:
            quiz_questions = self.pick_random_merged_questions()
        else:
            quiz_questions = self.pick_random_questions(category)

        self.start_test(quiz_questions)
        self.end_test()

    @staticmethod
    def load_questions():
        """Loads questions from a JSON file safely."""
        file_path = os.path.join(os.path.dirname(__file__), 'questions.json')

        try:
            with open(file_path, 'r', encoding="utf8") as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Error: questions.json not found at {file_path}")
            return {}
        except json.JSONDecodeError:
            print("Error: Invalid JSON format in questions.json.")
            return {}

    def show_catalogs(self):
        """Display available categories and allow user selection."""
        categories = list(self.questions.keys())
        for i, category in enumerate(categories, 1):
            print(f"{i}. {category}")
        print(f"{len(categories) + 1}. All Categories")

        try:
            choice = int(input(f"Choose a category (1-{len(categories) + 1}): "))
            if choice < 1 or choice > len(categories) + 1:
                print("Invalid choice! Please enter a valid number.")
                return -1
        except ValueError:
            print("Invalid input! Please enter a number.")
            return -1

        return 0 if choice == len(categories) + 1 else categories[choice - 1]

    def pick_random_merged_questions(self):
        """Merge all categories and pick 5 random questions."""
        all_questions = [(q_data["Q"], q_data["A"]) for cat in self.questions.values() for q_data in cat.values()]
        return random.sample(all_questions, min(5, len(all_questions)))

    def pick_random_questions(self, category):
        """Pick 5 random questions from a selected category."""
        category_questions = [(q_data["Q"], q_data["A"]) for q_data in self.questions[category].values()]
        return random.sample(category_questions, min(5, len(category_questions)))

    def start_test(self, questions):
        """Start the quiz and collect user responses."""
        for question, answer in questions:
            response = input(f"{question}\nTrue/False (T/F): ")
            if str2bool(response) == str2bool(str(answer)):  # Convert answer to string for comparison
                self.correct_score += 1
            else:
                self.incorrect_score += 1

    def end_test(self):
        """Display final score and ask for a rematch."""
        total = self.correct_score + self.incorrect_score
        score_percentage = (self.correct_score / total) * 100 if total > 0 else 0
        print(f"Score: {score_percentage:.1f}%")
        print(f"Correct Answers: {self.correct_score}")
        print(f"Incorrect Answers: {self.incorrect_score}")

        replay = input("Do you want to play again? (Y/N): ")
        if str2bool(replay):
            self.__init__()  # Restart quiz
        else:
            print("Thanks for playing! Have a great day!")

# Start the quiz
Quiz()
