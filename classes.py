from typing import Any
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, DeclarativeBase
import uuid

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False)
    master_password: Mapped[str] = mapped_column(String, nullable=False)

    passwords = relationship("Password", back_populates="user", cascade="all, delete-orphan")

    def __init__(self, username_input, password_input):
        self.username = username_input
        self.master_password = password_input
        self.id = User.make_user_id()

    @staticmethod
    def make_user_id():
        return str(uuid.uuid4())
    
    @staticmethod
    def get_user_id(Session, username_input, password_input):
        if not username_input or not password_input:
            return None
        
        with Session() as session:
            user = session.query(User).filter(
                User.username == username_input,
                User.master_password == password_input
            ).first()

            if user:
                return user.id
            else:
                return None
    
    @classmethod
    def add_user(cls, Session, username_input, password_input):
        if not username_input or not password_input:
            return {"status": "error", "message": "Username and password can't be empty"}
        
        with Session.begin() as session:
            existing_user = session.query(cls).filter_by(username=username_input).first()

            if existing_user:
                return {"status": "error", "message": "User already exists"}
            
            new_user = User(username_input, password_input)
            session.add(new_user)
        return {"status": "success", "message": "User added successfully"}
    
    @classmethod
    def delete_user(cls,Session,user_id,master_password):
        if master_password == "":
            return {"status": "error", "message": "Master password can't be empty"}
        
        with Session.begin() as session:
            query_result = session.query(User).filter(User.id==user_id, User.master_password==master_password).first()

            if not query_result:
                return {"status": "error", "message": "Master password is incorrect."}
            
            user_to_del = session.query(cls).filter(cls.id==user_id).first()

            if user_to_del:
                session.delete(user_to_del)
                return {"status": "success", "message": "User deleted successfull."} 
            else:
                return {"status": "error", "message": "User doesn't exist"}


class Password(Base):
    __tablename__ = "passwords"

    pw_id: Mapped[str] = mapped_column(primary_key=True)
    site_name: Mapped[str] = mapped_column(String, nullable=False)
    site_url: Mapped[str]
    user_id: Mapped[str] = mapped_column(ForeignKey("user_account.id"))
    password: Mapped[str] = mapped_column(String, nullable=False)

    user = relationship("User", back_populates="passwords")

    def __init__(self, user_id, site_name_input, site_url_input, password_input):
        self.pw_id = Password.make_pw_id()
        self.site_name = site_name_input
        self.site_url = site_url_input
        self.password = password_input
        self.user_id = user_id
        
    @staticmethod
    def make_pw_id():
        return str(uuid.uuid4())
    
    @classmethod
    def add_password_entry(cls, Session, user_id, site_name_input, password_input, site_url_input = None):
        if site_name_input == "" or password_input == "":
            return {"status": "error", "message": "Site Name and Password can't be empty"}
        
        with Session.begin() as session:
            existing_site_name = session.query(cls).filter(Password.user_id==user_id, Password.site_name==site_name_input).first()

            if existing_site_name:
                return {"status": "error", "message": "This site name already exists. Edit password to modify records."}
            
            new_entry = Password(user_id, site_name_input, site_url_input, password_input)
            session.add(new_entry)
        return {"status": "success", "message": "Password added successfully!"}
    
    @classmethod
    def get_password_entry(cls, Session, user_id, site_name_input):
        if not site_name_input:
            return 

        with Session.begin() as session:
            query_result = session.query(cls).filter(Password.user_id==user_id, Password.site_name==site_name_input).first()
            site_url = query_result.site_url
            password = query_result.password
        return site_url, password

    @classmethod
    def del_password(cls, Session, user_id, site_name_input, master_pw_input):
        if not master_pw_input or not site_name_input:
            return {"status": "error", "message": "Master password or site name can't be empty."}
        
        with Session.begin() as session:
            query_result = session.query(User).filter(User.id==user_id, User.master_password==master_pw_input).first()

            if not query_result:
                return {"status": "error", "message": "Master password is incorrect."}
            
            pw_del = session.query(cls).filter(cls.user_id==user_id, cls.site_name==site_name_input).first()
            
            if pw_del:
                session.delete(pw_del)
                return {"status": "success", "message": "Password deleted successfull."}
            else:
                return {"status": "error", "message": "No such record exists."}

    @classmethod
    def edit_password(cls, Session, user_id, master_password,old_name, new_name, new_url, new_password):
        if master_password == "" or old_name == "":
            return {"status": "error", "message": "Master password or site name can't be empty"}
        
        if not new_name and not new_url and not new_password:
            return {"status": "error", "message": "Fill atleast 1 field to perform edit."}
        
        with Session.begin() as session:
            query_result = session.query(User).filter(User.id==user_id, User.master_password==master_password).first()

            if not query_result:
                return {"status": "error", "message": "Master password is incorrect."}

            pw_record = session.query(cls).filter(cls.user_id==user_id, cls.site_name==old_name).first()

            if not pw_record:
                return {"status": "error", "message": "No such record exists."}

            if new_name:
                pw_record.site_name = new_name
            if new_url:
                pw_record.site_url = new_url
            if new_password:
                pw_record.password = new_password
        
        return {"status": "success", "message": "Edit successful."}