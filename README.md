# Quizzer

Quizzer is an interactive application that enables users to create and participate in quizzes. Users can take on the role of a Quiz Master to design quizzes or a Competitor to engage in quiz challenges.

## Features

- **Create Custom Quizzes**: As a Quiz Master, you can create quizzes with customizable settings such as the number of questions, options, and timing for each question.
- **Participate in Quizzes**: As a Quiz Competitor, you can take quizzes, answer questions, and receive a score based on your performance.
- **Secure Access**: The Quiz Master section is secured with a password for authorized access only.
- **Track Performance**: After completing a quiz, competitors can review their score, the number of correctly and wrongly answered questions.
- **Data Storage**: Quiz data is stored securely in Base64 encoded binary files.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Flet library

### Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/YourUsername/Quizzer.git
    ```

2. Navigate to the project directory:

    ```bash
    cd Quizzer
    ```

3. Install the required dependencies:

    ```bash
    pip install flet
    ```

### Usage

1. Run the application:

    ```bash
    python main.py
    ```

2. Choose between being a Quiz Master or Quiz Competitor.

- **Quiz Master**: Enter the password to access the quiz creation tools. The default password is `CopyCat-Developerz@rishi`.
- **Quiz Competitor**: Select a quiz, enter your name, and the quiz key to start quizzing.

3. Follow on-screen instructions to create or participate in quizzes.

### File Structure

- **main.py**: The main script that runs the Quizzer application.
- **Documents/Quizzer**: Directory where quiz data is stored as `.bin` files.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Developed by Rishi Aravind.
- Visit the developer's [GitHub page](https://github.com/RishiAravind2004) for more projects and updates.

