import requests
import json
# ############################################     PARAMETERS    #######################################################
# Fill in variables below. Meraki API, Org. Name, SSID Names to be copied, Source Network Name, Destination Network Names
# ######################################################################################################################
meraki_api = 'MerakiAPIkey'
organization_id = 'Organization Name'
ssids = ['SSID-Name1', 'SSID-Name2']
source_network_name = 'Source Network Name'
destination_network_name = ['Destination Network Name1', 'Destination Network Name2']
# ######################################################################################################################
net_dictionary = {}
ssid_dictionary = {}
headers = {
    'X-Cisco-Meraki-API-Key': meraki_api,
    'Accept': 'application/json',
    'Content-Type': 'application/json'
}


def pull_organization_id(head):
    url = "https://api.meraki.com/api/v0/organizations"
    payload = {}
    response = requests.request("GET", url, headers=head, data=payload)
    response = response.content
    response = json.loads(response)
    for dicti in response:
        name = dicti["name"]
        if name == organization_id:
            org_id = dicti["id"]
            print("#################################################")
            print(name + "\n" + "Organization ID: " + org_id)
            print("#################################################")
            return org_id
        else:
            continue


def pull_organization_networks(head):
    global organization_id, net_dictionary
    organization_id = pull_organization_id(head)
    url = "https://api.meraki.com/api/v0/organizations/" + organization_id + "/networks"
    payload = {}
    response = requests.request("GET", url, headers=head, data=payload)
    response = response.content
    json_response = json.loads(response)
    # print(response)
    for networks in json_response:
        name = networks['name']
        n_id = networks['id']
        # print(name + " : " + n_id)
        net_dictionary[name] = n_id
    # print(net_dictionary)
    return net_dictionary


def pull_source_network():
    global source_network_name
    source_network_id = ()
    for n in net_dictionary:
        # print(n)
        if n == source_network_name:
            # print(n)
            source_network_id = net_dictionary[n]
            # print(source_network_id)
            net_dictionary.pop(n)
            # print(my_dict)
            break
        else:
            continue
    print(net_dictionary)
    print("##########################################")
    print("Source Network: " + source_network_name + "\n" + "Source Network ID: " + source_network_id)
    return source_network_id


def pull_destination_networks():
    global destination_network_name
    dest_network_ids = []
    if destination_network_name[0] == 'ALL':
        print("##########################################")
        print("ALL Networks will be used as a DESTINATION")
        print("##########################################")
        # print(net_dictionary)
        for n in net_dictionary:
            dest_network_ids.append(net_dictionary[n])
        print(dest_network_ids)
        return dest_network_ids
    else:
        for n in net_dictionary:
            # print(n)
            # print(destination_network_name[id])
            for i in destination_network_name:
                # print(i)
                if n == i:
                    print("Destination Network: " + n)
                    dest_network_ids.append(net_dictionary[n])
                    break
                else:
                    continue
        print(dest_network_ids)
        return dest_network_ids


def pull_ssid_ids(head):
    global ssids, ssid_dictionary
    ssid_id = []
    url = "https://api.meraki.com/api/v0//networks/L_607422999741601685/ssids"
    payload = {}
    response = requests.request("GET", url, headers=head, data=payload)
    response = response.content
    response = json.loads(response)
    for ssid in response:
        name = ssid["name"]
        number = ssid["number"]
        if name[0:12] != "Unconfigured":
            ssid_dictionary[name] = str(number)
        else:
            continue
    print("SSIDs on the list:")
    print(ssid_dictionary)
    if ssids[0] == "ALL":
        for x, y in ssid_dictionary.items():
            ssid_id.append(str(y))
        print(ssid_id)
        return ssid_id
    else:
        for ssid_name in ssids:
            for x, y in ssid_dictionary.items():
                if ssid_name == x:
                    ssid_id.append(str(y))
                else:
                    continue
        print(ssid_id)
        return ssid_id


def get_name_from_id(dictionary, net_id):
    keys = list(dictionary.keys())
    vals = list(dictionary.values())
    return keys[vals.index(net_id)]


pull_organization_networks(headers)
networkss_src = pull_source_network()
networks_dest = pull_destination_networks()
ssid_param = pull_ssid_ids(headers)


def copy_ssids(net_sr, net_ds, ssid, head, sr_name):
    for network_dest in net_ds:
        for ssid_rollout in ssid:
            ssid_name = get_name_from_id(ssid_dictionary, ssid_rollout)
            print("#####################################################################################")
            print("Pulling SSID " + ssid_name + " - ID:" + str(ssid_rollout) + " information from network " +
                  sr_name + " : " + net_sr)
            url = ("https://api.meraki.com/api/v0/networks/" + net_sr + "/ssids/" + ssid_rollout)
            print(url)
            payload = {}
            response = requests.request("GET", url, headers=head, data=payload)
            print(response.text.encode('utf8'))
            ssid_json = response.content

            net_name = get_name_from_id(net_dictionary, network_dest)
            print("#####################################################################################")
            print("Applying SSID " + ssid_name + " - ID:" + str(ssid_rollout) + " settings to network " + net_name +
                  " : " + network_dest)
            url = ("https://api.meraki.com/api/v0/networks/" + network_dest + "/ssids/" + ssid_rollout)
            print(url)
            response = requests.request("PUT", url, headers=head, data=ssid_json)
            print(response.text.encode('utf8'))


