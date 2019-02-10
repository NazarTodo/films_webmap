def checkip(str):
    final = []
    if str.count(".") == 3:
        ip = str.split(".")
    else:
        return None
    if len(ip) != 4:
        return None
    for i in ip:
        if not i.isdigit():
            return None
        if int(i) < 0 or int(i) > 255:
            return("You have enetered wrong ip")
        else:
            final.append(int(i))
    return final


def ip_to_str(ip):
    return".".join(map(str, ip))


def net_num(ip, mask):
    net = []
    wild = []
    for i in range(len(ip)):
        net.append(int(ip[i]) & int(mask[i]))
        wild.append(int(ip[i]) & int(~mask[i]))
    return net, wild


if __name__ == "__main__":
    ip = checkip(input())
    mask = checkip(input())
    if ip and mask:
        network, wildcard = net_num(ip, mask)
        print(ip_to_str(network))
        print(ip_to_str(wildcard))