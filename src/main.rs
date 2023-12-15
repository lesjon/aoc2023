use std::collections::{HashMap, HashSet};

fn get_possibilities(s: &str) -> HashSet<String> {
    let mut result = HashSet::new();
    if !s.contains('?') {
        result.insert(s.to_string());
        return result;
    }
    let mut left_chars = vec![];
    for (i, c) in s.char_indices() {
        if c == '?' {
            let subs = get_possibilities(&s[i + 1..]);
            for mut sub in subs {
                sub.insert(0, '.');
                sub.insert_str(0, &String::from_utf8_lossy(&left_chars));
                result.insert(sub.clone());
                let dot_index = left_chars.len();
                sub.remove(dot_index);
                sub.insert(dot_index, '#');
                result.insert(sub);
            }
            return result;
        } else {
            left_chars.push(c as u8);
        }
    }
    panic!("Unreachable state '{s}' contains '?' but not found in for loop")
}

fn valid(possibility: &str, ints: &[i32]) -> bool {
    let mut compare: Vec<i32> = Vec::with_capacity(ints.len());
    let mut current = 0;
    for c in possibility.chars() {
        match c {
            '.' => {
                if current > 0 {
                    compare.push(current);
                    current = 0;
                }
            }
            '#' => {
                current += 1;
            }
            other => panic!("Unknown char {other}")
        }
    }
    if current > 0 {
        compare.push(current);
    }
    assert!(!compare.contains(&0));
    if compare.len() != ints.len(){
        return false;
    }
    return compare.iter().zip(ints).all(|(lhs, rhs)| rhs == lhs);
}

fn run(text: &str) -> usize {
    let mut rows = HashMap::new();
    for line in text.split("\n") {
        let mut s = "";
        for (i, part) in line.split_whitespace().enumerate() {
            match i {
                0 => s = part,
                1 => {
                    let ints = part.split(',').map(|num_str| num_str.parse::<i32>().unwrap()).collect::<Vec<i32>>();
                    rows.insert(s, ints);
                }
                _ => panic!("Unreachable state: {i}")
            }
        }
    }
    println!("rows = {rows:?}");
    let mut total = 0;

    for (s, ints) in rows {
        let possibilities = get_possibilities(s);
        let p_count =possibilities.len();
        println!("'{s}' has {p_count} possibilities");
        let q_count = s.chars().filter(|c| c.eq(&'?')).count();
        assert_eq!(p_count, usize::pow(2, q_count as u32));
        let p_count = possibilities.iter().filter(|p| valid(p, &ints)).count();
        total += p_count;
    }
    return total
}
fn main() {
    let input = include_str!("../input.txt");
    let total = run(input);
    // 7320 too low
    println!("{total}");
}

#[cfg(test)]
mod tests {
    use crate::{get_possibilities, run};

    #[test]
    fn test() {
        let text = "????";
        let expecteds = vec!["####", "###.", "##.#", "##..", "#.##", "#.#.", "#..#", "#...", ".###", ".##.", ".#.#", ".#..", "..##", "..#.", "...#", "...."];
        let actual = get_possibilities(text);
        assert_eq!(expecteds.len(), actual.len());
        for expected in expecteds {
            assert!(actual.contains(expected));
        }
    }

    #[test]
    fn test_sample(){
        let text = "???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1";
        assert_eq!(21, run(text))
    }

    #[test]
    fn test_sample1() {
        assert_eq!(1, run("???.### 1,1,3"));
    }
    #[test]
    fn test_sample1a() {
        assert_eq!(3, run("????.### 1,1,3"));
    }
    #[test]
    fn test_sample2() {
        assert_eq!(4, run(".??..??...?##. 1,1,3"));
    }
    #[test]
    fn test_sample3() {
        assert_eq!(1, run("?#?#?#?#?#?#?#? 1,3,1,6"));
    }
    #[test]
    fn test_sample4() {
        assert_eq!(1, run("????.#...#... 4,1,1"));
    }
    #[test]
    fn test_sample5() {
        assert_eq!(4, run("????.######..#####. 1,6,5"));
    }
    #[test]
    fn test_sample6() {
        assert_eq!(10, run("?###???????? 3,2,1"));
    }
    #[test]
    fn test_sample7() {
        assert_eq!(1, run(".###.##.#..? 3,2,1"));
    }
}