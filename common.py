import subprocess


def form_list(value_dict, limit=10):
    string_list = ''
    for value in list(sorted(value_dict.items(), key=lambda x: x[1], reverse=True))[:int(limit]:
        string_list += '%s: %s\n' % (value[0], value[1])
    return string_list


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', './messages/%s.txt' % fname], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])
