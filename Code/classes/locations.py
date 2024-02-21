        # Create a dictionary with locations and addresses
import pandas as pd

def get_fictious_locations():   
    locations_dict = {
        "city": ["Roscoeview", "Aliyaview", "Bartholomebury", "McKenziehaven", "Lebsackbury",
                    "Howemouth", "South Elvis", "Gwenborough", "Wisokyburgh", "South Christy"],
        "Address": ["Roscoe Village, Chicago, IL, USA",
                    "303, Al-Falah Building, Shahrah-e-Quaid-e-Azam, Garhi Shahu, Lahore, Punjab 54000, Pakistan",
                    "Null",  # Address not found
                    "11 Hillcross St # 83, McKenzie, AL 36456, USA",
                    "Null",  # Address not found
                    "Null",  # Address not found
                    "Memphis, TN 38106, USA",
                    "Guisborough TS14, UK",
                    "Winchburgh, UK",
                    "2490 S Woodworth Loop Suite 301, Palmer, AK 99645, USA"]
    }

    df = pd.DataFrame(locations_dict)
    return df