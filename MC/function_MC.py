import sys
sys.path.append("MC")
from MC_utils import *
from Coord import *
sys.path.append("Gesture/type")
import Msg 

origin = Vec3(553,8,1373)

players = {
    "BlueMoon06":User1,
    "LLH":User3,
    "ZJT":User2,
    "LSK":User4,
    "Global":Global
}

ready = {
    "BlueMoon06":[False,False,False],
    "LLH":[False,False,False],
    "LSK":[False,False,False],
    "ZJT":[False,False,False]
}

def my_handleWearing(_players: list, msg: str) -> bool:
    [username, pose] = msg.split(':')
    id = getID(username)
    if not ready.get(username)[0] and (pose == Msg.RIGHTLEG or pose == Msg.LEFTLEG) :
        [x,y,z] = players.get(username).get("coord_boots")
        armor_b(id,x,y,z)
        print(msg)
        ready.get(username)[0] = True
    if pose == Msg.BODY and not ready.get(username)[1]:
        [x,y,z] = players.get(username).get("coord_chestplate")
        armor_c(id,x,y,z)
        print(msg)
        ready.get(username)[1] = True
    if pose == Msg.HEAD and not ready.get(username)[2]:
        [x,y,z] = players.get(username).get("coord_helmet")
        armor_h(id,x,y,z)
        print(msg)
        ready.get(username)[2] = True
    for user in _players:
        v = ready.get(user)
        if not v[0] or not v[1] or not v[2]:
            return False
    print('testing')
    return True
    
def my_handleFighting(_players: dict, msg: str) -> bool:
    [username, skill] = msg.split(':')
    print(msg)
    id = getID(username)
    if skill == Msg.FIREBALL:
        [x,y,z] = players.get(username).get("coord_FB")
        spell_FireBall(id,x,y,z)
    if skill == Msg.CAGE:
        [x,y,z] = players.get(username).get("coord_cage")
        spell_Cage(id,x,y,z)
    if skill == Msg.LIGHTNING:
        [x,y,z] = players.get(username).get("coord_ln")
        spell_LN(id,x,y,z)
    if skill == Msg.TNT:
        [x,y,z] = players.get(username).get("coord_tnt")
        spell_TNT(id,x,y,z)
    if MC_Gameover(players.get("Global")):
        return True

