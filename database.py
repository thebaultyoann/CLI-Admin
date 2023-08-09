from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

Base = declarative_base()

#User class inside the database
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String)   
    password_hashed = Column(String)
    activated = Column(Boolean)
    expiration_date = Column(Date)

#Open a session
def start_a_db_session(
    DB_Username_For_Admin:str,
    DB_Password_For_Admin:str,
    DB_Name_For_Users_Tables:str,
    DB_Container_Name:str,
 ):
    engine = create_engine("mariadb+mariadbconnector://"+DB_Username_For_Admin+":"+DB_Password_For_Admin+"@"+DB_Container_Name+":3306/"+DB_Name_For_Users_Tables)
    Session = sessionmaker(bind=engine)
    return Session()

#Check if the
# user is connected or not
def test_credentials(
    DB_Username_For_Admin:str,
    DB_Password_For_Admin:str,
    DB_Name_For_Users_Tables:str,
    DB_Container_Name:str,
    ):
    engine = create_engine("mariadb+mariadbconnector://"+DB_Username_For_Admin+":"+DB_Password_For_Admin+"@"+DB_Container_Name+":3306/"+DB_Name_For_Users_Tables)
    engine.connect()
    engine.dispose()
    return

################  ALL REQUESTS INSIDE THE DB ################
def get_all_users(session: Session):
    return session.query(User).all()

def get_a_single_user(session: Session, username):
    return session.query(User).filter(User.username == username).first()
     
def get_users_by_activation(session: Session,status):
    return session.query(User).filter((User.activated == status)).all()

def delete_user(session: Session, username):
    user = session.query(User).filter(User.username == username).first()
    if user:
        session.delete(user)
        session.commit()
        return user
    else:
        return None

def add_user(session: Session, username, password, activated):
    user = session.query(User).filter(User.username == username).first()
    if user:
        return False
    else:
        new_user = User(username=username, password_hashed=password, activated=activated)
        session.add(new_user)
        session.commit()
        return True
    
def update_user_username(session: Session, username, newUsername):
    user = session.query(User).filter(User.username == username).first()
    if user:
        user.username = newUsername
        session.add(user)
        session.commit()
        return True
    return False

def update_user_password(session: Session, username, password):
    user = session.query(User).filter(User.username == username).first()
    if user:
        user.password = password
        session.commit()
        return True
    return False

def update_user_activated(session: Session, username, activated):
    user = session.query(User).filter(User.username == username).first()
    if user:
        user.activated = activated
        session.add(user)
        session.commit()
        return True
    return False

def update_user_expiration_date(session: Session, username, expirationDate):
    user = session.query(User).filter(User.username == username).first()
    if user:
        user.expiration_date = expirationDate
        session.add(user)
        session.commit()
        return True
    return False


def activate_user(session: Session, username):
    user = session.query(User).filter(User.username == username).first()
    if user.activated == False:
        user.activated = True
        session.add(user)
        session.commit()
        return True
    else:
        return False

def deactivate_user(session: Session, username):
    user = session.query(User).filter(User.username == username).first()
    if user.activated == True:
        user.activated = False
        session.add(user)
        session.commit()
        return True
    else:
        return False

def user_expiration_date(session: Session, username, expirationDate):
    user = session.query(User).filter(User.username == username).first()
    return user.expiration_date

def check_expiration_date(session: Session, username, expirationDate):
    user = session.query(User).filter(User.username == username).first()
    if not user.expiration_date or user.expiration_date >= expirationDate:
        return False
    return True

def change_expiration_date(session: Session, username, expirationDate):
    user = session.query(User).filter(User.username == username).first()
    user.expiration_date = expirationDate
    session.add(user)
    session.commit()
    return True

# ADD ADMIN USER = last modification to this project, function created then deleted automatically. 
# First ask for the root db name
# Then ask for the root db password
# Then ask for the future admin username and password
# End by creating this admin user with the appropriate rights and deleting the full file that allowed to create him

#### OR ####

# we need to have : 
# - db used 
# - admin user/password used 
# - root user/password
# selection of rights is automatic here 





