import socket, glob, json

port = 53
ip = '127.0.0.1'

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((ip, port))

# load dns zones
def load_zones():
    jsonzone = {}
    zonefiles = glob.glob('zones/*.zone')

    for zone in zonefiles:
        with open(zone) as zonedata:
            data = json.load(zonedata)
            zonename = data["$origin"]
            jsonzone[zonename] = data

    return jsonzone

zonedata = load_zones()

# construct the dns response flags
def getflags(flags):
    byte1 = bytes(flags[:1])
    byte2 = bytes(flags[1:2])

    rflags = ''

    QR = '1'

    OPCODE = ''
    for bit in range(1,5):
        OPCODE += str(ord(byte1)&(1<<bit))

    AA = '1'
    TC = '0'
    RD = '0'
    RA = '0'
    Z = '000'
    RCODE = '0000'

    return int(QR+OPCODE+AA+TC+RD, 2).to_bytes(1, byteorder='big') + int(RA+Z+RCODE, 2).to_bytes(1, byteorder='big')

# construct dns question
def getquestiondomain(data):

    state = 0
    expectedLength = 0
    domainstring = ''
    domainParts = []
    x = 0
    y = 0

    for byte in data:
        if state == 1:
            if byte != 0:
                domainstring += chr(byte)
            x += 1
            if x == expectedLength:
                domainParts.append(domainstring)
                domainstring = ''
                state = 0
                x = 0
            if byte == 0:
                domainParts.append(domainstring)
                break
        else:
            state = 1
            expectedLength = byte
        y += 1

    questiontype = data[y:y+2]

    return (domainParts, questiontype)

# get dns zone
def getzone(domain):
    global zonedata

    zone_name = '.'.join(domain)
    return zonedata[zone_name]

# get dns records
def getrecs(data):
    domain, questiontype = getquestiondomain(data)
    qt = ''

    if questiontype == b'\x00\x01':
        qt = 'a'
    
    zone = getzone(domain=domain)

    return (zone[qt], qt, domain)


# construct the dns question
def buildquestion(domainname, rectype):
    qbytes = b''

    for part in domainname:
        length = len(part)
        qbytes += bytes([length])

        for char in part:
            qbytes += ord(char).to_bytes(1, byteorder='big')
        
    if rectype == 'a':
        qbytes += (1).to_bytes(2, byteorder='big')
    
    qbytes += (1).to_bytes(2, byteorder='big')

    return qbytes


# change dns records to bytes
def rectobytes(domainname, rectype, recttl, recval):
    rbytes = b'\xc0\x0c'

    if rectype == 'a':
        rbytes = rbytes + bytes([0]) + bytes([1])
    
    rbytes += int(recttl).to_bytes(4, byteorder='big')

    if rectype == 'a':
        rbytes = rbytes + bytes([0]) + bytes([4])

        for part in recval.split('.'):
            rbytes += bytes([int(part)])

    return rbytes


# dns response builder
def build_response(data):
    # transaction Id
    TransactionId = data[:2]    

    # Ger the flags
    Flags = getflags(data[2:4])

    # Question Count
    QDCOUNT = b'\x00\x01'

    # Answer Count
    ANCOUNT = len(getrecs(data[12:])[0]).to_bytes(2, byteorder='big')

    # Nameserver Count
    NSCOUNT = (0).to_bytes(2, byteorder='big')

    # Additional Count
    ARCOUNT = (0).to_bytes(2, byteorder='big')

    # dns response header
    dnsheader = TransactionId+Flags+QDCOUNT+ANCOUNT+NSCOUNT+ARCOUNT

    # create response body
    dnsbody = b''

    # get answer for query
    records, rectype, domainname = getrecs(data[12:])

    dnsquestion = buildquestion(domainname, rectype=rectype)

    for record in records:
        dnsbody += rectobytes(domainname, rectype, record["ttl"], record["value"])
    
    return dnsheader + dnsquestion + dnsbody


    

while True:
    data, addr = sock.recvfrom(512)
    r = build_response(data)
    sock.sendto(r, addr)