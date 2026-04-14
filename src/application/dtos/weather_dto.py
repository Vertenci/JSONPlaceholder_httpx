from dataclasses import dataclass


@dataclass
class WeatherResponseDTO:
    city: str
    temperature: float
    feels_like: float
    humidity: float
    description: str
    wind_speed: float
    units: str
