"""

        Quizzer!

"""

# required modules
import flet as ft
import os
import json
import base64
from threading import Timer
import time, datetime
import random


# assign the path for Quizzer application
home_dir = os.path.expanduser("~")
Quizz_Folder_Path = os.path.join(home_dir, "Documents", "Quizzer")


# global func to update quiz file
def Update_Quiz_File(quiz_data):
    print(quiz_data)
    file_name = quiz_data["Details"]["quiz_name"]
    quiz_json_data = json.dumps(quiz_data)
        
    # encode the JSON string to bytes
    quiz_bin_data = quiz_json_data.encode('utf-8')
        
    # encode the bytes to Base64
    encoded_bin_data = base64.b64encode(quiz_bin_data)
        
    # write the Base64 encoded data to the binary file
    with open(f'{Quizz_Folder_Path}\\{file_name}.bin', 'wb') as binary_file:
        binary_file.write(encoded_bin_data)
        
    print(f"File '{file_name}.bin' has been updated successfully.")    

# main function
def main(page: ft.Page):
    
    # create application directory if it doesn't exist
    if not os.path.exists(Quizz_Folder_Path):
        os.makedirs(Quizz_Folder_Path)

    # empty var to hold questions
    question_containers = []
    question_column = ft.Column()

    # quiz master session
    def Quiz_Master_Page(e):
        


#
#       Create Quiz
#

        # creating quiz session where admin enters quiz details
        def Create_New_Quizz(quiz_name_field, quiz_key_field, num_questions_field, num_options_field, timing_field):
            # clear any existing error messages
            quiz_name_field.error_text = None
            quiz_key_field.error_text = None
            num_questions_field.error_text = None
            num_options_field.error_text = None
            timing_field.error_text = None

            # checking if the input values are valid
            if not quiz_name_field.value:
                quiz_name_field.error_text = "Quiz name is required"
            if not quiz_key_field.value:
                quiz_key_field.error_text = "Quiz key is required"
            if not num_questions_field.value or not num_questions_field.value.isdigit():
                num_questions_field.error_text = "Please enter a valid number of questions"
            if not num_options_field.value or not num_options_field.value.isdigit():
                num_options_field.error_text = "Please enter a valid number of options"
            if not timing_field.value or not timing_field.value.isdigit():
                timing_field.error_text = "Please enter a valid timing in seconds"

            # check if any error messages are set
            if quiz_name_field.error_text or quiz_key_field.error_text or num_questions_field.error_text or num_options_field.error_text or timing_field.error_text:
                page.update()
                return

            # if no errors, assign values
            quiz_name = quiz_name_field.value
            quiz_key = quiz_key_field.value
            num_questions = int(num_questions_field.value)
            num_options = int(num_options_field.value)
            timing = int(timing_field.value)

            Setup_Quizz(
                quiz_name_field, quiz_key_field, num_questions_field, num_options_field, timing_field,
                quiz_name, quiz_key, num_questions, num_options, timing
            )

