# file imports
import json
import utils
import datatypes
# dep imports
from typing import List, Optional, Any
from functools import reduce

# Example data to use
exampleData = [];

def get_nested_attr(obj, attr):
    """ Recursively get the attribute specified by a dotted string path."""
    attrs = attr.split('.')
    for a in attrs:
        obj = getattr(obj, a)
    return obj

def getDataIndex(field_path: str, target_value: Any) -> Optional[int]:
    """
    Finds the index of the dataclass in the array where the specified field matches the target value.
    """
    for index, item in enumerate(exampleData):
        try:
            value = get_nested_attr(item, field_path)
            if value == target_value:
                return index
        except AttributeError:
            continue
    return None

def main():
    print(exampleData[0].song.artist.yt_id)
    index = getDataIndex(field_path="song.artist.yt_id", target_value="reina - Topic")
    print(index)

# Actual start
if __name__ == "__main__":
    with open("exampleData.json") as dataFile:
        rawData = json.load(dataFile)
        for s in rawData:
            fmtData = datatypes.mattfm_item(
                song = datatypes.Song(**s["song"]),
                post = datatypes.Post(**s["post"])
            )
            fmtData.song.artist = datatypes.Artist(**s["song"]["artist"])
            exampleData.append(fmtData)
    main()