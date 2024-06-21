import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

BASE_PATH = os.getenv('BASE_PATH')
ALL_PATHES_FILENAME = os.getenv('ALL_PATHES_FILENAME')
ALL_PATHES_FILEPATH = os.path.join(BASE_PATH, ALL_PATHES_FILENAME)
PPX_TEMPLATE_PATH = os.getenv('PPX_TEMPLATE_PATH')
PPX_FILE = os.getenv('PPX_FILE')
PROXIES_PATH = os.getenv('PROXIES_PATH')


def add_proxy_xml(proxy_list_parent_obj, proxy_id, proxy_type, username, password, options, port, address, label):
    # Створюємо новий проксі
    new_proxy = ET.SubElement(proxy_list_parent_obj, "Proxy", id=str(proxy_id), type=proxy_type)

    authentication = ET.SubElement(new_proxy, "Authentication", enabled="true")
    ET.SubElement(authentication, "Username").text = username
    ET.SubElement(authentication, "Password").text = password

    ET.SubElement(new_proxy, "Options").text = str(options)
    ET.SubElement(new_proxy, "Port").text = str(port)
    ET.SubElement(new_proxy, "Address").text = address
    ET.SubElement(new_proxy, "Label").text = label

    return proxy_list_parent_obj


def add_rule_xml(rule_list_parent_obj, action_type, action_value, applications, name, enabled=True):
    # Створюємо нове правило
    new_rule = ET.SubElement(rule_list_parent_obj, "Rule", enabled=str(enabled).lower())

    # Додаємо елементи до правила
    ET.SubElement(new_rule, "Action", type=action_type).text = str(action_value)
    ET.SubElement(new_rule, "Applications").text = str(applications).replace('/','\\').strip()
    ET.SubElement(new_rule, "Name").text = name

    return rule_list_parent_obj


def add_proxies_from_file(proxies_path, apps_path, proxy_list_parent, rule_list_parent):

    app_path = 'hello\\'

    with open(proxies_path, 'r') as fileobj:
            proxy_list = fileobj.readlines()

    with open(apps_path, 'r') as fileobj:
            apps_pathes_list = fileobj.readlines()

    if len(proxy_list) < len(apps_pathes_list):
         print('Not enough proxies!')
         return (None, None)


    for index, app_path in enumerate(apps_pathes_list):
        proxy = proxy_list[index]
        ip = proxy[proxy.index('@')+1:-7]
        port = proxy[-6:].strip()
        username = proxy[:proxy.index(':')]
        password = proxy[proxy.index(':')+1:proxy.index('@')]
        id = index + 100

        proxy_list_parent = add_proxy_xml(proxy_list_parent, id, "SOCKS5", username, password, 48, port, ip, port)
        rule_list_parent = add_rule_xml(rule_list_parent, 'Proxy', id, app_path.strip(), 'New')

    return proxy_list_parent, rule_list_parent


def add_standalone_attribute(xml_file):

    # Отримання XML-декларації
    xml_declaration = '<?xml version=\'1.0\' encoding=\'UTF-8\'?>'

    # Додаємо атрибут standalone="yes" до XML-декларації
    modified_declaration = xml_declaration.replace('?>', ' standalone="yes"?>')
    modified_declaration = modified_declaration.replace('\'','\"')

    # Змінюємо XML-декларацію в самому файлі
    with open(xml_file, 'r+', encoding='UTF-8') as file:
        content = file.read()
        content = content.replace(xml_declaration, modified_declaration)
        file.seek(0)
        file.write(content)
        file.truncate()



def create_proxy_list():
    tree = ET.parse(PPX_TEMPLATE_PATH)
    root = tree.getroot()
    proxy_list_parent = root.find('ProxyList')
    rule_list_parent = root.find('RuleList')

    if proxy_list_parent is None or rule_list_parent is None:
        print('problem with file')
    else:
        proxy_list_parent, rule_list_parent = add_proxies_from_file(PROXIES_PATH, ALL_PATHES_FILEPATH, proxy_list_parent, rule_list_parent)
        if proxy_list_parent is None or rule_list_parent is None:
             print('scripts stops!')
             input()
             return 0

        tree.write(PPX_FILE, encoding="UTF-8", xml_declaration=True, method="xml", short_empty_elements=False)

    add_standalone_attribute(PPX_FILE)

    print(f"File destination: {os.path.abspath(PPX_FILE)}")
    input()


if __name__ == '__main__':
     create_proxy_list()


