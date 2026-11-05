from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(
    title="Zoo Visitors API 2569",
    description="API รายงานสถิติจำนวนผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569",
    version="1.0.0"
)

# ข้อมูลอ้างอิงจากโจทย์
RESOURCE_ID = "0ecc96cf-d914-42a1-b184-dbbd013c3c9c"
DATA_GO_TH_API_URL = f"https://data.go.th/api/3/action/datastore_search?resource_id={RESOURCE_ID}"

@app.get("/api/zoo-visitors")
async def get_zoo_visitors():
    """
    ดึงข้อมูลสถิติจำนวนผู้เข้าชมสวนสัตว์ ปีงบประมาณ 2569 จาก Data.go.th
    """
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(DATA_GO_TH_API_URL, timeout=10.0)
            
        if response.status_code == 200:
            data = response.json()
            records = data.get("result", {}).get("records", [])
        else:
            records = []
    except Exception as e:
        # หากเชื่อมต่อไม่ได้ ให้คืนค่าลิสต์ว่างไว้ล่วงหน้า
        records = []

    return {
        "source": "Data.go.th - องค์การสวนสัตว์แห่งประเทศไทย ในพระบรมราชูปถัมภ์",
        "fiscal_year": "2569",
        "resource_id": RESOURCE_ID,
        "total_records": len(records),
        "data": records
    }
