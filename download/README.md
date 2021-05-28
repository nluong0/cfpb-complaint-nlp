# Download
Download and process CFPB data into JSON files.

## Structure

__download.sh__ queries the CFPB API and downloads all complaints with a complaint narrative to JSON file.
__load_narratives.py__ extracts only complaint ID and complaint narratives from JSON returned from CFPB API query.
