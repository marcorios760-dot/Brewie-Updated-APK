from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    brewie_transport: str = Field('mock', alias='BREWIE_TRANSPORT')
    brewie_host: str = Field('192.168.1.50', alias='BREWIE_HOST')
    brewie_port: int = Field(8332, alias='BREWIE_PORT')
    brewie_http_base: str = Field('http://192.168.1.50:8081', alias='BREWIE_HTTP_BASE')
    brewie_serial_port: str = Field('/dev/ttyUSB0', alias='BREWIE_SERIAL_PORT')
    brewie_serial_baud: int = Field(115200, alias='BREWIE_SERIAL_BAUD')
    recipe_dir: str = Field('recipes', alias='RECIPE_DIR')

    class Config:
        env_file = '.env'
        populate_by_name = True

settings = Settings()

# Update these values to match the exact ReBrewie firmware command names on your unit.
COMMANDS = {
    'status': 'STATUS',
    'start': 'START',
    'pause': 'PAUSE',
    'resume': 'RESUME',
    'stop': 'STOP',
    'heat_on': 'HEAT ON',
    'heat_off': 'HEAT OFF',
    'pump_mash_on': 'PUMP MASH ON',
    'pump_mash_off': 'PUMP MASH OFF',
    'pump_sparge_on': 'PUMP SPARGE ON',
    'pump_sparge_off': 'PUMP SPARGE OFF',
    'valves_close': 'VALVES CLOSE',
    'firmware': 'VERSION',
}
