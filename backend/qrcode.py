from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import qrcode
from io import BytesIO
import base64

router = APIRouter()

class QRData(BaseModel):
    name: str
    email: str
    phone: str
    website: str

@router.post("/generate_qr")
async def generate_qr(data: QRData):
    try:
        # Generate QR code with website URL
        qr = qrcode.make(data.website)

        # Convert QR Code to Base64
        buffer = BytesIO()
        qr.save(buffer, format="PNG")
        qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")

        # Return JSON response with business card details and QR code
        return {
            "name": data.name,
            "email": data.email,
            "phone": data.phone,
            "website": data.website,
            "qr_code": f"data:image/png;base64,{qr_base64}"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"QR Generation Error: {str(e)}")
    