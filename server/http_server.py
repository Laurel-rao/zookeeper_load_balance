import time
import traceback
import uuid
from multiprocessing import Process

from flask import Flask
from flask import request
from kazoo.client import KazooClient
from retry import retry

from server.config import Config

app = Flask(__name__)


@retry(tries=3, delay=2)
def create_zoo_client():
    client = KazooClient(hosts=Config.zookeeper_server)
    client.start()
    return client


def register(func):
    def inner(*args, **kwargs):
        session_id = uuid.uuid4().hex
        client = None
        try:
            client = create_zoo_client()
            increase_server(client, session_id)
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                return "Error %s" % e
            else:
                return result
            finally:
                decrease_server(client, session_id)
        except Exception as e:
            return "Error %s" % e
        finally:
            if client is not None:
                client.stop()
                client.close()
    return inner


def increase_server(client, session_id):
    try:
        cur_path = Config.BASE_PATH + "/" + request.host
        client.create("%s/%s" % (cur_path, session_id), ephemeral=True)
    except:
        traceback.print_exc()


def decrease_server(client, session_id):
    try:
        cur_path = Config.BASE_PATH + "/" + request.host + "/" + session_id
        if client.exists(cur_path) is not None:
            client.delete(cur_path)
    except Exception as e:
        traceback.print_exc()


@app.route("/")
@register
def hello():
    time.sleep(2)
    return "done"


def create_base_path(path, ):
    client = KazooClient(hosts=Config.zookeeper_server)
    client.start()
    try:
        temp_path = ''
        for i in Config.BASE_PATH.split("/"):
            temp_path = temp_path + "/" + i
            if client.exists(temp_path) is None:
                client.create(temp_path)
    except Exception as e:
        print("Error %s" % e)
        return "Error %s" % e
    finally:
        client.stop()
        client.close()


def multi_server():
    P = []
    for i in range(10):
        P.append(Process(target=runserver, kwargs={"port": 9090 + i}))
        # app.run("127.0.0.1", 9090)

    for p in P:
        p.start()

    for p in P:
        p.join()


def runserver(port):
    # 服务启动时，创建服务节点(永久节点)和探测节点(临时节点)
    client = KazooClient(hosts=Config.zookeeper_server)
    client.start()
    cur_path = Config.BASE_PATH + "/" + "127.0.0.1:%s" % port
    client.delete(cur_path, recursive=True)
    client.create(cur_path)
    alive_path = Config.BASE_ALIVE_PATH + "/" + "127.0.0.1:%s" % port
    try:
        client.delete(alive_path, recursive=True)
    except:
        pass

    client.create(alive_path, ephemeral=True, makepath=True)
    app.run("127.0.0.1", port)


if __name__ == '__main__':
    multi_server()
