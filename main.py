import requests
import logging
import yaml
from time import sleep

with open("./config.yml", "r") as config_file:
    config = yaml.load(config_file, Loader=yaml.Loader)

logging.basicConfig(filename=config['logfile'], level=logging.INFO)

api_base_url = config['api_base_url']

def create_like(status_id: int, token: str):
    logging.info(f'Creating like for status {str(status_id)}')
    requests.post(f"{api_base_url}/status/{status_id}/like", headers={
        'authorization': f'Bearer {token}'
    })

def get_statuses(token: str):
    logging.info('Getting statuses')
    resp = requests.get(f"{api_base_url}/dashboard", headers={
        'authorization': f'Bearer {token}'
    })
    if (resp.status_code != 200):
        logging.error(f'Error getting statuses: Server responded with status_code {resp.status_code}')
    return resp.json()['data']

def main():
    for account in config['accounts']:
        friends = account['friends']
        excluded_lines = account['excluded_lines']
        statuses = get_statuses(account['token'])

        for status in statuses:
            status_id: int = status['id']
            is_liked: bool = status['liked']
            user: str = status['userDetails']['username']
            line_name: str = status['train']['lineName']

            if is_liked == True:
                continue

            if user not in friends:
                continue

            excluded = False
            for excluded_line in excluded_lines:
                if excluded_line in line_name:
                    excluded = True
                    break

            if excluded:
                continue

            create_like(status_id, account['token'])
            sleep(1)
        sleep(1)

if __name__ == "__main__":
    main()