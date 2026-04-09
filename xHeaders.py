import requests , os , psutil , sys , jwt , pickle , json , binascii , time , urllib3 , base64 , datetime , re ,socket , threading
from protobuf_decoder.protobuf_decoder import Parser
from xC4 import *
from datetime import datetime
from google.protobuf.timestamp_pb2 import Timestamp
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning) 
RELEASE_VERSION = "OB53"

def ToK():
    while True:
        try:
            r = requests.get('https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?&type=ToKens')
            t = r.text
            i = t.find("ToKens : [")
            if i != -1:
                j = t.find("]", i)
                L = [x.strip(" '\"") for x in t[i+11:j].split(',') if x.strip()]
                if L:
                    with open("token.txt", "w") as f:
                        f.write(random.choice(L))
        except: pass
        time.sleep(5 * 60 * 60)

Thread(target=ToK , daemon = True).start()



def equie_emote(JWT,url):
    url = f"{url}/ChooseEmote"

    headers = {
        "Accept-Encoding": "gzip",
        "Authorization": f"Bearer {JWT}",
        "Connection": "Keep-Alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Expect": "100-continue",
        #"Host": "clientbp.ggblueshark.com",
        "ReleaseVersion": RELEASE_VERSION,
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 9; G011A Build/PI)",
        "X-GA": "v1 1",
        "X-Unity-Version": "2018.4.11f1",
    }

    data = bytes.fromhex("CA F6 83 22 2A 25 C7 BE FE B5 1F 59 54 4D B3 13")

    requests.post(url, headers=headers, data=data)





def GeTToK():  
    with open("token.txt") as f: return f.read().strip()
    
def Likes(id):
    try:
        text = requests.get(f"https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?id={id}&type=likes").text
        get = lambda p: re.search(p, text)
        name, lvl, exp, lb, la, lg = (get(r).group(1) if get(r) else None for r in 
            [r"PLayer NamE\s*:\s*(.+)", r"PLayer SerVer\s*:\s*(.+)", r"Exp\s*:\s*(\d+)", 
             r"LiKes BeFore\s*:\s*(\d+)", r"LiKes After\s*:\s*(\d+)", r"LiKes GiVen\s*:\s*(\d+)"])
        return name , f"{lvl}" if lvl else None, int(lb) if lb else None, int(la) if la else None, int(lg) if lg else None
    except: return None, None, None, None, None
    
def Requests_SPam(id):
    Api = requests.get(f'https://tokens-asfufvfshnfkhvbb.francecentral-01.azurewebsites.net/ReQuesT?id={id}&type=spam')        
    if Api.status_code in [200, 201] and '[SuccessFuLy] -> SenDinG Spam ReQuesTs !' in Api.text: return True
    else: return False

def GeT_Name(uid , Token):
    data = bytes.fromhex(EnC_AEs(f"08{EnC_Uid(uid , Tp = 'Uid')}1007"))
    url = "https://clientbp.common.ggbluefox.com/GetPlayerPersonalShow"
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': RELEASE_VERSION,
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Authorization': f'Bearer {GeTToK()}',
        'Content-Length': '16',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'
    }
    response = requests.post(url , headers=headers , data=data ,verify=False)
    if response.status_code == 200 or 201:
        packet = binascii.hexlify(response.content).decode('utf-8')
        BesTo_data = json.loads(DeCode_PackEt(packet))      
        try:
            a1 = BesTo_data["1"]["data"]["3"]["data"]
            return a1
        except: return ''  
    else: return ''
            	  	
