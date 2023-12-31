fn count_possibilities(s: &str, ints: &[i32], mut state: char) -> usize {
    if ints.len() == 0 && (!s.contains('#') || s.is_empty()){
        return 1;
    }
    let mut result = 0;
    let mut ints_index = 0;
    let mut ints_vec = Vec::from(ints);
    for (i,c) in s.char_indices() {
        match (state, c) {
            ('.', '.') => (),
            ('.', '#') => {
                if ints_vec.len() == ints_index || ints_vec[ints_index] == 0 {
                    break
                }
                ints_vec[ints_index] -= 1;
                state = c;
            }
            ('#', '.') => {
                if ints_vec[ints_index] != 0 {
                    break
                }
                ints_index += 1;
                state = c;
                if ints_index == ints_vec.len() {
                    if s[i..].contains('#') {
                        return 0;
                    }
                    break
                }
            }
            ('#', '#') => {
                if ints_vec[ints_index] == 0 {
                    break
                }
                ints_vec[ints_index] -= 1;
            }
            ('.', '?') => {
                result += count_possibilities(&s[i+1..], &ints_vec[ints_index..], '.');
                if ints_index >= ints_vec.len() {
                    break
                }
                state = '#';
                ints_vec[ints_index] -= 1;
                if ints_vec[ints_index] == -1 {
                    break
                }
            }
            ('#', '?') => {
                if ints_vec[ints_index] == 0 {
                    result += count_possibilities(&s[i+1..], &ints_vec[ints_index+1..], '.');
                }
                if ints_index >= ints_vec.len() {
                    break
                }
                state = '#';
                ints_vec[ints_index] -= 1;
                if ints_vec[ints_index] == -1 {
                    break
                }
            }
            other => panic!("Unknown {other:?}")
        }
    }
    if ints_vec.len() == 0 || ints_vec[ints_vec.len()-1] == 0 {
        result += 1;
    }
    result
}

fn parse(line: &str) -> (&str, Vec<i32>) {
    let parts = line.split_whitespace().collect::<Vec<&str>>();
    let ints: Vec<i32> = parts[1].split(",").map(|s|s.parse().unwrap()).collect();
    (parts[0], ints)
}

fn run(text: &str) -> usize {
    let mut total = 0;
    for line in text.lines() {
        let (s, mut ints) = parse(line);
        let possibilities = count_possibilities(s, &mut ints[..], '.');
        println!("{:?}, possibilities:{possibilities}", (s, ints));
        total += possibilities;
    }
    total
}

fn main() {
    let input = include_str!("../input.txt");
    let total = run(input);
    // 7320 too low
    // 8252 incorrect
    println!("{total}");
}

#[cfg(test)]
mod tests {
    use crate::{run};

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
    fn test_sample6a() {
        assert_eq!(10, run("??????? 2,1"));
    }

    #[test]
    fn test_sample6b() {
        assert_eq!(6, run("?????? 2,1"));
    }

    #[test]
    fn test_sample7() {
        assert_eq!(1, run(".###.##.#..? 3,2,1"));
    }
}