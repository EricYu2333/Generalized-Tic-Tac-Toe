import requests
from TTTHeader import *

class TTTGame():
    def __init__(self, url, teamId, gameId, myturn, userId, apiKey):
        self.url = url
        self.teamId = teamId
        self.gameId = gameId
        self.myturn = myturn
        self.userId = userId
        self.apiKey = apiKey
        self.headers = {
          'x-api-key': apiKey,
          'userId': userId,
          'User-Agent': 'PostmanRuntime/7.31.3'
##          'Accept': 'application/json,text/plain',
##          'Accept-Encoding': 'gzip,deflate,br',
##          'Accept-Language': 'en-US,en;q=0.9',
##          'Content-Type': 'application/json;charset=UTF-8'
        }

    def CreateTeam(self, name):
##        url = "https://www.notexponential.com/aip2pgaming/api/index.php"

        payload={'type': 'team',
        'name': name}
        files=[

        ]
##        headers = {
##          'x-api-key': 'd64cc161e1c3a039c8f4',
##          'userId': '1183',
##          'User-Agent': 'PostmanRuntime/7.31.3'
##        }

        response = requests.request("POST", self.url, headers=self.headers, data=payload, files=files)

##        print(response.text)
        return eval(response.text)

    def AddTeamMember(self, teamId, userId):
        payload={'type': 'member',
        'teamId': teamId,
        'userId': userId}
        files=[

        ]

        response = requests.request("POST", self.url, headers=self.headers, data=payload, files=files)

        return eval(response.text)

    def RemoveTeamMember(self, teamId, userId):
        payload={'type': 'removeMember',
        'teamId': teamId,
        'userId': userId}
        files=[

        ]

        response = requests.request("POST", self.url, headers=self.headers, data=payload, files=files)

        return eval(response.text)

    def GetTeamMembers(self, teamId):
        payload={}

        response = requests.request("GET", self.url+"?type=team&teamId="+teamId,
                                    headers=self.headers, data=payload)

        return eval(response.text)

    def GetMyTeams(self):
        payload={}

        response = requests.request("GET", self.url+"?type=myTeams",
                                    headers=self.headers, data=payload)

        return eval(response.text)

    def CreateGame(self, teamId1, teamId2, gameType, boardSize, target):
        payload={'type': 'game',
        'teamId1': teamId1,
        'teamId2': teamId2,
        'gameType': gameType,
        'boardSize': boardSize,
        'target': target}
        files=[

        ]

        response = requests.request("POST", self.url, headers=self.headers, data=payload, files=files)

        return eval(response.text)

    def GetMyGames(self):
        payload={}

        response = requests.request("GET", self.url+"?type=myGames",
                                    headers=self.headers, data=payload)

        return eval(response.text)

    def MakeMove(self, move, teamId, gameId):
        payload={'type': 'move',
        'move': move,
        'teamId': teamId,
        'gameId': gameId}
        files=[

        ]

        response = requests.request("POST", self.url, headers=self.headers, data=payload, files=files)

        return eval(response.text)

    def GetMoves(self, gameId, count):
        payload={}

        response = requests.request("GET", self.url+"?type=moves&gameId="+gameId+"&count="+count,
                                    headers=self.headers, data=payload)

        return eval(response.text)

    def GetBoardString(self, gameId):
        payload={}

        response = requests.request("GET", self.url+"?type=boardString&gameId="+gameId,
                                    headers=self.headers, data=payload)

        return eval(response.text)

    def GetBoardMap(self, gameId):
        payload={}

        response = requests.request("GET", self.url+"?type=boardMap&gameId="+gameId,
                                    headers=self.headers, data=payload)

        return eval(response.text)


# main function
if __name__ == '__main__':
    
    TTT = TTTGame(URL, TEAMID, GAMEID, MYTURN, USERID, APIKEY)
##    dict = TTT.GetMoves("3707", str(BOARDSIZE*BOARDSIZE))
##    print(len(dict['moves']))
##    dict = TTT.CreateGame("1339", TEAMID, "TTT", BOARDSIZE, TARGET)
##    print(dict)
    dict = TTT.GetMyGames()
    print(dict)
