'''module for storing the data'''
import csv
import sqlalchemy as db
from database import ResponseRecords, connection
from custom_logging import loggers

def store_data(response_data,post_data):
    """Store response data in the database and write it to a CSV file"""
    if not response_data:
        loggers.error("No response data to store.")
        return

    try:
        status = response_data['meta']['status']
        msg = response_data['meta']['msg']
        post_id = response_data['response']['id']
        post_state = response_data['response']['state']
        post_display_text = response_data['response'].get('display_text', '')

        # Insert into the database
        query = db.insert(ResponseRecords).values(
            id=post_id,
            status=status,
            msg=msg,
            state=post_state,
            display_text=post_display_text,
            post_data=post_data
        )
        connection.execute(query)
        connection.commit()
        loggers.info("Post data stored successfully in the database")

        # Write into CSV file
        with open('tumblr.csv', mode='a', newline='', encoding='utf-8') as csv_file:
            fieldnames = ['status', 'msg', 'post_id', 'state', 'display_text','postdata']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
            if csv_file.tell() == 0:  # Write header if file is empty
                writer.writeheader()
            dataset = {
                'status': status,
                'msg': msg,
                'post_id': post_id,
                'state': post_state,
                'display_text': post_display_text,
                'postdata':post_data
            }
            writer.writerow(dataset)
        loggers.info("Post data written successfully to CSV")

    except ImportError as e:
        loggers.error("Failed to store post data:%s",{e})
    