import io
import csv
from fastapi.responses import StreamingResponse

def convert_resposne_to_csv(response):
    llm_csv = response.strip()
    csv_file = io.StringIO(llm_csv)
    return StreamingResponse(
        csv_file,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=weather.csv"}
    )
