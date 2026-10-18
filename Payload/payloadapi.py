
from fastapi import FastAPI, HTTPException, Body
from typing import Any
import httpx

app = FastAPI()

# Your existing AWS API Gateway POST endpoint
API_GATEWAY_URL = "https://0i0rytnq8k.execute-api.us-east-1.amazonaws.com/dev/employees"


@app.post("/employees")
async def create_employee(
    employee: dict[str, Any] = Body(...)
):
    try:
        # Send the employee payload to AWS API Gateway
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(
                API_GATEWAY_URL,
                json=employee
            )

        # Check whether API Gateway returned an error
        if not 200 <= response.status_code < 300:
            try:
                error_response = response.json()
            except ValueError:
                error_response = response.text

            raise HTTPException(
                status_code=response.status_code,
                detail={
                    "message": "AWS API Gateway returned an error",
                    "gateway_response": error_response
                }
            )

        # Return the successful API Gateway response
        try:
            return response.json()
        except ValueError:
            return {"message": response.text}

    except httpx.TimeoutException:
        raise HTTPException(
            status_code=504,
            detail="AWS API Gateway request timed out"
        )

    except httpx.RequestError as exc:
        raise HTTPException(
            status_code=502,
            detail=f"Could not connect to AWS API Gateway: {exc}"
        )
