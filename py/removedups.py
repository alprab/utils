# Works with Python 2.7 Anaconda
#
# -----------------------------------------
# STILL EXPERIMENTING! DO NOT USE THIS YET!
# -----------------------------------------
# Removes duplicate files.  
# Starts from the parent directory and moves downwards.
# Covers all subdirectories
# Considers all files in the parent directory and all subdirectories together.
# Doesn't care about the file name - only if the content is identical.
# Leaves only one arbitrary instance of the file.
#
# It generates a shell script file with rm commands, 
# BUT actually does the deletes in the course of the run
#
# TODOs:
#  1. GUIfication for better usability
#  2. Dry-run feature
#  3. Temporary folder for work files
#  4. Clean up once done, e.g. delete work files
#  5. Document for Sphinx using restrucured text accoding to the instructins at: https://docs.python.org/devguide/documenting.html
#  6. Checks for file types and permissions / error recovery and reporting
#  7. Statistics - files space recovered / saved, total files, deleted files, total directories, max / min ...
#  8. Should work on Python 2 as well as 3
#  9. Parametrization of top-level directory
# 10. Logging
# 11. Results print out
# 12. 

import hashlib, csv, os


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def process_directory_csv(current_dir_fullpath, sub_dir_list, files, csvwriter):
    for file in files:
        full_name = current_dir_fullpath + '/' + file
        # print("                         " + full_name)
        csvwriter.writerow([md5(full_name), str(os.path.getsize(full_name)), full_name])


def walk_all_subdirectories(path, output_file_name):
    # count = 0
    with open(output_file_name, "w") as csvfile:
        csvwriter = csv.writer(csvfile, delimiter=':', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for current_dir, sub_dirs, files in os.walk(path):
            print(current_dir)
            process_directory_csv(current_dir, sub_dirs, files, csvwriter)
            csvfile.flush()
            # DEBUG CODE - process only 5 directories
            # count += 1
            # if count >= 10:
            # csvfile.close()
            # break;
        csvfile.close()


def sort_file(inname, outname):
    input_file = open(inname, "r")
    output_file = open(outname, "w", 1)
    lines = []  # give lines variable a type of list
    for line in input_file:
        lines.append(line)
    lines.sort()
    for line in lines:
        output_file.write(line)
    input_file.close()
    output_file.close()


def generate_delete_commands(sortedfile, outname):
    import csv
    output_file = open(outname, "w", 1)
    previous_checksum = "IMPOSSIBLE_CHECKSUM"
    with open(sortedfile) as f:
        reader = csv.reader(f, delimiter=':', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for row in reader:
            # print(row[0], row)
            if previous_checksum == row[0]:
                output_file.write("rm '" + row[2] + "'\n")
                print("removing " + row[2])
                os.remove(row[2])
            previous_checksum = row[0]
        f.close()
    output_file.close()


# Main program follows

directory_name = ".."
unsorted_file_name = "filelist.csv"
sorted_file_name = "sortedfilelist.csv"
delete_command_file_name = "deletecommands.sh"

if __name__ == '__main__':
    walk_all_subdirectories('..', unsorted_file_name)
    sort_file(unsorted_file_name, sorted_file_name)
    generate_delete_commands(sorted_file_name, delete_command_file_name)
