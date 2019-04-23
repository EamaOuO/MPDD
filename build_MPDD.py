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
    
    crawler = scriptcrawler.ScriptCrawler(args.data_dir)
    mpdd = crawler.get_dialogue()

    if not os.path.isdir(args.output_dir):
        os.mkdir(args.output_dir)
        
    output_path = os.path.join(args.output_dir, 'Dialogue.json')
    with open(output_path, 'w', encoding='utf8') as f:
        json.dump(mpdd, f)

if __name__ == '__main__':
    main()
