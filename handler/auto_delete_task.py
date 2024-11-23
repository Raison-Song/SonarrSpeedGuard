import asyncio
from datetime import datetime, timezone

import utils.api
import utils.config
from utils.log import Logger


async def handler():
    logger = Logger.get_logger()
    logger.info("Starting download monitor handler")
    api = utils.api.SonarrAPI(utils.config.config.host, utils.config.config.apikey)

    while True:
        try:
            logger.debug("Fetching queue data from API")
            data = await api.get('v3/queue')

            if 'records' in data:
                logger.debug(f"Found {len(data['records'])} records in queue")
                await analyze_downloads(api, data['records'])
            else:
                logger.warning("No records found in queue data")

            await asyncio.sleep(utils.config.config.refresh_interval * 60)
        except Exception as e:
            logger.error(f"Error in handler: {str(e)}")
            await asyncio.sleep(60)  # Wait a minute before retrying

async def analyze_downloads(api, records):
    logger = Logger.get_logger()
    logger.info(f"Analyzing {len(records)} downloads")

    now = datetime.now(timezone.utc)
    for record in records:
        try:
            added_time = datetime.fromisoformat(record['added'].replace('Z', '+00:00'))
            elapsed_time = (now - added_time).total_seconds()

            size = record['size']
            size_left = record['sizeleft']
            downloaded = size - size_left

            # Calculate speeds
            average_speed = downloaded / elapsed_time if elapsed_time > 0 else 0
            recent_speed = 0

            # Calculate estimated time
            estimated_time = (size_left / average_speed if average_speed > 0 else 99999999) / 60

            # Calculate percentage
            percentage_downloaded = (downloaded / size) * 100 if size > 0 else 0

            logger.debug(f"Download stats for {record['title']}: "
                         f"Elapsed time: {elapsed_time/60:.2f}min, "
                         f"Average speed: {average_speed/1024:.2f}KB/s, "
                         f"Estimated time: {estimated_time:.2f}min, "
                         f"Progress: {percentage_downloaded:.2f}%")

            # Check conditions
            if process_rules(elapsed_time, average_speed, record['status'], estimated_time, percentage_downloaded):
                logger.info(f"Deleting and re-searching download - "
                            f"ID: {record['id']}, "
                            f"Title: {record['title']}, "
                            f"Status: {record['status']}")
                await delete_download(api, record['id'])

        except Exception as e:
            logger.error(f"Error processing record {record.get('id', 'unknown')}: {str(e)}")


async def delete_download(api, id):
    logger = Logger.get_logger()
    try:
        params = {
            "removeFromClient": "true",
            "blocklist": "true",
            "skipRedownload": "false",
            "changeCategory": "false"
        }
        logger.debug(f"Attempting to delete download with ID: {id}")
        await api.delete('v3/queue/' + str(id), params)
        logger.info(f"Successfully deleted download with ID: {id}")
    except Exception as e:
        logger.error(f"Failed to delete download with ID {id}: {str(e)}")


def process_rules(elapsed_time, average_speed, status, estimated_time, percentage_downloaded):
    logger = Logger.get_logger()

    if not utils.config.config.rules:
        logger.debug("No rules configured, returning True")
        return True

    isFilter = True
    logger.debug(f"Processing rules for download - "
                 f"Elapsed time: {elapsed_time/60:.2f}min, "
                 f"Speed: {average_speed/1024:.2f}KB/s, "
                 f"Status: {status}, "
                 f"Est. time: {estimated_time:.2f}min, "
                 f"Progress: {percentage_downloaded:.2f}%")

    rule_checks = {
        "C1": lambda x, et: et / 60 > float(x),
        "C2": lambda x, st: st in x.split(','),
        "C3": lambda x, as_: as_ < float(x) * 1024,
        "C4": lambda x, et: x < et,
        "C5": lambda x, pd: x > pd,
    }

    for condition, rule_dict in utils.config.config.rules:
        if not condition:
            continue

        for key, value in rule_dict.items():
            if key in rule_checks:
                result = False
                if key == "C1":
                    result = rule_checks[key](value, elapsed_time)
                    logger.debug(f"Rule C1 check: {value}min threshold, Result: {result}")
                elif key == "C2":
                    result = rule_checks[key](value, status)
                    logger.debug(f"Rule C2 check: status in {value}, Result: {result}")
                elif key == "C3":
                    result = rule_checks[key](value, average_speed)
                    logger.debug(f"Rule C3 check: speed < {value}KB/s, Result: {result}")
                elif key == "C4":
                    result = rule_checks[key](value, estimated_time)
                    logger.debug(f"Rule C4 check: est. time > {value}min, Result: {result}")
                elif key == "C5":
                    result = rule_checks[key](value, percentage_downloaded)
                    logger.debug(f"Rule C5 check: progress < {value}%, Result: {result}")
                isFilter = isFilter and result

    logger.debug(f"Final rule processing result: {isFilter}")
    return isFilter