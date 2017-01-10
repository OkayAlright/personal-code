"""
Naive Bayes Spam Filter

By Logan Davis

Python 2.7 | Ubunutu 15 | Atom Text Editor

textblob is a third-party library. For further reading
and download links head here: https://textblob.readthedocs.org/en/dev/
"""
from textblob.classifiers import NaiveBayesClassifier
from os import listdir
from sets import Set

class NB_Spam_Filter(object):
    """
    NB_Spam_Filter is a toy implementation of a Naive Bayesian
    Spam Filter. The way to get the working is so create two
    sub directories where the file is being run, one for holding training
    (named "training") files and another for holding test files (named "test").
    With in the training folder, two more folders should exists "spam" and
    "nonspam."

    To get the filter to run, just instance the object and then call
    "self.classify()".

    Arguements = 2:
      - path = a string that is the file path from the root directory
               to where your traing and test directories are located.
      - quantity_for_training = the amount of texts from each catagory
        (spam and nonspam) the filter will use to train.
    """
    def __init__(self, path, quantity_for_training = 10):
        self.file_path = path   #a path to training and test files
        self.training_data = (self._collect_features("training/spam/","spam", quantity_for_training)[1] +
                              self._collect_features("training/nonspam/","ham", quantity_for_training)[1])
        self.classifier = NaiveBayesClassifier(self.training_data)
        self.results = None #Tests have not yet been run

    def __str__(self):
        """
        pretty printing for the object
        """
        return "This classifier has a training set of {} files and the results of testing are {}." \
        .format(len(self.training_data), self.results)

    def classify(self, subdir ="test/", display_table = False):
        """
        Classifies texts in a given directory as being spam or not spam
        and returns the results while sorting them in self.results.

        Arguements = 2:
          - subdir = the sub-path from the path passed in at object instancing
                     to the files you wish to analyze.
          - display_table = Boolean value, will print out the results in
            real-time.
        """
        files_to_test = self._collect_features(subdir, "test", None)
        results = {}
        counter = 1
        for i in xrange(len(files_to_test[0])):
            answer = self.classifier.classify(files_to_test[1][i][0])
            results[files_to_test[0][i]] = answer
            if display_table == True:
                print "The file {} has been classified as {}".format(counter,answer)
            counter += 1
        self.results = results
        return results



    def _collect_features(self, subdir, type, quantity = None):
        """
        Collects words from files and turns them into a dictionary that catalogs
        what words have been found and how many times they were found.

        Arguements = 3:
          - subdir = the sub-path from the path passed in at object instancing
                     to the files you wish to analyze.
          - type = whether you are collecting spam, ham, or testing.
          - quantity = the amount of texts the filter reads and compiles.
        """
        files_to_collect = listdir(self.file_path + subdir)
        useless_words = Set(['the','a','of','an','to'])
        punct_and_formatting_chars = Set([",",".",":",";","\n","\t","?","!"])
        files_as_list = []
        list_of_names = []
        if quantity == None:
            quantity = len(files_to_collect)
        for i in xrange(quantity):
            training_data = open(self.file_path + subdir + files_to_collect[i])
            indiv_file = ""
            for line in training_data:
                line_as_list = line.lower().split(" ")  #creates a list of consistently formatted words
                for word in line_as_list:
                    if (word == "") or (max(map(ord, word)) > 128):
                        break
                    if word[-1] in punct_and_formatting_chars: #shaves off puncuation and meta chars
                        word = word[:-1:]
                    if word not in useless_words:  #shaves off articles
                        indiv_file += word
            training_data.close()
            list_of_names.append(files_to_collect[i])
            files_as_list.append((indiv_file,type))
        return (list_of_names,files_as_list)
