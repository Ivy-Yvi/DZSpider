import requests

def func_request(url):
    cookie = ""
    headers = {
        "cookie": cookie,
        "Host": "www.dianping.com",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
    }

    resp = requests.get(url, headers=headers)
    if resp.status_code in [200, 302]:
        return resp.text
    else:
        print(resp.status_code)
        return resp.text

def func_response(resp: str):
    print(resp)


def main():
    url = "https://www.dianping.com/shop/jTYIYHRl2kiDdYGe/review_all/p4"
    resp = func_request(url)
    func_response(resp)


if __name__ == '__main__':
    main()


