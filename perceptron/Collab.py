import os
import collections
from multi_key_dict import multi_key_dict

wordsList = {}
# userMap=collections.defaultdict(list)
# movieMap=collections.defaultdict(list)
movieUserMap = collections.defaultdict(dict)
userMovieMap = collections.defaultdict(dict)
# userSet = collections.defaultdict(set)
# userMovieMap = multi_key_dict()
# userMovieMap["n","m"] ="p"
users =[]
movies =[]

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
    for row in lineText:
        data =row.split(',')
        #userMap.append({'movieId':data[1],'rating' :data[2]})
        #movieMap.append({'userId': data[2], 'rating': data[2]})

        # userMovie Map
        if not userMovieMap.has_key(data[1]):
            userMovieMap[data[1]] = {}
            users.append(data[1])

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

    # users = tempUsers.keys()
    # movies = tempMovies.keys()

        #userMap[data[1]].append({'movieId':data[0],'rating' :data[2]})
        #movieMap[data[0]].append({'userId':data[1],'rating':data[2]})
    #    userMovieMap[(data[1],data[0])] = data[2]
    #print userMovieMap
    #print "usermap", userMap['1744889']
    #print "moviemap", movieMap['8']
    averageUserRating()
    #print userMap['1032488'][0]['rating'],movieMap
   # print userMap['1032488'][0][0], movieMap


def averageUserRating():
    for userId in userMap.keys():
        print 'userid',userId
        ratingSum =0
        count =0
        #print 'usermap',userMap[userId]
        for userIdMap in userMap[userId]:
            #print  'useridmap',userId,userIdMa
            count +=1
            ratingSum += float(userIdMap['rating'])

        avgUserRating[userId]=ratingSum/count
    #    print ratingSum,count

    print userMovieMap
    #print avgUserRating

#def predictedVote(userId,movideId):

   # predictVote = avgUserRating[userId] + k*()


parseTrainData("C:/Users/tejamukka/PycharmProjects/Perceptron/assignment3/netflix/TrainingRatings.txt")