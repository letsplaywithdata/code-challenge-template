import pandas as pd
from sqlalchemy import insert
from sqlalchemy.orm import Session
from tqdm import tqdm

def upload_data(class_Name, data: pd.DataFrame, session: Session, batch_size=1000):
    """
    Uploads data to the database using bulk insert for faster performance.
    """
    # Convert dataframe to list of dictionaries
    data_dict = data.to_dict('records')

    # Insert data into database table in chunks
    num_records = len(data_dict)
    with tqdm(total=num_records, desc=f"Uploading {class_Name.__tablename__}") as progress:
        for i in range(0, num_records, batch_size):
            chunk = data_dict[i:i+batch_size]
            stmt = insert(class_Name).values(chunk)
            session.execute(stmt)
            session.commit()
            progress.update(len(chunk))
