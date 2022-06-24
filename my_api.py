def data_convert(data_text):
    # game_id = current_url.split('/')[-1]
    data_dict = {
        'time': 0,
        'set': 0,
        'away': {
            'name': '',
            'scores': [],
            'total_point': 0,
            'hist_games_score': [],
            'hist_total_points': [],
        },
        'home': {
            'name': '',
            'scores': [],
            'total_point': 0,
            'hist_games_score': [],
            'hist_total_points': [],
        }
    }
    try:
        data_text = data_text[:data_text.index('Дополнительные матчи')]
    except ValueError:
        pass
    if data_text[0] == '1.':
        for i in range(len(data_text)):
            match data_text[i]:
                case '1.':
                    data_dict['away']['name'] = data_text[i+1]
                    continue
                case '2.':
                    data_dict['home']['name'] = data_text[i+1]
                    points = "".join(
                        [',' if i == '(' else i for i in data_text[i+2] if not i in [')', ' ', 'O', 'T']])
                    points = [i.split(':') for i in points.split(',')]
                    if len(points) == 1:
                        k = 0
                    else:
                        k = 1
                    data_dict['away']['scores'] = [int(i[0]) for i in points][k:]
                    data_dict['away']['total_point'] = int(points[0][0])
                    data_dict['home']['scores'] = [int(i[1]) for i in points][k:]
                    data_dict['home']['total_point'] = int(points[0][1])
                    data_dict['time'] = data_text[i+3]
                    data_dict['set'] = len(data_dict['away']['scores'])
                    continue
                case ' - ':
                    hist_away_name = data_text[i-1]
                    hist_home_name = data_text[i+1]
                    if hist_away_name == 'Хозяева' or hist_home_name == 'Гости':
                        continue
                    hist_points = "".join(
                        [',' if i == '(' else i for i in data_text[i+2] if not i in [')', ' ', 'O', 'T', 'Д', 'В', 'П', 'е', 'н']])
                    hist_points = [i.split(':') for i in hist_points.split(',')]
                    away_hist_points = [int(i[0]) for i in hist_points][1:]
                    home_hist_points = [int(i[1]) for i in hist_points][1:]

                    if hist_away_name == data_dict['away']['name']:
                        data_dict['away']['hist_games_score'].extend(
                            away_hist_points)
                        data_dict['away']['hist_games_score'].sort()
                        data_dict['away']['hist_total_points'].append(
                            int(hist_points[0][0]))
                    if hist_away_name == data_dict['home']['name']:
                        data_dict['home']['hist_games_score'].extend(
                            away_hist_points)
                        data_dict['home']['hist_games_score'].sort()
                        data_dict['home']['hist_total_points'].append(
                            int(hist_points[0][1]))
                    if hist_home_name == data_dict['away']['name']:
                        data_dict['away']['hist_games_score'].extend(
                            home_hist_points)
                        data_dict['away']['hist_games_score'].sort()
                        data_dict['away']['hist_total_points'].append(
                            int(hist_points[0][0]))
                    if hist_home_name == data_dict['home']['name']:
                        data_dict['home']['hist_games_score'].extend(
                            home_hist_points)
                        data_dict['home']['hist_games_score'].sort()
                        data_dict['home']['hist_total_points'].append(
                            int(hist_points[0][1]))
    elif data_text[0] == '2.':
        for i in range(len(data_text)):
            match data_text[i]:
                case '2.':
                    data_dict['away']['name'] = data_text[i+1]
                    continue
                case '1.':
                    data_dict['home']['name'] = data_text[i+1]
                    points = "".join(
                        [',' if i == '(' else i for i in data_text[i+2] if not i in [')', ' ', 'O', 'T']])
                    points = [i.split(':') for i in points.split(',')]
                    if len(points) == 1:
                        k = 0
                    else:
                        k = 1
                    data_dict['away']['scores'] = [int(i[0]) for i in points][k:]
                    data_dict['away']['total_point'] = int(points[0][0])
                    data_dict['home']['scores'] = [int(i[1]) for i in points][k:]
                    data_dict['home']['total_point'] = int(points[0][1])
                    data_dict['time'] = data_text[i+3]
                    data_dict['set'] = len(data_dict['away']['scores'])
                    continue
                case ' - ':
                    hist_away_name = data_text[i-1]
                    hist_home_name = data_text[i+1]
                    if hist_away_name in ['Хозяева','Гости'] or hist_home_name in ['Хозяева','Гости']:
                        continue
                    hist_points = "".join(
                        [',' if i == '(' else i for i in data_text[i+2] if not i in [')', ' ', 'O', 'T', 'Д', 'В', 'П', 'е', 'н']])
                    hist_points = [i.split(':') for i in hist_points.split(',')]
                    away_hist_points = [int(i[0]) for i in hist_points][1:]
                    home_hist_points = [int(i[1]) for i in hist_points][1:]

                    if hist_away_name == data_dict['away']['name']:
                        data_dict['away']['hist_games_score'].extend(
                            away_hist_points)
                        data_dict['away']['hist_games_score'].sort()
                        data_dict['away']['hist_total_points'].append(
                            int(hist_points[0][0]))
                    if hist_away_name == data_dict['home']['name']:
                        data_dict['home']['hist_games_score'].extend(
                            away_hist_points)
                        data_dict['home']['hist_games_score'].sort()
                        data_dict['home']['hist_total_points'].append(
                            int(hist_points[0][1]))
                    if hist_home_name == data_dict['away']['name']:
                        data_dict['away']['hist_games_score'].extend(
                            home_hist_points)
                        data_dict['away']['hist_games_score'].sort()
                        data_dict['away']['hist_total_points'].append(
                            int(hist_points[0][0]))
                    if hist_home_name == data_dict['home']['name']:
                        data_dict['home']['hist_games_score'].extend(
                            home_hist_points)
                        data_dict['home']['hist_games_score'].sort()
                        data_dict['home']['hist_total_points'].append(
                            int(hist_points[0][1]))

    return data_dict
