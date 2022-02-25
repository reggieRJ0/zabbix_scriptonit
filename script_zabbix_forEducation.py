from pyzabbix import ZabbixAPI
import csv


# Инициализация метода авторизации 

def login():
    i = 1
    for i in range(3):
        username = input("Введите логин: ")
        password = input("Введите пароль: ")
        try:
            zapi = ZabbixAPI("http://192.168.1.9/zabbix")
            zapi.login(user=username, password=password)
            return zapi
        except:
            if i == 2:
                print("\nАвторизация временно заблокирована, попробуйте через 5 минут\n")
                quit()
            else:
                print("\nЛогин и/или пароль неверные, повторите попытку\n")

# Вызов метода авторизации
auth=login()

# Инициализация метода создания узлов
def create_host(par1,par2,par3,par4):
    createhost = auth.host.create(
        host = par1,
        interfaces = [{
            "type": 1,
            "main": 1,
            "useip": 1,
            "ip": f"{par2}",
            "dns": "",
            "port": f"{par3}"

        }],

        groups = [{
            "groupid": "18"
        }],

        templates = [{
            "templateid": "10447"
        }],

        macros = [{

                "macro": "{$INT}",
                "value": f"{par4}"

        }]
    )

# Инициализация метода получения параметров узлов
def get_inf(find):
    param = []
    get_information_host = auth.host.get(
        filter = {
                "host": [
                    f"{find}", 
                ]
                })
    param.append(get_information_host[0].get('hostid'))
    param.append(get_information_host[0].get('host'))

    get_inf_int = auth.hostinterface.get(
        hostids = get_information_host[0].get('hostid')

    )

    param.append(get_inf_int[0].get('ip'))
    param.append(get_inf_int[0].get('port'))

    get_inf_macro = auth.usermacro.get(
        hostids = get_information_host[0].get('hostid')

    )
    param.append(get_inf_macro[0].get('value'))

    return param

# Инициализация метода обноваления параметров узлов
def update_host(par0, par1,par2,par3,par4):
    if par1 == "":
        par1 = par0[1]
    else:
        pass
    if par2 == "":
        par2 = par0[2]
    else:
        pass
    if par3 == "":
        par3 = par0[4]
    else:
        pass
    if par4 == "":
        par4 = par0[3]
    else:
        pass

    update = auth.host.update(
        hostid = par0[0],
        templates_clear = 
            {
                "templateid": "10447"
            },
        
        host = par1,
        interfaces = [{
            "type": 1,
            "main": 1,
            "useip": 1,
            "ip": par2,
            "dns": "",
            "port": f"{par3}"
        }],

        groups = [{
            "groupid": "18"
        }],

        templates = [{
            "templateid": "10447"
        }],

        macros = [{

                "macro": "{$INT}",
                "value": f"{par4}"

        }]

    )

# Инциализация родитнльского метода и вызов дочерних методов
def main():
    choose = input("\n 1. Создание узла\n 2. Обновление параметров узла\n 3. Массовое создание узлов\n 4. Массовое обновление параметров узлов\n\n Выберите операцию: " )
    try:
        if choose == "1":
            hostname = input("Введите название узла: ")
            addr = input("Введите адрес узла: ")
            int = input("Введите интерфейс узла: ")
            port = input("Введите порт узла: ")
            create_host(hostname,addr,int,port)
    

        elif choose == "2":
            find = input("Поиск узла(имя): ")
            a = get_inf(find)
            hostname = input("Введите новое имя узла: ")
            addr = input("Введите новый адрес узла: ")
            int = input("Введите новый интерфейс узла: ")
            port = input("Введите новый порт узла: ")
            update_host(a,hostname,addr,int,port)
      

        elif choose == "3":
            data_create = input("Введите название файла(прим.: test.csv): ")
            with open(data_create, encoding='utf-8') as f: 
                for [host,ip,port,int] in csv.reader(f, delimiter=';'):
                    create_host(host,ip,port,int) 
                    update_host(get_inf(old_name),new_name,ip,port,int) 
    

        elif choose == "4":
            data_update = input("Введите название файла(прим.: test.csv): ")
            with open(data_update, encoding='utf-8') as f: 
                for [old_name,new_name,ip,port,int] in csv.reader(f, delimiter=';'):
                    update_host(get_inf(old_name),new_name,ip,port,int) 
        else:
            main()

    except:
        print("\nПроверьте введеные данные и повторите попытку")
        main()

# Вызов главного метода     
main()

