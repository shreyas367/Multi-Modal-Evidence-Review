import os

def image_ids_from_paths(path_string):
    ids = []
    for p in path_string.split(";"):
        image_id = os.path.splitext(
            os.path.basename(p)
        )[0]
        ids.append(image_id)
    return ids
