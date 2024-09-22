# predicted ids are between 0 to 5, representing unknown, serious, minor, possible, fatal, no-injury. 
def get_prediction_labels(id):
    prediction = ""
    if id == 0:
        prediction = "unknown"
    elif id == 1:
        prediction = "serious"
    elif id == 2:
        prediction = "minor"
    elif id == 3:
        prediction = "possible"
    elif id == 4:
        prediction = "fatal"
    elif id == 5:
        prediction = "no-injury"
    return prediction