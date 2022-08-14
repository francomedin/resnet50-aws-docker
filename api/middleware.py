import time
import redis
import settings
import uuid
import json

db = redis.Redis(
host=settings.REDIS_IP, 
port=settings.REDIS_PORT, 
db=settings.REDIS_DB_ID
)



def model_predict(image_name):
    """
    Receives an image name and queues the job into Redis.
    Will loop until getting the answer from our ML service.

    Parameters
    ----------
    image_name : str
        Name for the image uploaded by the user.

    Returns
    -------
    prediction, score : tuple(str, float)
        Model predicted class as a string and the corresponding confidence
        score as a number.
    """
   
    job_id = str(uuid.uuid4())
    job_data =  {
    "id": job_id,
    "image_name": image_name,
    }
    job_data = json.dumps(job_data)
    
    db.rpush(settings.REDIS_QUEUE, job_data)
    # Loop until we received the response from our ML model
    while True:
        if db.exists(job_id):
            model_prediction = db.get(job_id)
            db.delete(job_id)
            break
        time.sleep(settings.API_SLEEP)
    dict_pred = json.loads(model_prediction)

    return dict_pred["prediction"], dict_pred["score"]


    
