
from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from datetime import datetime
from databases import Database
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine, insert_logs
from lotuspay_nach_service.data.settings_model import (
    settings,
    SettingsBase,
    SettingsDB,
    SettingsCreate,
)


router = APIRouter()


@router.post("/settings", status_code=status.HTTP_202_ACCEPTED,  tags=["Settings"])
async def create_update_settings(
    settings_insert: SettingsCreate, database: Database = Depends(get_database)
) -> SettingsDB:

    try:
        settings_info = settings_insert.dict()
        settings_info['created_date'] = datetime.now()
        select_settings_query = settings.select()
        settings_id = await database.fetch_one(select_settings_query)
        print('getting settings from table - ', settings_id)
        if settings_id is not None:
            print('settings has value')
            query = settings.update().values(
                number_of_sources_to_pick=settings_info.get('number_of_sources_to_pick'), number_of_iterations=settings_info.get('number_of_iterations'), created_date=settings_info.get('created_date'))
            settings_id = await database.execute(query)
            print('updating the settings - ', settings_id)
        else:
            print('settings is none')
            insert_query = settings.insert().values(settings_info)
            settings_id = await database.execute(insert_query)
        result = {"settings_info": settings_info, "settings_status": "Updated"}
    except Exception as e:
        log_id = await insert_logs('MYSQL', 'DB', 'NA', '500', 'Error Occurred at DB level',
                                   datetime.now())
        result = JSONResponse(status_code=500, content={"message": f"Error Occurred at DB level - {e.args[0]}"})
    return result