def GeT_PLayer_InFo(uid , Token):
    data = bytes.fromhex(EnC_AEs(f"08{EnC_Uid(uid , Tp = 'Uid')}1007"))
    url = "https://clientbp.common.ggbluefox.com/GetPlayerPersonalShow"
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': RELEASE_VERSION,
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Authorization': f'Bearer {GeTToK()}',
        'Content-Length': '16',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'}
    response = requests.post(url , headers=headers , data=data ,verify=False)
    if response.status_code == 200 or 201:
        packet = binascii.hexlify(response.content).decode('utf-8')
        BesTo_data =  json.loads(DeCode_PackEt(packet))
        NoCLan = False   
        try:        
            a1 = str(BesTo_data["1"]["data"]["1"]["data"])
            a2 = BesTo_data["1"]["data"]["21"]["data"]
            a3 = BesTo_data["1"]["data"]["3"]["data"]
            player_server = BesTo_data["1"]["data"]["5"]["data"]
            player_bio = BesTo_data["9"]["data"]["9"]["data"]
            player_level = BesTo_data["1"]["data"]["6"]["data"]
            account_date = datetime.fromtimestamp(BesTo_data["1"]["data"]["44"]["data"]).strftime("%I:%M %p - %d/%m/%y")
            last_login = datetime.fromtimestamp(BesTo_data["1"]["data"]["24"]["data"]).strftime("%I:%M %p - %d/%m/%y")
            try:
                clan_id = BesTo_data["6"]["data"]["1"]["data"]
                clan_name = BesTo_data["6"]["data"]["2"]["data"]
                clan_leader = BesTo_data["6"]["data"]["3"]["data"]
                clan_level = BesTo_data["6"]["data"]["4"]["data"]
                clan_members_num = BesTo_data["6"]["data"]["6"]["data"]
                clan_leader_name = BesTo_data["7"]["data"]["3"]["data"]                       
            except:
                NoCLan = True
            if NoCLan:
            	a = f'''
[b][c][90EE90] [SuccessFully] - Get PLayer s'InFo !

[FFFF00][1] - ProFile InFo :
[ffffff]	
 Name : {a3}
 Uid : {xMsGFixinG(a1)}
 Likes : {xMsGFixinG(a2)}
 LeveL : {player_level}
 Server : {player_server}
 Bio : {player_bio}
 Creating : {account_date}
 LasT LoGin : {last_login}
 
  [90EE90]Dev : S M\n'''            
            	a = a.replace('[i]','')
            	return a
            	  	            	            
            else:            	          	                        
            	a = f'''
[b][c][90EE90] [SuccessFully] - Get PLayer s'InFo !

[FFFF00][1] - ProFile InFo :
[ffffff]	
 Name : {a3}
 Uid : {xMsGFixinG(a1)}
 Likes : {xMsGFixinG(a2)}
 LeveL : {player_level}
 Server : {player_server}
 Bio : {player_bio}
 Creating : {account_date}
 LasT LoGin : {last_login}

[b][c][FFFF00][2] - Guild InFo :
[ffffff]
 Guild Name : {clan_name}
 Guild Uid : {xMsGFixinG(clan_id)}
 Guild LeveL : {clan_level}
 Guild Members : {clan_members_num}
 Leader s'Uid : {xMsGFixinG(clan_leader)}
 Leader s'Name : {clan_leader_name}

  [90EE90]Dev : S M\n'''	
            	a = a.replace('[i]','')    
            	return a
                                       
        except Exception as e:
           return f'\n[b][c][FFD700]FaiLEd GeTinG PLayer InFo !\n'
    else:
        return f'\n[b][c][FFD700]FaiLEd GeTinG PLayer InFo !\n'
    
def DeLet_Uid(id , Tok):
    print(f' Done FuckinG > {id} ')
    url = 'https://clientbp.common.ggbluefox.com/RemoveFriend'
    headers = {
        'X-Unity-Version': '2018.4.11f1',
        'ReleaseVersion': RELEASE_VERSION,
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-GA': 'v1 1',
        'Authorization': f'Bearer {Tok}',
        'Content-Length': '16',
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; ASUS_Z01QD Build/QKQ1.190825.002)',
        'Host': 'clientbp.ggblueshark.com',
        'Connection': 'Keep-Alive',
        'Accept-Encoding': 'gzip'}
    data = bytes.fromhex(EnC_AEs(f"08a7c4839f1e10{EnC_Uid(id , Tp = 'Uid')}"))
    ResPonse = requests.post(url , headers=headers , data=data , verify=False)    
    if ResPonse.status_code == 400 and 'BR_FRIEND_NOT_SAME_REGION' in ResPonse.text:
        return f'[b][c]Id : {xMsGFixinG(id)} Not In Same Region !'
    elif ResPonse.status_code == 200:
        return f'[b][c]Good Response Done Delete Id : {xMsGFixinG(id)} !'
    else:
        return f'[b][c]Erorr !'
                                                        
def ChEck_The_Uid(id):
    Api = requests.get("https://panel-g2ccathtf6gdcmdw.polandcentral-01.azurewebsites.net/Uids")
    if Api.status_code not in [200, 201]: 
        return False    
    lines = Api.text.splitlines()    
    for i, line in enumerate(lines):
        if f' - Uid : {id}' in line:
            expire, status = None, None
            for sub_line in lines[i:]:
                if "Expire In" in sub_line: 
                    expire = re.search(r"Expire In\s*:\s*(.*)", sub_line).group(1).strip()
                if "Status" in sub_line: 
                    status = re.search(r"Status\s*:\s*(\w+)", sub_line).group(1)
                if expire and status: return status, expire
            return False
    return False
