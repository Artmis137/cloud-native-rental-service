from pydantic import BaseModel

class CarBase(BaseModel):
    """_summary_
    Attributes:
        plateNumber (str): _description_
        brand (str): _description_
        price (float): _description_
    
    """
    plateNumber: str 
    brand: str 
    price: float
    is_rented: bool = False # Default value is False
    
class Dates(BaseModel):
    """_summary_
    Attributes:
        begin (str): _description_
        end (str): _description_
    
    """
    begin: str
    end: str