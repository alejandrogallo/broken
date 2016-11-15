#! /usr/bin/env python
# -*- coding: utf-8 -*-


import argparse
import json
import yaml
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

    def __init__(self, filePath, debug = False):
        self._filePath = filePath
        self._json = self.getJson()
        self._result_json = []
        self._debug = debug

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
        """
        If debug mode is on then it only returns the parsed information in form
        of string.

        :filePath: Location of the parser script
        :returns: dictionary if debug mode is off, string with json object if
        it is on.

        """
        parserLocation = self.getParser()
        yamlDataString = os.popen( parserLocation  + " " + filePath).read()
        printv(yamlDataString)
        yamlData = yaml.load(yamlDataString) if not self._debug else yamlDataString
        return yamlData

    def appendToResults(self, dictObject):
        """TODO: Docstring for appendToResults.

        :dictObject: TODO
        :returns: TODO

        """
        self._result_json.append(dictObject)

    def save(self, fileName="results"):
        """TODO: Docstring for save.

        :fileName: TODO
        :returns: TODO

        """
        with open(fileName+".yaml", "w") as outfile:
            yaml.dump(self._result_json, outfile)
        with open(fileName+".json", "w") as outfile:
            json.dump(self._result_json, outfile)

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

    parser.add_argument("--debug",
            help    = "Debug mode, for testing parser and crawler scripts",
            default = False,
            action="store_true")

    # Parse arguments
    args = parser.parse_args()

    if args.verbose:
        print("Making the command verbose...")
        VERBOSE=True
    else:
        VERBOSE=False

    configuration = Configuration(args.config, debug = args.debug)
    configuration.run()
    configuration.save()



#vim-run: python3 % -v
#vim-run: python % -v -h
