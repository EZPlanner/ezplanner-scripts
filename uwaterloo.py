import requests

API_BASE_URL = "https://api.uwaterloo.ca/v2"

class UWaterloo:
    def __init__(self, api_key):
        self.api_key = api_key

    def get_courses(self):
        payload = {
            'key': self.api_key
        }
        
        resp = requests.get(API_BASE_URL + "/courses.json", params = payload)

        if (resp.status_code != 200):
            print("ERROR CODE: {}".format(resp.status_code))
            return []

        courses = []

        for course_data in resp.json()['data']:
            courses.append({
                'subject': course_data['subject'],
                'catalog_number': course_data['catalog_number'],
                'data': course_data
            })

        return courses
