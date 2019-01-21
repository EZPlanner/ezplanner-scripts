import requests
import os
from math import *

API_BASE_URL = "https://api.uwaterloo.ca/v2"

class UWaterloo:
    def __init__(self, api_key):
        self.api_key = api_key
        self.course_count = 0.0
        self.current_count = 0.0

    def get_courses(self):
        payload = {
            'key': self.api_key
        }
        
        resp = requests.get(API_BASE_URL + "/courses.json", params=payload)

        if resp.status_code != 200:
            print("ERROR, response status code: {}".format(resp.status_code))
            return []

        courses = []

        for course_data in resp.json()['data']:
            courses.append({
                'subject': course_data['subject'],
                'catalog_number': course_data['catalog_number'],
                'data': course_data
            })

        self.course_count = len(courses)

        return courses

    def get_prereqs(self, args):
        course = args['course']
        payload = {
            'key': ('api_key' in args and args['api_key']) or self.api_key
        }

        resp = requests.get(API_BASE_URL + "/courses/{}/{}/prerequisites.json".format(course['subject'], course['catalog_number']), params=payload)

        if resp.status_code != 200:
            print("ERROR, response status code: {}".format(resp.status_code))
            return

        resp = resp.json()

        return {
            'course': '{}/{}'.format(course['subject'], course['catalog_number']),
            'prereqs': ('prerequisites_parsed' in resp['data'] and resp['data']['prerequisites_parsed'] is not None and resp['data']['prerequisites_parsed']) or []
        }