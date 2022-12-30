from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status, Response
from firebase_admin import auth, credentials
import firebase_admin
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
# import app.models.task as task_model
# import app.schemas.task as task_schema
import app.models.user as user_model
import app.schemas.user as user_schema
from sqlalchemy.engine import Result
from typing import List, Tuple, Optional
import uuid




# cred = credentials.Certificate('./account_key.json')
# app/account_key.json
cred = credentials.Certificate('./app/account_key.json')
firebase_admin.initialize_app(cred)

def get_user(res: Response, cred: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False))):
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        print(cred)
        decoded_token = auth.verify_id_token(cred.credentials)
        # print(decoded_token)
        print("aefijaeiofjaoifje")
        print(decoded_token['uid'])
        print(decoded_token['email'])
    except Exception as err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return decoded_token

async def get_or_create_user(db: AsyncSession,res: Response, cred: HTTPAuthorizationCredentials=Depends(HTTPBearer(auto_error=False))):
    if cred is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Bearer authentication required",
            headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
        )
    try:
        print(cred)
        decoded_token = auth.verify_id_token(cred.credentials)

        result: Result = await db.execute(
        select(user_model.User).filter(
            user_model.User.uid == decoded_token['uid'],
            user_model.User.email == decoded_token['email']
            )
        )
        user: Optional[Tuple[user_model.User]] = result.first()


        # print(user)
        # print(user[0] if user is not None else None)
        if user == None:
            print("No")
            # create
            user = user_model.User(
                uid = decoded_token['uid'],
                email = decoded_token['email']
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        pass

        print(user)
        print(user[0] if user is not None else None)

        print(decoded_token['uid'])
        print(decoded_token['email'])

        print("aefijaeiofjaoifje")
    except Exception as err:
        # 通信エラーの場合
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return user



async def get_or_create_user(db: AsyncSession,decoded_token):
    # if cred is None:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Bearer authentication required",
    #         headers={'WWW-Authenticate': 'Bearer realm="auth_required"'},
    #     )
    try:
        # print(cred)
        # decoded_token = auth.verify_id_token(cred.credentials)

        result: Result = await db.execute(
        select(user_model.User).filter(
            user_model.User.uid == decoded_token['uid'],
            user_model.User.email == decoded_token['email']
            )
        )
        user: Optional[Tuple[user_model.User]] = result.first()


        # print(user)
        # print(user[0] if user is not None else None)
        if user == None:
            print("No")
            # create
            user = user_model.User(
                uid = decoded_token['uid'],
                email = decoded_token['email'],
                cid = str(uuid.uuid4())
            )
            db.add(user)
            await db.commit()
            await db.refresh(user)
            return user
        pass

        print(user)
        print(user[0] if user is not None else None)

        print(decoded_token['uid'])
        print(decoded_token['email'])

        print("aefijaeiofjaoifje")
    except Exception as err:
        # 通信エラーの場合
        print(err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials. {err}",
            headers={'WWW-Authenticate': 'Bearer error="invalid_token"'},
        )
    # res.headers['WWW-Authenticate'] = 'Bearer realm="auth_required"'
    return user