import sqlalchemy;
from sqlalchemy import create_engine;
from sqlalchemy.orm import declarative_base;
from sqlalchemy import Column, Integer, String, DateTime;
from sqlalchemy import ForeignKey;
from sqlalchemy.orm import backref, relationship;
from sqlalchemy import PrimaryKeyConstraint;
from sqlalchemy.orm import sessionmaker;
from sqlalchemy import func, desc, distinct,select;
 
engine = create_engine(
      "mysql+pymysql://root:pw@127.0.0.1/PS1", echo=True);

conn = engine.connect();

# Declear the mapping
Base = declarative_base();

class Sailor(Base):
    __tablename__ = 'sailors'

    sid = Column(Integer, primary_key=True);
    sname = Column(String);
    rating = Column(Integer);
    age = Column(Integer);

    def __repr__(self):
        return "<Sailor(id=%s, name='%s', rating=%s)>" % (self.sid, self.sname, self.age);


class Boat(Base):
    __tablename__ = 'boats';

    bid = Column(Integer, primary_key=True);
    bname = Column(String);
    color = Column(String);
    length = Column(Integer);

    reservations = relationship('Reservation',
                                backref=backref('boat', cascade='delete'));

    def __repr__(self):
        return "<Boat(id=%s, name='%s', color=%s)>" % (self.bid, self.bname, self.color);

class Reservation(Base):
    __tablename__ = 'reserves';
    __table_args__ = (PrimaryKeyConstraint('sid', 'bid', 'day'), {});

    sid = Column(Integer, ForeignKey('sailors.sid'));
    bid = Column(Integer, ForeignKey('boats.bid'));
    day = Column(DateTime);

    sailor = relationship('Sailor');

    def __repr__(self):
        return "<Reservation(sid=%s, bid=%s, day=%s)>" % (self.sid, self.bid, self.day);


session = sessionmaker(bind=engine);
s = session();

# Check whther output of the orm is equal to thhe table executed by ORM
def check(sql_Statement, result_Table):
    sql_list = [];
    orm_list = [];
    with engine.connect() as connection:
        actual_result = connection.execute(sql_Statement);
        for row in actual_result:
            sql_list.append(row);
    
    for row in result_Table:
        orm_list.append(row);

    return orm_list == sql_list;

def test_Q1():
    query = "SELECT b.bid, b.bname, COUNT(*) as nReserved FROM boats b, reserves r WHERE b.bid = r.bid GROUP BY b.bid;"
    
    orm_Result = s.query(Boat.bid, Boat.bname, func.count('*').label('nReserved')).filter(Boat.bid == Reservation.bid).group_by(Boat.bid);
    
    assert check(query, orm_Result);

def test_Q3():
    query = "SELECT DISTINCT s.sname, s.sid FROM sailors s, reserves r, boats b WHERE s.sid = r.sid AND r.bid = b.bid AND b.color = 'red' AND s.sid NOT IN (SELECT s.sid FROM sailors s, boats b, reserves r WHERE s.sid = r.sid AND r.bid = b.bid AND b.color !='red');"

    sub_Query = s.query(Sailor.sid).filter(Sailor.sid == Reservation.sid, Reservation.bid == Boat.bid, Boat.color != 'red').subquery();
    
    orm_Result = s.query(distinct(Sailor.sname),Sailor.sid).filter(Sailor.sid == Reservation.sid, Reservation.bid == Boat.bid, Boat.color == 'red', Sailor.sid.not_in(select(sub_Query)));

    assert check(query, orm_Result);


def test_Q4():
    query = "SELECT b.bid, b.bname FROM boats b, reserves r WHERE b.bid = r.bid GROUP BY b.bid ORDER BY COUNT(b.bid) DESC LIMIT 1;"
    
    orm_Result = s.query(Boat.bid, Boat.bname).filter(Boat.bid == Reservation.bid).group_by(Boat.bid).order_by(desc(func.count(Boat.bid))).limit(1);
    
    assert check(query, orm_Result);

def test_Q6():
    query = "SELECT AVG(s.age) as AvgAge_10RateSailors FROM sailors s WHERE s.rating = 10;"

    orm_Result = s.query(func.avg(Sailor.age).label('AvgAge_10RateSailors')).filter(Sailor.rating == 10);
    
    assert check(query, orm_Result);

def test_Q7():
    query = "SELECT s.sid, s.sname, s.rating, MIN(s.age) as Age FROM sailors s GROUP BY s.rating;"

    orm_Result = s.query(Sailor.sid, Sailor.sname, Sailor.rating, func.min(Sailor.age).label("Age")).group_by(Sailor.rating);

    assert check(query, orm_Result);


# Part 3
# Sailor Stipend for each reservation
class Sailor_Stipend(Base):
    __tablename__ = 'sailor_Stipend';
    __table_args__ = (PrimaryKeyConstraint('sid'), {});

    sid = Column(Integer, ForeignKey('sailors.sid'));
    stipend = Column(Integer);

    sailor = relationship('Sailor');

    def __repr__(self):
        return "<Sailor_Stipend(sid=%s, stipend=%s)>" % (self.sid, self.stipend);

# Insert Additional Data
sailor_Stipends = [(22,10),(23,10),(24,20),(29,15),(31,10),(32,15),(35,8),(58,9),(59,34),(60,34),(61,6),(62,14),(64,23),(71,34),(74,11),(85,24),(88,23),(89,13),(90,24),(95,33)];

# Uncomment to 
# for sp in sailor_Stipends:
#     sailor_Stipend = Sailor_Stipend(sid=sp[0], stipend=sp[1]);
#     s.add(sailor_Stipend);

# s.commit()

def calc_SailorIncome():
    # Calculate the sailor's income from all the reservations
    result_Income = s.query(Sailor.sid, Sailor.sname, func.sum(Sailor_Stipend.stipend)).filter(Sailor.sid == Sailor_Stipend.sid, Sailor.sid == Reservation.sid).group_by(Sailor.sid);

    for row in result_Income:
        print(row);



class Inventory:
     def __init__(self, day, boatLeft):
         self.day = day;
         self.boatLeft = boatLeft;

mInventory = [];

def daily_Inventory():
    # Calculate how many Boats are left in the inventory for each day 

    boatRented = s.query(Reservation.day, func.count('*')).group_by(Reservation.day);

    for row in boatRented:
        mInventory.append(Inventory(row[0], 12-row[1]));
    


calc_SailorIncome();
daily_Inventory();

for eachDay in mInventory:
    print(str(eachDay.day) + ' '+ str(eachDay.boatLeft));
    

