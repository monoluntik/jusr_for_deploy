from driver import MarathonBotDriver

class BasketballBet(MarathonBotDriver):

    def __init__(self):
        sport_id = 45356
        super().__init__(sport_id)

    def analysis(self, data_dict):
        time = data_dict['time']
        if time == 'Пер.':
            timek = 10
        elif '—' in f'{time}':
            timek = 10
        else:
            timek = int(time.split(':')[0])
        set = int(data_dict['set'])
        if set in [1,2]:
            return f"{data_dict['away']['name']} - WORLD{data_dict['home']['name']} set : {set} time : {time}"
        if set == 3 and timek <= 8:
            return f"{data_dict['away']['name']} - HELLO{data_dict['home']['name']} set : {set} time : {time}"
        elif set == 4 and timek >= 4:
            return f"{data_dict['away']['name']} - {data_dict['home']['name']} set : {set} time : {time}"
           
        team1 = data_dict['away']
        team2 = data_dict['home']
        team1_percent = 20
        team2_percent = 20
        team1_hap_percent = self.count_percent(points=team1['scores'])
        team2_hap_percent = self.count_percent(points=team2['scores'])
        team1_min_point_4_set = self.count_min_point_4_set(
            points=team1['scores'], percent=team1_percent)
        team2_min_point_4_set = self.count_min_point_4_set(
            points=team2['scores'], percent=team2_percent)
        if abs(team1['total_point'] - team2['total_point']) <= 4:
            team1_percent -= 7
            team2_percent -= 7

        if all([i <= team1_min_point_4_set for i in team1['hist_games_score'][:2]]):
            team1_percent += 5

        if all([i <= team2_min_point_4_set for i in team2['hist_games_score'][:2]]):
            team2_percent += 5

        team1_results = self.create_message(
            team1['name'], team1['scores'][:3], team1_min_point_4_set, team1_hap_percent)
        team2_results = self.create_message(
            team2['name'], team2['scores'][:3], team2_min_point_4_set, team2_hap_percent)
        set = f'set : {set} time {time}'
        return '\n'.join([team1_results, team2_results, set])

    def create_message(self, name, points_3_set, min_point_4_set, percent):
        return f"{name}: {round(sum(points_3_set)+min_point_4_set,2)}   Вероятность {percent}%"

    def count_min_point_4_set(self, points, percent):
        return sum(points[:3])/3*((100-percent)/100)

    def count_percent(self, points):
        ab1 = self.perc(abs(points[0] - points[1]))
        bc1 = self.perc(abs(points[1] - points[2]))
        percent = (ab1 + bc1)/2
        return percent

    def perc(self, bc):
        if bc in (0, 1, 2, 3, 4):
            bc = 80
        elif bc in (5, 6):
            bc = 65
        elif bc in (7, 8):
            bc = 50
        else:
            bc = 40
        return bc

if '__main__' == __name__:
    driver_ = BasketballBet()
    new_message = driver_.get_live_matches()
    print(new_message)
    driver_.driver_.close()