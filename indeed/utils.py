import hashlib


def combinations(job_or_title):
    tokens = job_or_title.split(' ')
    partial_string = ''
    for i in range(0, len(tokens)):
        yield u'{}{}'.format(partial_string, tokens[i])
        partial_string += u'{} '.format(tokens[i])


def get_job_id(job):
    hasher = hashlib.md5()
    job_string = job['title'] + job['company']
    hasher.update(job_string.encode('utf-8'))
    return hasher.hexdigest()
