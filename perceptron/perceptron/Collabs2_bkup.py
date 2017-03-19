import os
import collections
import math
from multi_key_dict import multi_key_dict

#wordsList = {}
# userMap=collections.defaultdict(list)
# movieMap=collections.defaultdict(list)
movieUserMap = collections.defaultdict(dict)
userMovieMap = collections.defaultdict(dict)
corrweightMap = collections.defaultdict(dict)
# userSet = collections.defaultdict(set)
# userMovieMap = multi_key_dict()
# userMovieMap["n","m"] ="p"
kappa = 0
users =[]
movies =[]
ratingAvgUserMap ={}
# print  userMovieMap
avgUserRating ={}
def parseTrainData(filePath):
    trainpath = filePath
    #dirham = os.listdir(trainpath)
    f = open(trainpath, 'r')
    text = f.readlines()
#    print textRead
    lineText = [rows.strip() for rows in text]
    tempUsers = {}
    tempMovies = {}
    usersCount = 0
    for row in lineText:
        data =row.split(',')
        #userMap.append({'movieId':data[1],'rating' :data[2]})
        #movieMap.append({'userId': data[2], 'rating': data[2]})

        # userMovie Map
        if not userMovieMap.has_key(data[1]):
            if usersCount<=10000:
                userMovieMap[data[1]] = {}
                users.append(data[1])

        if userMovieMap.has_key(data[1]):
            currentUser = userMovieMap[data[1]]
            if not currentUser.has_key(data[0]):
                currentUser[data[0]] = data[2]

            # movieUser Map
            if not movieUserMap.has_key(data[0]):
                movieUserMap[data[0]] = {}
                movies.append(data[0])

            currentMovie = movieUserMap[data[0]]
            if not currentMovie.has_key(data[1]):
                currentMovie[data[1]] = data[2]
        usersCount += 1

    # users = tempUsers.keys()
    # movies = tempMovies.keys()

        #userMap[data[1]].append({'movieId':data[0],'rating' :data[2]})
        #movieMap[data[0]].append({'userId':data[1],'rating':data[2]})
    #    userMovieMap[(data[1],data[0])] = data[2]
    #print userMovieMap
    #print "usermap", userMap['1744889']
    #print "moviemap", movieMap['8']
    userRatingAverage()
    calcAllCorrelationWeights()
    #print userMap['1032488'][0]['rating'],movieMap
   # print userMap['1032488'][0][0], movieMap


def userRatingAverage():
    for user in users:
        ratingsum =0
        count =0
        for rating in userMovieMap[user]:
            ratingsum += float(userMovieMap[user][rating])
        ratingAvgUserMap[user] = ratingsum/len(userMovieMap[user])
    print ratingAvgUserMap


def predictVote(userId,movieId):
    # if userMovieMap.has_key(userId):
    weightedvotesum =0
    for user in users:
        if userMovieMap[user].has_key(movieId):
            weightedvotesum += corrweightMap[userId][user]*(float(userMovieMap[user][movieId]) - ratingAvgUserMap[user])
    predictedValue = ratingAvgUserMap[userId] + kappa*(weightedvotesum)
    return predictedValue


def corrweight(user1,user2):
    numerator =0
    userdenom = 0
    user1denom = 0
    user2denom = 0
    for movie in movies:
        if userMovieMap[user1].has_key(movie) and userMovieMap[user2].has_key(movie):
            temp1 = float(userMovieMap[user1][movie]) - ratingAvgUserMap[user1]
            temp2 = float(userMovieMap[user2][movie]) - ratingAvgUserMap[user2]

            numerator +=(temp1)*(temp2)

            user1denom += math.pow(temp1,2)
            user2denom += math.pow(temp2,2)

    userdenom = user1denom * user2denom
    userdenom = math.sqrt(userdenom)
    if userdenom != 0:
        result = numerator / userdenom
        return result
    else:
        return 0

def calcAllCorrelationWeights():
    outerLoopIndex = 0
    userLength = len(users)
    totalCorrelationSum = 0
    while (outerLoopIndex< userLength):
        if not corrweightMap.has_key(users[outerLoopIndex]):
            corrweightMap[users[outerLoopIndex]] = {}
        innerLoopIndex = outerLoopIndex+ 1
        while (innerLoopIndex < userLength):
            if not corrweightMap.has_key(users[innerLoopIndex]):
                corrweightMap[users[innerLoopIndex]] = {}
            temp = corrweight(users[outerLoopIndex], users[innerLoopIndex])
            corrweightMap[users[outerLoopIndex]][users[innerLoopIndex]] = temp
            corrweightMap[users[innerLoopIndex]][users[outerLoopIndex]] = temp
            totalCorrelationSum += temp
            innerLoopIndex+=1
        outerLoopIndex += 1
    kappa = 1/totalCorrelationSum



    # 8, 573364

#     for userId in userMap.keys():
#         print 'userid',userId
#         ratingSum =0
#         count =0
#         #print 'usermap',userMap[userId]
#         for userIdMap in userMap[userId]:
#             #print  'useridmap',userId,userIdMa
#             count +=1
#             ratingSum += float(userIdMap['rating'])
#
#         avgUserRating[userId]=ratingSum/count
#     #    print ratingSum,count
#
#     print userMovieMap
#     print corrweightMap
    #print avgUserRating


def Test(filePath):
    testPath = filePath
    # dirham = os.listdir(trainpath)
    f = open(testPath,'r')
    text = f.readlines()
    #    print textRead
    lineText = [rows.strip() for rows in text]
    tempUsers = {}
    tempMovies = {}
    usersCount = 0
    errorsum =0
    count =0
    for row in lineText:
        data = row.split(',')
        if userMovieMap.has_key(data[1]):
            count+=1
            result =predictVote(data[1],data[0])
            errorsum += math.pow(result -float(data[2]),2)

    print errorsum/count
            # print result, data[2]




        #def predictedVote(userId,movideId):

   # predictVote = avgUserRating[userId] + k*()


if __name__ == "__main__":
    parseTrainData("assignment3/netflix/TrainingRatings.txt")
    Test("assignment3/netflix/TestingRatings.txt")