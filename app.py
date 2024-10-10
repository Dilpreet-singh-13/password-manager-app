from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import PySimpleGUI as sg
from layouts import create_main_window, create_user_window
from classes import User, Password, Base
from utils import user_window_functions, main_window_functions
from dotenv import load_dotenv
import os

def main():
    load_dotenv()

    username = os.getenv('DB_USERNAME')
    db_password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    db_name = os.getenv('DB_NAME')

    engine = create_engine(f"postgresql+psycopg2://{username}:{db_password}@{host}/{db_name}")

    Base.metadata.create_all(engine)
    Session = sessionmaker(engine)

    sg.theme('BlueMono')
    window_main = create_main_window()
    window_user = None

    user_id = None

    while True:
        window, event, values = sg.read_all_windows()
        print(event, values)
        if window == window_main and event in (sg.WIN_CLOSED, "-EXIT-"):
            break
        
        if window == window_main and event == "-LOGIN-":
            username = values['-USERNAME-']
            password = values['-PW-']
            user_id = User.get_user_id(Session, username, password)

            window_main["-ERROR-"].update(f"User {username} successfully logged in." if user_id else "Such user does not exist.", text_color="green" if user_id else "red", font=('Helvetica', 10, 'bold'))

            if not user_id:
                continue
            
            window_main.hide()
            window_user = create_user_window(Session, user_id)

        if window == window_main and event == "-SIGNUP-":
            main_window_functions(window_main, event, values, Session)

        if window == window_user:
            user_window_functions(window_user, window_main, event, values, Session, user_id)

        if window == window_user and (event in (sg.WIN_CLOSED, "-LOGOUT-")):
            user_id = None
            window_user.close()
            window_user = None
            window_main.un_hide()

    window.close()

if __name__ == "__main__":
    main()