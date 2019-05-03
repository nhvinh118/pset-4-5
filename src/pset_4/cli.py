# -*- coding: utf-8 -*-
"""
    Module that contains the command line app.
    This will set the command arguments in <args> and call Stylize

"""
import argparse
import luigi

import pset_4.tasks.stylize as stylize

def main(args=None):
	
	main_arg_parser = argparse.ArgumentParser(description="parser for fast-neural-style")
	main_arg_parser.add_argument("--content-image", type=str, default = '')
	main_arg_parser.add_argument("--content-scale", type=float, default = 1.0)
	main_arg_parser.add_argument("--output-image", type=str, default = '')
	main_arg_parser.add_argument("--cuda", type=int, default = 0)
	main_arg_parser.add_argument("--export_onnx", type=str, default = '')
	main_arg_parser.add_argument("-i", "--image", default='luigi.jpg')
	main_arg_parser.add_argument("-m", "--model", default='rain_princess.pth')

	args = main_arg_parser.parse_args()

	luigi.build([
		stylize.Stylize(image=args.image, model=args.model)
		], local_scheduler=True)

if __name__ == "__main__": 
	main()
