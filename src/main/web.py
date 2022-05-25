from falcon import API


def create_app() -> API:
    web_api = API()
    return web_api
