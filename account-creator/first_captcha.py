import requests
import time

api_key = 'd9dd3bdb07074dea9ff2479374632ec5'
SiteKey = "6LeTnxkTAAAAAN9QEuDZRpn90WwKk_R1TRW_g-JC"
SiteUrl = "https://www.reddit.com/account/register/"
# encode siteurl
SiteUrl = SiteUrl.replace("://", "%3A%2F%2F").replace("/", "%2F")


class ReCapthca():
    @staticmethod
    def crate_task():
        try:
            url = f"https://api.1stcaptcha.com/recaptchav2?apikey={api_key}&sitekey={SiteKey}&siteurl={SiteUrl}"
            response = requests.get(url)
            # get task id
            task_id = response.json()['TaskId']
            return task_id
        except:
            return False
    
    @staticmethod
    def get_results(task_id):
        while True:
            try:
                url = f"https://api.1stcaptcha.com/getResult?apikey={api_key}&taskid={task_id}"
                response = requests.get(url)
                status = response.json()['Status']
                if status == 'PENDING' or status == 'PROCESSING':
                    time.sleep(3)
                    continue
                elif status == 'ERROR':
                    return False
                else:
                    token = response.json()['Data']['Token']
                    return token
            except:
                return False