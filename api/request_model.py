from pydantic import BaseModel

class InputData(BaseModel):
    airline: str
    flight: str
    source_city: str
    departure_time: str
    stops: str
    arrival_time: str
    destination_city: str
    Class: str
    duration: float
    days_left : int