def copy_splash_settings(net_sr, net_ds, ssid, head, sr_name):
    for network_dest in net_ds:
        for ssid_rollout in ssid:
            ssid_name = get_name_from_id(ssid_dictionary, ssid_rollout)
            print("#####################################################################################")
            print("Pulling Splash Page settings from SSID " + ssid_name + " - ID:" + str(ssid_rollout) +
                  " network " + sr_name + " : " + net_sr)
            url = ("https://api.meraki.com/api/v0/networks/" + net_sr + "/ssids/" + ssid_rollout + "/splashSettings")
            print(url)
            payload = {}
            response = requests.request("GET", url, headers=head, data=payload)
            print(response.text.encode('utf8'))
            ssid_json = response.content
            net_name = get_name_from_id(net_dictionary, network_dest)
            print("#####################################################################################")
            print("Applying Splash Page settings to SSID " + ssid_name + " - ID:" + str(ssid_rollout) +
                  " to network " + net_name + " : " + network_dest)
            url = ("https://api.meraki.com/api/v0/networks/" + network_dest + "/ssids/" + ssid_rollout +
                   "/splashSettings")
            print(url)
            response = requests.request("PUT", url, headers=head, data=ssid_json)
            print(response.text.encode('utf8'))


def copy_firewall_l3(net_sr, net_ds, ssid, head, sr_name):
    for network_dest in net_ds:
        for ssid_rollout in ssid:
            ssid_name = get_name_from_id(ssid_dictionary, ssid_rollout)
            print("#####################################################################################")
            print("Pulling firewall L3 rules from SSID " + ssid_name + " - ID:" + str(ssid_rollout) +
                  " network " + sr_name + " : " + net_sr)
            url = ("https://api.meraki.com/api/v0/networks/" + net_sr + "/ssids/" + ssid_rollout + "/l3FirewallRules")
            print(url)
            payload = {}
            response = requests.request("GET", url, headers=head, data=payload)
            response = json.loads(response.text)
            firewall_rules = {"rules": response}
            firewall_rules = json.dumps(firewall_rules)
            net_name = get_name_from_id(net_dictionary, network_dest)
            print(firewall_rules)
            print("#####################################################################################")
            print("Applying L3 Firewall Rules to SSID " + ssid_name + " - ID:" + str(ssid_rollout) +
                  " to network " + net_name + " : " + network_dest)
            url = ("https://api.meraki.com/api/v0/networks/" + network_dest + "/ssids/" + ssid_rollout +
                   "/l3FirewallRules")
            print(url)
            response = requests.request("PUT", url, headers=head, data=firewall_rules)
            print(response.text.encode('utf8'))


def copy_traffic_shaping(net_sr, net_ds, ssid, head, sr_name):
    for network_dest in net_ds:
        for ssid_rollout in ssid:
            ssid_name = get_name_from_id(ssid_dictionary, ssid_rollout)
            print("#####################################################################################")
            print("Pulling Traffic Shaping information from SSID " + ssid_name + " - ID:" + str(ssid_rollout) +
                  " network " + sr_name + " : " + net_sr)
            url = ("https://api.meraki.com/api/v0/networks/" + net_sr + "/ssids/" + ssid_rollout + "/trafficShaping")
            print(url)
            payload = {}
            response = requests.request("GET", url, headers=head, data=payload)
            print(response.text.encode('utf8'))
            traffic_shaping = response.content
            net_name = get_name_from_id(net_dictionary, network_dest)
            print("#####################################################################################")
            print("Applying Traffic Shaping settings from SSID " + ssid_name + " - ID:" + str(ssid_rollout) +
                  " to network " + net_name + " : " + network_dest)
            url = ("https://api.meraki.com/api/v0/networks/" + network_dest + "/ssids/" + ssid_rollout +
                   "/trafficShaping")
            print(url)
            response = requests.request("PUT", url, headers=head, data=traffic_shaping)
            print(response.text.encode('utf8'))


copy_ssids(networkss_src, networks_dest, ssid_param, headers, source_network_name)
copy_splash_settings(networkss_src, networks_dest, ssid_param, headers, source_network_name)
copy_firewall_l3(networkss_src, networks_dest, ssid_param, headers, source_network_name)
copy_traffic_shaping(networkss_src, networks_dest, ssid_param, headers, source_network_name)
