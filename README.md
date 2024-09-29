# Quizzer

Quizzer is an interactive application designed for creating and participating in quizzes, providing an engaging and user-friendly interface built with the Flet library. Users can effortlessly switch between roles as a Quiz Master (for creating quizzes) or a Quiz Competitor (for taking quizzes), ensuring a seamless experience for everyone involved.

## Features

- **Create Custom Quizzes**: As a Quiz Master, you can craft quizzes tailored to your needs with customizable settings, including the number of questions, answer options, and timing for each question.
  
- **Participate in Quizzes**: As a Quiz Competitor, dive into quizzes, respond to questions, and receive scores reflecting your performance.
  
- **Secure Access**: The Quiz Master section is fortified with a password for authorized access only, ensuring quiz integrity and privacy.
  
- **Track Performance**: Competitors can review their scores, along with the number of correctly and incorrectly answered questions, providing valuable feedback after completing a quiz.
  
- **Data Storage**: All quiz data is securely stored in Base64 encoded binary files, ensuring both security and efficiency in data handling.

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

3. Follow the on-screen instructions to create or participate in quizzes.

### Download Executable

You can download the compiled executable version of Quizzer from the [Releases](https://github.com/RishiAravind2004/Quizzer/releases) section of this repository. This version allows you to run the application without requiring Python to be installed.

## File Structure

- **main.py**: The main script that runs the Quizzer application.
- **Documents/Quizzer**: Directory where quiz data is securely stored as `.bin` files.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements

- Developed by Rishi Aravind.
- Visit the developer's [GitHub page](https://github.com/RishiAravind2004) for more projects and updates.