# For login page Quiz Master

        def Create_Quiz(e):
            page.controls.clear()
            
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.vertical_alignment = ft.MainAxisAlignment.CENTER

            # input fields for creating a quiz
            quiz_name_field = ft.TextField(label='Quiz Name')
            quiz_key_field = ft.TextField(label='Quiz Key')
            num_questions_field = ft.TextField(label='Number of Questions', keyboard_type='number')
            num_options_field = ft.TextField(label='Number of Options', keyboard_type='number')
            timing_field = ft.TextField(label='Timing (seconds) per question', keyboard_type='number')

            # container to hold quiz creation fields
            container = ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Creating Quiz...", size=20, weight="bold"),
                        quiz_name_field,
                        quiz_key_field,
                        num_questions_field,
                        num_options_field,
                        timing_field,
                        ft.ElevatedButton(
                            text='Create', 
                            on_click=lambda e: Create_New_Quizz(
                                quiz_name_field, quiz_key_field, num_questions_field, num_options_field, timing_field
                            )
                        )
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                border=ft.Border(left=ft.BorderSide(1, "black"), right=ft.BorderSide(1, "black"),
                                 top=ft.BorderSide(1, "black"), bottom=ft.BorderSide(1, "black")),
                padding=20,
                width=400, 
                height=400, 
                alignment=ft.alignment.center,
            )

            page.add(container)
            page.update()

        # setup session, admin to feed questions
        def Setup_Quizz(quiz_name_field, quiz_key_field, num_questions_field, num_options_field, timing_field, quiz_name, quiz_key, num_questions, num_options, timing):
            page.controls.clear()
            page.add(ft.Text(f"Settings up questions for '{quiz_name}' Quizz!", size=18, weight="bold"))
            page.update()
            question_column = ft.Column(scroll="auto")

            # function to update configuration
            def Update_Config(e):
                print(f'Quiz Name: {quiz_name_field.value}')
                print(f'Quiz Key: {quiz_key_field.value}')
                print(f'Number of Questions: {num_questions_field.value}')
                print(f'Number of Options: {num_options_field.value}')
                print(f'Timing: {timing_field.value} seconds')

                def btn_click(e):
                    page.close(dlg_modal)

                dlg_modal = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Updated!"),
                    content=ft.Column(
                        controls=[
                            ft.Text("Configurations are successfully updated!"),
                        ],
                        tight=True,
                    ),
                    actions=[
                        ft.TextButton("Close", on_click=btn_click)
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )

                page.open(dlg_modal)

            # scrollable container for question column
            scrollable_container = ft.Container(
                content=question_column,
                height=600,
                width=1350,
            )

            # add scrollable container to the page
            page.add(scrollable_container)

            # function to delete a question container
            def delete_container(e):
                container_id = e.control.data
                for cont in question_containers:
                    if cont.data == container_id:
                        question_column.controls.remove(cont)
                        question_containers.remove(cont)
                        break
                page.update()

            # function to add a question container
            def add_question_container():
                container_id = len(question_containers)

                option_fields = ft.Column()

                # option fields
                for i in range(1, num_options + 1):
                    option_fields.controls.append(
                        ft.TextField(label=f"Option {i}", width=350, multiline=True)
                    )

                # container for question and options
                new_container = ft.Container(
                    content=ft.Column([
                        ft.Text(f"Question {container_id}:", weight="bold"),
                        ft.TextField(label="Enter your question", width=550, multiline=True),
                        ft.Text("Options:", weight="bold"),
                        option_fields,
                        ft.Text("Answer:", weight="bold"),
                        ft.TextField(label=f"Answer", width=350, multiline=True),
                        ft.ElevatedButton("Delete Question", data=container_id, on_click=delete_container)
                    ]),
                    data=container_id,
                    border=ft.Border(left=ft.BorderSide(1, "black"), right=ft.BorderSide(1, "black"),
                                     top=ft.BorderSide(1, "black"), bottom=ft.BorderSide(1, "black")),
                    padding=10,
                    margin=5,
                    width=1350
                )

                # adding container to the list
                question_containers.append(new_container)
                question_column.controls.append(new_container)
                page.update()

            # function to add questions based on user input
            def add_questions():

                # Add the specified number of questions
                for _ in range(num_questions):
                    add_question_container()

            # function to add an extra question
            def add_extra_question(e):
                add_question_container()

            # Configuration container
            config_container = ft.Container(
                content=ft.Column([
                    ft.Text("Edit Configurations", weight="bold"),
                    quiz_name_field,
                    quiz_key_field,
                    num_questions_field,
                    num_options_field,
                    timing_field,
                    ft.Text("Note: Updating the number of questions will not change the count of existing questions, So add manually by clicking 'Add Extra Question', It is used to show no of questions to Competitors.", weight="bold"),
                    ft.ElevatedButton("Update Configuration", on_click=Update_Config),
                    ft.Text(""),
                    ft.Text("Notes: 1. Answer field must be same as option, So copy correct answer from filed of 'Options' and paste on to the 'Answer' field.", weight="bold"),
                    ft.Text("      \t2. Programming languages are applicable for feed-up.", weight="bold"),
                    ft.Text("      \t3. Don't worry about the count after deleting and create a question, it will not be on count.", weight="bold"),
                ]),
                border=ft.Border(left=ft.BorderSide(1, "black"), right=ft.BorderSide(1, "black"),
                                 top=ft.BorderSide(1, "black"), bottom=ft.BorderSide(1, "black")),
                padding=10,
                margin=5,
                width=1350
            )
            
            question_containers.append(config_container)
            question_column.controls.append(config_container)
            page.update()
            
            # automatically generate questions based on the given input
            add_questions()
            
            def Gen_Quizz(quiz_name, quiz_key, num_questions, num_options, timing):
                # Structure of Quiz JSON
                quiz_data = {
                    "Details": {
                        "quiz_name": quiz_name,
                        "quiz_key": quiz_key,
                        "num_questions": num_questions,
                        "num_options": num_options,
                        "timing": timing
                    },
                    "Competitor":{
                        "name": None,
                        "scored": 0,
                        "date & time": None,
                        "correctly_answered": 0,
                        "wrongly_answered": 0,
                        "questions_answered": []
                    },
                    "Questions": []
                }

                # Iterate over each question container (skip the first one, which is the configuration)
                for container in question_containers[1:]:
                    question_data = {}

                    # Extract the question text from the container's content
                    question_text_field = container.content.controls[1]
                    question_text = question_text_field.value
                    question_data['question'] = question_text

                    # Extract options
                    # The options are in the Column at index 3 (0-based index)
                    options_column = container.content.controls[3]
                    options = []
                    if isinstance(options_column, ft.Column):
                        for control in options_column.controls:
                            if isinstance(control, ft.TextField):
                                options.append(control.value)
                    question_data['options'] = options

                    # Extract the answer
                    answer_text_field = container.content.controls[5]
                    answer = answer_text_field.value
                    question_data['answer'] = answer

                    quiz_data['Questions'].append(question_data)

                # convert quiz data to JSON format
                quiz_json = json.dumps(quiz_data, indent=4)

                # encode JSON data to Base64
                quiz_bin = base64.b64encode(quiz_json.encode('utf-8')).decode('utf-8')

                with open(f'{Quizz_Folder_Path}\\{quiz_name}.bin', 'wb') as binary_file:
                    binary_file.write(quiz_bin.encode('utf-8'))

                print(f"Quiz data written to binary file: {Quizz_Folder_Path}\\{quiz_name}.bin")
                def show_folder(e):
                    os.startfile(Quizz_Folder_Path)
                def on_click(e):
                    page.close(dlg_modal)
                    return Session_Page(e)

                    
                dlg_modal = ft.AlertDialog(
                    modal=True,
                    title=ft.Text("Generated!"),
                    content=ft.Column(
                        controls=[
                            ft.Text("Successfully Quizz Generated!"),
                        ],
                        tight=True,
                    ),
                    actions=[
                        ft.TextButton("Close", on_click=on_click),
                        ft.TextButton("Show in folder", on_click=show_folder)
                    ],
                    actions_alignment=ft.MainAxisAlignment.END,
                )

                
                page.open(dlg_modal)
                print(quiz_json)

                
            # button to add extra questions at the end & submit
            button_row = ft.Row(
                controls=[
                    ft.ElevatedButton("Add Extra Question", on_click=add_extra_question),
                    ft.ElevatedButton("Generate Quizz...",on_click=lambda e: Gen_Quizz(
                                                                                quiz_name_field.value,
                                                                                quiz_key_field.value,
                                                                                num_questions_field.value,
                                                                                num_options_field.value,
                                                                                timing_field.value
                                                                                )
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )

            page.add(button_row)
            page.update()

            
#
#       Edit Quiz
#
        def Edit_Quiz(e):
            # editing quiz under develeopment
            construction_dlg = ft.AlertDialog(
                        title=ft.Text("Information!"),
                        content=ft.Column(
                            [
                                ft.Text("For your kind information the editing quiz is on under developing!"),
                            ],
                            tight=True
                        ),
                        actions=[ft.TextButton("OK", on_click=lambda e: page.close(construction_dlg))]
                    )
            page.open(construction_dlg)
#
#       QUIZ MASTER LOGIN PAGE
#
        page.controls.clear()
        def login_action(e):
            password = password_field.value
            if password:
                if password != "CopyCat-Developerz@rishi":
                    password_field.error_text = "Incorrect password. Please try again."
                else:
                    page.controls.clear()

                    page.add(
                        ft.Column(
                            controls=[
                                ft.Text("Select you Quiz works!", size=20, weight="bold"),
                                ft.Row(
                                    controls=[
                                        ft.ElevatedButton("Create Quiz", on_click=Create_Quiz),
                                        ft.ElevatedButton("Edit Quiz", on_click=Edit_Quiz)
                                    ],
                                    spacing=10,
                                    alignment=ft.MainAxisAlignment.CENTER
                                ),
                            ],
                            spacing=20,
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            expand=True
                        )
                    )
            else:
                password_field.error_text = "Please enter the password."
                
            page.update()


        password_field = ft.TextField(
            label="Password",
            password=True,
            width=300
        )
            
        page.add(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Please enter your password", size=20, weight="bold"),
                            password_field,
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton("Back", on_click=Session_Page),
                                    ft.ElevatedButton("Login", on_click=login_action)
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER, 
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True 
            )
        )

        page.update()


#
#       Quiz Competitor Page
#
    def Quiz_Comp_Page(e):
        
        # playing quiz
        def Quizzing(e, quiz_data):
            # Function to get a random question from remaining questions
            def get_random_question(remaining_questions):
                if not remaining_questions:
                    return None
                question = random.choice(remaining_questions)
                random.shuffle(question["options"])
                return question

            # Function to handle countdown timer
            def start_timer(page, update_question_func, timer_display, timer_duration):
                timer_duration = int(timer_duration)
                def countdown():
                    nonlocal timer_duration
                    if timer_duration > 0:
                        timer_display.value = f"Time Left: {timer_duration}s"
                        page.update()
                        timer_duration -= 1
                        Timer(1, countdown).start()
                    else:
                        update_question_func()
                
                countdown()

            # Function to update questions and handle answers
            def update_question():
                nonlocal current_question
                nonlocal current_question_index
                
                # Get selected answer
                selected_answer = radio_group.value
                quiz_data["Competitor"]["questions_answered"].append(current_question)
                correct_answer = current_question.get("answer")

                if selected_answer:
                    if selected_answer == correct_answer:
                        quiz_data["Competitor"]["correctly_answered"] += 1
                        
                        open_modal = ft.AlertDialog(
                            modal=True,
                            title=ft.Text("Congratulations! You Got it!", size=30, weight=ft.FontWeight.BOLD, color="green"),
                            content=ft.Text(f"It is ' {correct_answer} '", weight=ft.FontWeight.BOLD),
                            actions_alignment=ft.MainAxisAlignment.END,
                        )
                        
                        page.open(open_modal)
                        time.sleep(8)
                        page.close(open_modal)
                    else:
                        quiz_data["Competitor"]["wrongly_answered"] += 1
                        
                        open_modal = ft.AlertDialog(
                            modal=True,
                            title=ft.Text("Oops! Wrong Answer!", size=30, weight=ft.FontWeight.BOLD, color="red"),
                            content=ft.Text(f"Your selected answer ' {selected_answer} ' is incorrect. The correct answer is ' {correct_answer} '", weight=ft.FontWeight.BOLD),
                            actions_alignment=ft.MainAxisAlignment.END,
                        )
                        
                        page.open(open_modal)
                        time.sleep(8)
                        page.close(open_modal)
                else:
                    quiz_data["Competitor"]["wrongly_answered"] += 1

                    open_modal = ft.AlertDialog(
                        modal=True,
                        title=ft.Text("Oops! I am sorry you are not selected an option within time :(", size=30, weight=ft.FontWeight.BOLD, color="red"),
                        content=ft.Text(f"It will be counted as wrong answer!, The correct answer is ' {correct_answer} '", weight=ft.FontWeight.BOLD),
                        actions_alignment=ft.MainAxisAlignment.END,
                    )
                    page.open(open_modal)
                    time.sleep(8)
                    page.close(open_modal)

                quiz_data["Competitor"]["scored"] = quiz_data["Competitor"]["correctly_answered"]

                Update_Quiz_File(quiz_data)

                # Remove the answered question and get a new random question
                radio_group.value = None
                remaining_questions.remove(current_question)
                current_question = get_random_question(remaining_questions)

                if current_question is None:
                    radio_group.content.controls = []
                    os.rename(f"{Quizz_Folder_Path}\\{quiz_data['Details']['quiz_name']}.bin", f"{Quizz_Folder_Path}\\{quiz_data['Details']['quiz_name']}[Finished].bin")
                    
                    page.controls.clear()
                    
                    def visit_github(e):
                        page.launch_url("https://github.com/RishiAravind2004")

                    page.add(ft.Text("Quiz Completed", size=23, color="orange", weight=ft.FontWeight.BOLD))
                    page.add(ft.Text(""))
                    page.add(ft.Text(f"Hey '{quiz_data['Competitor']['name']}'! you have,"))
                    page.add(ft.Text(f"Date of Quiz taken: {quiz_data['Competitor']['date & time']}"))
                    page.add(ft.Text(f"Scored: {quiz_data['Competitor']['scored']}, Out of {quiz_data['Details']['num_questions']}"))
                    page.add(ft.Text(f"Correctly Answered: {quiz_data['Competitor']['correctly_answered']}"))
                    page.add(ft.Text(f"Wrongly Answered: {quiz_data['Competitor']['wrongly_answered']}"))
                    page.add(ft.Text("Congratulations! Thank you for participating. We hope this quiz has been a valuable challenge to your knowledge,", size=15, weight="bold"))
                    page.add(ft.Text("Whether the result is good or bad, we encourage you to keep learning and growing!", size=15, weight="bold"))
                    page.add(ft.TextButton(text="By Developer: Rishi Aravind! :)", on_click = visit_github))
                    page.add(ft.ElevatedButton("Back to Main Menu!", on_click=Session_Page))
                else:
                    current_question_index += 1
                    question_no.value = f"Question {current_question_index}"
                    question_text.value = current_question['question']
                    radio_group.content.controls = [
                        ft.Radio(value=option, label=option) for option in current_question["options"]
                    ]
                    start_timer(e.page, update_question, timer_display, quiz_data["Details"]["timing"])

                e.page.update()

            page.controls.clear()

            remaining_questions = quiz_data["Questions"][:]
            
            # Ensure timer_duration is an integer
            timer_duration = int(quiz_data["Details"]["timing"])

            # Remove already answered questions from remaining questions
            if len(quiz_data["Competitor"]["questions_answered"]) > 0:
                # Copy answered questions for safe iteration
                answered_questions = quiz_data["Competitor"]["questions_answered"][:]
                
                # Remove questions from remaining_questions that were already answered
                for answered_qn in answered_questions:
                    remaining_questions = [
                        question for question in remaining_questions 
                        if question["question"] != answered_qn["question"]
                    ]

            # Initialize timer display
            timer_display = ft.Text(f"Time Left: {timer_duration}s", size=20, color="red", weight=ft.FontWeight.BOLD)

            # Initialize question and controls
            current_question_index = 1
            current_question = get_random_question(remaining_questions)

            question_no = ft.Text(f"Question {current_question_index}", size=25, weight=ft.FontWeight.BOLD)
            question_text = ft.Text(current_question['question'])

            quiz_data["Competitor"]["date & time"] = datetime.datetime.now().strftime("%d-%m-%Y at %H:%M:%S")
            Update_Quiz_File(quiz_data)

            radio_group = ft.RadioGroup(
                content=ft.Column(
                    [ft.Radio(value=option, label=option) for option in current_question["options"]]
                )
            )

            start_timer(e.page, update_question, timer_display, timer_duration)
            
            page.add(ft.Text("Quiz in Motion!", size=18, weight="bold"))
            
            quiz_container = ft.Container(
                content=ft.Column(
                    [
                        question_no,
                        question_text,
                        radio_group,
                        ft.Row(
                            [
                                timer_display,
                                ft.Container(width=250)
                            ],
                            alignment=ft.MainAxisAlignment.END
                        )
                    ],
                    spacing=10,
                    alignment=ft.MainAxisAlignment.START
                ),
                padding=10,
                expand=True,
                border_radius=10,
                border=ft.Border(
                    top=ft.BorderSide(1, "black"),
                    right=ft.BorderSide(1, "black"),
                    bottom=ft.BorderSide(1, "black"),
                    left=ft.BorderSide(1, "black")
                ),
                alignment=ft.alignment.center
            )
            
            e.page.add(ft.Row([quiz_container], alignment=ft.MainAxisAlignment.CENTER))



#########                               FILE PROCESSING AND VERIFICATION OF KEY

#
#       Selection 'Quiz' files operations
#
        #action for selected quiz
        def on_click(e):
            file_name = e.control.data
            print(f"File clicked: {file_name}")

            # read the .bin file
            with open(f'{Quizz_Folder_Path}\\{file_name}.bin', 'rb') as binary_file:
                quiz_bin_data = binary_file.read()

            # decode Base64 encoded data
            quiz_json_data = base64.b64decode(quiz_bin_data).decode('utf-8')

            # convert the JSON string back to dict var
            quiz_data = json.loads(quiz_json_data)

            if "[Finished]" in file_name:
                dlg = ft.AlertDialog(
                    title=ft.Text("Information!"),
                    content=ft.Column(
                        [
                            ft.Text("This quiz is already participated by another one!"),
                            ft.Text("Competitor Information!"),
                            ft.Text(f"Name: {quiz_data['Competitor']['name']}"),
                            ft.Text(f"Date of Quiz taken: {quiz_data['Competitor']['date & time']}"),
                            ft.Text(f"Scored: {quiz_data['Competitor']['scored']}, Out of {quiz_data['Details']['num_questions']}"),
                            ft.Text(f"Correctly Answered: {quiz_data['Competitor']['correctly_answered']}"),
                            ft.Text(f"Wrongly Answered: {quiz_data['Competitor']['wrongly_answered']}")
                        ],
                        tight=True
                    ),
                    actions=[ft.TextButton("OK", on_click=lambda e: page.close(dlg))]
                )

                page.open(dlg)
                page.update()

            else:
                page.controls.clear()
                # action for key field
                def btn_click(e):
                    
                    # clear any existing error texts
                    name_field.error_text = None
                    key_field.error_text = None

                    # validate fields
                    if not name_field.value:
                        name_field.error_text = "Please enter the competitor name"
                    if not key_field.value:
                        key_field.error_text = "Please enter the quiz key"
                    elif key_field.value != quiz_data['Details']['quiz_key']:
                        key_field.error_text = "Wrong Key! key does not matches quiz's."

                    # if there are any errors, update the page and return
                    if name_field.error_text or key_field.error_text:
                        page.update()
                        return


                    # if everything is correct, proceed with the quiz
                    page.controls.clear()

                    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
                    page.vertical_alignment = ft.MainAxisAlignment.CENTER
            
                    page.add(ft.Text(f"Hey {name_field.value}! Get ready for the '{quiz_data['Details']['quiz_name']}' quiz. It has {quiz_data['Details']['num_questions']} questions, with {quiz_data['Details']['timing']} seconds to answer each one.", size=24, weight="bold"))
                    page.add(ft.Text("Good luck! I'm sure you'll do great!", size=20, weight="bold"))
                    page.add(ft.ElevatedButton("Start Quizzing..!", on_click=lambda e: Quizzing(e, quiz_data)))
                    
                    page.update()

                    quiz_data["Competitor"]["name"] = name_field.value
                    Update_Quiz_File(quiz_data)

                # after selecting file
                name_field = ft.TextField(label="Competitor Name")
                key_field = ft.TextField(label="Quiz Key")
                submit_button = ft.ElevatedButton("Submit!", on_click=btn_click)
                back_button = ft.ElevatedButton("Back!", on_click=Quiz_Comp_Page)

                page.add(
                    ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    ft.Text(f"Please enter key for '{quiz_data['Details']['quiz_name']}' Quiz!", size=20, weight="bold"),
                                    name_field,
                                    key_field, 
                                    ft.Row(
                                        controls=[
                                            submit_button,
                                            back_button
                                        ],
                                        spacing=10,
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER,
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True
                    )
                )
                page.update()

#
#       Displaying 'Quiz' files
#
        page.controls.clear()
        
        # get files in the path without extensions
        files = [os.path.splitext(f)[0] for f in os.listdir(Quizz_Folder_Path) if os.path.isfile(os.path.join(Quizz_Folder_Path, f))]

        # when no quizzes founded at directory
        if not files:
            
            page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
            page.vertical_alignment = ft.MainAxisAlignment.CENTER
            page.add(ft.Text("No Quizzes found :(", size=20, color=ft.colors.RED,weight="bold"))
            page.add(ft.ElevatedButton("Back!", on_click=Session_Page))

        # selecting quiz in directory
        else:
            page.add(ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=Session_Page))
            page.add(ft.Text("Pick Your Challenge...", size=18, weight="bold"))

            file_containers = [
                ft.Container(
                    content=ft.Text(f, weight="bold"),
                    width=150,
                    height=50,
                    alignment=ft.alignment.center,
                    bgcolor=ft.colors.LIGHT_BLUE,
                    border_radius=8,
                    padding=10,
                    on_click=on_click,
                    data=f
                ) for f in files
            ]

            page.add(
                ft.ListView(
                    controls=file_containers,
                    spacing=10,
                    expand=True,
                    auto_scroll=True
                )
            )
        page.update()

        
#
#       SELECTING PAGE(SESSION SELECTION)
#
    def Session_Page(e):
        page.controls.clear()
        page.add(
            ft.Row(
                controls=[
                    ft.Column(
                        controls=[
                            ft.Text("Get Started with the Quizzer, As...", size=20, weight="bold"),
                            ft.Row(
                                controls=[
                                    ft.ElevatedButton("Quiz Master(Admin)", on_click=Quiz_Master_Page),
                                    ft.ElevatedButton("Quiz Competitor(User)", on_click=Quiz_Comp_Page),
                                ],
                                spacing=10,
                                alignment=ft.MainAxisAlignment.CENTER
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True
            )
        )
        page.update()


#
#       INITAL PAGE
#

    # initial screen
    def visit_github(e):
        page.launch_url("https://github.com/RishiAravind2004")
        
    page.add(
        ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text("Welcome to Quizzer! Create your own quizzes or challenge your knowledge with us. Let the fun begin!", size=24, weight="bold"),
                        ft.TextButton(text="Developer: Rishi Aravind!", on_click = visit_github),
                        ft.ElevatedButton("Let's GO!", on_click=Session_Page)
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

# launcher
ft.app(target=main, assets_dir="assets")
