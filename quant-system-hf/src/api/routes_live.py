from fastapi import APIRouter
router = APIRouter()
@router.get('/live/status')
def status():
    return {'live':'disabled'}
