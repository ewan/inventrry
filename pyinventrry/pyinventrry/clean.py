import sys
import argparse
import pandas
import data_manager as _dm


def clean_data_frame(dataframe):
	duplicates = set(dataframe.replace('0','-').drop_duplicates().index)
	print(duplicates)
	bad_ones = set(dataframe.index) - duplicates
	print(bad_ones)
	final = dataframe.loc[list(set(dataframe.index)-bad_ones)].replace('0','-')
	final = final.append(dataframe.loc[list(bad_ones)].replace('0','+'))
	return final.sort_index()

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("inventory", help = 'A file with the correct format for the inventory')
	parser.add_argument("-w", "--write", default=sys.stdout, help = 'The path to the file where results will be written. ')
	args = parser.parse_args(sys.argv[1:])
	clean_data_frame(_dm.open_file(args.inventory)).to_csv(args.write)

if __name__ == "__main__":
	main()