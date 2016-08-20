
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import  Column, Integer, String, ForeignKey, create_engine, Table, Text, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session, relationship
from pecan import conf
import datetime
import time

"""
Classes mapped using the Declarative system are defined in terms of a base
class which maintains a catalog of classes and tables relative to that base -
this is known as the declarative base class
"""
Base = declarative_base()

#Relacion muchos a muchos entre users y sistemas clientes
user_sis_client_association = Table('user_sis_client_association', Base.metadata,
                                    Column('user_id', ForeignKey('users.id'), primary_key=True),
                                    Column('client_system_id', ForeignKey('client_systems.id'), primary_key=True))

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_id = Column(String)
    password = Column(String)
    fullname = Column(String)
    email = Column(String)
    phone = Column(Integer)
    admin = Column(Integer)

    client_systems = relationship('Client_system',
                                 secondary=user_sis_client_association,
                                 back_populates='users')

    def __repr__(self):
        return "<User(user_id='%s', fullname='%s', password='%s', email='%s', phone='%s', admin='%s')>" % \
               (self.user_id, self.fullname, self.password, self.email, self.phone, self.admin)

class Client_system(Base):
    __tablename__ = 'client_systems'

    id = Column(Integer, primary_key=True)
    client_system_id = Column(String)
    detail = Column(String)
    last_keepalive = Column(String)
    state = Column(Integer)

    users = relationship('User',
                        secondary=user_sis_client_association,
                        back_populates='client_systems')

    co_alerts= relationship('Alert_CO')
    fail_sensor_alerts= relationship('Alert_fail_sensor')

    def __repr__(self):
        return "<Client_system(client_system_id='%s', detail='%s', last_keepalive='%s', state='%s')>" % \
               (self.client_system_id, self.detail, self.last_keepalive, self.state)


class Alert_CO(Base):
    __tablename__ = 'alerts_co'

    id = Column(Integer, primary_key=True)
    client_system_id = Column(Integer, ForeignKey('client_systems.id'))
    timestamp = Column(String)
    measure_value = Column(String)

    def __repr__(self):
        return "Alert_CO(client_system_id='%s', timestamp='%s', measure_value='%s')" % \
               (self.client_system_id, self.timestamp, self.measure_value)

class Alert_fail_sensor(Base):
    __tablename__ = 'alerts_failsensor'

    id = Column(Integer, primary_key=True)
    client_system_id = Column(Integer, ForeignKey('client_systems.id'))
    timestamp = Column(String)

    def __repr__(self):
        return "Alert_CO(client_system_id='%s', timestamp='%s')" % \
               (self.client_system_id, self.timestamp)


#Funciones de la base de datos
def _engine_from_config(configuration):
    configuration = dict(configuration)
    url = configuration.pop('url')
    return create_engine(url, **configuration)


def init_model():
    conf.sqlalchemy.engine = _engine_from_config(conf.sqlalchemy)
    Base.metadata.create_all(conf.sqlalchemy.engine)

init_model()

#FUNCIONES PARA USERS
def get_all_users():
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    return sess.query(User).all()


def get_user(user_id='none', email='none', phone=0):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
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
        Session = sessionmaker(bind=conf.sqlalchemy.engine)
        sess = Session()
        new_user = User(user_id=user_id, password=password, fullname=fullname, email=email, phone=phone, admin=admin)
        sess.add(new_user)
        sess.commit()
        return True
    except ValueError:
        return False


def del_user(user_id='none', email='none', phone=0):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    if sess.query(User).filter(User.user_id == user_id).count():
        sess.delete(sess.query(User).filter(User.user_id == user_id).first())
    elif sess.query(User).filter(User.email == email).count():
        sess.delete(sess.query(User).filter(User.email == email).first())
    elif sess.query(User).filter(User.phone == phone).count():
        sess.delete(sess.query(User).filter(User.phone == phone).first())
    sess.commit()


def edit_user(user_id_old='none', email_old='none', phone_old=0,
              user_id='null', password='null', fullname='null', email='null', phone=0, admin=1):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    if sess.query(User).filter(User.user_id == user_id_old).count():
        sess.query(User).filter(User.user_id == user_id_old).update({"user_id" : user_id, "password" : password,
                                                                     "fullname" : fullname, "email" : email,
                                                                     "phone" : phone, "admin" : admin})
    elif sess.query(User).filter(User.email == email_old).count():
        sess.query(User).filter(User.email == email_old).update({"user_id" : user_id, "password" : password,
                                                                     "fullname" : fullname, "email" : email,
                                                                     "phone" : phone, "admin" : admin})
    elif sess.query(User).filter(User.phone == phone_old).count():
        sess.query(User).filter(User.phone == phone_old).update({"user_id" : user_id, "password" : password,
                                                                     "fullname" : fullname, "email" : email,
                                                                     "phone" : phone, "admin" : admin})
    sess.commit()


"""FUNCIONES PARA CLIENT_SYSTEMS"""
def get_all_client_systems():
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    return sess.query(Client_system).all()


def get_client_system(client_system_id):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    return sess.query(Client_system).filter(Client_system.client_system_id == client_system_id).first()


def add_client_system(client_system_id):
    try:
        Session = sessionmaker(bind=conf.sqlalchemy.engine)
        sess = Session()
        new_client_system = Client_system(client_system_id=client_system_id, detail='null', last_keepalive='null', state=1)
        sess.add(new_client_system)
        sess.commit()
        return True
    except ValueError:
        return False


def del_client_system(client_system_id):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    if sess.query(Client_system).filter(Client_system.client_system_id == client_system_id).count():
        sess.delete(sess.query(Client_system).filter(Client_system.client_system_id == client_system_id).first())
    sess.commit()


def edit_client_system(client_system_id_old, client_system_id, detail):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    if sess.query(Client_system).filter(Client_system.client_system_id == client_system_id_old).count():
            sess.query(Client_system).\
                filter(Client_system.client_system_id == client_system_id_old).\
                update({"client_system_id" : client_system_id, "detail" : detail})
    sess.commit()


def keepalive_client_system(client_system_id):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    ts = time.time()
    timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    if sess.query(Client_system).filter(Client_system.client_system_id == client_system_id).count():
            sess.query(Client_system).\
                filter(Client_system.client_system_id == client_system_id).\
                update({"last_keepalive" : timestamp, "state" : 1})
    sess.commit()


def add_client_system_to_user(user_email, client_system_id):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    aux = sess.query(User).filter(User.email==user_email).first()
    aux.client_systems.append(sess.query(Client_system).filter(Client_system.client_system_id == \
                                                              client_system_id).first())
    sess.commit()


def add_co_alert(clientsystem_id, measure_value):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    ts = time.time()
    timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    new_co_alert = Alert_CO(client_system_id=clientsystem_id, timestamp=timestamp, measure_value=measure_value)
    sess.add(new_co_alert)
    sess.commit()


def add_fail_system_alert(clientsystem_id):
    Session = sessionmaker(bind=conf.sqlalchemy.engine)
    sess = Session()
    ts = time.time()
    timestamp=datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    new_fail_system_alert = Alert_fail_sensor(client_system_id=clientsystem_id, timestamp=timestamp)
    sess.add(new_fail_system_alert)
    sess.commit()
