import argparse
import os
import sys


class Parameters:
    """This class is being used for parsing the commandline arguments"""

    def __init__(self):
        self.cadasterPath = None
        self.pointCloudPath = None
        self.outputPath = None
        self.xoffset = 0.0
        self.yoffset = 0.0

        self.writeArgs()

    def parseArguments(self, args):
        """Method is parsing the commandline arguments to the variables create in __init__(self)"""

        parser = argparse.ArgumentParser(prog='Geodatenverarbeitung')

        filehandling = parser.add_argument_group('file handling')
        filehandling.add_argument("-c", "--cadaster", type=self.dir_path, help="path to cadaster directory")
        filehandling.add_argument("-p", "--pointcloud", type=self.dir_path, help="path to pointcloud directory")
        filehandling.add_argument("-o", "--output", type=self.writeable_dir, help="path to output directory")

        parser.add_argument("-x", "--xoffset", type=float, default=0, help="float expected, offset in direction x")
        parser.add_argument("-y", "--yoffset", type=float, default=0, help="flaot expected, offset in direction y")
        parser.add_argument("-v", '--version', action='version', version='%(prog)s 0.1')
        return parser.parse_args()
        

    def writeArgs(self):
        """Checks if certain arguments are given writes them to class variables then"""

        args = self.parseArguments(sys.argv[:1])

        if args.cadaster:
            self.cadasterPath = args.cadaster
        if args.pointcloud:
            self.pointCloudPath = args.pointcloud
        if args.output:
            self.outputPath = args.output
        if args.xoffset:
            self.xoffset = args.xoffset
        if args.yoffset:
            self.yoffset = args.yoffset


    def dir_path(self, path):
        """Checks the given directory paths"""

        if os.path.isdir(path):
            return path
        else:
            raise argparse.ArgumentTypeError(f"given directory {path} is not a valid path")
    
    def writeable_dir(self, path):
        """Checks if the given output path is also writeable"""
        
        if os.path.isdir(path):
            if os.access(path, os.W_OK):
                return path
            else:
                raise argparse.ArgumentTypeError(f"given directory {path} is not a writeable path")
        else: argparse.ArgumentTypeError(f"given directory {path} is not a valid path")


    def getCadasterPath(self):
        """Returns path to cadaster files if specified. 
        Otherwise returns None"""  
        return self.cadasterPath
    
    def getPointCloudPath(self):
        """Returns path to point cloud files if specified.
        Otherwise returns None"""
        return self.pointCloudPath

    def getOutputPath(self):
        """Returns path to output directory if specified.
        Otherwise returns None"""
        return self.outputPath

    def getXOffset(self):
        """Returns x-offset if given.
        Otherwise returns default (0.0)"""
        return self.xoffset

    def getYOffset(self):
        """Returns y-offset if given.
        Otherwise returns default (0.0)"""
        return self.yoffset

