use std::collections::HashMap;

fn main() {
    let input = include_str!("../input.txt");
    let mut counts = HashMap::new();
    counts.insert("red", 3);
    counts.insert("green", 5);
    counts.insert("blue", 4);

    let mut total = 0;
    for line in input.lines() {
        println!("{}", line);
        let line = line.split_whitespace().collect::<Vec<_>>();

        let mut id = 0;
        let mut valid = true;
        for i in (0..line.len()).step_by(2) {
            if i == 0 {
                id = line.get(1).unwrap().trim_end_matches(":").parse::<i32>().unwrap();
            } else {
                let count = line.get(i).unwrap().parse::<i32>().unwrap();
                let color = line.get(i + 1).unwrap().trim_matches(|c: char| c.is_ascii_punctuation());
                let min_count = counts.get(color).unwrap();
                if count < *min_count {
                    valid = false;
                    break;
                }
            }
        }
        if valid {
            total += id;
        }
    }
    println!("{}", total)
}
