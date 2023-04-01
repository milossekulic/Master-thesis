from logging import raiseExceptions
from typing import List
from fastapi import APIRouter,Depends,HTTPException, Response,status
from sqlalchemy.orm.session import Session
from .. database import get_db
from .. import models,schemas ,oauth2



router=APIRouter(
    prefix='/license-plate',
    tags=['License-plate']

)

@router.get('/',response_model=List[schemas.LicensePlateOut])
def get_lists( db:Session=Depends(get_db),current_user: int =Depends(oauth2.get_current_user)):
    ps=db.query(models.LicensePlate).all()
    # for i in ps:
    #     print(i.license_plate,i.owner,i.created_by,i.username)
    return  ps
    
@router.post("/")
def license_plate_list(license_plate:schemas.LicensePlateCreate,db:Session=Depends(get_db),current_user: int =Depends(oauth2.get_current_user)):
    new_license_plate=models.LicensePlate(created_by=current_user.id,** license_plate.dict())
    db.add(new_license_plate)
    db.commit()
    db.refresh(new_license_plate)
    return new_license_plate

@router.get("/{id}")
def get_license_plate_by_id(id:int ,db:Session=Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    post = db.query(models.LicensePlate).filter(models.LicensePlate.id == id).first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,
        detail=f"License plate with id {id} not found")
    return post

@router.put("/{id}",status_code=status.HTTP_200_OK)
def update_license_plate(id:int,updated_license_plate:schemas.LicensePlateCreate ,db:Session=Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    post_query=db.query(models.LicensePlate).filter(models.LicensePlate.id==id)
    post=post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"License plate with id {id} not found")
    post_query.update(updated_license_plate.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

@router.delete("/{id}" ,status_code=status.HTTP_204_NO_CONTENT)
def delete_license_plate(id:int ,db:Session=Depends(get_db), current_user: int =Depends(oauth2.get_current_user)):
    post_query=db.query(models.LicensePlate).filter(models.LicensePlate.id == id)
    post=post_query.first()
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"License plate with id {id} not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.get('/controlIn/{license_plate_number}',status_code=status.HTTP_200_OK)
def license_plate_controller_in(license_plate_number:str,db:Session=Depends(get_db)):
    ps=db.query(models.LicensePlate).filter(models.LicensePlate.license_plate == license_plate_number).first()
    if ps is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND ,detail=f"License plate with id {license_plate_number} not found")
    return  True