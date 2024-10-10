import PySimpleGUI as sg
from utils import get_all_user_entries

def create_main_window():
    layout = [
        [sg.Text("Username:"), sg.Input(key='-USERNAME-')],
        [sg.Text("Password:"), sg.Input(key='-PW-', password_char='*')],
        [sg.Button("Login", key="-LOGIN-", bind_return_key = True), sg.Button("Signup" , key="-SIGNUP-"), sg.Button("Exit", key="-EXIT-")],
        [sg.Text("", key='-ERROR-', text_color='red')]
    ]
    
    window = sg.Window("Password Manager", layout, finalize=True)
    
    return window

def create_user_window(Session, user_id):
    left_column = sg.Column([
        [sg.Button("View password", key="-VIEWPW-")],
        [sg.Button("Add password", key="-ADDPW-")],
        [sg.Button("Edit password", key="-EDITPW-")],
        [sg.Button("Delete password", key="-DELPW-")],
        [sg.VPush()],
        [sg.Button("Delete User", key="-DEL-USER-")],
        [sg.Button("Logout", key="-LOGOUT-")]
    ], element_justification='left', expand_y=True)

    add_pw_column = sg.Column([
        [sg.Text("Site name"), sg.Push(), sg.Input(key="-SITE-")],
        [sg.Text("URL (optional)"), sg.Push(), sg.Input(key="-SITE-URL-")],
        [sg.Text("Password"), sg.Push(), sg.Input(key="-SITE-PW-", password_char="*")],
        [sg.Button("Save Password", key="-SAVEPW-")],
        [sg.Text("", key="-ADD-WARN-", text_color='red', font=('Helvetica', 12, 'bold'))]
    ], key="-ADD-PW-COL-", visible=False)

    all_entries = get_all_user_entries(Session, user_id)

    view_pw_column = sg.Column([
        [sg.Text("Select Site to View"), sg.Combo(all_entries, key="-VIEW-ALL-ENTRIES-", enable_events=True)],
        [sg.Text("Site Name: "), sg.Text("", key="-VIEW-S-NAME-")],
        [sg.Text("Site URL: "), sg.Text("", key="-VIEW-S-URL-")],
        [sg.Text("Password: "), sg.Text("", key="-VIEW-S-PW-")]
    ], key="-VIEW-PW-COL-", visible=True)

    edit_pw_column = sg.Column([
        [sg.Text("The fields that are left empty will remain the same.", font=('Helvetica', 10, 'bold'))],
        [sg.Text("Atleast 1 field needs to be filled to perform edit.", font=('Helvetica', 10, 'bold'))],
        [sg.Text("Select Site to Edit"), sg.Combo(all_entries, key="-EDIT-ALL-ENTRIES-")],
        [sg.Text("Master password:"),sg.Push(), sg.Input(key="-EDIT-M-PW-",password_char="*")],
        [sg.Text("New site name"), sg.Push(), sg.Input(key="-EDIT-NEW-NAME-")],
        [sg.Text("New URL (Optional)"), sg.Push(), sg.Input(key="-EDIT-NEW-URL-")],
        [sg.Text("New Password"), sg.Push(), sg.Input(key="-EDIT-NEW-PW-", password_char="*")],
        [sg.Button("Save changes", key="-EDIT-SAVE")],
        [sg.VPush()],
        [sg.Text("", key="-EDIT-WARN-", text_color='red', font=('Helvetica', 12, 'bold'))]
    ], key="-EDIT-PW-COL-", visible=False)

    delete_pw_column = sg.Column([
        [sg.Text("Select Site to Delete:"), sg.Combo(all_entries, key="-DEL-ALL-ENTRIES-")],
        [sg.Text("Master password:")],
        [sg.Input(key="-DEL-M-PW-",password_char="*")],
        [sg.Button("Delete Password", key="-DELETE-SELECT-")],
        [sg.Text("", key="-DEL-WARN-", text_color='red', font=('Helvetica', 12, 'bold'))]
    ], key="-DELETE-PW-COL-", visible=False)

    delete_user_column = sg.Column([
        [sg.Text("Enter master password:")],
        [sg.Input(key="-DELU-M-PW-")],
        [sg.Button("Delete User", key="-DELU-BUTTON-")],
        [sg.Text("", key="-DELU-WARN-", text_color='red', font=('Helvetica', 12, 'bold'))]
    ], key="-DEL-USER-COL-", visible=False)

    layout = [
        [left_column, 
        sg.VSeparator(), sg.Column([[sg.pin(view_pw_column)],[sg.pin(add_pw_column)], [sg.pin(edit_pw_column)], [sg.pin(delete_pw_column)], [sg.pin(delete_user_column)]])
        ]
    ]

    window = sg.Window("User Page", layout, finalize=True)
    return window