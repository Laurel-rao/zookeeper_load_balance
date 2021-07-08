import time

from kazoo.client import KazooClient

from client.config import Config


# 查看节点负载情况
def query_connections():
    client = KazooClient(hosts=Config.zookeeper_server)
    client.start(timeout=30)
    nodes = client.get_children(Config.BASE_PATH)
    choice_path = {}

    for node in nodes:
        cur_path = Config.BASE_PATH + "/" + node
        session_num = len(client.get_children(cur_path))
        choice_path.update({node: session_num})

    print(choice_path)
    client.stop()
    return choice_path


if __name__ == '__main__':
    while True:
        time.sleep(10)
        query_connections()
