use std::cmp::Ordering;
use std::collections::{BTreeSet, HashMap};
use std::fmt::{Display, Formatter};

#[derive(Ord, Eq, Debug, Clone, Hash)]
struct State {
    width: i32,
    height: i32,
    rocks: BTreeSet<(i32, i32)>,
    boulders: BTreeSet<(i32, i32)>,
}

impl PartialEq<Self> for State {
    fn eq(&self, other: &Self) -> bool {
        return self.boulders == other.boulders
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        self.boulders.partial_cmp(&other.boulders)
    }
}

impl Display for State {
    fn fmt(&self, f: &mut Formatter<'_>) -> std::fmt::Result {
        for y in 0..self.height {
            for x in 0..self.width {
                if self.rocks.contains(&(x, y)) {
                    write!(f, "#")?;
                } else if self.boulders.contains(&(x, y)) {
                    write!(f, "O")?;
                } else {
                    write!(f, ".")?;
                }
            }
            writeln!(f)?;
        }
        Ok(())
    }
}

fn parse(text: &str) -> State {
    let width = text.lines().next().unwrap().len() as i32;
    let height = text.lines().collect::<Vec<&str>>().len() as i32;
    let mut rocks = BTreeSet::new();
    let mut boulders = BTreeSet::new();
    for (y, line) in text.lines().enumerate() {
        for (x, c) in line.char_indices() {
            match c {
                '#' => rocks.insert((x as i32, y as i32)),
                'O' => boulders.insert((x as i32, y as i32)),
                '.' => false,
                other => panic!("Unknown char {other}")
            };
        }
    }
    return State {
        height,
        width,
        rocks,
        boulders,
    };
}

fn north_load(state: &State) -> i32 {
    let mut total = 0;
    for (_, y) in state.boulders.iter() {
        total += state.height - y;
    }
    total
}

fn roll_west(state: State) -> State {
    let mut next_boulders = BTreeSet::new();
    let mut sorted_boulders = state.boulders.into_iter().collect::<Vec<(i32, i32)>>();
    sorted_boulders.sort_by_key(|t| t.0);

    for (x, y) in sorted_boulders {
        let mut next_x = 0;
        for check_x in (0..=x).rev() {
            if state.rocks.contains(&(check_x, y)) {
                break;
            }
            if next_boulders.contains(&(check_x, y)) {
                break;
            }
            next_x = check_x;
        }
        next_boulders.insert((next_x, y));
    }
    return State {
        width: state.width,
        boulders: next_boulders,
        rocks: state.rocks,
        height: state.height,
    };
}

fn roll_east(state: State) -> State {
    let mut next_boulders = BTreeSet::new();
    let mut sorted_boulders = state.boulders.into_iter().collect::<Vec<(i32, i32)>>();
    sorted_boulders.sort_by_key(|t| -t.0);

    for (x, y) in sorted_boulders {
        let mut next_x = state.width-1;
        for check_x in x..state.width {
            if state.rocks.contains(&(check_x, y)) {
                break;
            }
            if next_boulders.contains(&(check_x, y)) {
                break;
            }
            next_x = check_x;
        }
        next_boulders.insert((next_x, y));
    }
    return State {
        width: state.width,
        boulders: next_boulders,
        rocks: state.rocks,
        height: state.height,
    };
}

fn roll_north(state: State) -> State {
    let mut next_boulders = BTreeSet::new();
    let mut sorted_boulders = state.boulders.into_iter().collect::<Vec<(i32, i32)>>();
    sorted_boulders.sort_by_key(|t| t.1);

    for (x, y) in sorted_boulders {
        let mut next_y = 0;
        for check_y in (0..=y).rev() {
            if state.rocks.contains(&(x, check_y)) {
                break;
            }
            if next_boulders.contains(&(x, check_y)) {
                break;
            }
            next_y = check_y;
        }
        next_boulders.insert((x, next_y));
    }
    return State {
        width: state.width,
        boulders: next_boulders,
        rocks: state.rocks,
        height: state.height,
    };
}

fn roll_south(state: State) -> State {
    let mut next_boulders = BTreeSet::new();
    let mut sorted_boulders = state.boulders.into_iter().collect::<Vec<(i32, i32)>>();
    sorted_boulders.sort_by_key(|t| -t.1);

    for (x, y) in sorted_boulders {
        let mut next_y = state.height-1;
        for check_y in y..state.height {
            if state.rocks.contains(&(x, check_y)) {
                break;
            }
            if next_boulders.contains(&(x, check_y)) {
                break;
            }
            next_y = check_y;
        }
        next_boulders.insert((x, next_y));
    }
    return State {
        width: state.width,
        boulders: next_boulders,
        rocks: state.rocks,
        height: state.height,
    };
}

fn run(text: &str, cycles: i32) -> i32 {
    let mut seen = HashMap::new();
    let mut seen_rev = HashMap::new();
    let mut state = parse(text);
    for i in 1..=cycles {
        state = roll_north(state);
        state = roll_west(state);
        state = roll_south(state);
        state = roll_east(state);
        let load = north_load(&state);
        println!("cycle {i}: load={load} {state} ");
        if seen.contains_key(&state) {
            println!("Found repeat state at {i} ");
            let target_in_cycle = cycles - seen.get(&state).unwrap();
            let cycle_len = i - seen.get(&state).unwrap();
            let key = seen.get(&state).unwrap() + target_in_cycle % cycle_len;
            println!("cycle_len={cycle_len} repeat is {key}");
            return north_load(seen_rev.get(&key).unwrap());
        }else {
            seen.insert(state.clone(), i);
            seen_rev.insert(i, state.clone());
        }
    }
    north_load(&state)
}

fn main() {
    let text = include_str!("../input.txt");
    println!("{}", run(text, 1000000000));
}

#[cfg(test)]
mod tests {
    use crate::{run};

    #[test]
    fn test() {
        let text = "\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....";
        assert_eq!(64, run(text, 1000000000));
    }
}
