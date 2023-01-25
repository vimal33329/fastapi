from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import Optional
from ..service import account_detail
router = APIRouter()

@router.get("/account_summary/", tags=["Get account details by rsf_id or user_id"])
async def get_by_rsf_id(rsf_id: Optional[int] = Query(None, description="Enter rsf_id to fetch data"), 
                        user_id: Optional[int] = Query(None, description="Enter user_id to fetch data"), 
                        search_name: Optional[str] = Query(None, description="Enter keyword to search name"), 
                        starts_with: Optional[str] = Query(None, description="Enter Alphabet to get data starts with that Alphabet"), 
                        duration_week: Optional[int] = Query(None, description="Enter value to get unapproved list before one week"), 
                        offset: int = 0, 
                        limit: int = Query(default=20, lte=500)):
    if rsf_id is not None:
        get_ndis_data = account_detail.get_ndis(rsf_id)
        ndis_data = list(get_ndis_data.values())
        is_ndis = True
        if (ndis_data.count([]) == len(ndis_data)):
            is_ndis = False

        if is_ndis == False:
            return account_detail.get_acc_details(rsf_id, search_name, starts_with, duration_week, offset, limit)
        elif is_ndis == True:
            return account_detail.get_account_ndis(rsf_id, search_name, starts_with, duration_week, offset, limit)
    if user_id is not None and rsf_id is None:
        return account_detail.get_account_by_user_id(user_id, search_name, starts_with, duration_week, offset, limit)
