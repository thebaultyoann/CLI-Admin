from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

#DB_Username_For_Admin="root"
#DB_Password_For_Admin="lol"
#DB_Name_For_Admin_User="adminuserdatabase"
DB_Container_Name="localhost"

Base = declarative_base()

class users2(Base):
    __tablename__ = "users2"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hashed = Column(String)

def start_a_db_session(
    DB_Username_For_Admin:str,
    DB_Password_For_Admin:str,
    DB_Name_For_Admin_User:str,
 ):
    engine = create_engine("mariadb+mariadbconnector://"+DB_Username_For_Admin+":"+DB_Password_For_Admin+"@"+DB_Container_Name+":3306/"+DB_Name_For_Admin_User)
    Session = sessionmaker(bind=engine)
    return Session()

def get_user_name(session):
    print("1")
    user = session.query(users2).first()
    pritn("2")
    return user
