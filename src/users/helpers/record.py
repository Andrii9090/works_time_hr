def get_time_diff(start, finish):
    return finish - start


def records_to_list(records):
    result = {
        'items': [],
        'total': ''
    }
    total = 0
    for record in records:
        diff = get_time_diff(record.start, record.finish)
        total += diff.seconds
        diff_str = str(diff)
        result['items'].append(
            {'start': record.start, 'finish': record.finish, 'comment': record.comment, 'diff': diff.seconds,
             'diff_str': diff_str})
    result['total'] = total
    result['total_hours_str'] = convert_seconds_to_hours_str(total)
    return result


def convert_seconds_to_hours_str(seconds):
    seconds = seconds % (24 * 3600)
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%02d:%02d:%02d" % (hour, minutes, seconds)