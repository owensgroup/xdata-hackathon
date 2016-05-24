def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return (int(json['_source']['doc']['timestamp_ms']), int(json['_source']['doc']['place']['bounding_box']['coordinates'][0][0][0]),
               int(json['_source']['doc']['place']['bounding_box']['coordinates'][0][0][1]))
    except KeyError:
        return 0
