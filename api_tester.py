from fastapi import FastAPI, HTTPException
from firebase_admin import firestore, credentials
import firebase_admin
from dotenv import load_dotenv
import os
import uuid
from pydantic import BaseModel, EmailStr
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from typing import Tuple

# Load environment variables from .env file
load_dotenv()

# Initialize Firebase Admin SDK
cred = credentials.Certificate(
    '/Users/saiarjunshroff/Desktop/backend/loginintegrator-3cf4c-firebase-adminsdk-uvywz-01ec7d948e.json'
)
firebase_admin.initialize_app(cred)
db = firestore.client()

# Define the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins. Adjust this for production.
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.).
    allow_headers=["*"],  # Allows all headers.
)

# Pydantic model for the original user data
class User(BaseModel):
    name: str
    password: str

# Pydantic model for new login user details
class NewLoginUserDetails(BaseModel):
    confirmPassword: str
    email: EmailStr
    password: str
    userId: Optional[str] = None

# Pydantic model for work item data
class WorkItem(BaseModel):
    workItemsList: list[str]

class UpdateWorkItem(BaseModel):
    old_item: str
    new_item: str

class DeleteWorkItem(BaseModel):
    work_item: str

# Endpoint to retrieve a user by ID
@app.get("/get_user/{user_id}/")
async def get_user(user_id: str):
    try:
        doc_ref = db.collection("login_authentication").document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to add a new user
