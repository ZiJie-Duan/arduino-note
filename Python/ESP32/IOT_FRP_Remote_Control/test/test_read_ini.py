import configparser
config = configparser.ConfigParser()
# set a number of parameters

datas = {
    "common":{
        "server_addr" : "82.156.111.1",
        "server_port" : "7000",
        "token" : "12345678"
    },
    "rdp":{
        "type" : "tcp",
        "local_ip" : "127.0.0.1",
        "local_port" : "3389",
        "remote_port" : "7001"
    }
}

for section, data in datas.items():
    config.add_section(section)
    for key, value in data.items():
        config.set(section, key, value)

config.write(open('frpc.ini', "w"))