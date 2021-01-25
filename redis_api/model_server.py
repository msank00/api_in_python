import redis
import os
import time
import json 
import numpy as np

# Connect to Redis server
REDIS_HOST="localhost" #os.environ.get("REDIS_HOST")
db = redis.StrictRedis(host=REDIS_HOST)

IMAGE_QUEUE="image_queue"# os.environ.get("IMAGE_QUEUE")

SERVER_SLEEP = 0.25  # Time in ms between each poll by model server against Redis # os.environ.get("SERVER_SLEEP")
BATCH_SIZE = 32

def get_prediction(batch:list):
    n = len(batch)
    return list(np.random.rand(n))

def classify_process():
    # Continually poll for new images to classify
    while True:
        # Pop off multiple images from Redis queue atomically
        with db.pipeline() as pipe:
            pipe.lrange(IMAGE_QUEUE, 0, BATCH_SIZE - 1)
            pipe.ltrim(IMAGE_QUEUE, BATCH_SIZE, -1)
            queue, _ = pipe.execute()

        imageIDs = []
        batch = []
        for q in queue:
            # Deserialize the object and obtain the input image
            q = json.loads(q.decode("utf-8"))
            
            # Update the list with inputs
            batch.append(q["input_text"])

            # Update the list of image IDs
            imageIDs.append(q["id"])

        # Check to see if we need to process the batch
        if len(imageIDs) > 0:
            # Classify the batch
            print(">> Batch size: {}".format(len(batch)))
            print(f"\t input: {batch}")
            preds = get_prediction(batch) # return list 
            

            # Loop over the image IDs and their corresponding set of results from our model
            for (imageID, resultSet) in zip(imageIDs, preds):
                # Initialize the list of output predictions
                
                # Store the output predictions in the database, using image ID as the key so we can fetch the results
                db.set(imageID, json.dumps(resultSet))

        # Sleep for a small amount
        time.sleep(float(SERVER_SLEEP))

if __name__ == "__main__":
    classify_process()
