def lat_lon_to_grid_square(lat, lon):
    """
    Convert latitude and longitude to Maidenhead grid square
    """
    # Normalize coordinates
    lon = lon + 180
    lat = lat + 90
    
    # Calculate first level (field)
    field_lon = int(lon / 20)
    field_lat = int(lat / 10)
    
    # Calculate second level (square)
    square_lon = int((lon % 20) / 2)
    square_lat = int((lat % 10) / 1)
    
    # Calculate third level (subsquare)
    subsquare_lon = int((lon % 2) * 12)
    subsquare_lat = int((lat % 1) * 24)
    
    # Convert to characters
    field_lon_char = chr(ord('A') + field_lon)
    field_lat_char = chr(ord('A') + field_lat)
    square_lon_char = str(square_lon)
    square_lat_char = str(square_lat)
    subsquare_lon_char = chr(ord('a') + subsquare_lon)
    subsquare_lat_char = chr(ord('a') + subsquare_lat)
    
    # Combine into grid square
    return f"{field_lon_char}{field_lat_char}{square_lon_char}{square_lat_char}{subsquare_lon_char}{subsquare_lat_char}" 