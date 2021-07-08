import time

from kazoo.client import KazooClient
from retry import retry

from client.config import Config


def get_all_alive_node():
    client = KazooClient(hosts=Config.zookeeper_server)
    client.start()
    nodes = client.get_children(Config.BASE_PATH)
    client.stop()
    return nodes

@retry(tries=3, delay=2)
def create_zoo_client():
    client = KazooClient(hosts=Config.zookeeper_server)
    client.start()
    return client


def get_lease_node():
    client = create_zoo_client()
    nodes = client.get_children(Config.BASE_PATH)
    cur_num = -1
    choice_path = ""

    for node in nodes:
        # print(node)
        cur_path = Config.BASE_PATH + "/" + node
        session_num = len(client.get_children(cur_path))

        if cur_num == -1:
            cur_num = session_num
            choice_path = node
        else:
            # print(session_num, cur_num)
            if cur_num > session_num:
                choice_path = node
    if not choice_path:
        raise ValueError("Can't get server host %s" % nodes)
    # print(choice_path)
    client.stop()

    return choice_path

