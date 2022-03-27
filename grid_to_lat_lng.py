
def to_lat_lng(pos, num_rows, num_cols, min_lat, max_lat, min_lng, max_lng):

    degree_change_row = (max_lng - min_lng) / num_rows
    new_lat = max_lng - degree_change_row*pos[0]

    degree_change_col = (max_lat - min_lat) / num_cols
    new_lng = min_lat + degree_change_col*pos[1]
    return (new_lng,new_lat)

if __name__ == "__main__":
    print(to_lat_lng((0, 20), 50, 30,48.69961, 48.70011, 6.18461, 6.28504))