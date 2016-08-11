from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, Integer, String, ForeignKey, create_engine, Table, Text, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from pecan import conf

"""
Classes mapped using the Declarative system are defined in terms of a base
class which maintains a catalog of classes and tables relative to that base -
this is known as the declarative base class
"""
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    password = Column(String)
    fullname = Column(String)
    email = Column(String)
    phone = Column(Integer)
    admin = Column(Integer)

    def __repr__(self):
        return "<User(user_id='%s', fullname='%s', password='%s', email='%s', phone='%s', admin='%s')>" % \
               (self.user_id, self.fullname, self.password, self.email, self.phone, self.admin)

class Sis_client(Base):
    __tablename__ = 'sis_clients'

    id = Column(Integer, primary_key=True)
    sis_client_id = Column(String)
    detail = Column(String)
    last_keepalive = Column(String)
    state = Column(Integer)

#Relacion muchos a muchos entre users y sistemas clientes
user_sis_client_association = Table('association', Base.metadata,
    Column('user_id', Integer, ForeignKey('users.id')),
    Column('sis_client_id', Integer, ForeignKey('sis_clients.id'))
)

class Alert_CO(Base):
    __tablename__ = 'alerts_co'

    id = Column(Integer, primary_key=True)
    sis_client_id = Column(Integer, ForeignKey('sis_clients.id'))
    timestamp = Column(String)
    measure_value = Column(String)

class Alert_fail_sensor(Base):
    __tablename__ = 'alerts_failsensor'

    id = Column(Integer, primary_key=True)
    sis_client_id = Column(Integer, ForeignKey('sis_clients.id'))
    timestamp = Column(String)

#Funciones de la base de datos
def init_model():
    motor = create_engine('sqlite:///data/co_server.db')
    #Crea la base de datos (tablas)
    Base.metadata.create_all(motor)
    return motor

#Crea una sesion para comunicarse con la base de datos
engine = init_model()


def get_all_users():
    Session = sessionmaker(bind=engine)
    sess = Session()
    return sess.query(User).all()


def get_user(user_id='none', email='none', phone=0):
    Session = sessionmaker(bind=engine)
    sess = Session()
    aux = sess.query(User).filter(User.user_id == user_id).first()
    aux2 = sess.query(User).filter(User.email == email).first()
    aux3 = sess.query(User).filter(User.phone == phone).first()
    if aux:
        return aux
    elif aux2:
        return aux2
    elif aux3:
        return aux3
    else:
        return


def add_user(user_id, password, fullname, email, phone, admin):
    try:
        Session = sessionmaker(bind=engine)
        sess = Session()
        new_user = User(user_id=user_id, password=password, fullname=fullname, email=email, phone=phone, admin=admin)
        sess.add(new_user)
        sess.commit()
        return True
    except ValueError:
        return False