@app.post("/add_user/")
async def add_user(user: User):
    try:
        user_id = str(uuid.uuid4())
        db.collection("login_authentication").document(user_id).set(user.dict())
        return {"id": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to delete a user by ID
@app.delete("/delete_user/{user_id}/")
async def delete_user(user_id: str):
    try:
        doc_ref = db.collection("login_authentication").document(user_id)
        doc_ref.delete()
        return {"status": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get user ID by name
@app.get("/get_user_id_by_name/")
async def get_user_id_by_name(name: str):
    try:
        query = db.collection("login_authentication").where("name", "==", name).limit(1).get()
        
        if not query:
            raise HTTPException(status_code=404, detail="User not found")
        
        for doc in query:
            return {"user_id": doc.id}
        
        raise HTTPException(status_code=404, detail="User not found")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to add a new login user detail
@app.post("/add_login_user/")
async def add_login_user(user: NewLoginUserDetails):
    try:
        user_id = user.userId or str(uuid.uuid4())
        user_data = user.dict()
        user_data["userId"] = user_id
        
        db.collection("new_login_user_details").document(user_id).set(user_data)
        return {"userId": user_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to retrieve new login user details by userId
@app.get("/get_login_user/{user_id}/")
async def get_login_user(user_id: str):
    try:
        doc_ref = db.collection("new_login_user_details").document(user_id)
        doc = doc_ref.get()
        if doc.exists:
            return doc.to_dict()
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to update new login user details by userId
@app.put("/update_login_user/{user_id}/")
async def update_login_user(user_id: str, user: NewLoginUserDetails):
    try:
        doc_ref = db.collection("new_login_user_details").document(user_id)
        doc = doc_ref.get()
        if not doc.exists():
            raise HTTPException(status_code=404, detail="User not found")
        
        user_data = user.dict()
        user_data["userId"] = user_id
        doc_ref.update(user_data)
        return {"status": "User updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to delete new login user details by userId
@app.delete("/delete_login_user/{user_id}/")
async def delete_login_user(user_id: str):
    try:
        doc_ref = db.collection("new_login_user_details").document(user_id)
        doc_ref.delete()
        return {"status": "User deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to retrieve the work items list from the specific document
@app.get("/get_work_items/")
async def get_work_items():
    try:
        doc_id = "4auFIFV71epkCARvkSX9"
        doc_ref = db.collection("workItemFromAdmin").document(doc_id)
        doc = doc_ref.get()
        if doc.exists:  # Notice the removal of parentheses
            return doc.to_dict()
        raise HTTPException(status_code=404, detail="Document not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to add work items to the existing list in the specific document
@app.post("/add_work_items/")
async def add_work_items(work_items: WorkItem):
    try:
        doc_id = "4auFIFV71epkCARvkSX9"
        doc_ref = db.collection("workItemFromAdmin").document(doc_id)
        doc = doc_ref.get()
        
        if doc.exists:
            existing_data = doc.to_dict()
            existing_items = existing_data.get("workItemsList", [])
            updated_items = existing_items + work_items.workItemsList
            doc_ref.update({"workItemsList": updated_items})
            return {"status": "Work items added"}
        else:
            # If document doesn't exist, create it with the new work items
            doc_ref.set(work_items.dict())
            return {"status": "Work items added to new document"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to update a specific work item in the list
@app.put("/update_work_items/")
async def update_work_items(update_item: UpdateWorkItem):
    try:
        doc_id = "4auFIFV71epkCARvkSX9"
        doc_ref = db.collection("workItemFromAdmin").document(doc_id)
        doc = doc_ref.get()
        
        if not doc.exists:
            raise HTTPException(status_code=404, detail="Document not found")
        
        existing_data = doc.to_dict()
        work_items = existing_data.get("workItemsList", [])
        
        if update_item.old_item in work_items:
            # Replace the old item with the new item
            updated_items = [update_item.new_item if item == update_item.old_item else item for item in work_items]
            doc_ref.update({"workItemsList": updated_items})
            return {"status": "Work item updated"}
        else:
            raise HTTPException(status_code=404, detail="Work item not found in the list")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to delete the work items list from the specific document
@app.delete("/delete_work_items/")
async def delete_work_items():
    try:
        doc_id = "4auFIFV71epkCARvkSX9"
        doc_ref = db.collection("workItemFromAdmin").document(doc_id)
        doc_ref.delete()
        return {"status": "Work items deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to delete a specific work item from the list
@app.delete("/delete_work_item/")
async def delete_specific_work_item(delete_item: DeleteWorkItem):
    try:
        doc_id = "4auFIFV71epkCARvkSX9"
        doc_ref = db.collection("workItemFromAdmin").document(doc_id)
        doc = doc_ref.get()
        
        if not doc.exists:  # Corrected: .exists should be accessed as a property
            raise HTTPException(status_code=404, detail="Document not found")
        
        existing_data = doc.to_dict()
        work_items = existing_data.get("workItemsList", [])
        
        if delete_item.work_item in work_items:
            # Remove the specific item from the list
            updated_items = [item for item in work_items if item != delete_item.work_item]
            doc_ref.update({"workItemsList": updated_items})
            return {"status": "Work item deleted"}
        else:
            raise HTTPException(status_code=404, detail="Work item not found in the list")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pydantic model for work item assignment
class AssignWorkItemRequest(BaseModel):
    workItemName: str
    assignedTo: str  # User ID to whom the work item is assigned

# Assign work item to a user
@app.post("/assign_work_item/")
async def assign_work_item(request: AssignWorkItemRequest):
    try:
        # Get the user document from the new_login_user_details collection
        user_ref = db.collection("new_login_user_details").where("userId", "==", request.assignedTo).limit(1).get()
        if not user_ref:
            raise HTTPException(status_code=404, detail="User not found")
        
        # Create a new work item document in the user's userWorkItems sub-collection
        user_id = user_ref[0].id
        work_item_id = str(uuid.uuid4())  # Unique ID for the work item
        work_item_data = {
            "workItemName": request.workItemName,
            "createdBy": "admin",  # Assuming the admin is assigning it
            "assignedTo": request.assignedTo,
            "status": "pending"  # Default status
        }

        db.collection("new_login_user_details").document(user_id).collection("userWorkItems").document(work_item_id).set(work_item_data)

        return {"status": "Work item assigned successfully", "workItemId": work_item_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Retrieve all work items assigned to a specific user
@app.get("/get_user_work_items/{user_id}/")
async def get_user_work_items(user_id: str):
    try:
        # Fetch all work items from the user's userWorkItems sub-collection
        user_ref = db.collection("new_login_user_details").document(user_id).collection("userWorkItems").get()
        work_items = [item.to_dict() for item in user_ref]

        if not work_items:
            raise HTTPException(status_code=404, detail="No work items found for the user")

        return {"workItemsList": work_items}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# Endpoint to retrieve all users
@app.get("/get_all_users/")
async def get_all_users():
    try:
        # Fetch all documents from the 'new_login_user_details' collection
        users_ref = db.collection("new_login_user_details").stream()
        
        # Collect user data
        users = [user.to_dict() for user in users_ref]
        
        if not users:
            raise HTTPException(status_code=404, detail="No users found")
        
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
