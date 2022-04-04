from .models import ConnectionNode

connectionNodes = ConnectionNode.objects.all()

# Create your views here.
localHostList = [
    'https://c404-social-distribution.herokuapp.com/',
    'http://localhost:8000/',
    'http://127.0.0.1:8000/'
]


def node_matching(host):
    objectNode = None

    # match node in our db
    if "project-socialdistribution" in host:
        ''' matching T08's node (Ruilin Ma) '''
        objectNode = connectionNodes.filter(
            name__contains='T8').first()

    elif "cmput404-w22-project-backend" in host:
        ''' matching T05's node (Kerry Cao) '''
        objectNode = connectionNodes.filter(
            name__contains='T5').first()

    elif "social-dist-wed" in host:
        ''' matching T02's node (lefan) '''
        objectNode = connectionNodes.filter(
            name__contains='T2').first()

    elif "psdt11.herokuapp.com" in host:
        ''' matching T11's node (floored) '''
        objectNode = connectionNodes.filter(
            name__contains='T11').first()

    else:
        ''' probably our own clone '''
        objectNode = connectionNodes.filter(
            url=f"{host}service/").first()

    return objectNode