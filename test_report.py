import argparse
import json

#define CLI args
parser = argparse.ArgumentParser(description='Generate a test report based on test resullt in json.')
parser.add_argument('file_path', type=str, help='JSON fil path as input')
parser.add_argument('--type', type=str, default='text', help='The type of report to generate: "text" or "json" (default: "text")')
parser.add_argument('--output', type=str, default='report', help='The name of the output file')
args = parser.parse_args()

# Open the JSON file from command file_path
with open(args.file_path, 'r') as file:
    data = json.load(file)

# set info variable
version = data['distribution']['description']
fail_list=[]
time_sec = 0.0
passed = 0
failed = 0
skipped = 0

for result in data['results']:
    #accumulating testtime
    time_sec += result['duration']

    #pass condition
    if result['status'] == 'pass':
        passed += 1

    #skip condition
    elif result['status'] == 'skip':
        skipped += 1

    #fail condition
    elif result['status'] == 'fail':
        fail_list.append(result['id'])
        failed += 1
    
total = passed + failed + skipped

skipped_percent = round((skipped / total) * 100)
failed_percent = round((failed / total) * 100)
passed_percent = round((passed / total) * 100)

#type options
if args.type == 'text':
# Format 
    ostring = ""
    ostring += "Version: {}\n".format(version)
    ostring += "Number of tests run: {}\n".format(total)
    ostring += "Outcome:\n"
    ostring += "- pass: {} ({}%)\n".format(passed,passed_percent)
    ostring += "- fail: {} ({}%)\n".format(failed,failed_percent)
    ostring += "- skip: {} ({}%)\n".format(skipped,skipped_percent)
    ostring += "Total run duration: {:.2f} seconds\n".format(time_sec)
    ostring += "List of failed tests:\n"
    for i, fail_test in enumerate(fail_list):
        ostring += "{}. {}\n".format(i+1,fail_test)

# Export
    with open(args.output + '.txt', 'w') as report_file:
        report_file.write(ostring)
        print("Test Report saved to {}.txt".format(args.output))

elif args.type=='json':
# Format json
    ostring = {
        'version': version,
        'Number of tests run': total,
        'pass': passed,
        'fail': failed,
        'skip': skipped,
        'total_duration': time_sec,
        'failed_tests': fail_list
    }
# Export
    with open(args.output + '.json', 'w') as report_file:
        json.dump(ostring, report_file)
        print("Test Report saved to {}.json".format(args.output))
