from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users2"
    id = Column(Integer, primary_key=True)
    username = Column(String)   
    password_hashed = Column(String)
    activated = Column(Boolean)
    expiration_date = Column(Date)

def start_a_db_session(
    DB_Username_For_Admin:str,
    DB_Password_For_Admin:str,
    DB_Name_For_Admin_User:str,
    DB_IP_adress:str,
 ):
    engine = create_engine("mariadb+mariadbconnector://"+DB_Username_For_Admin+":"+DB_Password_For_Admin+"@"+DB_IP_adress+":3306/"+DB_Name_For_Admin_User)
    Session = sessionmaker(bind=engine)
    return Session()

def test_credentials(
    DB_Username_For_Admin:str,
    DB_Password_For_Admin:str,
    DB_Name_For_Admin_User:str,
    DB_IP_adress:str,
    ):
    engine = create_engine("mariadb+mariadbconnector://"+DB_Username_For_Admin+":"+DB_Password_For_Admin+"@"+DB_IP_adress+":3306/"+DB_Name_For_Admin_User)
    engine.connect()
    engine.dispose()
    return

def get_all_users(session):
    return session.query(User).all()

def get_a_single_user(session, username):
    return session.query(User).filter(User.username == username).first()
     
def get_users_by_activation(session,status):
    return session.query(User).filter((User.disabled == status)).all()

def delete_user(session, username):
    user = session.query(User).filter(User.username == username).first()
    if user:
        session.delete(user)
        session.commit()
        return user
    else:
        return None

def add_user(session, username, password, disabled):
    user = session.query(User).filter(User.username == username).first()
    if user:
        return False
    else:
        new_user = User(username=username, password_hashed=password, disabled=disabled)
        session.add(new_user)
        session.commit()
        return True

def update_user(session, username, newUsername, password, disabled, expirationDate):
    user = session.query(User).filter(User.username == username).first()
    code=[]
    if user:
        if disabled==True or disabled==False:
            user.disabled = disabled
            code.append("1")
        if password:
            user.password_hashed = password
            code.append("2")
        if newUsername:
            user.username = newUsername
            code.append("3")
        if expirationDate:
            if check_expiration_date():
                user.expiration_date = expirationDate
                code.append("4")
            else:
                code.append("5")        
        session.add(user)
        session.commit()
        return code
    else:
        return code

def activate_user(session, username):
    user = session.query(User).filter(User.username == username).first()
    if user.disabled == False:
        user.disabled = True
        session.add(user)
        session.commit()
        return True
    else:
        return False

def deactivate_user(session, username):
    user = session.query(User).filter(User.username == username).first()
    if user.disabled == True:
        user.disabled = False
        session.add(user)
        session.commit()
        return True
    else:
        return False

def check_expiration_date(session, username, expirationDate):
    user = session.query(User).filter(User.username == username).first()
    if user.expiration_date >= expirationDate:
        return False
    return True

def change_expiration_date(session, username, expirationDate):
    user = session.query(User).filter(User.username == username).first()
    user.expiration_date = expirationDate
    session.add(user)
    session.commit()
    return True
