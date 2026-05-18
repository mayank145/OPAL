"""
Reference Tables Models - fsection, fstaff, and clients.users
These tables provide dropdown options for FATS and Summit Logging forms.
"""
from sqlalchemy import Column, String, Integer
from app.db.session import Base

class FSection(Base):
    """
    Section reference table - provides dropdown options for section and section2
    """
    __tablename__ = "fsection"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    section = Column(String(50), nullable=False)
    
    def __repr__(self):
        return f"<FSection(id={self.id}, section='{self.section}')>"

class FStaff(Base):
    """
    Staff reference table - provides dropdown options for operator
    """
    __tablename__ = "fstaff"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(15), nullable=False)
    
    def __repr__(self):
        return f"<FStaff(id={self.id}, name='{self.name}')>"



