import pandas as pd
from sqlalchemy.orm import Session
from tqdm import tqdm

def upload_data(class_Name, data: pd.DataFrame, session: Session):
    """
    Uploads data to the database using bulk insert for faster performance.
    """
    # Convert dataframe to list of dictionaries
    data_dict = data.to_dict('records')

    # Bulk insert data into database table
    num_records = len(data_dict)
    with tqdm(total=num_records, desc=f"Uploading {class_Name.__tablename__}") as progress:
        session.bulk_insert_mappings(class_Name, data_dict)
        session.commit()
        progress.update(num_records)
