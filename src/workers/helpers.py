from datetime import timedelta


def get_time_diff(start, finish):
    return finish - start


def records_to_list(records):
    result = {
        'items': {},
        'total': ''
    }
    total = timedelta(seconds=0)
    total_day = timedelta(seconds=0)

    for record in records:
        total_item = timedelta(seconds=0)
        if record.finish:
            diff = get_time_diff(record.start, record.finish)
            total += diff
            total_day += diff
            total_item = diff

        if str(record.date) not in result['items']:
            total_day = timedelta(seconds=0)
            result['items'][str(record.date)] = {
                'records': [],
                'total_day': ''
            }
        total_day += total_item
        result['items'][str(record.date)]['records'].append({
            'start': record.start,
            'finish': record.finish,
            'comment': record.comment,
            'total_str': convert_seconds_to_hours_str(total_item)
        })

        result['items'][str(record.date)]['total_day'] = convert_seconds_to_hours_str(total_day)
    result['total_hours_str'] = convert_seconds_to_hours_str(total)
    return result


def convert_seconds_to_hours_str(time_delta_obj):
    total_seconds = time_delta_obj.total_seconds()
    seconds = total_seconds
    hour = seconds // 3600
    seconds %= 3600
    minutes = seconds // 60
    seconds %= 60

    return "%02d:%02d:%02d" % (hour, minutes, seconds)
