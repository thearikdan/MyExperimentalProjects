def extract_part_from_file(in_file, out_file, part):
    out_f = open(out_file, "w")
    with open(in_file) as in_f:
        for line in in_f:
            parts = line.split("|")
            txt = parts[part]
            out_f.write(txt)
            out_f.write('\n')

extract_part_from_file("tickers/nasdaqlisted_orig.txt", "tickers/nasdaqlisted.txt", 0)
extract_part_from_file("tickers/otherlisted_orig.txt", "tickers/otherlisted.txt", 0)
