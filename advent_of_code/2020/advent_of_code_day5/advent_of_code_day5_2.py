from pathlib import Path

if __name__ == "__main__":
    print('Part 1: {}'.format(max({int(boarding_pass.replace("F","0").replace("B", "1").replace("L", "0").replace("R","1")[:7] + boarding_pass.replace("F","0").replace("B", "1").replace("L", "0").replace("R","1")[7:], base=2) for boarding_pass in Path("advent_of_code/2020/advent_of_code_day5/input.txt").read_text().split("\n")})))
 
    available_seat_ids = list({i * 8 + j for j in range(8) for i in range(128)} - {int(boarding_pass.replace("F","0").replace("B", "1").replace("L", "0").replace("R","1")[:7] + boarding_pass.replace("F","0").replace("B", "1").replace("L", "0").replace("R","1")[7:], base=2) for boarding_pass in Path("advent_of_code/2020/advent_of_code_day5/input.txt").read_text().split("\n")})

    print('Part 2: {}'.format(sum([available_seat_ids[i] if i > 1 and i < len(available_seat_ids)-1 and available_seat_id + 1 != available_seat_ids[i+1] and available_seat_id - 1 != available_seat_ids[i-1] else False for i, available_seat_id in enumerate(available_seat_ids)])))
      
