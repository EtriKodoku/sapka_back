from db import get_db
from fastapi import APIRouter

router = APIRouter()

@router.get('/')
def test(db: MongoClient = Depends(get_db)):
    return {'message': db.fastapp.cards.find()}