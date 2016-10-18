#! /usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import json
import sys
import os


defaultConfigName="bronfig.json"

def printv(arg1):
    """
    Verbose print
    """
    if VERBOSE:
        print(arg1)

class Configuration(object):

    """Docstring for Configuration. """

    def __init__(self, filePath):
        self._filePath = filePath
        self._json = self.getJson()
        self._result_json = []

    def getJson(self):
        printv("Reading in the configuration")
        configFp = open(self._filePath,"r")
        return json.load(configFp)

    def getCrawler(self):
        """TODO: Docstring for getCrawler.

        :f: TODO
        :returns: TODO

        """
        printv("Parsing crawler location")
        return self._json["crawler-location"]

    def execCrawler(self):
        """TODO: Docstring for execCrawler.
        :returns: TODO

        """
        crawlerLocation = self.getCrawler()
        output = [line \
                for line in os.popen(crawlerLocation).read().split("\n") \
                if not len(line) == 0]
        printv("Filtered files")
        printv(output)
        return output

    def getParser(self):
        """TODO: Docstring for getParser.

        :f: TODO
        :returns: TODO

        """
        printv("Parsing parser location")
        return self._json["parser-location"]

    def execParser(self, filePath):
        """TODO: Docstring for execParse.

        :f: TODO
        :returns: TODO

        """
        parserLocation = self.getParser()
        jsonDataString = os.popen( parserLocation  + " " + filePath).read()
        printv(jsonDataString)
        jsonData = json.loads(jsonDataString)
        return jsonData

    def appendToResults(self, dictObject):
        """TODO: Docstring for appendToResults.

        :dictObject: TODO
        :returns: TODO

        """
        self._result_json.append(dictObject)

    def run(self):
        """TODO: Docstring for run.

        :f: TODO
        :returns: TODO

        """
        printv("Running the main config task")
        folders = self.execCrawler()
        for folder in folders:
            jsonObject = self.execParser(folder)
            self.appendToResults(jsonObject)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculation data miner")

    parser.add_argument("-v",
            "--verbose",
            help   = "Make the output verbose",
            action = "store_true")

    parser.add_argument("-f",
            help   = "Input file.",
            action = "store")

    parser.add_argument("--config",
            help    = "Custom configuration file",
            default = defaultConfigName,
            action="store")

    # Parse arguments
    args = parser.parse_args()

    if args.verbose:
        print("Making the command verbose...")
        VERBOSE=True
    else:
        VERBOSE=False

    configuration = Configuration(args.config)
    configuration.run()



#vim-run: python % -v
#vim-run: python % -v -h
