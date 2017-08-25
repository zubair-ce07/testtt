import sys
import getopt
from tweet_reader import TweetReader
from tweet_parser import TweetParser


def get_search_query():
    """
    Checking whether command line arguments are given or not
    """
    if len(sys.argv) == 1:
        print ("Compile program as : test.py -s <Search Query>")
        sys.exit(2)

    """
    Checking whether the arguments given are 
    in the correct format or not
    """
    try:
        opts, args = getopt.getopt(sys.argv[1:],"s:")
    except getopt.GetoptError:
        print ("Compile program as : test.py -s <Search Query>")
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-s':
            print ("To Search Query : " + arg)
            return arg

if __name__ == "__main__":
    search_query = get_search_query()

    reader = TweetReader()
    reader.authorize_connection()
    tweet_generator = reader.read_public_tweets()

    parser = TweetParser()

    for i in range(0, 10):
        tweet = next(tweet_generator)
        if search_query in tweet:
            print ("\n======================Tweet=======================\n")
            print (tweet)
            print ("\n----------------------Parsed----------------------\n")
            for tag in parser.parse(tweet):
                print (tag + "\t")
