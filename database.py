from sqlalchemy import create_engine, Column, Integer, String, Boolean, Date, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users2"
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password_hashed = Column(String)
    disabled = Column(Boolean)

class DataDay(Base):
    __tablename__ = 'testwithdict'
    id = Column(Integer, primary_key=True)
    simulationDate = Column(Date)
    sample = Column(Integer)
    targetDays = Column(JSON)

def start_a_db_session(
    DB_Username_For_Admin:str,
    DB_Password_For_Admin:str,
    DB_Name_For_Admin_User:str,
    DB_Container_Name:str,
 ):
    engine = create_engine("mariadb+mariadbconnector://"+DB_Username_For_Admin+":"+DB_Password_For_Admin+"@"+DB_Container_Name+":3306/"+DB_Name_For_Admin_User)
    Session = sessionmaker(bind=engine)
    return Session()

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

def update_user(session, username, password, disabled):
    user = session.query(User).filter(User.username == username).first()
    if user:
        if username:
            user.username = username
        if password:
            user.password_hashed = password
        if disabled:
            user.disabled = disabled
        session.add(user)
        session.commit()
        return True
    else:
        return False

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

def get_datadays(session):
    return session.query(DataDay).all()

def get_simulations(session,simulationDate):
    return session.query(DataDay).filter(DataDay.simulationDate == simulationDate).all()

def get_simulations_by_sample(session, sample):
    return session.query(DataDay).filter((DataDay.simulationDate == simulationDate)&(DataDay.sample == sample)).all()

def get_simulation_for_target_day(session, simulationDate,targetedDay):
    data = get_simulation(session=session)
    output = []
    for k in range(len(data)):
        simulationDateJSON = data[k].simulationDate
        sampleJson = data[k].sample
        targetDaysJson = data[k].targetDays[str(targetedDay)]
        output.append({
            'simulationDate':simulationDateJSON,
             'sample':sampleJson,
             'targetDays':{
                 str(targetedDay):targetDaysJson
                }
        })
    return output
    