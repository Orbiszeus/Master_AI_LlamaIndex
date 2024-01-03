import mariadb
import sys
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URI = "mariadb+mariadbconnector://master:zN4ji#F-QQ!@localhost:3306/invesment_ai"
# Connect to MariaDB Platform
"""try:
    conn = mariadb.connect(
        user="master",
        password="zN4ji#F-QQ",
        host="invesmentai.cwippl3i0akx.eu-north-1.rds.amazonaws.com",
        port=3306,
        database="invesment_ai"
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1) 
"""
"""def test_connection():
    cur.execute("SELECT countryName FROM dbo.COUNTRIES")
    print("hello")
    a = cur.fetchall()
    
    return a[0][0]"""
#cur = conn.cursor()
"""""
engine = sqlalchemy.create_engine(DATABASE_URI)
Base = declarative_base()

class Organizations(Base):
    __tablename__ = 'ORGANIZATIONS'
    organizationID = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    organizationName = sqlalchemy.Column(sqlalchemy.String(length=100))

Session = sqlalchemy.orm.sessionmaker()
Session.configure(bind=engine)
session = Session()

def addOrganization(organizationName):
    organization = Organizations(organizationName=organizationName)
    session.add(organization)
    session.commit()
    return organization.organizationID
    """