from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Insights API",
    version="1.0.0",
    description="Simple public REST API for anomaly insights."
)
app.add_middleware(
    CORSMiddleware,
    # For quick testing, allow everything:
    allow_origins=["*"],          # <-- or replace "*" with your Visual Builder URL
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# --- Data model (for docs + validation) ---

class Insight(BaseModel):
    id: str
    description: str
    pov: str
    insightType: str
    priority: str

# --- Your JSON data, as native Python list ---

INSIGHTS: List[Insight] = [
    Insight(
        description="Actual Volume 88.1% lower  in Jan FY23",
        pov="Sales US-Working-USD-Forecast.-eReader-US Market-TTM",
        insightType="Anomaly",
        id="59",
        priority="High",
    ),
    Insight(
        description="Actual Volume 85.8% lower  in Jan FY23",
        pov="Sales US-Working-USD-Forecast.-Tablet 8 in-US Market-TTM",
        insightType="Anomaly",
        id="62",
        priority="High",
    ),
    Insight(
        description="Actual Product Revenue 79.29% lower  in Jun FY24",
        pov="Sales West Region-Sentinal Standard Notebook",
        insightType="Anomaly",
        id="20",
        priority="High",
    ),
    Insight(
        description="Actual Product Revenue 76.06% lower  in Jun FY24",
        pov="Sales West Region-Sentinal Custom Notebook",
        insightType="Anomaly",
        id="19",
        priority="High",
    ),
    Insight(
        description="Predicted Staples Sales 16.20% lower than forecast",
        pov="Sales NorthEast Region-Sentinal Standard Notebook",
        insightType="Prediction",
        id="2",
        priority="High",
    ),
]

# --- Endpoints (RESTCountries-style) ---

@app.get("/insights", response_model=List[Insight])
def list_insights(
    insightType: Optional[str] = Query(None, description="Filter by insightType, e.g. 'Anomaly'"),
    priority: Optional[str] = Query(None, description="Filter by priority, e.g. 'High'"),
    pov_contains: Optional[str] = Query(None, description="Filter where POV contains this substring"),
):
    """
    Return all insights, optionally filtered by query parameters.
    Similar idea to GET /v3.1/all or filtered queries in restcountries.
    """
    results = INSIGHTS

    if insightType:
        results = [i for i in results if i.insightType.lower() == insightType.lower()]

    if priority:
        results = [i for i in results if i.priority.lower() == priority.lower()]

    if pov_contains:
        pv = pov_contains.lower()
        results = [i for i in results if pv in i.pov.lower()]

    return results


@app.get("/insights/{insight_id}", response_model=Insight)
def get_insight_by_id(insight_id: str):
    """
    Return a single insight by its ID.
    Similar idea to GET /v3.1/alpha/{code} in restcountries.
    """
    for insight in INSIGHTS:
        if insight.id == insight_id:
            return insight
    raise HTTPException(status_code=404, detail="Insight not found")


@app.get("/")
def root():
    return {
        "message": "Welcome to the Insights API. See /insights or /docs for details."
    }
