import requests
import logging
import yaml
from time import sleep

with open("./config.yml", "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.Loader)

logging.basicConfig(filename=config['logfile'], level=logging.INFO)

token = config['token']
friends = config['friends']

api_base_url = config['api_base_url']
auth_header = {
    'authorization': f'Bearer {token}'
}

def create_like(status_id: int):
    logging.info(f'Creating like for status {str(status_id)}')
    requests.post(f"{api_base_url}/status/{status_id}/like", headers=auth_header)

def get_statuses():
    logging.info('Getting statuses')
    resp = requests.get(f"{api_base_url}/dashboard", headers=auth_header)
    if (resp.status_code != 200):
        logging.error(f'Error getting statuses: Server responded with status_code {resp.status_code}')
    return resp.json()['data']

def main():
    statuses = get_statuses()

    for status in statuses:
        status_id: int = status['id']
        is_liked: bool = status['liked']
        user: str = status['userDetails']['username']

        if is_liked == True:
            continue

        if user not in friends:
            continue

        create_like(status_id)
        sleep(1)
    sleep(1)

if __name__ == "__main__":
    main()