from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from datetime import datetime

class BrewStatus(BaseModel):
    connected: bool = False
    mode: str = 'idle'
    phase: str = 'Ready'
    progress: int = 0
    temperature_c: float = 20.0
    target_c: float = 0.0
    elapsed_min: int = 0
    remaining_min: int = 0
    heaters: bool = False
    pumps: Dict[str, bool] = Field(default_factory=lambda: {'mash': False, 'sparge': False})
    valves: Dict[str, bool] = Field(default_factory=dict)
    firmware: str = 'unknown'
    last_update: str = Field(default_factory=lambda: datetime.utcnow().isoformat() + 'Z')
    raw: Dict[str, Any] = Field(default_factory=dict)

class RecipeStep(BaseModel):
    name: str
    kind: str = 'mash'
    temperature_c: float = 65
    duration_min: int = 60
    note: str = ''

class Recipe(BaseModel):
    name: str
    batch_l: float = 20
    boil_min: int = 60
    grain_bill: List[Dict[str, Any]] = Field(default_factory=list)
    hops: List[Dict[str, Any]] = Field(default_factory=list)
    steps: List[RecipeStep] = Field(default_factory=list)
    notes: str = ''

class CommandRequest(BaseModel):
    command: str
    payload: Optional[Dict[str, Any]] = None
