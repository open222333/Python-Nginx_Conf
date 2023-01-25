from genral import NGINX_DIR
from genral.function import ProgressBar, get_all_files, get_domain_from_nginx_config, is_domain, check_ns, is_own_ns
from pprint import pprint
import json


test = 1000
count = 0

command_dict = {}
with open('result.txt', 'w') as f:
    p = ProgressBar()
    files = get_all_files(NGINX_DIR, ['conf'])
    for conf in files:
        count += 1
        p(len(files), in_loop=True)
        file_name = get_domain_from_nginx_config(conf)
        if is_domain(file_name):
            check_result = check_ns(file_name)
            if check_result[0]:
                if not is_own_ns(check_result[1]):
                    f.write(f'{file_name}: {check_result[1]}\n')
                    dir_name = 'test'
                    if dir_name not in command_dict:
                        command_dict[dir_name] = [f"rm -rf {file_name}"]
                    else:
                        command_dict[dir_name].append(f"rm -rf {file_name}")
            else:
                f.write(f'{file_name}: {check_result[1]}\n')

        if count == test:
            break


with open('result_command.txt', 'w') as f:
    f.write(json.dumps(command_dict))
    pprint(command_dict)
