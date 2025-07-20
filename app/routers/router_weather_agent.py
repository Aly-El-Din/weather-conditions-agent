from fastapi import APIRouter, HTTPException, Request
from ..services.weather_service import get_weather_conditions_week

router = APIRouter(prefix="/agent")

@router.post("/weather")
async def get_weather_conditions_week():
    try:
        response = get_weather_conditions_week()
        
        return 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))