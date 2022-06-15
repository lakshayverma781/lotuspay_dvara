import logging
from fastapi import Depends
from lotuspay_nach_service.data.logs_model import applogs
from databases import Database
from lotuspay_nach_service.data.database import get_database, sqlalchemy_engine


async def nach_log():
    logger = logging.getLogger("arthmate-lender-handoff-service")
    logfile_handler = logging.FileHandler('lotuspay-nach-service/logs/lotuspay_nach_logs.log')
    logfile_handler.setLevel(logging.DEBUG)
    logger.addHandler(logfile_handler)
    return logger


async def save_log(request_str, response_str, created_date, db: Database = Depends(get_database)):
    print('coming inside save_log')

    log_info = {
        'request': request_str,
        'response': response_str,
        'created_date': created_date
    }
    print(log_info)
    insert_query = applogs.insert().values(log_info)
    source_id = await db.execute(insert_query)
    print(insert_query)
    return None
    # source_id = await database.execute(insert_query)