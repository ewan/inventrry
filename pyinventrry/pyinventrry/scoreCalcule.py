import sys
import argparse
import pandas as _pd
import pyinventrry as _pi
import pyinventrry.util as _ut
import pyinventrry.data_manager as _dm

def calculate_score( inv_whole, spec_whole, norm_tab, write_file) :
    '''
    Calculate and print economic, local and global scores of multiple inventories.
    :param inv_whole: The DataFrame regrouping all inventories.
    :param spec_whole: The DataFrame regrouping all specifications for these inventories.
    :param norm_tab: The normalization tab.
    :param write_file: the destination for writting results
    :type inv_whole: DataFrame
    :type spec_whole: DataFrame
    :type norm_tab: DataFrame
    :type write_file: str
    '''
    meta_keys = _dm.calculate_keys(inv_whole)

    meta_keys_spec = _dm.calculate_keys(spec_whole)

    delta_keys = list(set(meta_keys_spec) - set(meta_keys))
    unique = _dm.calculate_unique(inv_whole,[[]], list(meta_keys))
    if norm_tab is None :
        result_global = _pd.DataFrame(columns=meta_keys + delta_keys + ['size','nfeat','nmpairs','nimbalance'])
    else :
        result_global = _pd.DataFrame(columns=meta_keys + delta_keys + ['econ','loc','glob'])
    result_global.to_csv(write_file,index=False)

    for t in unique:
        inv = _dm.extract_data_frame(inv_whole, t)
        spe = _dm.extract_data_frame(spec_whole, t)
        spec_keys = _dm.calculate_unique(spe, [[]], list(delta_keys))
        for s_key in spec_keys :
            x = (_dm.extract_data_frame(spe,s_key))
            d = dict(t+s_key)
            s, e_f, l, g = _pi.stats.stat(inv, (_ut.get_true_specs(x.iloc[0].to_dict())),norm_tab)
            if norm_tab is None :
                result = _pd.DataFrame(columns=meta_keys + delta_keys + ['size','nfeat','nmpairs','nimbalance'])
                d['size'] = s
                d['nfeat'] = e_f
                d['nmpairs'] = l
                d['nimbalance'] = g
            else :
                result = _pd.DataFrame(columns=meta_keys + delta_keys +['econ','loc','glob'])
                d['econ'] = e_f
                d['loc'] = l
                d['glob'] = g
            result = result.append(d, ignore_index=True)
            result.to_csv(write_file, mode = 'a', header=False, index=False)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument("inventory",
        help = 'A file with the correct format for the inventory')
    parser.add_argument("specs",
        help = 'A file with the correct format for the specs')
    parser.add_argument("-n", "--norm_tab", default = None,
        help = 'A file used for normalize data')
    parser.add_argument("-w", "--write", default=sys.stdout,
        help = 'The path to the file where results will be written. ')
    parser.add_argument("-i", "--ignore-columns", default='', type=str,
        help = 'Comma-separated list of columns to ignore')

    args = parser.parse_args(sys.argv[1:])
    ignore_columns = filter(None, args.ignore_columns.split(','))
    inv_raw = _dm.open_file(args.inventory)
    inv = inv_raw.drop(ignore_columns, axis=1)
    specs = _dm.open_file(args.specs)
    if args.norm_tab is None :
        norm_tab = None
    else:
        norm_tab = _dm.open_file(args.norm_tab),
    calculate_score(inv, specs, norm_tab, args.write)

if __name__ == "__main__":
    main()

