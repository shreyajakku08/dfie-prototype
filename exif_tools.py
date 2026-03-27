import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def extract_exif_data(image_path):
    """
    Extracts EXIF metadata from an image, focusing on Device Info and GPS Coordinates.
    Returns a dictionary of the found intelligence.
    """
    metadata = {
        "device": "Unknown",
        "date_taken": "Unknown",
        "gps_coordinates": None,
        "other_tags": []
    }
    
    try:
        image = Image.open(image_path)
        exif_info = image._getexif()
        
        if not exif_info:
            return {"error": "No EXIF metadata found in this image. It may have been scrubbed or it's not a photo."}
            
        for tag, value in exif_info.items():
            tag_name = TAGS.get(tag, tag)
            
            # Skip very long binary data (like MakerNotes or PrintIM) to keep JSON clean
            if isinstance(value, bytes):
                continue
                
            if tag_name == "Model":
                metadata["device"] = value
            elif tag_name == "DateTimeOriginal":
                metadata["date_taken"] = value
            elif tag_name == "GPSInfo":
                gps_data = {}
                for t in value:
                    sub_tag = GPSTAGS.get(t, t)
                    gps_data[sub_tag] = value[t]
                
                # Format GPS Coordinates if available
                if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
                    try:
                        lat = convert_to_degrees(gps_data['GPSLatitude'])
                        if gps_data.get('GPSLatitudeRef') != 'N':
                            lat = 0 - lat
                        
                        lon = convert_to_degrees(gps_data['GPSLongitude'])
                        if gps_data.get('GPSLongitudeRef') != 'E':
                            lon = 0 - lon
                            
                        metadata["gps_coordinates"] = f"{lat:.5f}, {lon:.5f}"
                    except Exception as ge:
                        metadata["gps_coordinates"] = "Found, but could not parse."
                        
            elif tag_name not in ["MakerNote", "PrintIM", "UserComment"]: # Filter out mess
                 metadata["other_tags"].append(f"{tag_name}: {str(value)[:50]}")
                 
        return metadata
    except Exception as e:
        return {"error": f"Failed to process image file: {str(e)}"}

def convert_to_degrees(value):
    """
    Helper function to convert GPS coordinates in EXIF format to standard float degrees.
    """
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)
