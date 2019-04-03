# coding=utf-8

import os
import json
import argparse

import scriptcrawler

def main():
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="The input data directory. Should contain 'Urls.json' and 'Label.json'.")
    parser.add_argument("--output_dir",
                        default=None,
                        type=str,
                        required=True,
                        help="The output directory of MPDD.")
    args = parser.parse_args()
    
    crawler = scriptcrawler.ScriptCrawler(args.data_dir, args.output_dir)
    dialogue = crawler.get_dialogue()
    
    
if __name__ == '__main__':
    main()
