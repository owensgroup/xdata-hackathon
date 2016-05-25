def extract_time(json):
    try:
        # Also convert to int since update_time will be string.  When comparing
        # strings, "10" is smaller than "2".
        return (int(json['_source']['created_time']), int(json['_source']['geoloc']['lon']), int(json['_source']['geoloc']['lat']))
    except KeyError:
        return 0
    except TypeError:
        return 0
