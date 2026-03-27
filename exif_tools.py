import os
import hashlib
import re
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS

def analyze_image_forensics(file_path):
    """
    Executes a multi-vector Digital Forensics scan on a file.
    Performs:
    1. Cryptographic Hashing (MD5, SHA256)
    2. Magic Byte Signature Verification
    3. EXIF Telemetry Extraction (Optional, won't fail if missing)
    4. Steganography basic String Extraction
    """
    report = {
        "hashes": {},
        "magic_bytes": "Unknown",
        "strings": [],
        "exif": None,
        "error": None
    }
    
    try:
        # 1. Cryptographic Hashing
        with open(file_path, "rb") as f:
            file_bytes = f.read()
            report["hashes"]["MD5"] = hashlib.md5(file_bytes).hexdigest()
            report["hashes"]["SHA-256"] = hashlib.sha256(file_bytes).hexdigest()
            
            # 2. Magic Byte Signature Validation
            # Check the first 8 bytes for common file signatures
            header = file_bytes[:8].hex().upper()
            if header.startswith("FFD8FF"):
                report["magic_bytes"] = "JPEG Image Phase Identity (FF D8 FF)"
            elif header.startswith("89504E47"):
                report["magic_bytes"] = "PNG Image Phase Identity (89 50 4E 47)"
            elif header.startswith("47494638"):
                report["magic_bytes"] = "GIF Image Phase Identity (47 49 46 38)"
            elif header.startswith("25504446"):
                report["magic_bytes"] = "PDF Document Spoof Detected! (25 50 44 46)"
            elif header.startswith("504B0304"):
                report["magic_bytes"] = "ZIP Archive Spoof Detected! (50 4B 03 04)"
            else:
                report["magic_bytes"] = f"Unknown Signature Payload ({header})"
                
            # 3. Basic String Extraction (Steganography surface check)
            # Find contiguous printable ASCII characters of length >= 8
            strings_found = re.findall(rb'[ -~]{8,}', file_bytes)
            
            # Filter out predictable noise, keep the most interesting looking strings
            interesting_strings = []
            for s in strings_found:
                try:
                    decoded = s.decode('utf-8')
                    # Exclude basic imaging schema noise to keep Hackathon UI clean
                    if "adobe" not in decoded.lower() and "xmlns" not in decoded.lower() and "exif" not in decoded.lower():
                        interesting_strings.append(decoded)
                except:
                    pass
            # Return up to 15 interesting strings for the UI terminal
            report["strings"] = interesting_strings[:15]
            
    except Exception as e:
        report["error"] = f"Failed to perform low-level binary analysis: {str(e)}"
        return report

    # 4. EXIF Telemetry Extraction (Will not fail the main suite if missing)
    try:
        report["exif"] = extract_gps_exif(file_path)
    except Exception:
        report["exif"] = {"error": "Image structural parsing failed (Not an Image)."}
        
    return report

def extract_gps_exif(image_path):
    """
    Standalone targeted EXIF extractor that returns standard dictionary
    """
    metadata = {
        "device": "Unknown",
        "date_taken": "Unknown",
        "gps_coordinates": None,
        "gps_dms_raw": None,
        "other_tags": []
    }
    
    try:
        image = Image.open(image_path)
        exif_info = image._getexif()
        
        if not exif_info:
            return {"error": "No EXIF metadata found. Image headers may be scrubbed natively."}
            
        for tag, value in exif_info.items():
            tag_name = TAGS.get(tag, tag)
            
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
                
                if 'GPSLatitude' in gps_data and 'GPSLongitude' in gps_data:
                    try:
                        lat = convert_to_degrees(gps_data['GPSLatitude'])
                        if gps_data.get('GPSLatitudeRef') != 'N':
                            lat = 0 - lat
                        lon = convert_to_degrees(gps_data['GPSLongitude'])
                        if gps_data.get('GPSLongitudeRef') != 'E':
                            lon = 0 - lon
                            
                        metadata["gps_coordinates"] = f"{lat:.5f}, {lon:.5f}"
                        
                        raw_lat_d, raw_lat_m, raw_lat_s = float(gps_data['GPSLatitude'][0]), float(gps_data['GPSLatitude'][1]), float(gps_data['GPSLatitude'][2])
                        lat_ref = gps_data.get('GPSLatitudeRef', 'N')
                        
                        raw_lon_d, raw_lon_m, raw_lon_s = float(gps_data['GPSLongitude'][0]), float(gps_data['GPSLongitude'][1]), float(gps_data['GPSLongitude'][2])
                        lon_ref = gps_data.get('GPSLongitudeRef', 'W')
                        
                        metadata['gps_dms_raw'] = f"{raw_lat_d}° {raw_lat_m}' {raw_lat_s}\" {lat_ref}, {raw_lon_d}° {raw_lon_m}' {raw_lon_s}\" {lon_ref}"
                        
                    except Exception as ge:
                        metadata["gps_coordinates"] = "Found, but could not parse."
                        
            elif tag_name not in ["MakerNote", "PrintIM", "UserComment"]: 
                 metadata["other_tags"].append(f"{tag_name}: {str(value)[:50]}")
                 
        return metadata
    except Exception as e:
        return {"error": f"Pillow failed to open image logic: {str(e)}"}

def convert_to_degrees(value):
    """
    Helper function to convert GPS coordinates in EXIF format to standard float degrees.
    """
    d = float(value[0])
    m = float(value[1])
    s = float(value[2])
    return d + (m / 60.0) + (s / 3600.0)
