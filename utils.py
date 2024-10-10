from classes import Password, User
import PySimpleGUI as sg

def get_all_user_entries(Session, user_id):
    with Session() as session:
        query_result = session.query(Password.site_name).filter_by(user_id=user_id).all()

        site_names = [obj.site_name for obj in query_result]
    return site_names

def user_window_functions(window, window_main, event, values, Session, user_id):
    if event == "-ADDPW-":
        window["-EDIT-PW-COL-"].update(visible=False)
        window["-DELETE-PW-COL-"].update(visible=False)
        window["-VIEW-PW-COL-"].update(visible=False)
        window["-DEL-USER-COL-"].update(visible=False)
        window["-ADD-PW-COL-"].update(visible=True)

    if event == "-EDITPW-":
        all_entries = get_all_user_entries(Session, user_id)
        window["-EDIT-ALL-ENTRIES-"].update(values=all_entries)

        window["-DELETE-PW-COL-"].update(visible=False)
        window["-ADD-PW-COL-"].update(visible=False)
        window["-VIEW-PW-COL-"].update(visible=False)
        window["-DEL-USER-COL-"].update(visible=False)
        window["-EDIT-PW-COL-"].update(visible=True)

    if event == "-DELPW-":
        all_entries = get_all_user_entries(Session, user_id)
        window["-DEL-ALL-ENTRIES-"].update(values=all_entries)

        window["-EDIT-PW-COL-"].update(visible=False)
        window["-VIEW-PW-COL-"].update(visible=False)
        window["-ADD-PW-COL-"].update(visible=False)
        window["-DEL-USER-COL-"].update(visible=False)
        window["-DELETE-PW-COL-"].update(visible=True)

    if event == "-DEL-USER-":
        window["-EDIT-PW-COL-"].update(visible=False)
        window["-VIEW-PW-COL-"].update(visible=False)
        window["-ADD-PW-COL-"].update(visible=False)
        window["-DELETE-PW-COL-"].update(visible=False)
        window["-DEL-USER-COL-"].update(visible=True)

    if event == "-VIEWPW-":
        all_entries = get_all_user_entries(Session, user_id)
        window["-VIEW-ALL-ENTRIES-"].update(values=all_entries)
        
        window["-EDIT-PW-COL-"].update(visible=False)
        window["-DELETE-PW-COL-"].update(visible=False)
        window["-ADD-PW-COL-"].update(visible=False)
        window["-DEL-USER-COL-"].update(visible=False)
        window["-VIEW-PW-COL-"].update(visible=True)

    if event == "-VIEW-ALL-ENTRIES-":
        site_name_input = values["-VIEW-ALL-ENTRIES-"]
        site_url, password = Password.get_password_entry(Session, user_id, site_name_input)

        window["-VIEW-S-NAME-"].update(site_name_input)
        window["-VIEW-S-URL-"].update(site_url)
        window["-VIEW-S-PW-"].update(password)

    if event == "-DELU-BUTTON-":
        master_pw = values["-DELU-M-PW-"]
        if delete_popup():
            result = User.delete_user(Session,user_id,master_pw)

            window["-DELU-WARN-"].update(result["message"],font=('Helvetica', 10, 'bold'), text_color="red" if result["status"] == "error" else "green")

            if result["status"] == "success":
                user_id = None
                window.close()
                window = None
                window_main.un_hide()



    if event == "-SAVEPW-":
        site_name = values["-SITE-"]
        site_url = values["-SITE-URL-"]
        password = values["-SITE-PW-"]

        result = Password.add_password_entry(Session, user_id, site_name, password, site_url)

        window["-ADD-WARN-"].update(result["message"],font=('Helvetica', 10, 'bold'), text_color="red" if result["status"] == "error" else "green")

    if event == "-EDIT-SAVE":
        old_name = values["-EDIT-ALL-ENTRIES-"]
        master_password = values["-EDIT-M-PW-"]
        new_name = values["-EDIT-NEW-NAME-"]
        new_url = values["-EDIT-NEW-URL-"]
        new_password = values["-EDIT-NEW-PW-"]

        result = Password.edit_password(Session, user_id, master_password, old_name, new_name, new_url, new_password) 

        window["-EDIT-WARN-"].update(result["message"],font=('Helvetica', 10, 'bold'), text_color="red" if result["status"] == "error" else "green")

    if event == "-DELETE-SELECT-" and values["-DEL-ALL-ENTRIES-"]:
        site_name = values["-DEL-ALL-ENTRIES-"]
        master_password = values["-DEL-M-PW-"]

        result = Password.del_password(Session, user_id, site_name, master_password)

        window["-DEL-WARN-"].update(result["message"],font=('Helvetica', 10, 'bold'), text_color="red" if result["status"] == "error" else "green")


def main_window_functions(window, event, values, Session):
    if event == "-SIGNUP-":      
        username = values['-USERNAME-']
        password = values['-PW-']

        result = User.add_user(Session, username, password)

        window["-ERROR-"].update(result["message"],font=('Helvetica', 10, 'bold'), text_color="red" if result["status"] == "error" else "green")

def delete_popup():
    if sg.popup_yes_no("Are your sure you want to delete this account.", no_titlebar=False, keep_on_top=True, modal=True, location=(None, None)) == "Yes":
        return True
    else:
        return False